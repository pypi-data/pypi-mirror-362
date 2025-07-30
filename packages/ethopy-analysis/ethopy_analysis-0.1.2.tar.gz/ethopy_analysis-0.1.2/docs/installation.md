# Installation

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for development installation)

## Installation Methods

### Development Installation (Recommended)

For development or the latest features:

```bash
# Clone the repository
git clone <repository-url>
cd ethopy_analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Package Installation

```bash
pip install ethopy-analysis
```

## Optional Dependencies

### Documentation Tools
```bash
pip install -e ".[docs]"
```

Includes:
- mkdocs
- mkdocs-material
- mkdocstrings

### Development Tools
```bash
pip install -e ".[dev]"
```

Includes:
- pytest (testing)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- jupyter (notebooks)

## Verify Installation

Test that the package is installed correctly:

```bash
# Test CLI
ethopy-analysis --help

# Test Python import
python -c "import ethopy_analysis; print('Installation successful')"
```

## Dependencies

### Core Dependencies
- **datajoint** (≥0.13.0) - Database connectivity
- **matplotlib** (≥3.5.0) - Plotting
- **pandas** (≥1.3.0) - Data manipulation
- **numpy** (≥1.20.0) - Numerical computing
- **seaborn** (≥0.11.0) - Statistical visualization
- **plotly** (≥5.0.0) - Interactive plots
- **opencv-python** (≥4.5.0) - Video analysis
- **click** (≥8.0.0) - Command-line interface
- **tqdm** (≥4.60.0) - Progress bars
- **ipykernel** (≥6.0.0) - Jupyter support

## Database Setup

The package works without database configuration, but for full functionality:

1. **Configure database connection** (see [Configuration Guide](configuration.md))
2. **Test connection**:
   ```bash
   ethopy-analysis test-db-connection
   ```

## Troubleshooting

### Common Issues

**Import errors**:
```bash
# Reinstall with all dependencies
pip install -e ".[dev,docs]"
```

**Permission errors**:
```bash
# Use user installation
pip install --user -e .
```

**Database connection issues**:
- Check network connectivity
- Verify database credentials
- See [Configuration Guide](configuration.md)

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search existing GitHub issues
3. Create a new issue with error details