#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  KCK Swap Shop - Development Startup"
echo "========================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "${BLUE}Starting Backend Server...${NC}"
cd "$SCRIPT_DIR/backend"

# Activate virtual environment if it exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "${GREEN}Activated virtual environment${NC}"
fi

python3 run_dev.py &
BACKEND_PID=$!

# Wait for backend to initialize
sleep 3

# Start Frontend
echo "${BLUE}Starting Frontend React App...${NC}"
cd "$SCRIPT_DIR/frontend"
npm start &
FRONTEND_PID=$!

# Wait for both to start
sleep 2

# Display URLs
echo ""
echo "========================================"
echo "  ${GREEN}Services Started Successfully!${NC}"
echo "========================================"
echo ""
echo "${YELLOW}Backend API:${NC}"
echo "  - API Docs:         http://localhost:8000/docs"
echo "  - ReDoc:            http://localhost:8000/redoc"
echo "  - API Root:         http://localhost:8000"
echo ""
echo "${YELLOW}Frontend:${NC}"
echo "  - React App:        http://localhost:3000"
echo ""
echo "========================================"
echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Keep script running
wait
