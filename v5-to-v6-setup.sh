#!/bin/bash

# Film Production Scheduler v5 to v6 Transition Script
# This script creates a complete backup of v5 and sets up v6 for Claude Code development

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V5_DIR="${SCRIPT_DIR}"
V6_DIR="${SCRIPT_DIR}/../film-scheduler-v6"
BACKUP_BASE_DIR="${SCRIPT_DIR}/../backups"
BACKUP_DIR="${BACKUP_BASE_DIR}/film-scheduler-v5-stable-${TIMESTAMP}"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Create backup directory structure
create_backup_structure() {
    print_status "Creating backup directory structure..."
    
    mkdir -p "${BACKUP_DIR}"
    mkdir -p "${BACKUP_DIR}/logs"
    mkdir -p "${BACKUP_BASE_DIR}/scripts"
    
    print_success "Backup directory created: ${BACKUP_DIR}"
}

# Backup v5 installation
backup_v5() {
    print_status "Creating comprehensive v5 backup..."
    
    # Copy entire application
    print_status "Copying application files..."
    cp -R "${V5_DIR}/." "${BACKUP_DIR}/"
    
    # Create compressed data backup
    print_status "Creating compressed data backup..."
    if [ -d "${V5_DIR}/data" ]; then
        tar -czf "${BACKUP_DIR}/data-backup-${TIMESTAMP}.tar.gz" -C "${V5_DIR}" data/
        print_success "Data backup created"
    else
        print_warning "No data directory found in v5"
    fi
    
    # Backup Docker state
    print_status "Backing up Docker configuration..."
    if [ -f "${V5_DIR}/docker-compose.yml" ]; then
        docker-compose -f "${V5_DIR}/docker-compose.yml" config > "${BACKUP_DIR}/docker-compose-verified.yml" 2>/dev/null || true
    fi
    
    # Backup container state if running
    if docker ps | grep -q "film-scheduler-v5"; then
        print_status "Backing up running container state..."
        docker inspect film-scheduler-v5 > "${BACKUP_DIR}/container-state.json" 2>/dev/null || true
        docker logs film-scheduler-v5 > "${BACKUP_DIR}/container-logs.txt" 2>/dev/null || true
    else
        print_warning "v5 container is not currently running"
    fi
    
    # Create restore script
    cat > "${BACKUP_DIR}/restore-v5.sh" << 'EOF'
#!/bin/bash
# Restore script for v5 from this backup

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
V5_RESTORE_DIR="${1:-../film-scheduler-v5-restored}"

echo "Restoring v5 to: ${V5_RESTORE_DIR}"

# Create restore directory
mkdir -p "${V5_RESTORE_DIR}"

# Copy all files except this backup directory
cp -R "${SCRIPT_DIR}"/* "${V5_RESTORE_DIR}/" 2>/dev/null || true
rm -rf "${V5_RESTORE_DIR}/backups" 2>/dev/null || true

# Extract data backup if it exists
if [ -f "${SCRIPT_DIR}/data-backup-"*.tar.gz ]; then
    echo "Extracting data backup..."
    tar -xzf "${SCRIPT_DIR}"/data-backup-*.tar.gz -C "${V5_RESTORE_DIR}/"
fi

echo "v5 restored to: ${V5_RESTORE_DIR}"
echo "To start: cd ${V5_RESTORE_DIR} && docker-compose up -d"
EOF
    
    chmod +x "${BACKUP_DIR}/restore-v5.sh"
    
    print_success "v5 backup completed"
}

# Verify backup integrity
verify_backup() {
    print_status "Verifying backup integrity..."
    
    local errors=0
    
    # Check essential files
    if [ ! -f "${BACKUP_DIR}/app.py" ]; then
        print_error "app.py not found in backup"
        ((errors++))
    fi
    
    if [ ! -f "${BACKUP_DIR}/docker-compose.yml" ]; then
        print_error "docker-compose.yml not found in backup"
        ((errors++))
    fi
    
    if [ -d "${V5_DIR}/data" ] && [ ! -d "${BACKUP_DIR}/data" ]; then
        print_error "Data directory not backed up"
        ((errors++))
    fi
    
    if [ $errors -gt 0 ]; then
        print_error "Backup verification failed with $errors errors"
        exit 1
    fi
    
    print_success "Backup verification passed"
}

# Create v6 project structure
create_v6_structure() {
    print_status "Creating v6 project structure..."
    
    # Remove existing v6 directory if it exists
    if [ -d "${V6_DIR}" ]; then
        print_warning "Existing v6 directory found, backing it up..."
        mv "${V6_DIR}" "${V6_DIR}-backup-${TIMESTAMP}"
    fi
    
    # Copy v5 to v6
    cp -R "${V5_DIR}" "${V6_DIR}"
    
    print_success "v6 project structure created"
}

# Update v6 configuration files
update_v6_config() {
    print_status "Updating v6 configuration files..."
    
    # Update docker-compose.yml for v6
    cat > "${V6_DIR}/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  film-scheduler:
    build: .
    container_name: film-scheduler-v6
    restart: unless-stopped
    ports:
      - "5076:5000"  # Changed from 5075 to avoid conflict with v5
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - TZ=Europe/Dublin
      - VIEWER_PASSWORD=${VIEWER_PASSWORD}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD}
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=${FLASK_ENV:-development}
      - FLASK_DEBUG=${FLASK_DEBUG:-1}
      - PYTHONUNBUFFERED=1
    networks:
      - film-scheduler-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  film-scheduler-network:
    driver: bridge

volumes:
  scheduler-data:
    driver: local
EOF
    
    # Create v6 environment template
    cat > "${V6_DIR}/.env.example" << 'EOF'
# Film Production Scheduler v6 Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-v6-change-this
TZ=Europe/Dublin

# Authentication (use different passwords for v6)
VIEWER_PASSWORD=viewer_v6
ADMIN_PASSWORD=admin_v6

# Development
FLASK_DEBUG=1
PYTHONUNBUFFERED=1
EOF
    
    # Create actual .env file if it doesn't exist
    if [ ! -f "${V6_DIR}/.env" ]; then
        cp "${V6_DIR}/.env.example" "${V6_DIR}/.env"
        print_warning "Created default .env file - please update with your settings"
    fi
    
    print_success "v6 configuration updated"
}

# Initialize git repository for Claude Code
setup_git_for_claude_code() {
    print_status "Setting up Git repository for Claude Code..."
    
    cd "${V6_DIR}"
    
    # Initialize git if not already done
    if [ ! -d ".git" ]; then
        git init
        print_status "Initialized new Git repository"
    fi
    
    # Create .gitignore
    cat > .gitignore << 'EOF'
# Environment and secrets
.env
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Data directories (comment out if you want to track data)
data/
logs/

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Backup files
*-backup-*/
*.backup
EOF
    
    # Add files and create initial commit
    git add .
    git commit -m "Initial v6 setup from v5 stable backup

- Migrated from film-scheduler-v5
- Updated container name to film-scheduler-v6
- Changed port from 5075 to 5076
- Set up for Claude Code development
- Backup created at: ${BACKUP_DIR}" || true
    
    # Create development branch for Claude Code
    git checkout -b claude-code-development
    git checkout main  # Return to main branch
    
    cd "${SCRIPT_DIR}"
    
    print_success "Git repository configured for Claude Code"
}

