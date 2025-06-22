# Scripts Directory

This directory contains all development, deployment, migration, and utility scripts organized by purpose.

## Directory Structure

### `/dev/` - Development Scripts
- **`setup.sh`** - Claude Code development environment setup
- **`start.sh`** - Start development server
- **`start-v6.sh`** - Start v6 development server
- **`stop.sh`** - Stop development server  
- **`stop-v6.sh`** - Stop v6 development server
- **`status.sh`** - Check server status
- **`restore-git.sh`** - Git restoration utilities
- **`dev-shell.sh`** - Development shell access

### `/deployment/` - Deployment Scripts
- **`logs-v6.sh`** - View application logs

### `/migration/` - Data Migration Scripts
- **`migrate_projects.py`** - Project data migration utility
- **`run_migration.sh`** - Execute migration in Docker container
- **`v5-to-v6-setup.sh`** - Version upgrade setup script

### `/testing/` - Testing & Validation Scripts
- **`test_sun_optimizations.py`** - Sun calculation performance tests
- **`validate_optimizations.py`** - Validation utilities for optimizations

### `/tools/` - Command Line Tools
- **`cc`** - Claude Code CLI tool
- **`claude-code`** - Main Claude Code executable  
- **`dev-shell`** - Development shell tool

## Usage

### Development
```bash
# Start development environment
./scripts/dev/start.sh

# Check status
./scripts/dev/status.sh

# Stop development environment  
./scripts/dev/stop.sh
```

### Migration
```bash
# Run project migration
./scripts/migration/run_migration.sh
```

### Tools (Available from Root)
```bash
# Command line tools are symlinked to root for convenience
./cc
./claude-code
./dev-shell
```

## Note

All scripts maintain their original functionality. This reorganization improves project structure without changing script behavior.