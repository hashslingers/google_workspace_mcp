# Google Workspace MCP Development Guide

## Project Overview

This is a Google Workspace MCP (Model Context Protocol) server that provides AI assistants with tools to interact with Google Workspace services. The server has been optimized from a monolithic architecture to a tool-specific, modular approach.

## Fork Development Setup

### Repository Structure
This repository is a **fork** of the original Google Workspace MCP project:
- **Original**: `taylorwilsdon/google_workspace_mcp`
- **Your Fork**: `hashslingers/google_workspace_mcp`

### Git Remote Configuration
Your local repository is configured with:
- **`origin`**: Points to your fork (`hashslingers/google_workspace_mcp`)
- **`upstream`**: Points to original repository (`taylorwilsdon/google_workspace_mcp`)

## Development Workflow

### Daily Development
```bash
# Make your changes to slides/sheets functionality
# Edit gsheets/sheets_tools.py or gslides/slides_tools.py

# Commit your changes
git add .
git commit -m "Your enhancement description"
git push origin main    # Pushes to YOUR fork
```

### Staying Updated with Original Repository
```bash
# Fetch latest changes from original repository
git fetch upstream
git merge upstream/main  # Or git rebase upstream/main
git push origin main     # Update your fork with merged changes
```

### Contributing Back (Optional)
- Create pull requests from your fork to the original repository
- Use GitHub's web interface to propose useful enhancements

## Security Best Practices

### ✅ Protected Files
The following sensitive files are automatically excluded from version control:

```gitignore
# OAuth credentials
client_secret.json
client_secrets.json

# User credentials
.credentials/

# Logs
mcp_server_debug.log
```

### 🔒 OAuth Credentials Setup

**NEVER commit OAuth credentials to git!** Use one of these secure methods:

#### Method 1: Environment Variables (Recommended)
```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```

#### Method 2: Local Client Secrets File
Create a local `client_secret.json` file (automatically gitignored):
```json
{
  "web": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "client_secret": "your-client-secret",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["http://localhost:8000/oauth2callback"]
  }
}
```

### Getting Your OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable Google Workspace APIs (Sheets, Slides, Drive, etc.)
4. Create OAuth 2.0 credentials
5. Add `http://localhost:8000/oauth2callback` as redirect URI

## Architecture Changes

### Original Architecture
- Single MCP server loading all ~50 Google Workspace tools
- High token usage (3,000-4,000 tokens per message)
- All tools loaded regardless of need
- Single port (8000) handling all services
- Memory overhead from loading unused tools

### Current Modular Architecture
- Multiple tool-specific servers, each with focused functionality
- Reduced token usage (~400-600 tokens per message)
- Tools loaded on-demand based on specific server
- Dedicated ports (8000-8005) for service isolation
- Lower memory footprint per server instance

### Benefits of the Modular Fork Architecture

#### 1. **Token Efficiency**
- **Before**: Every message included context for all 50+ tools
- **After**: Only 5-10 relevant tools per server
- **Impact**: 80-85% reduction in token usage per interaction

#### 2. **Service Isolation**
- Each service runs independently on its own port
- Crashes or issues in one service don't affect others
- Easier to debug service-specific problems
- Can restart individual services without affecting others

#### 3. **Development Advantages**
- Work on sheets tools without affecting slides functionality
- Test individual services in isolation
- Cleaner logs (only relevant service output)
- Faster startup times for each server

#### 4. **OAuth Management**
- Each service has its own OAuth callback port
- No conflicts between simultaneous authentications
- Service-specific credential management possible

#### 5. **Resource Optimization**
- Only load Python modules for required tools
- Reduced memory usage per server instance
- Better performance for specialized workflows

### Architecture Diagram

```
Claude Desktop
    │
    ├── google_sheets (Port 8000)
    │   ├── sheets_tools.py
    │   └── drive_tools.py (shared)
    │
    ├── google_slides (Port 8001)
    │   ├── slides_tools.py
    │   └── drive_tools.py (shared)
    │
    ├── google_docs (Port 8002)
    │   ├── docs_tools.py
    │   └── drive_tools.py (shared)
    │
    ├── google_communication (Port 8003)
    │   ├── gmail_tools.py
    │   └── chat_tools.py
    │
    ├── google_calendar_tasks (Port 8004)
    │   ├── calendar_tools.py
    │   └── tasks_tools.py
    │
    └── google_forms (Port 8005)
        ├── forms_tools.py
        └── drive_tools.py (shared)
```

