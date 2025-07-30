"""
Main data loading functions for Ethopy analysis.

This module provides user-friendly functions to load behavioral data
and return it as pandas DataFrames or DataJoint expressions ready for analysis and visualization.
"""

from typing import List, Optional, Union, Tuple, Any
import pandas as pd
import os
from ethopy_analysis.db.schemas import get_schema
from ethopy_analysis.data.utils import combine_children_tables


def get_sessions(
    animal_id,
    from_date: str = "",
    to_date: str = "",
    format: str = "df",
    min_trials: Optional[int] = None,
):
    """
    Get sessions for an animal within a specified date range.

    Args:
        animal_id (int): The animal identifier
        from_date (str, optional): Start date in format 'YYYY-MM-DD'. Defaults to ''.
        to_date (str, optional): End date in format 'YYYY-MM-DD'. Defaults to ''.
        format(str, optional): if format equals 'dj' return datajoint expression.
        min_trials(int, optional): minimum number of trials per session.

    Returns:
        Union[pd.DataFrame, Any]: Session DataFrame if format="df",
                                 Session expression if format="dj"
    """
    from .analysis import trials_per_session

    experiment = get_schema("experiment")

    animal_session_tmt = experiment.Session & {"animal_id": animal_id}
    if from_date != "":
        animal_session_tmt = animal_session_tmt & f'session_tmst > "{from_date}"'

    if to_date != "":
        animal_session_tmt = animal_session_tmt & f'session_tmst < "{to_date}"'

    sessions_dj = animal_session_tmt - experiment.Session.Excluded
    if min_trials:
        trials_session = trials_per_session(animal_id, min_trials=2, format="dj")
        sessions_dj = trials_session * sessions_dj

    if format == "dj":
        return sessions_dj
    return sessions_dj.fetch(format="frame").reset_index()


