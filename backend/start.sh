#!/bin/bash
echo "Starting CloseGuard API..."
echo "PORT environment variable: $PORT"

# Use default port 8000 if PORT is not set or empty
if [ -z "$PORT" ]; then
    export PORT=8000
    echo "PORT not set, using default: $PORT"
else
    echo "Using PORT from environment: $PORT"
fi

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port $PORT