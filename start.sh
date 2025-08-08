#!/bin/bash

# CloseGuard Startup Script
# Starts both frontend and backend servers simultaneously

set -e

echo "🚀 Starting CloseGuard Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ]; then
    print_error "Please run this script from the mortgagebuddy root directory"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    print_status "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

print_status "Starting backend server..."
cd backend
source venv/bin/activate
python3 main.py &
BACKEND_PID=$!
cd ..

print_status "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

print_success "🎉 CloseGuard is starting up!"
print_status "Frontend: http://localhost:3000"
print_status "Backend:  http://localhost:8000"
print_status ""
print_status "Press Ctrl+C to stop both servers"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID