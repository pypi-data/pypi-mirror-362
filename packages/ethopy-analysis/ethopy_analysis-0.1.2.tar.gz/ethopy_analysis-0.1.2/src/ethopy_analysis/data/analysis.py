"""
Data analysis functions for Ethopy experiments.

This module provides functions to analyze behavioral data,
calculate performance metrics, and generate session summaries.
"""

from typing import List, Optional, Union, Any
import pandas as pd
import numpy as np
from ethopy_analysis.db.schemas import get_schema


def get_performance(
    animal_id, session, trials: Optional[List[int]] = None
) -> Optional[float]:
    """
    Calculate performance as the ratio of reward trials to total decisive trials.

    Args:
        animal_id (int): Animal identifier
        session (int): Session identifier
        trials (Optional[List[int]], optional): List of trial indices to filter by.
                                              Defaults to None.

    Returns:
        Optional[float]: Performance ratio (0-1), or None if no decisive trials found

    Note:
        Decisive trials are those with state 'Reward' or 'Punish'.
        Performance is calculated as: count_reward_trials / (count_reward_trials + count_punish_trials)
    """
    from .loaders import get_trial_states
    
    df = get_trial_states(animal_id, session)
    if df is None or df.empty:
        print("Warning: DataFrame is empty or None - cannot calculate performance")
        return None

    # Filter by trials if provided
    if trials is not None:
        df = df[df["trial_idx"].isin(trials)]
        if df.empty:
            print(
                "Warning: No trials found matching the provided trial list - cannot calculate performance"
            )
            return None

    # Filter to only decisive trials (Reward or Punish) - vectorized operation
    decisive_trials = df[df["state"].isin(["Reward", "Punish"])]

    if decisive_trials.empty:
        available_states = df["state"].unique()
        print(
            f"Warning: No Reward or Punish states found. Available states: {available_states}"
        )
        return None

    # Count using vectorized operations for speed
    state_counts = decisive_trials["state"].value_counts()
    count_reward_trials = state_counts.get("Reward", 0)
    count_punish_trials = state_counts.get("Punish", 0)

    # Handle division by zero edge case
    total_decisive = count_reward_trials + count_punish_trials
    if total_decisive == 0:
        print("Warning: Total decisive trials is zero - cannot calculate performance")
        return None

    return count_reward_trials / total_decisive


def session_summary(animal_id: int, session: int) -> None:
    """
    Print a comprehensive summary of a session including metadata and performance.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Prints:
        - Animal ID and session number
        - User name and setup information
        - Session start time and duration
        - Experiment, stimulus, and behavior classes
        - Task filename and git hash
        - Session performance and number of trials
    """
    from .loaders import get_session_classes, get_session_duration, get_session_task, get_trial_states
    
    session_classes = get_session_classes(animal_id, session)
    print(f"Animal id: {animal_id}, session: {session}")
    print(f"User name: {session_classes['user_name'].values[0]}")
    print(f"Setup: {session_classes['setup'].values[0]}")
    print(f"Session start: {pd.to_datetime(session_classes['session_tmst'].values[0])}")
    print(f"Session duration: {get_session_duration(animal_id, session)}")

    print()
    print("Experiment: ", session_classes["experiment_class"].values[0])
    print("Stimulus: ", session_classes["stimulus_class"].values[0])
    print("Behavior: ", session_classes["behavior_class"].values[0])

    filename, git_hash = get_session_task(animal_id, session, save_file=False)
    print()
    print(f"Task filename: {filename}")
    print(f"Git hash: {git_hash}")

    df = get_trial_states(animal_id, session)
    print()
    print(f"Session performance: {get_performance(animal_id, session)}")
    print(f"Number of trials: {max(df['trial_idx'])}")


def trials_per_session(animal_id: int, min_trials=2, format="df"):
    """Returns the number of trials per session

    Args:
        animal_id (int): The animal identifier
        min_trials (int, optional): Minimum number of trials to include session. Defaults to 2.
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: DataFrame with trials_count column if format="df",
                                 DataJoint expression if format="dj"
    """
    experiment = get_schema("experiment")

    session_trials_dj = (experiment.Session & {"animal_id": animal_id}).aggr(
        experiment.Trial & {"animal_id": animal_id}, trials_count="count(trial_idx)"
    ) - experiment.Session.Excluded & f"trials_count>{min_trials}"
    
    if format == "dj":
        return session_trials_dj
    return session_trials_dj.fetch(format="frame").reset_index()