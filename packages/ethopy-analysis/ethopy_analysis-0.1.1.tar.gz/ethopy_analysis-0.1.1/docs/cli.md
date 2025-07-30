# CLI Reference

The Ethopy Analysis package provides a comprehensive command-line interface for batch analysis and data processing.

## Installation

After installing the package, the CLI is available as:

```bash
ethopy-analysis --help
```

## Commands

The CLI provides 5 main commands:

- `analyze-animal` - Generate comprehensive analysis plots for an animal
- `generate-report` - Create detailed analysis report with plots and statistics
- `session-summary` - Display detailed information about a specific session
- `config-summary` - Show current configuration and source file path
- `test-db-connection` - Test database connectivity and schema access

### analyze-animal

Generate comprehensive analysis plots for a specific animal.

```bash
ethopy-analysis analyze-animal --animal-id 123 [OPTIONS]
```

**Options:**
- `--animal-id INTEGER` (required): Animal ID to analyze
- `--save-plots`: Save plots to output directory
- `--output-dir PATH`: Output directory for plots (default: `./plots`)
- `--min-trials INTEGER`: Minimum trials per session (default: 2)

**Examples:**
```bash
# Basic analysis with plots displayed
ethopy-analysis analyze-animal --animal-id 123

# Save plots to custom directory
ethopy-analysis analyze-animal --animal-id 123 --save-plots --output-dir ./results

# Filter sessions with minimum 20 trials
ethopy-analysis analyze-animal --animal-id 123 --min-trials 20 --save-plots
```

**Generated Plots:**
- Session dates over time
- Performance vs liquid consumption
- Session-wise performance trends
- Trials per session distribution

### generate-report

Create a comprehensive analysis report for an animal.

```bash
ethopy-analysis generate-report --animal-id 123 [OPTIONS]
```

**Options:**
- `--animal-id INTEGER` (required): Animal ID for report
- `--output-dir PATH`: Output directory for report (default: `./reports`)

**Examples:**
```bash
# Generate report in default location
ethopy-analysis generate-report --animal-id 123

# Custom output directory
ethopy-analysis generate-report --animal-id 123 --output-dir ./animal_reports
```

**Report Contents:**
- Session summary statistics
- Performance metrics per session
- Generated plots saved to subdirectory
- Text report with analysis details

### session-summary

Print detailed information about a specific session.

```bash
ethopy-analysis session-summary --animal-id 123 --session 5
```

**Options:**
- `--animal-id INTEGER` (required): Animal ID
- `--session INTEGER` (required): Session number
- Short options: `-a` for animal-id, `-s` for session

**Examples:**
```bash
# Basic usage
ethopy-analysis session-summary --animal-id 123 --session 5

# Using short options
ethopy-analysis session-summary -a 123 -s 5
```

**Output Information:**
- Session metadata (user, setup, timestamps)
- Performance metrics
- Trial counts and statistics
- Experiment configuration details

### config-summary

Display current configuration summary and source file path.

```bash
ethopy-analysis config-summary
```

**No options required.**

**Output:**
- Configuration file path being used
- Environment variable overrides
- Database connection settings (without password)
- Schema mappings
- Output directory settings

**Example output:**
```
Ethopy Analysis Configuration Summary:
==================================================
Configuration file: /path/to/dj_conf.json
Environment overrides: DJ_PASSWORD

Database Host: database.example.org:3306
Database User: username
Database Password: Set
Schemas: 3
Schema mappings:
  experiment: lab_experiments
  stimulus: lab_stimuli
  behavior: lab_behavior

Output Directory: ./output
```

### test-db-connection

Test database connectivity and schema access.

```bash
ethopy-analysis test-db-connection
```

**No options required.**

**Output:**
- Database connection status
- Schema accessibility verification
- Connection configuration details

## Global Options

All commands support these global options:

- `--help`: Show command help
- `--version`: Show package version

## Configuration

The CLI uses the same configuration system as the Python API:

1. **Environment variables**: `DJ_HOST`, `DJ_USER`, `DJ_PASSWORD`
2. **Configuration files**: `dj_conf.json`, `config.json`, `ethopy_config.json`
3. **Default values**: Reasonable defaults for most settings

See [Configuration Guide](configuration.md) for detailed setup.

## Usage Workflows

### Single Animal Analysis
```bash
# 1. Check configuration
ethopy-analysis config-summary

# 2. Test database connection
ethopy-analysis test-db-connection

# 3. Analyze animal with plots
ethopy-analysis analyze-animal --animal-id 123 --save-plots

# 4. Generate comprehensive report
ethopy-analysis generate-report --animal-id 123
```

### Session Investigation
```bash
# 1. Get session overview
ethopy-analysis session-summary --animal-id 123 --session 5

# 2. Generate plots for analysis
ethopy-analysis analyze-animal --animal-id 123 --save-plots
```

### Batch Processing
```bash
# Process multiple animals
for animal_id in 123 124 125; do
    ethopy-analysis analyze-animal --animal-id $animal_id --save-plots --output-dir ./batch_results
done
```

## Output Files

### analyze-animal
```
./plots/
├── animal_123_session_dates.png
├── animal_123_performance_liquid.png
├── animal_123_session_performance.png
└── animal_123_trials_per_session.png
```

### generate-report
```
./reports/
├── animal_123_report.txt
└── animal_123_plots/
    ├── animal_123_session_dates.png
    ├── animal_123_performance_liquid.png
    ├── animal_123_session_performance.png
    └── animal_123_trials_per_session.png
```

## Error Handling

The CLI provides informative error messages:

- **Database connection issues**: Check configuration
- **Missing animal data**: Verify animal ID and database content
- **Permission errors**: Check output directory permissions
- **Invalid arguments**: Review command syntax

## Integration

### Shell Scripts
```bash
#!/bin/bash
# analyze_daily.sh
ANIMAL_ID=$1
DATE=$(date +%Y-%m-%d)
OUTPUT_DIR="./daily_analysis/$DATE"

ethopy-analysis analyze-animal --animal-id $ANIMAL_ID --save-plots --output-dir $OUTPUT_DIR
ethopy-analysis generate-report --animal-id $ANIMAL_ID --output-dir $OUTPUT_DIR
```

### Python Integration
```python
import subprocess

# Run CLI from Python
result = subprocess.run([
    'ethopy-analysis', 'analyze-animal', 
    '--animal-id', '123', '--save-plots'
], capture_output=True, text=True)

print(result.stdout)
```

## Troubleshooting

### Common Issues

**Command not found**:
```bash
# Check installation
pip show ethopy-analysis

# Reinstall if needed
pip install -e .
```

**Database connection errors**:
```bash
# Test connection
ethopy-analysis test-db-connection

# Check configuration
export DJ_HOST="your-database:3306"
export DJ_USER="your-username"
export DJ_PASSWORD="your-password"
```

**Permission errors**:
```bash
# Check directory permissions
ls -la ./plots

# Use different output directory
ethopy-analysis analyze-animal --animal-id 123 --output-dir ~/analysis
```

For more help, see the [Troubleshooting Guide](troubleshooting.md).