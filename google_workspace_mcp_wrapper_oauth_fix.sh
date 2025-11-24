#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_debug() {
    echo "[MCP-WRAPPER $(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

log_debug "=== Google Workspace MCP Server Wrapper Starting ==="

cd "$SCRIPT_DIR"

if [ $# -eq 0 ]; then
    echo "ERROR: Missing arguments" >&2
    echo "Usage: $0 <port> [tool1] [tool2] ..." >&2
    exit 1
fi

PORT="$1"
shift

# Set BOTH the MCP port and OAuth callback port to the same value
export WORKSPACE_MCP_PORT="$PORT"
export OAUTH_CALLBACK_PORT="$PORT"

log_debug "Port: $PORT (using for both MCP and OAuth callback)"
log_debug "Tools: $*"

if [ $# -gt 0 ]; then
    TOOLS_ARGS="--tools $*"
else
    TOOLS_ARGS=""
fi

# Find uv by checking multiple common locations
# This is critical for Claude Desktop compatibility, which doesn't inherit shell PATH
log_debug "Searching for uv executable..."

UV_PATH=""
UV_LOCATIONS=(
    "$HOME/.local/bin/uv"
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
    "/opt/homebrew/bin/uv"
    "/usr/local/bin/uv"
)

# Check each location
for location in "${UV_LOCATIONS[@]}"; do
    if [ -x "$location" ]; then
        UV_PATH="$location"
        log_debug "Found uv at: $UV_PATH"
        break
    fi
done

# If not found in standard locations, try command -v as last resort
if [ -z "$UV_PATH" ]; then
    UV_PATH="$(command -v uv 2>/dev/null || true)"
    if [ -n "$UV_PATH" ]; then
        log_debug "Found uv via command -v: $UV_PATH"
    fi
fi

# If still not found, exit with clear error
if [ -z "$UV_PATH" ] || [ ! -x "$UV_PATH" ]; then
    echo "ERROR: uv executable not found" >&2
    echo "Searched locations:" >&2
    for location in "${UV_LOCATIONS[@]}"; do
        echo "  - $location" >&2
    done
    echo "" >&2
    echo "Please install uv or update this script with your uv location." >&2
    echo "Find your uv location with: which uv" >&2
    exit 1
fi

CMD="$UV_PATH run main.py $TOOLS_ARGS"
log_debug "Executing: $CMD"

exec $CMD
