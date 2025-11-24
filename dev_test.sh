#!/bin/bash

# Development Testing Script for Google Workspace MCP
# This script helps test changes locally before committing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Google Workspace MCP Development Test ==="
echo "Working directory: $SCRIPT_DIR"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to test a specific server
test_server() {
    local PORT=$1
    local TOOLS=$2
    local NAME=$3

    echo -e "${YELLOW}Testing $NAME server on port $PORT...${NC}"

    # Kill any existing process on this port
    lsof -ti :$PORT | xargs kill -9 2>/dev/null || true

    # Start the server in background
    ./google_workspace_mcp_wrapper_oauth_fix.sh $PORT $TOOLS > /tmp/mcp_test_$PORT.log 2>&1 &
    local PID=$!

    # Wait for server to start
    sleep 3

    # Check if server is running
    if ps -p $PID > /dev/null; then
        echo -e "${GREEN}✓ $NAME server started successfully (PID: $PID)${NC}"

        # Check if port is listening
        if lsof -i :$PORT | grep LISTEN > /dev/null; then
            echo -e "${GREEN}✓ Server listening on port $PORT${NC}"
        else
            echo -e "${RED}✗ Server not listening on port $PORT${NC}"
        fi

        # Kill the test server
        kill $PID 2>/dev/null || true
    else
        echo -e "${RED}✗ $NAME server failed to start${NC}"
        echo "Check log: /tmp/mcp_test_$PORT.log"
        tail -5 /tmp/mcp_test_$PORT.log
    fi

    echo ""
}

# Menu for testing
echo "Select test option:"
echo "1) Test Google Sheets server (port 8000)"
echo "2) Test Google Slides server (port 8001)"
echo "3) Test Google Docs server (port 8002)"
echo "4) Test all servers"
echo "5) Run syntax check only"
echo "6) Check git status"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        test_server 8000 "sheets drive" "Google Sheets"
        ;;
    2)
        test_server 8001 "slides drive" "Google Slides"
        ;;
    3)
        test_server 8002 "docs drive" "Google Docs"
        ;;
    4)
        test_server 8000 "sheets drive" "Google Sheets"
        test_server 8001 "slides drive" "Google Slides"
        test_server 8002 "docs drive" "Google Docs"
        ;;
    5)
        echo -e "${YELLOW}Running Python syntax check...${NC}"
        python -m py_compile main.py
        python -m py_compile gsheets/sheets_tools.py
        python -m py_compile gslides/slides_tools.py
        echo -e "${GREEN}✓ Syntax check passed${NC}"
        ;;
    6)
        echo -e "${YELLOW}Git status:${NC}"
        git status
        echo ""
        echo -e "${YELLOW}Recent commits:${NC}"
        git log --oneline -5
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=== Test Complete ==="
echo "To test in Claude Desktop:"
echo "1. Restart Claude Desktop to reload MCP servers"
echo "2. Start a new chat and test your changes"
echo ""
echo "To test in Claude Code:"
echo "1. Run: claude --mcp-config ~/claude-code-mcp-config.json"
echo "2. Use /mcp to verify servers are loaded"