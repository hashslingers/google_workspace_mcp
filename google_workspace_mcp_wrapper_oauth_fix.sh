#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_debug() {
    echo "[MCP-WRAPPER $(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

log_debug "=== Google Workspace MCP Server Wrapper Starting ==="

# Add uv to PATH
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

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

UV_PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
CMD="$UV_PATH run main.py $TOOLS_ARGS"
log_debug "Executing: $CMD"

exec $CMD
