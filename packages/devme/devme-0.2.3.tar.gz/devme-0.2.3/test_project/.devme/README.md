# DevMe Configuration

This directory contains DevMe configuration files:

- **config.json**: Main configuration
- **env-paths.json**: Additional environment file paths
- **ignore.txt**: Additional ignore patterns
- **custom-services.yaml**: Custom service definitions (create as needed)

## Configuration Options

### env_file_patterns
Patterns for finding environment files recursively:
```json
[
  ".env*",
  "server/.env*",
  "config/.env*"
]
```

### search_depth
How deep to search for environment files (default: 3)

### ignore_patterns
Patterns to ignore when counting project files
