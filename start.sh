#!/bin/sh
# Railway deployment script
echo "=== Environment Debug ==="
echo "PORT variable: '$PORT'"
echo "PORT length: ${#PORT}"
echo "All environment variables containing PORT:"
env | grep PORT || echo "No PORT variables found"
echo "All RAILWAY variables:"
env | grep RAILWAY || echo "No RAILWAY variables found"
echo "=== End Debug ==="

# Force port to 8000 since Railway isn't setting PORT
PORT=8000
echo "Using port: $PORT"
uvicorn app:app --host 0.0.0.0 --port $PORT