Each server instance:
- Runs via `google_workspace_mcp_wrapper_oauth_fix.sh`
- Has isolated environment variables
- Maintains separate debug logs
- Can be updated independently

## Key Files Modified

### 1. main.py
- Added support for `forms` and `tasks` tools (previously missing)
- Updated tool_imports dictionary
- Added icons for all tools

### 2. Wrapper Scripts (Critical for Fork Functionality)

#### google_workspace_mcp_wrapper_oauth_fix.sh (PRODUCTION USE)
The primary wrapper script that enables Claude Desktop to properly launch MCP servers from the fork:

**Key Features:**
- **Directory Context Fix**: Ensures Python runs from the project directory regardless of where Claude launches it
- **PATH Resolution**: Explicitly adds `/Library/Frameworks/Python.framework/Versions/3.12/bin` to PATH to find `uv` command
- **OAuth Port Synchronization**: Sets both `WORKSPACE_MCP_PORT` and `OAUTH_CALLBACK_PORT` to the same value for proper authentication
- **Tool-Specific Loading**: Passes arguments to load only required tools per server instance

**Why This Script is Essential:**
- Without it, Python can't find local module imports (`core`, `auth`, etc.)
- Claude Desktop doesn't inherit your shell's PATH configuration
- Each server needs its OAuth callback on its specific port (8000-8005)

#### google_workspace_mcp_wrapper_fixed.sh (BACKUP)
Alternative wrapper with more verbose logging and validation, useful for debugging issues.

### 3. Claude Desktop Configuration
- Split monolithic server into tool-specific instances using wrapper scripts:
  - `google_sheets` (Port 8000): sheets, drive
  - `google_slides` (Port 8001): slides, drive
  - `google_docs` (Port 8002): docs, drive
  - `google_communication` (Port 8003): gmail, chat
  - `google_calendar_tasks` (Port 8004): calendar, tasks
  - `google_forms` (Port 8005): forms, drive

**Configuration Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Each server entry uses the `google_workspace_mcp_wrapper_oauth_fix.sh` script with absolute paths.

## Development Focus Areas

### Primary Enhancement Targets
Based on your use case, focus on these modules:

#### 1. Google Sheets (`gsheets/sheets_tools.py`)
**Current Functionality:**
- `list_spreadsheets` - List accessible spreadsheets
- `get_spreadsheet_info` - Get metadata (with merged cells & named ranges)
- `read_sheet_values` - Read cell ranges (with merged cell detection)
- `modify_sheet_values` - Write/update/clear cells
- `create_spreadsheet` - Create new spreadsheets
- `create_sheet` - Add sheets to existing files
- Comment management (read, create, reply, resolve)
- `format_cells` - Comprehensive cell formatting
- `merge_cells` / `unmerge_cells` - Cell merging operations
- Named range management
- Data validation and conditional formatting

**Enhancement Opportunities:**
- Row/column operations (insert/delete/resize)
- Sheet protection and permissions
- Pivot tables and charts
- Advanced formula management

#### 2. Google Slides (`gslides/slides_tools.py`)
**Current Functionality:**
- `list_presentations` - List accessible presentations
- `get_presentation_info` - Get presentation metadata
- `read_presentation_content` - Extract text and structure
- `create_presentation` - Create new presentations
- `add_slide` - Add slides with layouts

**Enhancement Opportunities:**
- Content manipulation (text, images, shapes)
- Slide formatting and themes
- Animation and transition management
- Template and master slide operations

## Dual-Environment Setup: Claude Desktop + Claude Code

### Overview
This fork is configured to work with BOTH Claude Desktop and Claude Code, providing Google Workspace MCP access in both environments.

### 1. Claude Desktop Setup (Fork-Specific)

#### Complete Setup Process

1. **Ensure Wrapper Script Exists**:
```bash
# Check that the oauth_fix wrapper is present and executable
ls -la google_workspace_mcp_wrapper_oauth_fix.sh
# If missing, see "Wrapper Script Creation" below
```

2. **Configure Claude Desktop**:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "google_sheets": {
      "command": "/Users/js/Documents/Claude/MCP_GoogleWorkspace/google_workspace_mcp/google_workspace_mcp_wrapper_oauth_fix.sh",
      "args": ["8000", "sheets", "drive"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret",
        "USER_GOOGLE_EMAIL": "your-email@gmail.com",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    },
    // Repeat pattern for other services on ports 8001-8005
  }
}
```

3. **Restart Claude Desktop** for changes to take effect

### 2. Claude Code Setup (MCP in Terminal Sessions)

Claude Code can ALSO use MCP servers, configured separately from Claude Desktop:

#### Configuration Resolution (What Fixed It)

The key fix for Claude Code MCP configuration was:

1. **Changed command from**:
   - ❌ `debug_uv.sh` (doesn't exist)
   - ✅ To: `google_workspace_mcp_wrapper_oauth_fix.sh` (the working script)

2. **Added necessary arguments**:
   - Port: `8000`
   - Services: `sheets`, `drive`

3. **Added required environment variables**:
   - Google OAuth credentials
   - User email: `your-email@gmail.com`
   - `OAUTHLIB_INSECURE_TRANSPORT`: `"1"`

#### Configuration Methods

**Option 1: Using `claude mcp` command** (RECOMMENDED):
```bash
# Configure MCP servers for Claude Code
claude mcp

