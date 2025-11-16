#!/bin/sh
# Railway deployment script - Direct approach
echo "Starting FastAPI server on port 8000"
uvicorn app:app --host 0.0.0.0 --port 8000
