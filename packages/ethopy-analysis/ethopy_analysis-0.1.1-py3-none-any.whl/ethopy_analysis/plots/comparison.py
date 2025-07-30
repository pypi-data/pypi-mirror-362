"""
Comparison plotting functions for Ethopy analysis.

These functions create visualizations comparing data across animals,
protocols, conditions, or other experimental factors.
"""
# ToDo: Implement comparison plots for animals, protocols, and difficulty levels
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import logging
# from typing import Optional, List, Dict, Any, Tuple
# from .utils import (
#     validate_dataframe,
#     create_figure,
#     create_subplot_grid,
#     save_plot,
# )

# logger = logging.getLogger(__name__)


# def plot_animals_comparison(
#     performance_df: pd.DataFrame,
#     animal_ids: Optional[List[int]] = None,
#     metric: str = "correct_rate",
#     comparison_type: str = "boxplot",
#     figsize: Tuple[int, int] = (12, 6),
#     save_path: Optional[str] = None,
# ) -> Tuple[plt.Figure, plt.Axes]:
#     """Compare performance metrics across multiple animals.

#     Args:
#         performance_df: DataFrame with performance data for multiple animals
#         animal_ids: List of animal IDs to compare (optional, uses all if None)
#         metric: Performance metric to compare
#         comparison_type: Type of comparison ('boxplot', 'violin', 'timeline')
#         figsize: Figure size
#         save_path: Path to save the plot (optional)

#     Returns:
#         Tuple of (figure, axes)
#     """
#     required_columns = ["animal_id", metric]
#     if not validate_dataframe(performance_df, required_columns, "animals_comparison"):
#         return None, None

#     # Filter by animal IDs if provided
#     df_copy = performance_df.copy()
#     if animal_ids:
#         df_copy = df_copy[df_copy["animal_id"].isin(animal_ids)]

#     if df_copy.empty:
#         logger.warning("No data available for animal comparison")
#         return None, None

#     fig, ax = create_figure(
#         figsize, title=f"{metric.replace('_', ' ').title()} Comparison Across Animals"
#     )

#     if comparison_type == "boxplot":
#         # Box plot comparison
#         sns.boxplot(data=df_copy, x="animal_id", y=metric, ax=ax)
#         ax.set_xlabel("Animal ID")
#         ax.set_ylabel(metric.replace("_", " ").title())

#     elif comparison_type == "violin":
#         # Violin plot comparison
#         sns.violinplot(data=df_copy, x="animal_id", y=metric, ax=ax)
#         ax.set_xlabel("Animal ID")
#         ax.set_ylabel(metric.replace("_", " ").title())

#     elif comparison_type == "timeline":
#         # Timeline comparison
#         if "session" in df_copy.columns:
#             animals = sorted(df_copy["animal_id"].unique())
#             colors = plt.cm.tab10(np.linspace(0, 1, len(animals)))

#             for i, animal in enumerate(animals):
#                 animal_data = df_copy[df_copy["animal_id"] == animal].sort_values(
#                     "session"
#                 )
#                 ax.plot(
#                     animal_data["session"],
#                     animal_data[metric],
#                     "o-",
#                     color=colors[i],
#                     label=f"Animal {animal}",
#                     alpha=0.7,
#                 )

#             ax.set_xlabel("Session")
#             ax.set_ylabel(metric.replace("_", " ").title())
#             ax.legend()
#         else:
#             logger.warning("Session column not available for timeline comparison")
#             return None, None

#     ax.grid(True, alpha=0.3)

#     # Add summary statistics
#     animal_stats = df_copy.groupby("animal_id")[metric].agg(["mean", "std", "count"])
#     best_animal = animal_stats["mean"].idxmax()

#     summary_text = f"Best performer: Animal {best_animal}\n"
#     summary_text += f"Mean: {animal_stats.loc[best_animal, 'mean']:.3f}\n"
#     summary_text += f"Animals compared: {len(animal_stats)}"

#     ax.text(
#         0.02,
#         0.98,
#         summary_text,
#         transform=ax.transAxes,
#         verticalalignment="top",
#         bbox=dict(boxstyle="round", facecolor="lightblue"),
#     )

#     if save_path:
#         save_plot(fig, save_path)

#     logger.info(f"Created animal comparison plot for {len(animal_stats)} animals")
#     return fig, ax


# def plot_protocol_comparison(
#     trials_df: pd.DataFrame,
#     protocol_column: str = "experiment_class",
#     outcome_column: str = "outcome",
#     animal_column: str = "animal_id",
#     figsize: Tuple[int, int] = (14, 8),
#     save_path: Optional[str] = None,
# ) -> Tuple[plt.Figure, np.ndarray]:
#     """Compare performance across different experimental protocols.