# Create management scripts
create_management_scripts() {
    print_status "Creating management scripts..."
    
    # Create start script for v6
    cat > "${V6_DIR}/start-v6.sh" << 'EOF'
#!/bin/bash
# Start Film Scheduler v6

echo "Starting Film Scheduler v6..."
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

echo "v6 started on http://localhost:5076"
echo "Admin: http://localhost:5076/admin/login"
EOF
    
    # Create stop script for v6
    cat > "${V6_DIR}/stop-v6.sh" << 'EOF'
#!/bin/bash
# Stop Film Scheduler v6

echo "Stopping Film Scheduler v6..."
docker-compose down
echo "v6 stopped"
EOF
    
    # Create logs script for v6
    cat > "${V6_DIR}/logs-v6.sh" << 'EOF'
#!/bin/bash
# View v6 logs

docker-compose logs -f
EOF
    
    # Create status script
    cat > "${V6_DIR}/status.sh" << 'EOF'
#!/bin/bash
# Check status of both v5 and v6

echo "=== Film Scheduler Status ==="
echo ""

# Check v5
if docker ps | grep -q "film-scheduler-v5"; then
    echo "✅ v5 (stable): Running on http://localhost:5075"
else
    echo "❌ v5 (stable): Not running"
fi

# Check v6
if docker ps | grep -q "film-scheduler-v6"; then
    echo "✅ v6 (development): Running on http://localhost:5076"
else
    echo "❌ v6 (development): Not running"
fi

echo ""
echo "Docker containers:"
docker ps | grep film-scheduler || echo "No film-scheduler containers running"
EOF
    
    # Make scripts executable
    chmod +x "${V6_DIR}"/*.sh
    
    print_success "Management scripts created"
}

# Create documentation
create_v6_documentation() {
    print_status "Creating v6 documentation..."
    
    # Create transition documentation
    cat > "${V6_DIR}/V5-TO-V6-TRANSITION.md" << EOF
# v5 to v6 Transition Documentation

## Transition Summary
- **Transition Date**: ${TIMESTAMP}
- **v5 Backup Location**: ${BACKUP_DIR}
- **v6 Location**: ${V6_DIR}

## Port Configuration
- **v5 (stable)**: http://localhost:5075
- **v6 (development)**: http://localhost:5076

## Quick Commands

### Start v6
\`\`\`bash
cd ${V6_DIR}
./start-v6.sh
\`\`\`

### Check Status
\`\`\`bash
cd ${V6_DIR}
./status.sh
\`\`\`

### View Logs
\`\`\`bash
cd ${V6_DIR}
./logs-v6.sh
\`\`\`

## Backup Information
Full v5 backup available at: ${BACKUP_DIR}

To restore v5 if needed:
\`\`\`bash
cd ${BACKUP_DIR}
./restore-v5.sh /path/to/restore/location
\`\`\`

## Claude Code Setup
1. Install Claude Code CLI
2. Navigate to: ${V6_DIR}
3. Start Claude Code session
4. Begin development on 'claude-code-development' branch

## Data Migration
When v6 is stable and ready for production:
\`\`\`bash
cp -R /path/to/v5/data/* ${V6_DIR}/data/
cd ${V6_DIR}
docker-compose restart
\`\`\`
EOF
    
    print_success "Documentation created"
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "  Film Production Scheduler v5 to v6 Transition"
    echo "=================================================="
    echo -e "${NC}"
    
    print_status "Starting transition process..."
    
    # Execute all steps
    check_prerequisites
    create_backup_structure
    backup_v5
    verify_backup
    create_v6_structure
    update_v6_config
    setup_git_for_claude_code
    create_management_scripts
    create_v6_documentation
    
    echo ""
    echo -e "${GREEN}🎉 Transition completed successfully! 🎉${NC}"
    echo ""
    echo "=== Summary ==="
    echo "✅ v5 backed up to: ${BACKUP_DIR}"
    echo "✅ v6 created at: ${V6_DIR}"
    echo "✅ Git repository initialized for Claude Code"
    echo "✅ Management scripts created"
    echo ""
    echo "=== Next Steps ==="
    echo "1. Review and update ${V6_DIR}/.env with your settings"
    echo "2. Start v6: cd ${V6_DIR} && ./start-v6.sh"
    echo "3. Test v6 at: http://localhost:5076"
    echo "4. Install Claude Code CLI for development"
    echo "5. Begin Claude Code development in the 'claude-code-development' branch"
    echo ""
    echo "=== Important ==="
    echo "• v5 remains untouched for stability"
    echo "• v6 runs on port 5076 (v5 uses 5075)"
    echo "• Both versions can run simultaneously"
    echo "• Full backup available for rollback if needed"
    echo ""
    print_success "Happy coding with Claude Code! 🚀"
}

# Run main function
main "$@"
