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
