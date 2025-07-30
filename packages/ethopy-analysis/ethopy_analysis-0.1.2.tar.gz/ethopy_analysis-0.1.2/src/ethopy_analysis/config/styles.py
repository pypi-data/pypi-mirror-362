"""
Optional styling system for Ethopy plots.

This module provides an optional Style class that users can use to apply
good styling defaults to their plots. Users can also customize the style
or completely ignore it and use their own matplotlib setup.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import logging

logger = logging.getLogger(__name__)


class Style:
    """Optional styling for Ethopy plots.

    This class provides good defaults for plot styling that users can
    optionally apply. Users can also customize individual aspects or
    completely ignore this and use their own matplotlib setup.

    Examples:
        # Use default styling
        Style().apply()

        # Customize specific aspects
        style = Style()
        style.font_size = 16
        style.primary_color = "#FF0000"
        style.apply()

        # Or ignore completely and use your own matplotlib setup
        plt.style.use('seaborn-v0_8')
    """

    def __init__(self):
        # Core settings
        self.font_size = 12
        self.title_size = 16
        self.label_size = 14
        self.tick_size = 10
        self.legend_size = 11
        self.font_family = "DejaVu Sans"

        # Figure settings
        self.figure_size = (10, 6)
        self.dpi = 300
        self.background_color = "white"

        # Colors
        self.primary_color = "#4169E1"  # Sea green
        self.secondary_color = "#2E8B57"  # Royal blue
        self.accent_color = "#DC143C"  # Crimson

        # Color palette for multiple categories
        self.color_palette = [
            "#4169E1",
            "#2E8B57",
            "#DC143C",
            "#FF8C00",
            "#8A2BE2",
            "#00CED1",
            "#FF69B4",
            "#32CD32",
            "#FFD700",
            "#FF6347",
        ]

        # Layout settings
        self.grid_enabled = True
        self.grid_color = "#E5E5E5"
        self.grid_alpha = 0.3
        self.remove_top_spine = True
        self.remove_right_spine = True
        self.spine_width = 1.0

        # Line and marker settings
        self.line_width = 2.0
        self.marker_size = 6.0

    def apply(self):
        """Apply this style to matplotlib."""
        # Reset to clean state
        plt.style.use("default")

        # Core settings
        mpl.rcParams["figure.figsize"] = self.figure_size
        mpl.rcParams["figure.dpi"] = self.dpi
        mpl.rcParams["savefig.dpi"] = self.dpi
        mpl.rcParams["figure.facecolor"] = self.background_color

        # Typography
        mpl.rcParams["font.size"] = self.font_size
        mpl.rcParams["font.family"] = self.font_family
        mpl.rcParams["axes.titlesize"] = self.title_size
        mpl.rcParams["axes.labelsize"] = self.label_size
        mpl.rcParams["xtick.labelsize"] = self.tick_size
        mpl.rcParams["ytick.labelsize"] = self.tick_size
        mpl.rcParams["legend.fontsize"] = self.legend_size

        # Colors
        mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=self.color_palette)
        mpl.rcParams["axes.facecolor"] = self.background_color
        mpl.rcParams["axes.edgecolor"] = "black"
        mpl.rcParams["axes.linewidth"] = self.spine_width

        # Grid
        mpl.rcParams["axes.grid"] = self.grid_enabled
        mpl.rcParams["grid.color"] = self.grid_color
        mpl.rcParams["grid.alpha"] = self.grid_alpha
        mpl.rcParams["grid.linewidth"] = 0.8

        # Spines
        mpl.rcParams["axes.spines.top"] = not self.remove_top_spine
        mpl.rcParams["axes.spines.right"] = not self.remove_right_spine

        # Lines and markers
        mpl.rcParams["lines.linewidth"] = self.line_width
        mpl.rcParams["lines.markersize"] = self.marker_size
        mpl.rcParams["errorbar.capsize"] = 3

        # Apply seaborn style for clean look
        sns.set_style("whitegrid")

        logger.info("Applied Ethopy default style")

    def customize(self, **kwargs):
        """Customize style parameters.

        Args:
            **kwargs: Style parameters to override

        Example:
            style = Style()
            style.customize(font_size=16, primary_color="#FF0000")
            style.apply()
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"Unknown style parameter: {key}")

    def __repr__(self):
        return (
            f"Style(font_size={self.font_size}, primary_color='{self.primary_color}')"
        )


# Convenience functions for easy usage
def apply_default_style():
    """Apply the default Ethopy style."""
    Style().apply()


def create_custom_style(**kwargs) -> Style:
    """Create and return a customized style.

    Args:
        **kwargs: Style parameters to customize

    Returns:
        Customized Style instance

    Example:
        style = create_custom_style(font_size=16, primary_color="#FF0000")
        style.apply()
    """
    style = Style()
    style.customize(**kwargs)
    return style