def get_trials(
    animal_id: int, session: int, format: str = "df", remove_abort: bool = False
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".
        remove_abort (bool): remove abort trials

    Returns:
        Union[pd.DataFrame, Any]: Trial DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    experiment = get_schema("experiment")
    trials_dj = experiment.Trial & {"animal_id": animal_id, "session": session}
    if remove_abort:
        trials_dj = trials_dj - experiment.Trial.Aborted()
    if format == "dj":
        return trials_dj
    return trials_dj.fetch(format="frame").reset_index()


def get_trial_states(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial state onset data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial states DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}

    trial_states_dj = experiment.Trial.StateOnset & key_animal_session

    if format == "dj":
        return trial_states_dj

    trial_states_df = trial_states_dj.fetch(format="frame").reset_index()
    return trial_states_df


def get_trial_experiment(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial experiment condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial experiment conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"

    Note:
        This function combines trial data with experiment conditions based on the
        experiment_type from the session classes.
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}
    combined_df = get_session_classes(animal_id, session)
    exp_conds = getattr(experiment.Condition, combined_df["experiment_type"].values[0])
    conditions_dj = (experiment.Trial & key_animal_session) * experiment.Condition
    trial_exp_conditions_dj = conditions_dj * exp_conds

    if format == "dj":
        return trial_exp_conditions_dj

    trial_exp_conditions_df = trial_exp_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_exp_conditions_df


def get_trial_behavior(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial behavior condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"

    Note:
        This function combines trial data with behavior conditions, handling cases
        where multiple behavior child tables need to be combined.
    """
    behavior = get_schema("behavior")
    key_animal_session = {"animal_id": animal_id, "session": session}
    combined_df = get_session_classes(animal_id, session)
    beh_conds = getattr(behavior, combined_df["behavior_class"].values[0])
    children = beh_conds.children(as_objects=True)

    if len(children) > 1:
        comb_tables = combine_children_tables(children)
    elif len(children) == 1:
        comb_tables = children[0]
    else:
        comb_tables = beh_conds

    trial_beh_conditions_dj = (
        behavior.BehCondition.Trial() & key_animal_session
    ) * comb_tables

    if format == "dj":
        return trial_beh_conditions_dj

    trial_beh_conditions_df = trial_beh_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_beh_conditions_df


def get_trial_stimulus(
    animal_id: int, session: int, stim_class: Optional[str] = None, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial stimulus condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        stim_class (Optional[str], optional): Specific stimulus class to use.
                                            If None, uses the stimulus class from session data.
                                            Defaults to None.
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"
    Raises:
        Exception: If the specified stimulus class table is not found in the stimulus schema

    Note:
        This function combines trial data with stimulus conditions and all related
        child tables that contain data for the session.
    """
    stimulus = get_schema("stimulus")
    combined_df = get_session_classes(animal_id, session)
    key_animal_session = {"animal_id": animal_id, "session": session}

    if stim_class is None:
        stim_class_name = combined_df["stimulus_class"].values[0]
        try:
            stim_conds = getattr(stimulus, stim_class_name)
        except AttributeError as e:
            raise Exception(
                f"Cannot find {stim_class_name} table in stimulus schema"
            ) from e
    else:
        try:
            stim_conds = getattr(stimulus, stim_class)
        except AttributeError as e:
            raise Exception(f"Cannot find {stim_class} table in stimulus schema") from e

    children = stim_conds.children(as_objects=True)
    base_dj = (stimulus.StimCondition.Trial & key_animal_session) * stim_conds
    all_stims = base_dj

    for child in children:
        comb_stims = base_dj * child
        if len(comb_stims) > 0:
            all_stims = all_stims * child

    trial_stim_conditions_dj = all_stims
    if format == "dj":
        return trial_stim_conditions_dj
    trial_stim_conditions_df = trial_stim_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_stim_conditions_df


def get_trial_licks(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve all licks of a session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    behavior = get_schema("behavior")
    key = {"animal_id": animal_id, "session": session}
    lick_dj = behavior.Activity.Lick & key
    if format == "dj":
        return lick_dj
    return lick_dj.fetch(format="frame").reset_index()


def get_trial_proximities(
    animal_id, session, ports: Optional[List] = None, format="df"
):
    """
    Retrieve proximity sensor data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        ports (Optional[List]): List of port numbers to filter by
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Proximity data DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    behavior = get_schema("behavior")
    if ports:
        proximity_dj = (
            behavior.Activity.Proximity
            & {"animal_id": animal_id, "session": session}
            & [f"port={p}" for p in ports]
        )
    else:
        proximity_dj = behavior.Activity.Proximity & {
            "animal_id": animal_id,
            "session": session,
        }
    if format == "dj":
        return proximity_dj
    return proximity_dj.fetch(format="frame").reset_index()


def get_session_classes(animal_id: int, session: int) -> pd.DataFrame:
    """
    Retrieve session information and experimental classes for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Returns:
        pd.DataFrame: Combined DataFrame containing session information and unique
                     combinations of stimulus_class, behavior_class, and experiment_class

    Raises:
        Exception: If no session found for the given animal_id and session
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}
    session_info_df = (
        (experiment.Session & key_animal_session).fetch(format="frame").reset_index()
    )

    conditions_dj = (experiment.Trial & key_animal_session) * experiment.Condition
    conditions_df = conditions_dj.fetch(format="frame").reset_index()

    # Get unique combinations
    unique_combinations = conditions_df[
        ["stimulus_class", "behavior_class", "experiment_class"]
    ].drop_duplicates()

    # Combine session_info_df and unique_combinations side by side
    combined_df = pd.concat(
        [session_info_df, unique_combinations.reset_index(drop=True)], axis=1
    )
    return combined_df


def get_session_duration(animal_id: int, session: int) -> Optional[str]:
    """
    Calculate the duration of a session based on the last state onset time.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Returns:
        Optional[str]: Formatted duration string (e.g., "1.2 hours (4320.0 seconds)")
                      or None if no state times found
    """
    from .utils import convert_ms_to_time

    experiment = get_schema("experiment")
    state_times = (
        experiment.Trial.StateOnset & {"animal_id": animal_id, "session": session}
    ).fetch("time")
    if len(state_times) < 1:
        return None
    return convert_ms_to_time(state_times[-1])["formatted"]


def get_session_task(
    animal_id: int, session: int, save_file: bool = True
) -> Tuple[str, str]:
    """
    Retrieve and optionally save the task configuration file for a specific session.

    Args:
        animal_id (int): Animal identifier
        session (int): Session identifier
        save_file (bool, optional): Whether to save the file to disk. Defaults to True.

    Returns:
        Tuple[str, str]: A tuple containing (filename, git_hash)

    Note:
        If save_file is True, the file is saved with a modified name including
        animal_id and session for uniqueness.
    """
    key_animal_session = {"animal_id": animal_id, "session": session}
    experiment = get_schema("experiment")
    file, git_hash, task_name = (experiment.Session.Task & key_animal_session).fetch1(
        "task_file", "git_hash", "task_name"
    )
    filename = task_name.split("/")[-1]

    if save_file:
        filename = f"{filename[:-3]}_animal_id_{animal_id}_session_{session}.py"
        print(f"Save task at path: {os.getcwd()}/{filename}")
        file.tofile(filename)
    return filename, git_hash
