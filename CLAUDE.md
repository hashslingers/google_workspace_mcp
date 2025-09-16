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

### Current Architecture
- Multiple tool-specific servers, each with focused functionality
- Reduced token usage (~400-600 tokens per message)
- Tools loaded on-demand based on specific server

## Key Files Modified

### 1. main.py
- Added support for `forms` and `tasks` tools (previously missing)
- Updated tool_imports dictionary
- Added icons for all tools

### 2. google_workspace_mcp_wrapper.sh
- Master wrapper script for all tool-specific servers
- Handles port assignment, environment setup, and debug output
- Usage: `./google_workspace_mcp_wrapper.sh <port> <tool1> <tool2> ...`

### 3. Claude Desktop Configuration
- Split monolithic server into tool-specific instances:
  - `google_sheets` (Port 8000): sheets, drive
  - `google_slides` (Port 8001): slides, drive  
  - `google_docs` (Port 8002): docs, drive
  - `google_communication` (Port 8003): gmail, chat
  - `google_calendar_tasks` (Port 8004): calendar, tasks
  - `google_forms` (Port 8005): forms, drive

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

## Development Setup

### Environment Setup
```bash
# Clone your fork
git clone https://github.com/hashslingers/google_workspace_mcp.git
cd google_workspace_mcp

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up OAuth credentials (see Security section above)
export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```

### Testing Your Changes
```bash
# Test with only sheets tools
uv run main.py --tools sheets drive

# Test with only slides tools
uv run main.py --tools slides drive

# Or use the wrapper (simulates Claude Desktop)
./google_workspace_mcp_wrapper.sh 8000 sheets drive
```

### Development Mode vs Production
- **Development Mode**: Uses local files for immediate changes
- **Production Mode**: Uses uvx/published package

For your fork development, always use development mode by running from your local directory.

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

### Common Issues
1. **"OAuth client credentials not found"**
   - Set environment variables or create `client_secret.json`

2. **"No credentials found for user"**
   - Run authentication flow first
   - Check credentials directory permissions

3. **"Token expired or revoked"**
   - Clear cached credentials and re-authenticate

4. **Import errors**
   - Ensure virtual environment is activated
   - Check dependencies are installed

### Getting Help
- Check `authentication_and_routing_guide.md` for detailed auth flow
- Review original repository documentation
- Test with minimal examples first

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