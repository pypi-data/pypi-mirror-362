"""
Data utility functions for Ethopy analysis.

This module provides utility functions for data manipulation, processing,
and various helper functions used across the analysis pipeline.
"""

from typing import List, Tuple, Dict, Any, Optional, Union
import pandas as pd
import numpy as np
from ethopy_analysis.db.schemas import get_schema
from functools import reduce


def combine_children_tables(children: List[Any]) -> Any:
    """
    Combine multiple DataJoint child tables using the join operator.

    Args:
        children (List[Any]): List of DataJoint table objects to combine

    Returns:
        Any: Combined DataJoint expression

    Note:
        This function uses the reduce function with the DataJoint multiplication operator
        to progressively join all child tables together.
    """
    return reduce(lambda x, y: x * y, children)

def find_combination(states_df: pd.DataFrame, state: str = "PreTrial") -> str:
    """
    Find the next state after the specified state in a trial sequence.

    Args:
        states_df (pd.DataFrame): DataFrame containing trial states with 'state' column
        state (str, optional): The state to find the next state after. Defaults to "PreTrial".

    Returns:
        str: The state that follows the specified state, or "None" if:
            - The specified state is not found in the trial
            - "Offtime" is present in the trial states
            - The specified state is the last state in the sequence

    Raises:
        IndexError: If the specified state is the last state in the sequence
    """
    trial_states = states_df["state"].values
    if state not in trial_states:
        return "None"
    if "Offtime" in trial_states:
        return "None"
    idx = np.where(trial_states == state)[0][0]
    if idx + 1 >= len(trial_states):
        return "None"
    return trial_states[idx + 1]


def get_setup(setup: str) -> Tuple[int, int]:
    """
    Retrieve animal_id and session for a given setup.

    Args:
        setup (str): The setup identifier

    Returns:
        Tuple[int, int]: A tuple containing (animal_id, session)

    Raises:
        IndexError: If no setup found with the given identifier
    """
    experiment = get_schema("experiment")
    setup_data = (
        (experiment.Control & f'setup="{setup}"').fetch(format="frame").reset_index()
    )
    return int(setup_data["animal_id"].values[0]), int(setup_data["session"].values[0])


def check_hashable_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Identify which columns in a DataFrame contain hashable and non-hashable values.

    Args:
        df (pd.DataFrame): The DataFrame to analyze

    Returns:
        Tuple[List[str], List[str]]: A tuple containing (hashable_columns, non_hashable_columns)

    Note:
        This function tests the first 5 non-null values of each column to determine
        if they can be used in set operations (i.e., are hashable).
    """
    hashable_cols = []
    non_hashable_cols = []

    for col in df.columns:
        try:
            # Try to use the column in a set operation (requires hashable values)
            set(df[col].dropna().iloc[:5])  # Test first 5 non-null values
            hashable_cols.append(col)
        except TypeError:
            non_hashable_cols.append(col)

    return hashable_cols, non_hashable_cols


def group_trials(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group trials by unique conditions, excluding time-based and non-hashable columns.

    Args:
        df (pd.DataFrame): DataFrame containing trial data with 'trial_idx' column

    Returns:
        pd.DataFrame: Summary DataFrame with unique conditions and their trial counts/indices

    Note:
        This function automatically excludes:
        - 'trial_idx' column
        - Columns containing 'time' in the name
        - Non-hashable columns (identified via check_hashable_columns)
    """
    # Define columns to use for condition uniqueness
    hashable_cols, non_hashable_cols = check_hashable_columns(df)
    exclude_cols = ["trial_idx"] + [
        col for col in df.columns if "time" in col or col in non_hashable_cols
    ]
    condition_cols = [col for col in df.columns if col not in exclude_cols]

    # Group by unique condition columns and aggregate trial indices
    condition_summary = (
        df.groupby(condition_cols)
        .agg(
            trial_count=("trial_idx", "count"),
            trial_indices=("trial_idx", lambda x: list(x)),
        )
        .reset_index()
    )
    return condition_summary


def group_by_conditions(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    """
    Group DataFrame by specified columns and aggregate trial_idx count and indices.

    Args:
        df (pd.DataFrame): Input DataFrame with 'trial_idx' column
        group_cols (List[str]): List of column names to group by

    Returns:
        pd.DataFrame: Summary DataFrame with trial_count and trial_indices columns

    Note:
        This function is more specific than group_trials() as it allows explicit
        specification of which columns to group by.
    """
    condition_summary = df.groupby(group_cols).agg(
        trial_count=("trial_idx", "count"),
        trial_indices=("trial_idx", lambda x: list(x)),
    )
    return condition_summary


def group_trial_hash(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process trial experiment data by finding unique conditions based on hash columns.

    Args:
        df (pd.DataFrame): DataFrame containing trial experiment data with hash column

    Returns:
        pd.DataFrame: DataFrame with unique conditions and their associated trial indices and counts

    Raises:
        ValueError: If no hash column is found in the DataFrame

    Note:
        This function looks for columns containing 'hash' in their name and uses them
        to identify unique experimental conditions.
    """
    # Build exclusion list
    exclude_cols = ["trial_idx"] + [col for col in df.columns if "time" in col]

    # Find hash columns and validate
    hash_columns = [col for col in df.columns if "hash" in col]

    if len(hash_columns) == 0:
        raise ValueError("No hash column found in DataFrame")
    elif len(hash_columns) > 1:
        print(
            f"Warning: Multiple hash columns found: {hash_columns}. Using first one: {hash_columns[0]}"
        )

    hash_column = hash_columns[0]

    # Get unique conditions (excluding time-based and trial_idx columns)
    condition_cols = [col for col in df.columns if col not in exclude_cols]
    unique_df = df[condition_cols].drop_duplicates(subset=[hash_column]).copy()

    # Create mappings for trial indices and counts
    trial_mappings = df.groupby(hash_column)["trial_idx"].agg([list, "count"])
    trial_mappings.columns = ["trial_indices", "trial_count"]

    # Add trial information to unique conditions
    unique_df = unique_df.merge(trial_mappings, on=hash_column, how="left")

    return unique_df


def convert_ms_to_time(
    time_ms: Optional[Union[int, float]],
) -> Optional[Dict[str, Any]]:
    """
    Convert milliseconds to seconds and hours with formatted output.

    Args:
        time_ms (Optional[Union[int, float]]): Time in milliseconds

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing:
            - 'milliseconds': Original time in milliseconds
            - 'seconds': Time in seconds
            - 'hours': Time in hours
            - 'formatted': Human-readable string representation
        Returns None if input is None.

    Example:
        >>> convert_ms_to_time(7200000)  # 2 hours
        {
            'milliseconds': 7200000,
            'seconds': 7200.0,
            'hours': 2.0,
            'formatted': '2.00 hours (7200.0 seconds)'
        }
    """
    if time_ms is None:
        return None

    seconds = time_ms / 1000
    hours = seconds / 3600

    # Format as human-readable string
    if hours >= 1:
        formatted = f"{hours:.2f} hours ({seconds:.1f} seconds)"
    elif seconds >= 60:
        minutes = seconds / 60
        formatted = f"{minutes:.2f} minutes ({seconds:.1f} seconds)"
    else:
        formatted = f"{seconds:.1f} seconds"

    return {
        "milliseconds": time_ms,
        "seconds": seconds,
        "hours": hours,
        "formatted": formatted,
    }