# Ethopy Analysis

A comprehensive Python package for analyzing and visualizing behavioral data from Ethopy experiments.

## Overview

Ethopy Analysis provides a modern, modular approach to behavioral data analysis with the following key features:

- **DataFrame-based**: Plotting functions work with pandas DataFrames
- **Modular Design**: Composable functions for different analysis levels (animal, session, comparison)
- **Database Agnostic**: Works with DataJoint databases, CSV files, or any pandas-compatible data source
- **Extensible**: Plugin system for custom plots and analysis functions
- **Production Ready**: Command-line interface, proper packaging, and configuration management

## Quick Links

- [Installation Guide](installation.md) - Get started with the package
- [Quick Start](quickstart.md) - Jump into analysis with examples
- [CLI Reference](cli.md) - Command-line interface documentation
- [Configuration](configuration.md) - Database and system configuration
- [API Reference](api-reference.md) - Function documentation

## Package Architecture

The package is organized into focused modules:

- **`data/`** - Data loading and processing functions
- **`plots/`** - Plotting functions (DataFrame-based, database-agnostic)
- **`db/`** - Database connectivity
- **`config/`** - Configuration management
- **`cli.py`** - Command-line interface

## Getting Started

1. **[Install the package](installation.md)** - Set up your environment
2. **[Configure your database](configuration.md)** - Set up database connection (optional)
3. **[Try the quick start](quickstart.md)** - Run your first analysis
4. **[Explore examples](quickstart.md#example-notebooks)** - Check out the Jupyter notebooks

## Example Usage

```python
# Basic animal analysis
from ethopy_analysis.data.loaders import get_sessions
from ethopy_analysis.plots.animal import plot_session_performance

# Load data
sessions = get_sessions(animal_id=123, min_trials=20)

# Create visualization
fig, ax = plot_session_performance(123, sessions['session'].values)
```

## Support

- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Complete API reference and examples
- **Examples**: Jupyter notebooks with real analysis workflows