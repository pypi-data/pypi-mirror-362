# Configuration

The Ethopy Analysis package uses a unified configuration system for database connections and analysis settings. Configuration is **optional** - the package works with defaults.

## Quick Setup

### Method 1: Template File (Recommended)
```bash
# Copy template and add your credentials
cp dj_conf.template.json dj_conf.json
# Edit dj_conf.json with your database details
```

### Method 2: Environment Variables
```bash
export DJ_HOST="database.example.org:3306"
export DJ_USER="your_username" 
export DJ_PASSWORD="your_password"
```

### Method 3: Custom Configuration
```bash
ethopy-analysis create-config --output-path config.json
```

## Configuration Format

All configuration files use unified JSON format:

```json
{
  "database": {
    "host": "your-database-host:3306",
    "user": "your_username",
    "password": "your_password",
    "schemas": {
      "experiment": "lab_experiments",
      "stimulus": "lab_stimuli",
      "behavior": "lab_behavior"
    }
  },
  "paths": {
    "data_dir": "./data",
    "output_dir": "./output"
  }
}
```

## Database Configuration

### Required Fields
- `host`: Database host and port
- `user`: Database username
- `password`: Database password
- `schemas`: Schema mappings for experiment tables

### Schema Mapping
```json
{
  "schemas": {
    "experiment": "lab_experiments",
    "stimulus": "lab_stimuli", 
    "behavior": "lab_behavior"
  }
}
```

## Configuration Discovery

The system searches for configuration files in this order:

1. Current directory: `ethopy_config.json`, `config.json`, `dj_conf.json`
2. Config subdirectory: `./config/`
3. User home: `~/.ethopy/`
4. Package directory

## Environment Variables

Override any configuration with environment variables:

```bash
# Database
export DJ_HOST="database.example.org:3306"
export DJ_USER="your_username"
export DJ_PASSWORD="your_password"

# Paths
export ETHOPY_DATA_DIR="/path/to/data"
export ETHOPY_OUTPUT_DIR="/path/to/output"
```

## Security Best Practices

### 1. Use Environment Variables
```bash
# Recommended for production
export DJ_PASSWORD="your_secure_password"
```

### 2. Local Configuration Files
- Configuration files with passwords are in `.gitignore`
- Use `dj_conf.template.json` as starting point
- Keep credentials in local `dj_conf.json`

### 3. Never Commit Passwords
- Template files contain no credentials
- Local config files are git-ignored
- Use environment variables for CI/CD

## Testing Configuration

### Test Database Connection
```bash
ethopy-analysis test-db-connection
```

### View Current Configuration
```bash
ethopy-analysis config-summary
```

## Usage Examples

### Basic Usage (No Configuration)
```python
from ethopy_analysis.plots.animal import plot_animal_performance

# Works with defaults
plot_animal_performance(your_dataframe)
```

### With Database
```python
from ethopy_analysis.data.loaders import load_animal_data

# Uses configured database
animal_data = load_animal_data(animal_id=123)
```

### Load Specific Config
```python
from ethopy_analysis.config.settings import load_config

# Load specific file
config = load_config("my_config.json")
```

## Common Configurations

### Development Setup
```json
{
  "database": {
    "host": "localhost:3306",
    "user": "dev_user",
    "schemas": {
      "experiment": "dev_experiments",
      "stimulus": "dev_stimuli",
      "behavior": "dev_behavior"
    }
  },
  "paths": {
    "data_dir": "./dev_data",
    "output_dir": "./dev_output"
  }
}
```

### Production Setup
```json
{
  "database": {
    "host": "production.database.org:3306",
    "user": "prod_user",
    "schemas": {
      "experiment": "lab_experiments",
      "stimulus": "lab_stimuli",
      "behavior": "lab_behavior"
    }
  },
  "paths": {
    "data_dir": "/data/experiments",
    "output_dir": "/data/analysis_output"
  }
}
```

## Troubleshooting

### Configuration Not Found
- Check file names and search paths
- Use absolute path: `load_config("/full/path/to/config.json")`

### Database Connection Issues
- Verify host:port format
- Check credentials
- Test with `ethopy-analysis test-db-connection`

### Permission Errors
- Check file permissions
- Verify directory write access
- Use environment variables for sensitive data

## No Configuration Required

The package works without configuration:
- Database: Uses environment variables or prompts
- Paths: Uses current directory
- Analysis: Uses reasonable defaults

Configure only what you need to customize!