#     Args:
#         trials_df: DataFrame with trial data including protocol information
#         protocol_column: Column identifying the experimental protocol
#         outcome_column: Column with trial outcomes
#         animal_column: Column with animal identifiers
#         figsize: Figure size
#         save_path: Path to save the plot (optional)

#     Returns:
#         Tuple of (figure, axes_array)
#     """
#     required_columns = [protocol_column, outcome_column, animal_column]
#     if not validate_dataframe(trials_df, required_columns, "protocol_comparison"):
#         return None, None

#     protocols = trials_df[protocol_column].unique()
#     if len(protocols) < 2:
#         logger.warning("Need at least 2 protocols for comparison")
#         return None, None

#     fig, axes = create_subplot_grid(2, 2, figsize)
#     fig.suptitle("Protocol Comparison Analysis")

#     # Calculate success rates per protocol and animal
#     df_copy = trials_df.copy()
#     df_copy["success"] = (df_copy[outcome_column] == "correct").astype(int)

#     # Plot 1: Overall success rates by protocol
#     ax = axes[0]
#     protocol_performance = df_copy.groupby(protocol_column)["success"].mean()

#     bars = ax.bar(
#         range(len(protocol_performance)),
#         protocol_performance.values,
#         alpha=0.7,
#         color=plt.cm.viridis(np.linspace(0, 1, len(protocols))),
#     )
#     ax.set_xlabel("Protocol")
#     ax.set_ylabel("Success Rate")
#     ax.set_title("Overall Success Rate by Protocol")
#     ax.set_xticks(range(len(protocol_performance)))
#     ax.set_xticklabels(protocol_performance.index, rotation=45)

#     # Add value labels on bars
#     for bar, value in zip(bars, protocol_performance.values):
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height() + 0.01,
#             f"{value:.2f}",
#             ha="center",
#             va="bottom",
#         )

#     # Plot 2: Success rates by protocol and animal
#     ax = axes[1]
#     animal_protocol_perf = (
#         df_copy.groupby([animal_column, protocol_column])["success"].mean().unstack()
#     )

#     if not animal_protocol_perf.empty:
#         sns.heatmap(
#             animal_protocol_perf,
#             annot=True,
#             fmt=".2f",
#             cmap="RdYlGn",
#             center=0.5,
#             ax=ax,
#             cbar_kws={"label": "Success Rate"},
#         )
#         ax.set_title("Success Rate by Animal and Protocol")
#         ax.set_ylabel("Animal ID")

#     # Plot 3: Trial counts by protocol
#     ax = axes[2]
#     trial_counts = df_copy.groupby(protocol_column).size()

#     bars = ax.bar(
#         range(len(trial_counts)),
#         trial_counts.values,
#         alpha=0.7,
#         color=plt.cm.plasma(np.linspace(0, 1, len(protocols))),
#     )
#     ax.set_xlabel("Protocol")
#     ax.set_ylabel("Number of Trials")
#     ax.set_title("Trial Counts by Protocol")
#     ax.set_xticks(range(len(trial_counts)))
#     ax.set_xticklabels(trial_counts.index, rotation=45)

#     # Add value labels
#     for bar, value in zip(bars, trial_counts.values):
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height() + max(trial_counts) * 0.01,
#             f"{value}",
#             ha="center",
#             va="bottom",
#         )

#     # Plot 4: Distribution of success rates per protocol
#     ax = axes[3]

#     # Calculate success rates per animal per protocol
#     animal_success_rates = (
#         df_copy.groupby([animal_column, protocol_column])["success"]
#         .mean()
#         .reset_index()
#     )

#     for i, protocol in enumerate(protocols):
#         protocol_rates = animal_success_rates[
#             animal_success_rates[protocol_column] == protocol
#         ]["success"]
#         if not protocol_rates.empty:
#             ax.hist(
#                 protocol_rates,
#                 alpha=0.6,
#                 label=protocol,
#                 bins=10,
#                 color=plt.cm.viridis(i / len(protocols)),
#             )

#     ax.set_xlabel("Success Rate")
#     ax.set_ylabel("Number of Animals")
#     ax.set_title("Distribution of Success Rates")
#     ax.legend()

#     plt.tight_layout()

#     if save_path:
#         save_plot(fig, save_path)

#     logger.info(f"Created protocol comparison plot for {len(protocols)} protocols")
#     return fig, axes


# def plot_difficulty_analysis(
#     trials_df: pd.DataFrame,
#     difficulty_column: str = "difficulty",
#     outcome_column: str = "outcome",
#     trial_column: str = "trial_idx",
#     figsize: Tuple[int, int] = (14, 10),
#     save_path: Optional[str] = None,
# ) -> Tuple[plt.Figure, np.ndarray]:
#     """Analyze and plot performance vs difficulty levels.

