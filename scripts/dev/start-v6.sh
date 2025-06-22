#!/bin/bash
# Start Film Scheduler v6

echo "Starting Film Scheduler v6..."
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

echo "v6 started on http://localhost:5076"
echo "Admin: http://localhost:5076/admin/login"
