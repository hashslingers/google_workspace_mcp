#!/bin/bash

# Enhanced Google Workspace MCP Wrapper Script with PATH fixes
# This wrapper ensures uv can be found by adding common installation directories to PATH

set -e  # Exit on any error

# Get the absolute directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Debug logging function
log_debug() {
    echo "[MCP-WRAPPER $(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

log_debug "=== Google Workspace MCP Server Wrapper Starting ==="
log_debug "Script location: $SCRIPT_DIR"
log_debug "Original PATH: $PATH"

# Add common uv installation paths to PATH
# Add Python framework directory where uv is installed
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"
# Add Homebrew paths (both Intel and Apple Silicon)
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
# Add cargo/rust paths
export PATH="$HOME/.cargo/bin:$PATH"
# Add local bin
export PATH="$HOME/.local/bin:$PATH"

log_debug "Updated PATH: $PATH"

# Change to the script directory
cd "$SCRIPT_DIR"
log_debug "Working directory: $(pwd)"

# Validate arguments
if [ $# -eq 0 ]; then
    echo "ERROR: Missing arguments" >&2
    echo "Usage: $0 <port> [tool1] [tool2] ..." >&2
    echo "Examples:" >&2
    echo "  $0 8000 sheets drive" >&2
    echo "  $0 8003 gmail chat" >&2
    exit 1
fi

# Extract port (first argument)
PORT="$1"
shift

log_debug "Port: $PORT"
log_debug "Tools: $*"

# Set environment variables
export WORKSPACE_MCP_PORT="$PORT"

# Check if uv is available after PATH update
UV_PATH=$(which uv 2>/dev/null || echo "")
if [ -z "$UV_PATH" ]; then
    # Try to find uv in common locations
    for loc in \
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv" \
        "$HOME/.cargo/bin/uv" \
        "$HOME/.local/bin/uv" \
        "/opt/homebrew/bin/uv" \
        "/usr/local/bin/uv"
    do
        if [ -x "$loc" ]; then
            UV_PATH="$loc"
            log_debug "Found uv at: $UV_PATH"
            break
        fi
    done
fi

if [ -z "$UV_PATH" ]; then
    echo "ERROR: Could not find 'uv' command" >&2
    echo "Searched in PATH and common locations:" >&2
    echo "  - /Library/Frameworks/Python.framework/Versions/3.12/bin/uv" >&2
    echo "  - $HOME/.cargo/bin/uv" >&2
    echo "  - $HOME/.local/bin/uv" >&2
    echo "  - /opt/homebrew/bin/uv" >&2
    echo "  - /usr/local/bin/uv" >&2
    echo "" >&2
    echo "Please install uv:" >&2
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

log_debug "Using uv at: $UV_PATH"

# Build the command with tools if provided
if [ $# -gt 0 ]; then
    TOOLS_ARGS="--tools $*"
else
    TOOLS_ARGS=""
fi

# Execute the main server
CMD="$UV_PATH run main.py $TOOLS_ARGS"
log_debug "Executing: $CMD"

exec $CMD
