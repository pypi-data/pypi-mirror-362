"""
Data access and analysis package for Ethopy experiments.

This package provides convenient access to data loading, analysis, and utility functions
for behavioral experiments. Import the main functions you need directly from this package.
"""

# Main data loading functions
from .loaders import (
    get_sessions,
    get_trials,
    get_trial_states,
    get_trial_experiment,
    get_trial_behavior,
    get_trial_stimulus,
    get_trial_licks,
    get_trial_proximities,
    get_session_classes,
    get_session_duration,
    get_session_task,
)

# Analysis functions
from .analysis import (
    get_performance,
    session_summary,
    trials_per_session,
)

# Utility functions
from .utils import (
    find_combination,
    get_setup,
    check_hashable_columns,
    group_trials,
    group_by_conditions,
    group_trial_hash,
    convert_ms_to_time,
)

__all__ = [
    # Data loaders
    "get_sessions",
    "get_trials",
    "get_trial_states",
    "get_trial_experiment",
    "get_trial_behavior",
    "get_trial_stimulus",
    "get_trial_licks",
    "get_trial_proximities",
    "get_session_classes",
    "get_session_duration",
    "get_session_task",
    # Analysis functions
    "get_performance",
    "session_summary",
    "trials_per_session",
    # Utility functions
    "find_combination",
    "get_setup",
    "check_hashable_columns",
    "group_trials",
    "group_by_conditions",
    "group_trial_hash",
    "convert_ms_to_time",
]
