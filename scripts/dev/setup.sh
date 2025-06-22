#!/bin/bash

# Claude Code Development Container Setup for Unraid
# This creates a persistent development environment for Claude Code

set -e

# Configuration
DEV_CONTAINER_NAME="claude-code-dev"
PROJECT_DIR="/mnt/user/appdata/film-scheduler-v6"
WORKSPACE_DIR="/workspace"

echo "🚀 Setting up Claude Code development environment for Unraid..."

# Check if container already exists
if docker ps -a | grep -q ${DEV_CONTAINER_NAME}; then
    echo "⚠️  Existing container found. Removing..."
    docker stop ${DEV_CONTAINER_NAME} 2>/dev/null || true
    docker rm ${DEV_CONTAINER_NAME} 2>/dev/null || true
fi

# Create the development container (no port mapping needed for Claude Code CLI)
echo "📦 Creating development container..."
docker run -d \
    --name ${DEV_CONTAINER_NAME} \
    --restart unless-stopped \
    -v ${PROJECT_DIR}:${WORKSPACE_DIR} \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w ${WORKSPACE_DIR} \
    --user root \
    node:22-alpine tail -f /dev/null

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 3

# Install development tools
echo "🔧 Installing development tools..."
docker exec ${DEV_CONTAINER_NAME} sh -c "
    apk add --no-cache git curl bash docker-cli openssh-client &&
    npm install -g @anthropic-ai/claude-code
"

# Create helper scripts
echo "📝 Creating helper scripts..."

# Create claude-code wrapper script
cat > "${PROJECT_DIR}/claude-code" << 'EOF'
#!/bin/bash
# Claude Code wrapper for Unraid

DEV_CONTAINER="claude-code-dev"

# Check if container is running
if ! docker ps | grep -q ${DEV_CONTAINER}; then
    echo "Starting development container..."
    docker start ${DEV_CONTAINER}
    sleep 2
fi

# Run claude-code in the container
docker exec -it ${DEV_CONTAINER} claude-code "$@"
EOF

# Create development shell script
cat > "${PROJECT_DIR}/dev-shell" << 'EOF'
#!/bin/bash
# Enter development environment

DEV_CONTAINER="claude-code-dev"

# Check if container is running
if ! docker ps | grep -q ${DEV_CONTAINER}; then
    echo "Starting development container..."
    docker start ${DEV_CONTAINER}
    sleep 2
fi

echo "🚀 Entering Claude Code development environment..."
echo "💡 You can now run: claude-code, npm, node, git, etc."
echo "📁 Your project is mounted at: /workspace"
echo "🚪 Type 'exit' to return to Unraid terminal"
echo ""

# Enter the container
docker exec -it ${DEV_CONTAINER} /bin/bash
EOF

# Make scripts executable
chmod +x "${PROJECT_DIR}/claude-code"
chmod +x "${PROJECT_DIR}/dev-shell"

# Test installation
echo "🧪 Testing Claude Code installation..."
if docker exec ${DEV_CONTAINER} claude-code --version >/dev/null 2>&1; then
    echo "✅ Claude Code installed successfully!"
else
    echo "❌ Claude Code installation failed"
    exit 1
fi

# Create usage documentation
cat > "${PROJECT_DIR}/CLAUDE-CODE-SETUP.md" << 'EOF'
# Claude Code Development Environment

## Quick Start

### Start a Claude Code session:
```bash
cd /mnt/user/appdata/film-scheduler-v6
./claude-code
```

### Enter development shell:
```bash
./dev-shell
# Inside the container you can run:
# - claude-code
# - npm, node
# - git commands
# - docker commands (for managing your app)
```

### Managing the development container:
```bash
# Start container
docker start claude-code-dev

# Stop container  
docker stop claude-code-dev

# View logs
docker logs claude-code-dev

# Remove container (if you want to recreate)
docker stop claude-code-dev
docker rm claude-code-dev
# Then re-run the setup script
```

## Development Workflow

1. **Start development session**:
   ```bash
   cd /mnt/user/appdata/film-scheduler-v6
   ./claude-code
   ```

2. **Make changes with Claude Code**:
   - Describe features in natural language
   - Let Claude Code implement across multiple files
   - Test changes immediately

3. **Test your application**:
   ```bash
   # Your film-scheduler-v6 is still accessible at:
   # http://your-unraid-ip:5076
   
   # Or rebuild/restart from the dev container:
   docker-compose down
   docker-compose up -d
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "Feature implemented with Claude Code"
   git push
   ```

## Troubleshooting

### If Claude Code command fails:
```bash
# Enter the dev container and check
./dev-shell
claude-code --version
```

### If container won't start:
```bash
docker logs claude-code-dev
# Or recreate:
docker rm claude-code-dev
./claude-code-dev-setup.sh
```

### To update Claude Code:
```bash
./dev-shell
npm update -g @anthropic-ai/claude-code
```
EOF

echo ""
echo "🎉 Claude Code development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Test Claude Code: ./claude-code --version"
echo "2. Enter dev environment: ./dev-shell"
echo "3. Start your first session: ./claude-code"
echo ""
echo "📚 See CLAUDE-CODE-SETUP.md for detailed usage instructions"