#     Args:
#         trials_df: DataFrame with trial data including difficulty levels
#         difficulty_column: Column with difficulty values
#         outcome_column: Column with trial outcomes
#         trial_column: Column with trial indices
#         figsize: Figure size
#         save_path: Path to save the plot (optional)

#     Returns:
#         Tuple of (figure, axes_array)
#     """
#     required_columns = [difficulty_column, outcome_column, trial_column]
#     if not validate_dataframe(trials_df, required_columns, "difficulty_analysis"):
#         return None, None

#     fig, axes = create_subplot_grid(2, 2, figsize)
#     fig.suptitle("Difficulty Analysis")

#     df_copy = trials_df.copy()
#     df_copy["success"] = (df_copy[outcome_column] == "correct").astype(int)

#     # Plot 1: Success rate vs difficulty
#     ax = axes[0]
#     difficulty_performance = df_copy.groupby(difficulty_column)["success"].agg(
#         ["mean", "std", "count"]
#     )

#     difficulties = difficulty_performance.index
#     means = difficulty_performance["mean"]
#     stds = difficulty_performance["std"]

#     ax.errorbar(difficulties, means, yerr=stds, fmt="o-", capsize=5, capthick=2)
#     ax.set_xlabel("Difficulty Level")
#     ax.set_ylabel("Success Rate")
#     ax.set_title("Success Rate vs Difficulty")
#     ax.grid(True, alpha=0.3)

#     # Add trend line
#     if len(difficulties) > 1:
#         z = np.polyfit(difficulties, means, 1)
#         trend_line = np.poly1d(z)
#         ax.plot(difficulties, trend_line(difficulties), "r--", alpha=0.7, label="Trend")
#         ax.legend()

#     # Plot 2: Trial distribution by difficulty
#     ax = axes[1]
#     difficulty_counts = df_copy[difficulty_column].value_counts().sort_index()

#     bars = ax.bar(
#         difficulty_counts.index,
#         difficulty_counts.values,
#         alpha=0.7,
#         color=plt.cm.viridis(np.linspace(0, 1, len(difficulty_counts))),
#     )
#     ax.set_xlabel("Difficulty Level")
#     ax.set_ylabel("Number of Trials")
#     ax.set_title("Trial Distribution by Difficulty")

#     # Add percentage labels
#     total_trials = difficulty_counts.sum()
#     for bar, count in zip(bars, difficulty_counts.values):
#         percentage = (count / total_trials) * 100
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             bar.get_height() + max(difficulty_counts) * 0.01,
#             f"{percentage:.1f}%",
#             ha="center",
#             va="bottom",
#         )

#     # Plot 3: Difficulty progression over trials
#     ax = axes[2]

#     # Create scatter plot with color-coded outcomes
#     outcome_colors = {"correct": "green", "incorrect": "red"}

#     for outcome, color in outcome_colors.items():
#         outcome_data = df_copy[df_copy[outcome_column] == outcome]
#         if not outcome_data.empty:
#             ax.scatter(
#                 outcome_data[trial_column],
#                 outcome_data[difficulty_column],
#                 color=color,
#                 alpha=0.6,
#                 s=20,
#                 label=outcome,
#             )

#     ax.set_xlabel("Trial Number")
#     ax.set_ylabel("Difficulty Level")
#     ax.set_title("Difficulty Progression Over Trials")
#     ax.legend()
#     ax.grid(True, alpha=0.3)

#     # Plot 4: Reaction time vs difficulty (if available)
#     ax = axes[3]

#     if "reaction_time" in df_copy.columns:
#         # Reaction time analysis
#         rt_by_diff = df_copy.groupby(difficulty_column)["reaction_time"].agg(
#             ["mean", "std"]
#         )

#         ax.errorbar(
#             rt_by_diff.index,
#             rt_by_diff["mean"],
#             yerr=rt_by_diff["std"],
#             fmt="o-",
#             capsize=5,
#             capthick=2,
#             color="orange",
#         )
#         ax.set_xlabel("Difficulty Level")
#         ax.set_ylabel("Reaction Time (ms)")
#         ax.set_title("Reaction Time vs Difficulty")
#     else:
#         # Alternative: outcome distribution by difficulty
#         outcome_by_diff = (
#             df_copy.groupby([difficulty_column, outcome_column])
#             .size()
#             .unstack(fill_value=0)
#         )
#         outcome_props = outcome_by_diff.div(outcome_by_diff.sum(axis=1), axis=0)

