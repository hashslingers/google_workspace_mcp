#!/bin/bash

# Enhanced Google Workspace MCP Wrapper Script
# This is the master wrapper script for all tool-specific servers
# Handles port assignment, environment setup, and debug output
# Usage: ./google_workspace_mcp_wrapper_fixed.sh <port> <tool1> <tool2> ...

set -e  # Exit on any error

# Get the absolute directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Debug logging function
log_debug() {
    echo "[MCP-WRAPPER $(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

log_debug "=== Google Workspace MCP Server Wrapper Starting ==="
log_debug "Script location: $SCRIPT_DIR"
log_debug "Original working directory: $(pwd)"
log_debug "Arguments received: $*"

# Change to the script directory to ensure all relative paths work correctly
cd "$SCRIPT_DIR"
log_debug "Changed working directory to: $(pwd)"

# Validate arguments
if [ $# -eq 0 ]; then
    echo "ERROR: Missing arguments" >&2
    echo "Usage: $0 <port> [tool1] [tool2] ..." >&2
    echo "Examples:" >&2
    echo "  $0 8000 sheets drive" >&2
    echo "  $0 8001 slides drive" >&2
    echo "  $0 8002 docs drive" >&2
    echo "  $0 8003 gmail chat" >&2
    echo "  $0 8004 calendar tasks" >&2
    echo "  $0 8005 forms drive" >&2
    exit 1
fi

# Extract port (first argument)
PORT="$1"
shift

# Validate port number
if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1024 ] || [ "$PORT" -gt 65535 ]; then
    echo "ERROR: Invalid port number '$PORT'. Must be between 1024-65535" >&2
    exit 1
fi

log_debug "Port: $PORT"
log_debug "Tools: $*"

# Set environment variables
export WORKSPACE_MCP_PORT="$PORT"

# Validate that main.py exists
if [ ! -f "main.py" ]; then
    echo "ERROR: main.py not found in $SCRIPT_DIR" >&2
    echo "Please ensure this script is in the google_workspace_mcp directory" >&2
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "ERROR: 'uv' command not found. Please install uv first:" >&2
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

# Build the command with tools if provided
if [ $# -gt 0 ]; then
    # Check for help flag first
    if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
        TOOLS_ARGS="--help"
        log_debug "Help requested, passing --help to main.py"
    else
        # Validate tool names
        VALID_TOOLS="gmail drive calendar docs sheets slides forms tasks chat"
        for tool in "$@"; do
            if ! echo "$VALID_TOOLS" | grep -q -w "$tool"; then
                echo "ERROR: Invalid tool '$tool'. Valid tools are: $VALID_TOOLS" >&2
                exit 1
            fi
        done

        TOOLS_ARGS="--tools $*"
        log_debug "Tools argument: $TOOLS_ARGS"
    fi
else
    TOOLS_ARGS=""
    log_debug "No tools specified, will load all tools"
fi

# Final command to execute
CMD="uv run main.py $TOOLS_ARGS"
log_debug "Executing: $CMD"
log_debug "=== Starting MCP Server ==="

# Execute the main server
exec $CMD