# In the configuration interface:
# 1. Set command to: /full/path/to/google_workspace_mcp_wrapper_oauth_fix.sh
# 2. Add arguments: 8000 sheets drive
# 3. Add environment variables (OAuth credentials, email, etc.)
```

**Option 2: Using `--mcp-config` flag**:
```bash
# Create a Claude Code specific MCP config file
cat > ~/claude-code-mcp-config.json << 'EOF'
{
  "mcpServers": {
    "google_sheets": {
      "command": "/Users/js/Documents/Claude/MCP_GoogleWorkspace/google_workspace_mcp/google_workspace_mcp_wrapper_oauth_fix.sh",
      "args": ["8000", "sheets", "drive"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret",
        "USER_GOOGLE_EMAIL": "your-email@gmail.com",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    }
  }
}
EOF

# Start Claude Code with MCP config
claude --mcp-config ~/claude-code-mcp-config.json
```

#### Verify MCP in Claude Code
```bash
# In a Claude Code session, check MCP status
/mcp

# Should show your configured Google Workspace servers
# If "No MCP servers configured", check the fix above
```

### Wrapper Script Creation

If the wrapper script is missing, create `google_workspace_mcp_wrapper_oauth_fix.sh`:

```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_debug() {
    echo "[MCP-WRAPPER $(date '+%Y-%m-%d %H:%M:%S')] $1" >&2
}

log_debug "=== Google Workspace MCP Server Wrapper Starting ==="

# Add uv to PATH (adjust path if needed for your system)
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

cd "$SCRIPT_DIR"

if [ $# -eq 0 ]; then
    echo "ERROR: Missing arguments" >&2
    echo "Usage: $0 <port> [tool1] [tool2] ..." >&2
    exit 1
fi

PORT="$1"
shift

# Critical: Set both ports to the same value
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
```

Make it executable:
```bash
chmod +x google_workspace_mcp_wrapper_oauth_fix.sh
```

### 3. Dual-Environment Workflow

With both environments configured, you now have powerful flexibility:

#### When to Use Each Environment

**Claude Desktop (Main Chat)**:
- ✅ Quick Google Workspace operations
- ✅ Natural language interactions ("Create a budget spreadsheet")
- ✅ Non-coding tasks
- ✅ Simple queries and updates

**Claude Code (Terminal Sessions)**:
- ✅ Development and debugging
- ✅ File editing and code generation
- ✅ Complex automations with Google Workspace
- ✅ Combining MCP tools with file operations

#### Example Workflows

**Workflow 1: Data Analysis Project**
```bash
# In Claude Code:
/code
# Create Python script to process data
# Use MCP to read Google Sheets data
# Process and analyze
# Write results back to Google Sheets
```

**Workflow 2: Report Generation**
```bash
# In Claude Desktop:
"Read data from my Sales 2024 spreadsheet"
"Create a summary presentation with key metrics"

# Switch to Claude Code:
/code
# Generate detailed analysis scripts
# Create visualization code
# Update multiple sheets programmatically
```

#### Usage Examples

**Claude Desktop Examples**:
```
User: "List my Google spreadsheets"
User: "Create a new sheet called Project Tracker"
User: "Read the data from Budget 2024 sheet A1:D10"
User: "Update cell B5 in my Sales sheet to 1500"
```

**Claude Code Examples**:
```bash
# After configuring MCP in Claude Code
/code

# Now you can combine file operations with Google Workspace:
"Create a Python script that reads from my Budget sheet and generates a report"
"Write a function to sync local CSV files with Google Sheets"
"Build an automation to update multiple Google Slides from a data source"
```

### Common Issues and Solutions

**Issue**: "MCP not available in Claude Code"
**Solution**: Ensure you used the correct wrapper script path (not debug_uv.sh)

**Issue**: "Different results in Desktop vs Code"
**Solution**: Both use the same wrapper script, so results should be identical. Check port conflicts.

**Issue**: "Authentication fails in one environment"
**Solution**: OAuth tokens are shared via `.credentials/` directory, so auth in one should work in both

## Development Setup

### Environment Setup
```bash
# Clone your fork
git clone https://github.com/hashslingers/google_workspace_mcp.git
cd google_workspace_mcp

# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up OAuth credentials (see Security section above)
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```

### Testing Your Changes
```bash
# Test with only sheets tools using the wrapper
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive

# Or test directly with uv (from project directory)
uv run main.py --tools sheets drive

# Test with only slides tools
./google_workspace_mcp_wrapper_oauth_fix.sh 8001 slides drive
```

### Development Mode vs Production
- **Development Mode**: Uses local files for immediate changes (your fork setup)
- **Production Mode**: Uses uvx/published package (original repository)

For your fork development, always use development mode by running from your local directory with the wrapper scripts.

## Implementation Patterns

### Adding New Tools
```python
from auth.service_decorator import require_google_service
from core.server import server

@server.tool()
@require_google_service("sheets", "sheets_write")
async def your_new_function(
    service,
    spreadsheet_id: str,
    your_parameters: str,
    user_google_email: str
) -> str:
    """
    Your function description.
    
    Args:
        spreadsheet_id: The ID of the spreadsheet
        your_parameters: Description of your parameters
        user_google_email: User's Google email for authentication
    
    Returns:
        Description of what the function returns
    """
    # Your implementation here
    result = service.spreadsheets().your_operation().execute()
    return f"Success: {result}"
```

### Authentication Scopes
Available scope groups in `auth/service_decorator.py`:
- `sheets_read` / `sheets_write`
- `slides_read` / `slides` (full access)
- `drive_read` / `drive_file`

## Troubleshooting

### Common Issues with Fork Setup

#### 1. **"Command not found: uv" or Silent Failures in Claude Desktop**
**Symptom**: Servers fail to start immediately (within ~30ms) when launched by Claude Desktop, or show "uv executable not found" error

**Cause**: Claude Desktop doesn't inherit your terminal's PATH environment, so it can't find `uv` using `which` or `command -v`

**Solution**: The wrapper script automatically checks multiple common uv installation locations:
- `$HOME/.local/bin/uv` (most common for uv installer)
- `/Library/Frameworks/Python.framework/Versions/3.12/bin/uv`
- `/opt/homebrew/bin/uv` (Homebrew on Apple Silicon)
- `/usr/local/bin/uv` (Homebrew on Intel Macs)

If uv is installed in a non-standard location:
```bash
# Find your uv location
which uv

# Add it to the UV_LOCATIONS array in the wrapper script (around line 42)
UV_LOCATIONS=(
    "$HOME/.local/bin/uv"
    "/your/custom/path/to/uv"  # Add your path here
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
    "/opt/homebrew/bin/uv"
    "/usr/local/bin/uv"
)
```

#### 2. **"ModuleNotFoundError: No module named 'core'"**
**Symptom**: Python can't find local modules like `core`, `auth`, etc.

**Cause**: Script running from wrong directory

**Solution**: Ensure wrapper script is being used (not direct uv/python commands)
```bash
# Wrong (from Claude Desktop config):
"command": "uv",
"args": ["run", "main.py"]

# Correct:
"command": "/path/to/google_workspace_mcp_wrapper_oauth_fix.sh",
"args": ["8000", "sheets", "drive"]
```

#### 3. **"OAuth callback failed on port 8000"**
**Symptom**: Authentication starts but callback fails

**Cause**: Port mismatch between server and OAuth callback

**Solution**: Wrapper script must set both port variables:
```bash
export WORKSPACE_MCP_PORT="$PORT"
export OAUTH_CALLBACK_PORT="$PORT"  # Critical!
```

#### 4. **"google_calendar_tasks server failed to start"**
**Symptom**: Some servers work, others don't

**Cause**: Inconsistent wrapper script paths in Claude config

**Solution**: Ensure ALL servers use same wrapper:
```bash
# Check Claude config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep command

# All should point to same wrapper script
```

#### 5. **"Permission denied" when running wrapper**
**Symptom**: Wrapper script won't execute

**Solution**:
```bash
chmod +x google_workspace_mcp_wrapper_oauth_fix.sh
chmod +x google_workspace_mcp_wrapper_fixed.sh  # If using backup
```

### Fork-Specific Debugging

#### Understanding the Claude Desktop PATH Issue

**Critical Concept**: Claude Desktop and your terminal have completely different environments.

**The Problem**:
- Your terminal loads shell config files (`.zshrc`, `.bash_profile`, etc.) which set up your PATH
- Claude Desktop launches processes directly without loading these configs
- Commands like `which`, `command -v`, and `$(...)` that work in terminal will fail in Claude Desktop
- This causes the wrapper script to fail silently if it relies on PATH-based command discovery

**The Solution Pattern**:
The wrapper script uses a **multi-location fallback pattern** instead of relying on PATH:

```bash
# ❌ DON'T: Relies on PATH (fails in Claude Desktop)
UV_PATH="$(which uv)"

# ✅ DO: Check explicit locations with fallback
UV_LOCATIONS=(
    "$HOME/.local/bin/uv"
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
    "/opt/homebrew/bin/uv"
    "/usr/local/bin/uv"
)

for location in "${UV_LOCATIONS[@]}"; do
    if [ -x "$location" ]; then
        UV_PATH="$location"
        break
    fi
done
```

**Verification**:
```bash
# 1. Find your uv location in terminal
which uv
# Output: /Users/yourname/.local/bin/uv

# 2. Verify wrapper script includes that location
grep -A5 "UV_LOCATIONS=" google_workspace_mcp_wrapper_oauth_fix.sh

# 3. Test wrapper can find uv (should show "Found uv at: ...")
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive 2>&1 | grep "Found uv"
```

#### Enable Debug Logging
The wrapper scripts include debug output to stderr. To see it:

1. **Run wrapper manually**:
```bash
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive 2>&1 | head -20
```

2. **Check MCP server log**:
```bash
tail -f mcp_server_debug.log
```

3. **Verify working directory**:
```bash
# Add to wrapper script temporarily:
echo "Current directory: $(pwd)" >&2
echo "Files here: $(ls -la | head -5)" >&2
```

### Original Troubleshooting (Still Applies)

1. **"OAuth client credentials not found"**
   - Set environment variables or create `client_secret.json`

2. **"No credentials found for user"**
   - Run authentication flow first
   - Check credentials directory permissions

3. **"Token expired or revoked"**
   - Clear cached credentials and re-authenticate

4. **Import errors**
   - Ensure running from project directory (wrapper handles this)
   - Check dependencies: `uv pip list`

### Quick Diagnostic Commands

```bash
# 1. Verify fork setup
pwd  # Should be in google_workspace_mcp directory
ls -la *.sh  # Should see wrapper scripts

# 2. Test wrapper directly
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive

# 3. Check Claude config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python -m json.tool | grep -A5 google_

# 4. Verify OAuth credentials
echo $GOOGLE_OAUTH_CLIENT_ID
ls -la client_secret.json 2>/dev/null || echo "Using env vars"
```

### Getting Help
- Check `authentication_and_routing_guide.md` for detailed auth flow
- Review wrapper script debug output for specific errors
- Test with minimal examples first
- See original repository issues: https://github.com/taylorwilsdon/google_workspace_mcp/issues

## Future Considerations

When you return to this project:

1. **Sync with upstream**: Check for updates in the original repository
2. **Review your enhancements**: Continue with sheets/slides functionality
3. **Consider contributing**: Share useful enhancements with the community
4. **Update dependencies**: Keep packages current for security

## Resources

- [Google Sheets API v4 Documentation](https://developers.google.com/sheets/api/reference/rest)
- [Google Slides API v1 Documentation](https://developers.google.com/slides/api/reference/rest)
- [Original Repository](https://github.com/taylorwilsdon/google_workspace_mcp)
- [Authentication Guide](./authentication_and_routing_guide.md)