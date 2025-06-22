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
