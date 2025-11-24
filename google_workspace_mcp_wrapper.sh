#!/bin/bash

# Google Workspace MCP Wrapper Script
# Ensures the MCP server runs from the correct directory with proper environment setup
# Usage: ./google_workspace_mcp_wrapper.sh <port> <tool1> <tool2> ...

set -e  # Exit on any error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory to ensure relative imports work
cd "$SCRIPT_DIR"

# Debug output
echo "MCP Wrapper: Running from directory: $SCRIPT_DIR" >&2
echo "MCP Wrapper: Arguments: $@" >&2

# Check if we have arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <port> [tool1] [tool2] ..." >&2
    echo "Example: $0 8000 sheets drive" >&2
    exit 1
fi

# Extract port (first argument)
PORT="$1"
shift

# Set environment variables for the server
export WORKSPACE_MCP_PORT="$PORT"

# If we have tool arguments, pass them to main.py
if [ $# -gt 0 ]; then
    TOOLS_ARGS="--tools $@"
else
    TOOLS_ARGS=""
fi

# Debug: Show what we're about to run
echo "MCP Wrapper: Executing: uv run main.py $TOOLS_ARGS" >&2

# Execute the main server with tools arguments
exec uv run main.py $TOOLS_ARGS