#         outcome_props.plot(kind="bar", stacked=True, ax=ax, alpha=0.7)
#         ax.set_xlabel("Difficulty Level")
#         ax.set_ylabel("Proportion")
#         ax.set_title("Outcome Distribution by Difficulty")
#         ax.legend(title="Outcome")
#         plt.setp(ax.get_xticklabels(), rotation=0)

#     ax.grid(True, alpha=0.3)

#     plt.tight_layout()

#     # Add summary statistics
#     correlation = df_copy[difficulty_column].corr(df_copy["success"])
#     summary_text = f"Difficulty-Performance Correlation: {correlation:.3f}\n"
#     summary_text += f"Difficulty Range: {df_copy[difficulty_column].min():.1f} - {df_copy[difficulty_column].max():.1f}\n"
#     summary_text += f"Total Trials: {len(df_copy)}"

#     fig.text(
#         0.02,
#         0.02,
#         summary_text,
#         transform=fig.transFigure,
#         bbox=dict(boxstyle="round", facecolor="lightgray"),
#     )

#     if save_path:
#         save_plot(fig, save_path)

#     logger.info(f"Created difficulty analysis plot for {len(df_copy)} trials")
#     return fig, axes


# def plot_learning_curves(
#     performance_df: pd.DataFrame,
#     animal_ids: Optional[List[int]] = None,
#     session_column: str = "session",
#     metric_column: str = "correct_rate",
#     grouping_column: Optional[str] = None,
#     figsize: Tuple[int, int] = (12, 8),
#     save_path: Optional[str] = None,
# ) -> Tuple[plt.Figure, plt.Axes]:
#     """Plot learning curves for animals or groups.

#     Args:
#         performance_df: DataFrame with performance data over time
#         animal_ids: List of animal IDs to include (optional)
#         session_column: Column with session/time information
#         metric_column: Performance metric to plot
#         grouping_column: Column to group animals by (e.g., 'protocol')
#         figsize: Figure size
#         save_path: Path to save the plot (optional)

#     Returns:
#         Tuple of (figure, axes)
#     """
#     required_columns = ["animal_id", session_column, metric_column]
#     if not validate_dataframe(performance_df, required_columns, "learning_curves"):
#         return None, None

#     # Filter by animal IDs if provided
#     df_copy = performance_df.copy()
#     if animal_ids:
#         df_copy = df_copy[df_copy["animal_id"].isin(animal_ids)]

#     fig, ax = create_figure(figsize, title="Learning Curves")

#     if grouping_column and grouping_column in df_copy.columns:
#         # Plot grouped learning curves
#         groups = df_copy[grouping_column].unique()
#         colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))

#         for i, group in enumerate(groups):
#             group_data = df_copy[df_copy[grouping_column] == group]

#             # Calculate mean and SEM across animals in group
#             group_stats = group_data.groupby(session_column)[metric_column].agg(
#                 ["mean", "sem"]
#             )

#             sessions = group_stats.index
#             means = group_stats["mean"]
#             sems = group_stats["sem"]

#             ax.plot(
#                 sessions,
#                 means,
#                 "o-",
#                 color=colors[i],
#                 linewidth=2,
#                 markersize=6,
#                 label=f"{grouping_column}: {group}",
#             )
#             ax.fill_between(
#                 sessions, means - sems, means + sems, color=colors[i], alpha=0.2
#             )
#     else:
#         # Plot individual animal curves
#         animals = sorted(df_copy["animal_id"].unique())
#         colors = plt.cm.tab10(np.linspace(0, 1, len(animals)))

#         for i, animal in enumerate(animals):
#             animal_data = df_copy[df_copy["animal_id"] == animal].sort_values(
#                 session_column
#             )

#             ax.plot(
#                 animal_data[session_column],
#                 animal_data[metric_column],
#                 "o-",
#                 color=colors[i],
#                 alpha=0.7,
#                 linewidth=1.5,
#                 markersize=4,
#                 label=f"Animal {animal}",
#             )

#         # Add group average
#         group_avg = df_copy.groupby(session_column)[metric_column].mean()
#         ax.plot(
#             group_avg.index,
#             group_avg.values,
#             "k-",
#             linewidth=3,
#             label="Group Average",
#             alpha=0.8,
#         )

#     ax.set_xlabel("Session")
#     ax.set_ylabel(metric_column.replace("_", " ").title())
#     ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
#     ax.grid(True, alpha=0.3)

#     # Add performance milestones
#     if metric_column in ["correct_rate", "reward_rate"]:
#         ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="Chance Level")
#         ax.axhline(y=0.8, color="green", linestyle="--", alpha=0.5, label="Proficiency")

#     plt.tight_layout()

#     if save_path:
#         save_plot(fig, save_path)

#     logger.info(
#         f"Created learning curves plot for {len(df_copy['animal_id'].unique())} animals"
#     )
#     return fig, ax
