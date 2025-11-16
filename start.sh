#!/bin/sh
# Railway deployment script
echo "Environment variables:"
env | grep -E "(PORT|RAILWAY)" || echo "No PORT or RAILWAY variables found"
echo "All environment variables:"
env
PORT=${PORT:-8000}
echo "Using port: $PORT"
uvicorn app:app --host 0.0.0.0 --port $PORT
