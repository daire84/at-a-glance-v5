#!/bin/bash

# Run migration script inside the Docker container

echo "Film Scheduler v5 - Running Migration"
echo "==================================="

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q 'film-scheduler-v5'; then
    echo "Error: film-scheduler-v5 container is not running!"
    echo "Please start the container first with: docker-compose up -d"
    exit 1
fi

echo "Executing migration script in container..."
docker exec -it film-scheduler-v5 python scripts/migration/migrate_projects.py
