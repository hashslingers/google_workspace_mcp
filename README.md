<!-- mcp-name: io.github.taylorwilsdon/workspace-mcp -->

<div align="center">

# Google Workspace MCP Server <img src="https://github.com/user-attachments/assets/b89524e4-6e6e-49e6-ba77-00d6df0c6e5c" width="80" align="right" />

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/workspace-mcp.svg)](https://pypi.org/project/workspace-mcp/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/workspace-mcp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/workspace-mcp)
[![Website](https://img.shields.io/badge/Website-workspacemcp.com-green.svg)](https://workspacemcp.com)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/eebbc4a6-0f8c-41b2-ace8-038e5516dba0)

**This is the single most feature-complete Google Workspace MCP server** now with 1-click Claude installation

*Full natural language control over Google Calendar, Drive, Gmail, Docs, Sheets, Slides, Forms, Tasks, Contacts, and Chat through all MCP clients, AI assistants and developer tools. Now includes a full featured CLI for use with tools like Claude Code and Codex!*

**The most feature-complete Google Workspace MCP server**, with Remote OAuth2.1 multi-user support and 1-click Claude installation.


###### Support for all free Google accounts (Gmail, Docs, Drive etc) & Google Workspace plans (Starter, Standard, Plus, Enterprise, Non Profit) with expanded app options like Chat & Spaces. <br/><br /> Interested in a private, managed cloud instance? [That can be arranged.](https://workspacemcp.com/workspace-mcp-cloud)


</div>

<div align="center">
<a href="https://glama.ai/mcp/servers/@taylorwilsdon/google_workspace_mcp">
  <img width="195" src="https://glama.ai/mcp/servers/@taylorwilsdon/google_workspace_mcp/badge" alt="Google Workspace Server MCP server" align="center"/>
</a>
<a href="https://www.pulsemcp.com/servers/taylorwilsdon-google-workspace">
<img width="456" src="https://github.com/user-attachments/assets/0794ef1a-dc1c-447d-9661-9c704d7acc9d" align="center"/>
</a>
</div>

---


**See it in action:**
<div align="center">
  <video width="832" src="https://github.com/user-attachments/assets/a342ebb4-1319-4060-a974-39d202329710"></video>
</div>

---

### A quick plug for AI-Enhanced Docs
<details>
<summary>But why?</summary>

**This README was written with AI assistance, and here's why that matters**
>
> As a solo dev building open source tools that many never see outside use, comprehensive documentation often wouldn't happen without AI help. Using agentic dev tools like **Roo** & **Claude Code** that understand the entire codebase, AI doesn't just regurgitate generic content - it extracts real implementation details and creates accurate, specific documentation.
>
> In this case, Sonnet 4 took a pass & a human (me) verified them 7/10/25.
</details>

## Overview

A production-ready MCP server that integrates all major Google Workspace services with AI assistants. Built with FastMCP for optimal performance, featuring advanced authentication handling, service caching, and streamlined development patterns.

## Features

**Maintainer Docs**: Automated release and registry publishing guide at [`docs/mcp_registry_publishing_guide.md`](docs/mcp_registry_publishing_guide.md).

## <span style="color:#adbcbc">Features</span>

<table align="center" style="width: 100%; max-width: 100%;">
<tr>
<td width="50%" valign="top">

**<span style="color:#72898f">@</span> Gmail** • **<span style="color:#72898f">≡</span> Drive** • **<span style="color:#72898f">⧖</span> Calendar** **<span style="color:#72898f">≡</span> Docs**
- Complete Gmail management, end to end coverage
- Full calendar management with advanced features
- File operations with Office format support
- Document creation, editing & comments
- Deep, exhaustive support for fine grained editing

---

**<span style="color:#72898f">≡</span> Forms** • **<span style="color:#72898f">@</span> Chat** • **<span style="color:#72898f">≡</span> Sheets** • **<span style="color:#72898f">≡</span> Slides**
- Form creation, publish settings & response management
- Space management & messaging capabilities
- Spreadsheet operations with flexible cell management
- Presentation creation, updates & content manipulation

---

**<span style="color:#72898f">◆</span> Apps Script**
- Automate cross-application workflows with custom code
- Execute existing business logic and custom functions
- Manage script projects, deployments & versions
- Debug and modify Apps Script code programmatically
- Bridge Google Workspace services through automation

</td>
<td width="50%" valign="top">

**<span style="color:#72898f">⊠</span> Authentication & Security**
- Advanced OAuth 2.0 & OAuth 2.1 support
- Automatic token refresh & session management
- Transport-aware callback handling
- Multi-user bearer token authentication
- Innovative CORS proxy architecture

---

**<span style="color:#72898f">✓</span> Tasks** • **<span style="color:#72898f">👤</span> Contacts** • **<span style="color:#72898f">◆</span> Custom Search**
- Task & task list management with hierarchy
- Contact management via People API with groups
- Programmable Search Engine (PSE) integration

</td>
</tr>
</table>

---

## Quick Start

<details>
<summary><b>Quick Reference Card</b> - Essential commands & configs at a glance</summary>

<table>
<tr><td width="33%" valign="top">

**Credentials**
```bash
export GOOGLE_OAUTH_CLIENT_ID="..."
export GOOGLE_OAUTH_CLIENT_SECRET="..."
```
[Full setup →](#credential-configuration)

</td><td width="33%" valign="top">

**Launch Commands**
```bash
uvx workspace-mcp --tool-tier core
uv run main.py --tools gmail drive
```
[More options →](#start-the-server)

</td><td width="34%" valign="top">

**Tool Tiers**
- `core` - Essential tools
- `extended` - Core + extras
- `complete` - Everything
[Details →](#tool-tiers)

</td></tr>
</table>

</details>

### 1. One-Click Claude Desktop Install (Recommended)

1. **Download:** Grab the latest `google_workspace_mcp.dxt` from the “Releases” page
2. **Install:** Double-click the file – Claude Desktop opens and prompts you to **Install**
3. **Configure:** In Claude Desktop → **Settings → Extensions → Google Workspace MCP**, paste your Google OAuth credentials
4. **Use it:** Start a new Claude chat and call any Google Workspace tool

>
**Why DXT?**
> Desktop Extensions (`.dxt`) bundle the server, dependencies, and manifest so users go from download → working MCP in **one click** – no terminal, no JSON editing, no version conflicts.

#### Required Configuration
<details>
<summary><b>Environment Variables</b> <sub><sup>← Click to configure in Claude Desktop</sup></sub></summary>

| Variable | Purpose |
|----------|---------|
| `GOOGLE_OAUTH_CLIENT_ID` | OAuth client ID from Google Cloud |
| `GOOGLE_OAUTH_CLIENT_SECRET` | OAuth client secret |
| `USER_GOOGLE_EMAIL` *(optional)* | Default email for single-user auth |
| `OAUTHLIB_INSECURE_TRANSPORT=1` | Development only (allows `http://` redirect) |

Claude Desktop stores these securely in the OS keychain; set them once in the extension pane.
</details>

<div align="center">
  <video width="832" src="https://github.com/user-attachments/assets/83cca4b3-5e94-448b-acb3-6e3a27341d3a"></video>
</div>
---

### Prerequisites

- **Python 3.10+**
- **[uvx](https://github.com/astral-sh/uv)** (for instant installation) or [uv](https://github.com/astral-sh/uv) (for development)
- **Google Cloud Project** with OAuth 2.0 credentials

### Configuration

<details open>
<summary><b>Google Cloud Setup</b> <sub><sup>← OAuth 2.0 credentials & API enablement</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**1. Create Project**
```text
console.cloud.google.com

→ Create new project
→ Note project name
```
<sub>[Open Console →](https://console.cloud.google.com/)</sub>

</td>
<td width="33%" align="center">

**2. OAuth Credentials**
```text
APIs & Services → Credentials
→ Create Credentials
→ OAuth Client ID
→ Desktop Application
```
<sub>Download & save credentials</sub>

</td>
<td width="34%" align="center">

**3. Enable APIs**
```text
APIs & Services → Library

Search & enable:
Calendar, Drive, Gmail,
Docs, Sheets, Slides,
Forms, Tasks, People,
Chat, Search
```
<sub>See quick links below</sub>

</td>
</tr>
<tr>
<td colspan="3">

<details>
<summary><b>OAuth Credential Setup Guide</b> <sub><sup>← Step-by-step instructions</sup></sub></summary>

**Complete Setup Process:**

1. **Create OAuth 2.0 Credentials** - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project (or use existing)
   - Navigate to **APIs & Services → Credentials**
   - Click **Create Credentials → OAuth Client ID**
   - Choose **Desktop Application** as the application type (no redirect URIs needed!)
   - Download credentials and note the Client ID and Client Secret

2. **Enable Required APIs** - In **APIs & Services → Library**
   - Search for and enable each required API
   - Or use the quick links below for one-click enabling

3. **Configure Environment** - Set your credentials:
   ```bash
   export GOOGLE_OAUTH_CLIENT_ID="your-client-id"
   export GOOGLE_OAUTH_CLIENT_SECRET="your-secret"
   ```

[Full Documentation →](https://developers.google.com/workspace/guides/auth-overview)

</details>

</td>
</tr>
</table>

<details>
  <summary><b>Quick API Enable Links</b> <sub><sup>← One-click enable each Google API</sup></sub></summary>
  You can enable each one by clicking the links below (make sure you're logged into the Google Cloud Console and have the correct project selected):

* [Enable Google Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
* [Enable Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com)
* [Enable Gmail API](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com)
* [Enable Google Docs API](https://console.cloud.google.com/flows/enableapi?apiid=docs.googleapis.com)
* [Enable Google Sheets API](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
* [Enable Google Slides API](https://console.cloud.google.com/flows/enableapi?apiid=slides.googleapis.com)
* [Enable Google Forms API](https://console.cloud.google.com/flows/enableapi?apiid=forms.googleapis.com)
* [Enable Google Tasks API](https://console.cloud.google.com/flows/enableapi?apiid=tasks.googleapis.com)
* [Enable Google Chat API](https://console.cloud.google.com/flows/enableapi?apiid=chat.googleapis.com)
* [Enable Google People API](https://console.cloud.google.com/flows/enableapi?apiid=people.googleapis.com)
* [Enable Google Custom Search API](https://console.cloud.google.com/flows/enableapi?apiid=customsearch.googleapis.com)
* [Enable Google Apps Script API](https://console.cloud.google.com/flows/enableapi?apiid=script.googleapis.com)

</details>

</details>

1.1. **Credentials**: See [Credential Configuration](#credential-configuration) for detailed setup options

2. **Environment Configuration**:

<details open>
<summary>◆ <b>Environment Variables</b> <sub><sup>← Configure your runtime environment</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**◆ Development Mode**
```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
```
<sub>Allows HTTP redirect URIs</sub>

</td>
<td width="33%" align="center">

**@ Default User**
```bash
export USER_GOOGLE_EMAIL=\
  your.email@gmail.com
```
<sub>Single-user authentication</sub>

</td>
<td width="34%" align="center">

**◆ Custom Search**
```bash
export GOOGLE_PSE_API_KEY=xxx
export GOOGLE_PSE_ENGINE_ID=yyy
```
<sub>Optional: Search API setup</sub>

</td>
</tr>
</table>

</details>

3. **Server Configuration**:

<details open>
<summary>◆ <b>Server Settings</b> <sub><sup>← Customize ports, URIs & proxies</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**◆ Base Configuration**
```bash
export WORKSPACE_MCP_BASE_URI=
  http://localhost
export WORKSPACE_MCP_PORT=8000
export WORKSPACE_MCP_HOST=0.0.0.0  # Use 127.0.0.1 for localhost-only
```
<sub>Server URL & port settings</sub>

</td>
<td width="33%" align="center">

**↻ Proxy Support**
```bash
export MCP_ENABLE_OAUTH21=
  true
```
<sub>Leverage multi-user OAuth2.1 clients</sub>

</td>
<td width="34%" align="center">

**@ Default Email**
```bash
export USER_GOOGLE_EMAIL=\
  your.email@gmail.com
```
<sub>Skip email in auth flows in single user mode</sub>

</td>
</tr>
</table>

<details>
<summary>≡ <b>Configuration Details</b> <sub><sup>← Learn more about each setting</sup></sub></summary>

| Variable | Description | Default |
|----------|-------------|---------|
| `WORKSPACE_MCP_BASE_URI` | Base server URI (no port) | `http://localhost` |
| `WORKSPACE_MCP_PORT` | Server listening port | `8000` |
| `WORKSPACE_MCP_HOST` | Server bind host | `0.0.0.0` |
| `WORKSPACE_EXTERNAL_URL` | External URL for reverse proxy setups | None |
| `GOOGLE_OAUTH_REDIRECT_URI` | Override OAuth callback URL | Auto-constructed |
| `USER_GOOGLE_EMAIL` | Default auth email | None |

</details>

</details>

### Google Custom Search Setup

<details>
<summary>◆ <b>Custom Search Configuration</b> <sub><sup>← Enable web search capabilities</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**1. Create Search Engine**
```text
programmablesearchengine.google.com
/controlpanel/create

→ Configure sites or entire web
→ Note your Engine ID (cx)
```
<sub>[Open Control Panel →](https://programmablesearchengine.google.com/controlpanel/create)</sub>

</td>
<td width="33%" align="center">

**2. Get API Key**
```text
developers.google.com
/custom-search/v1/overview

→ Create/select project
→ Enable Custom Search API
→ Create credentials (API Key)
```
<sub>[Get API Key →](https://developers.google.com/custom-search/v1/overview)</sub>

</td>
<td width="34%" align="center">

**3. Set Variables**
```bash
export GOOGLE_PSE_API_KEY=\
  "your-api-key"
export GOOGLE_PSE_ENGINE_ID=\
  "your-engine-id"
```
<sub>Configure in environment</sub>

</td>
</tr>
<tr>
<td colspan="3">

<details>
<summary>≡ <b>Quick Setup Guide</b> <sub><sup>← Step-by-step instructions</sup></sub></summary>

**Complete Setup Process:**

1. **Create Search Engine** - Visit the [Control Panel](https://programmablesearchengine.google.com/controlpanel/create)
   - Choose "Search the entire web" or specify sites
   - Copy the Search Engine ID (looks like: `017643444788157684527:6ivsjbpxpqw`)

2. **Enable API & Get Key** - Visit [Google Developers Console](https://console.cloud.google.com/)
   - Enable "Custom Search API" in your project
   - Create credentials → API Key
   - Restrict key to Custom Search API (recommended)

3. **Configure Environment** - Add to your shell or `.env`:
   ```bash
   export GOOGLE_PSE_API_KEY="AIzaSy..."
   export GOOGLE_PSE_ENGINE_ID="01764344478..."
   ```

≡ [Full Documentation →](https://developers.google.com/custom-search/v1/overview)

</details>

</td>
</tr>
</table>

</details>

### Start the Server

> **📌 Transport Mode Guidance**: Use **streamable HTTP mode** (`--transport streamable-http`) for all modern MCP clients including Claude Code, VS Code MCP, and MCP Inspector. Stdio mode is only for clients with incomplete MCP specification support.

<details open>
<summary>▶ <b>Launch Commands</b> <sub><sup>← Choose your startup mode</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**▶ Legacy Mode**
```bash
uv run main.py
```
<sub>⚠️ Stdio mode (incomplete MCP clients only)</sub>

</td>
<td width="33%" align="center">

**◆ HTTP Mode (Recommended)**
```bash
uv run main.py \
  --transport streamable-http
```
<sub>✅ Full MCP spec compliance & OAuth 2.1</sub>

</td>
<td width="34%" align="center">

**@ Single User**
```bash
uv run main.py \
  --single-user
```
<sub>Simplified authentication</sub>
<sub>⚠️ Cannot be used with OAuth 2.1 mode</sub>

</td>
</tr>
<tr>
<td colspan="3">

<details>
<summary>◆ <b>Advanced Options</b> <sub><sup>← Tool selection, tiers & Docker</sup></sub></summary>

**▶ Selective Tool Loading**
```bash
# Load specific services only
uv run main.py --tools gmail drive calendar
uv run main.py --tools sheets docs

# Combine with other flags
uv run main.py --single-user --tools gmail
```


**🔒 Read-Only Mode**
```bash
# Requests only read-only scopes & disables write tools
uv run main.py --read-only

# Combine with specific tools or tiers
uv run main.py --tools gmail drive --read-only
uv run main.py --tool-tier core --read-only
```
Read-only mode provides secure, restricted access by:
- Requesting only `*.readonly` OAuth scopes (e.g., `gmail.readonly`, `drive.readonly`)
- Automatically filtering out tools that require write permissions at startup
- Allowing read operations: list, get, search, and export across all services

**★ Tool Tiers**
```bash
uv run main.py --tool-tier core      # ● Essential tools only
uv run main.py --tool-tier extended  # ◐ Core + additional
uv run main.py --tool-tier complete  # ○ All available tools
```

**◆ Docker Deployment**
```bash
docker build -t workspace-mcp .
docker run -p 8000:8000 -v $(pwd):/app \
  workspace-mcp --transport streamable-http

# With tool selection via environment variables
docker run -e TOOL_TIER=core workspace-mcp
docker run -e TOOLS="gmail drive calendar" workspace-mcp
```

**Available Services**: `gmail` • `drive` • `calendar` • `docs` • `sheets` • `forms` • `tasks` • `contacts` • `chat` • `search`

</details>

</td>
</tr>
</table>

</details>

### CLI Mode

The server supports a CLI mode for direct tool invocation without running the full MCP server. This is ideal for scripting, automation, and use by coding agents (Codex, Claude Code).

<details open>
<summary>▶ <b>CLI Commands</b> <sub><sup>← Direct tool execution from command line</sup></sub></summary>

<table>
<tr>
<td width="50%" align="center">

**▶ List Tools**
```bash
workspace-mcp --cli
workspace-mcp --cli list
workspace-mcp --cli list --json
```
<sub>View all available tools</sub>

</td>
<td width="50%" align="center">

**◆ Tool Help**
```bash
workspace-mcp --cli search_gmail_messages --help
```
<sub>Show parameters and documentation</sub>

</td>
</tr>
<tr>
<td width="50%" align="center">

**▶ Run with Arguments**
```bash
workspace-mcp --cli search_gmail_messages \
  --args '{"query": "is:unread"}'
```
<sub>Execute tool with inline JSON</sub>

</td>
<td width="50%" align="center">

**◆ Pipe from Stdin**
```bash
echo '{"query": "is:unread"}' | \
  workspace-mcp --cli search_gmail_messages
```
<sub>Pass arguments via stdin</sub>

</td>
</tr>
</table>

<details>
<summary>≡ <b>CLI Usage Details</b> <sub><sup>← Complete reference</sup></sub></summary>

**Command Structure:**
```bash
workspace-mcp --cli [command] [options]
```

**Commands:**
| Command | Description |
|---------|-------------|
| `list` (default) | List all available tools |
| `<tool_name>` | Execute the specified tool |
| `<tool_name> --help` | Show detailed help for a tool |

**Options:**
| Option | Description |
|--------|-------------|
| `--args`, `-a` | JSON string with tool arguments |
| `--json`, `-j` | Output in JSON format (for `list` command) |
| `--help`, `-h` | Show help for a tool |

**Examples:**
```bash
# List all Gmail tools
workspace-mcp --cli list | grep gmail

# Search for unread emails
workspace-mcp --cli search_gmail_messages --args '{"query": "is:unread", "max_results": 5}'

# Get calendar events for today
workspace-mcp --cli get_events --args '{"calendar_id": "primary", "time_min": "2024-01-15T00:00:00Z"}'

# Create a Drive file from a URL
workspace-mcp --cli create_drive_file --args '{"name": "doc.pdf", "source_url": "https://example.com/file.pdf"}'

# Combine with jq for processing
workspace-mcp --cli list --json | jq '.tools[] | select(.name | contains("gmail"))'
```

**Notes:**
- CLI mode uses OAuth 2.0 (same credentials as server mode)
- Authentication flows work the same way - browser opens for first-time auth
- Results are printed to stdout; errors go to stderr
- Exit code 0 on success, 1 on error

</details>

</details>

### Tool Tiers

The server organizes tools into **three progressive tiers** for simplified deployment. Choose a tier that matches your usage needs and API quota requirements.

<table>
<tr>
<td width="65%" valign="top">

#### <span style="color:#72898f">Available Tiers</span>

**<span style="color:#2d5b69">●</span> Core** (`--tool-tier core`)
Essential tools for everyday tasks. Perfect for light usage with minimal API quotas. Includes search, read, create, and basic modify operations across all services.

**<span style="color:#72898f">●</span> Extended** (`--tool-tier extended`)
Core functionality plus management tools. Adds labels, folders, batch operations, and advanced search. Ideal for regular usage with moderate API needs.

**<span style="color:#adbcbc">●</span> Complete** (`--tool-tier complete`)
Full API access including comments, headers/footers, publishing settings, and administrative functions. For power users needing maximum functionality.

</td>
<td width="35%" valign="top">

#### <span style="color:#72898f">Important Notes</span>

<span style="color:#72898f">▶</span> **Start with `core`** and upgrade as needed
<span style="color:#72898f">▶</span> **Tiers are cumulative** – each includes all previous
<span style="color:#72898f">▶</span> **Mix and match** with `--tools` for specific services
<span style="color:#72898f">▶</span> **Configuration** in `core/tool_tiers.yaml`
<span style="color:#72898f">▶</span> **Authentication** included in all tiers

</td>
</tr>
</table>

#### <span style="color:#72898f">Usage Examples</span>

```bash
# Basic tier selection
uv run main.py --tool-tier core                            # Start with essential tools only
uv run main.py --tool-tier extended                        # Expand to include management features
uv run main.py --tool-tier complete                        # Enable all available functionality

# Selective service loading with tiers
uv run main.py --tools gmail drive --tool-tier core        # Core tools for specific services
uv run main.py --tools gmail --tool-tier extended          # Extended Gmail functionality only
uv run main.py --tools docs sheets --tool-tier complete    # Full access to Docs and Sheets
```

## 📋 Credential Configuration

<details open>
<summary>🔑 <b>OAuth Credentials Setup</b> <sub><sup>← Essential for all installations</sup></sub></summary>

<table>
<tr>
<td width="33%" align="center">

**🚀 Environment Variables**
```bash
export GOOGLE_OAUTH_CLIENT_ID=\
  "your-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET=\
  "your-secret"
```
<sub>Best for production</sub>

</td>
<td width="33%" align="center">

**📁 File-based**
```bash
# Download & place in project root
client_secret.json

# Or specify custom path
export GOOGLE_CLIENT_SECRET_PATH=\
  /path/to/secret.json
```
<sub>Traditional method</sub>

</td>
<td width="34%" align="center">

**⚡ .env File**
```bash
cp .env.oauth21 .env
# Edit .env with credentials
```
<sub>Best for development</sub>

</td>
</tr>
<tr>
<td colspan="3">

<details>
<summary>📖 <b>Credential Loading Details</b> <sub><sup>← Understanding priority & best practices</sup></sub></summary>

**Loading Priority**
1. Environment variables (`export VAR=value`)
2. `.env` file in project root (warning - if you run via `uvx` rather than `uv run` from the repo directory, you are spawning a standalone process not associated with your clone of the repo and it will not find your .env file without specifying it directly)
3. `client_secret.json` via `GOOGLE_CLIENT_SECRET_PATH`
4. Default `client_secret.json` in project root

**Why Environment Variables?**
- ✅ **Docker/K8s ready** - Native container support
- ✅ **Cloud platforms** - Heroku, Railway, Vercel
- ✅ **CI/CD pipelines** - GitHub Actions, Jenkins
- ✅ **No secrets in git** - Keep credentials secure
- ✅ **Easy rotation** - Update without code changes

</details>

</td>
</tr>
</table>

</details>

---

## 🧰 Available Tools

> **Note**: All tools support automatic authentication via `@require_google_service()` decorators with 30-minute service caching.

<table width="100%">
<tr>
<td width="50%" valign="top">

### 📅 **Google Calendar** <sub>[`calendar_tools.py`](gcalendar/calendar_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `list_calendars` | **Core** | List accessible calendars |
| `get_events` | **Core** | Retrieve events with time range filtering |
| `create_event` | **Core** | Create events with attachments & reminders |
| `modify_event` | **Core** | Update existing events |
| `delete_event` | Extended | Remove events |

</td>
<td width="50%" valign="top">

### 📁 **Google Drive** <sub>[`drive_tools.py`](gdrive/drive_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `search_drive_files` | **Core** | Search files with query syntax |
| `get_drive_file_content` | **Core** | Read file content (Office formats) |
| `get_drive_file_download_url` | **Core** | Get download URL for Drive files |
| `create_drive_file` | **Core** | Create files or fetch from URLs |
| `import_to_google_doc` | **Core** | Import files (MD, DOCX, HTML, etc.) as Google Docs |
| `share_drive_file` | **Core** | Share file with users/groups/domains/anyone |
| `get_drive_shareable_link` | **Core** | Get shareable links for a file |
| `list_drive_items` | Extended | List folder contents |
| `copy_drive_file` | Extended | Copy existing files (templates) with optional renaming |
| `update_drive_file` | Extended | Update file metadata, move between folders |
| `batch_share_drive_file` | Extended | Share file with multiple recipients |
| `update_drive_permission` | Extended | Modify permission role |
| `remove_drive_permission` | Extended | Revoke file access |
| `transfer_drive_ownership` | Extended | Transfer file ownership to another user |
| `set_drive_file_permissions` | Extended | Set link sharing and file-level sharing settings |
| `get_drive_file_permissions` | Complete | Get detailed file permissions |
| `check_drive_file_public_access` | Complete | Check public sharing status |

</td>
</tr>
<tr>

<tr>
<td width="50%" valign="top">

### 📧 **Gmail** <sub>[`gmail_tools.py`](gmail/gmail_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `search_gmail_messages` | **Core** | Search with Gmail operators |
| `get_gmail_message_content` | **Core** | Retrieve message content |
| `get_gmail_messages_content_batch` | **Core** | Batch retrieve message content |
| `send_gmail_message` | **Core** | Send emails |
| `get_gmail_thread_content` | Extended | Get full thread content |
| `modify_gmail_message_labels` | Extended | Modify message labels |
| `list_gmail_labels` | Extended | List available labels |
| `manage_gmail_label` | Extended | Create/update/delete labels |
| `draft_gmail_message` | Extended | Create drafts |
| `get_gmail_threads_content_batch` | Complete | Batch retrieve thread content |
| `batch_modify_gmail_message_labels` | Complete | Batch modify labels |
| `start_google_auth` | Complete | Legacy OAuth 2.0 auth (disabled when OAuth 2.1 is enabled) |

<details>
<summary><b>📎 Email Attachments</b> <sub><sup>← Send emails with files</sup></sub></summary>

Both `send_gmail_message` and `draft_gmail_message` support attachments via two methods:

**Option 1: File Path** (local server only)
```python
attachments=[{"path": "/path/to/report.pdf"}]
```
Reads file from disk, auto-detects MIME type. Optional `filename` override.

**Option 2: Base64 Content** (works everywhere)
```python
attachments=[{
    "filename": "report.pdf",
    "content": "JVBERi0xLjQK...",  # base64-encoded
    "mime_type": "application/pdf"   # optional
}]
```

**⚠️ Centrally Hosted Servers**: When the MCP server runs remotely (cloud, shared instance), it cannot access your local filesystem. Use **Option 2** with base64-encoded content. Your MCP client must encode files before sending.

</details>

</td>
<td width="50%" valign="top">

### 📝 **Google Docs** <sub>[`docs_tools.py`](gdocs/docs_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `get_doc_content` | **Core** | Extract document text |
| `create_doc` | **Core** | Create new documents |
| `modify_doc_text` | **Core** | Modify document text |
| `search_docs` | Extended | Find documents by name |
| `find_and_replace_doc` | Extended | Find and replace text |
| `list_docs_in_folder` | Extended | List docs in folder |
| `insert_doc_elements` | Extended | Add tables, lists, page breaks |
| `update_paragraph_style` | Extended | Apply heading styles, lists (bulleted/numbered with nesting), and paragraph formatting |
| `insert_doc_image` | Complete | Insert images from Drive/URLs |
| `update_doc_headers_footers` | Complete | Modify headers and footers |
| `batch_update_doc` | Complete | Execute multiple operations |
| `inspect_doc_structure` | Complete | Analyze document structure |
| `export_doc_to_pdf` | Extended | Export document to PDF |
| `create_table_with_data` | Complete | Create data tables |
| `debug_table_structure` | Complete | Debug table issues |
| `*_document_comments` | Complete | Read, Reply, Create, Resolve |

</td>
</tr>

<tr>
<td width="50%" valign="top">

### 📊 **Google Sheets** <sub>[`sheets_tools.py`](gsheets/sheets_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `read_sheet_values` | **Core** | Read cell ranges |
| `modify_sheet_values` | **Core** | Write/update/clear cells |
| `create_spreadsheet` | **Core** | Create new spreadsheets |
| `list_spreadsheets` | Extended | List accessible spreadsheets |
| `get_spreadsheet_info` | Extended | Get spreadsheet metadata |
| `format_sheet_range` | Extended | Apply colors, number formats, text wrapping, alignment, bold/italic, font size |
| `create_sheet` | Complete | Add sheets to existing files |
| `*_sheet_comment` | Complete | Read/create/reply/resolve comments |

</td>
<td width="50%" valign="top">

### 🖼️ **Google Slides** <sub>[`slides_tools.py`](gslides/slides_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `create_presentation` | **Core** | Create new presentations |
| `get_presentation` | **Core** | Retrieve presentation details |
| `batch_update_presentation` | Extended | Apply multiple updates |
| `get_page` | Extended | Get specific slide information |
| `get_page_thumbnail` | Extended | Generate slide thumbnails |
| `*_presentation_comment` | Complete | Read/create/reply/resolve comments |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📝 **Google Forms** <sub>[`forms_tools.py`](gforms/forms_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `create_form` | **Core** | Create new forms |
| `get_form` | **Core** | Retrieve form details & URLs |
| `set_publish_settings` | Complete | Configure form settings |
| `get_form_response` | Complete | Get individual responses |
| `list_form_responses` | Extended | List all responses with pagination |
| `batch_update_form` | Complete | Apply batch updates (questions, settings) |

</td>
<td width="50%" valign="top">

### ✓ **Google Tasks** <sub>[`tasks_tools.py`](gtasks/tasks_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `list_tasks` | **Core** | List tasks with filtering |
| `get_task` | **Core** | Retrieve task details |
| `create_task` | **Core** | Create tasks with hierarchy |
| `update_task` | **Core** | Modify task properties |
| `delete_task` | Extended | Remove tasks |
| `move_task` | Complete | Reposition tasks |
| `clear_completed_tasks` | Complete | Hide completed tasks |
| `*_task_list` | Complete | List/get/create/update/delete task lists |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 👤 **Google Contacts** <sub>[`contacts_tools.py`](gcontacts/contacts_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `search_contacts` | **Core** | Search contacts by name, email, phone |
| `get_contact` | **Core** | Retrieve detailed contact info |
| `list_contacts` | **Core** | List contacts with pagination |
| `create_contact` | **Core** | Create new contacts |
| `update_contact` | Extended | Update existing contacts |
| `delete_contact` | Extended | Delete contacts |
| `list_contact_groups` | Extended | List contact groups/labels |
| `get_contact_group` | Extended | Get group details with members |
| `batch_*_contacts` | Complete | Batch create/update/delete contacts |
| `*_contact_group` | Complete | Create/update/delete contact groups |
| `modify_contact_group_members` | Complete | Add/remove contacts from groups |

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 💬 **Google Chat** <sub>[`chat_tools.py`](gchat/chat_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `list_spaces` | Extended | List chat spaces/rooms |
| `get_messages` | **Core** | Retrieve space messages |
| `send_message` | **Core** | Send messages to spaces |
| `search_messages` | **Core** | Search across chat history |

</td>
<td width="50%" valign="top">

### 🔍 **Google Custom Search** <sub>[`search_tools.py`](gsearch/search_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `search_custom` | **Core** | Perform web searches |
| `get_search_engine_info` | Complete | Retrieve search engine metadata |
| `search_custom_siterestrict` | Extended | Search within specific domains |

</td>
</tr>
<tr>
<td colspan="2" valign="top">

### **Google Apps Script** <sub>[`apps_script_tools.py`](gappsscript/apps_script_tools.py)</sub>

| Tool | Tier | Description |
|------|------|-------------|
| `list_script_projects` | **Core** | List accessible Apps Script projects |
| `get_script_project` | **Core** | Get complete project with all files |
| `get_script_content` | **Core** | Retrieve specific file content |
| `create_script_project` | **Core** | Create new standalone or bound project |
| `update_script_content` | **Core** | Update or create script files |
| `run_script_function` | **Core** | Execute function with parameters |
| `create_deployment` | Extended | Create new script deployment |
| `list_deployments` | Extended | List all project deployments |
| `update_deployment` | Extended | Update deployment configuration |
| `delete_deployment` | Extended | Remove deployment |
| `list_script_processes` | Extended | View recent executions and status |

</td>
</tr>
</table>


**Tool Tier Legend:**
- <span style="color:#2d5b69">•</span> **Core**: Essential tools for basic functionality • Minimal API usage • Getting started
- <span style="color:#72898f">•</span> **Extended**: Core tools + additional features • Regular usage • Expanded capabilities
- <span style="color:#adbcbc">•</span> **Complete**: All available tools including advanced features • Power users • Full API access

---

### Connect to Claude Desktop

The server supports two transport modes:

#### Stdio Mode (Legacy - For Clients with Incomplete MCP Support)

> **⚠️ Important**: Stdio mode is a **legacy fallback** for clients that don't properly implement the MCP specification with OAuth 2.1 and streamable HTTP support. **Claude Code and other modern MCP clients should use streamable HTTP mode** (`--transport streamable-http`) for proper OAuth flow and multi-user support.

In general, you should use the one-click DXT installer package for Claude Desktop.
If you are unable to for some reason, you can configure it manually via `claude_desktop_config.json`

**Manual Claude Configuration (Alternative)**

<details>
<summary>📝 <b>Claude Desktop JSON Config</b> <sub><sup>← Click for manual setup instructions</sup></sub></summary>

1. Open Claude Desktop Settings → Developer → Edit Config
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:
```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    }
  }
}
```
</details>

### Connect to LM Studio

Add a new MCP server in LM Studio (Settings → MCP Servers) using the same JSON format:

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1",
      }
    }
  }
}
```


### 2. Advanced / Cross-Platform Installation

If you’re developing, deploying to servers, or using another MCP-capable client, keep reading.

#### Instant CLI (uvx)

```bash
# Requires Python 3.11+ and uvx
export GOOGLE_OAUTH_CLIENT_ID="xxx"
export GOOGLE_OAUTH_CLIENT_SECRET="yyy"
uvx workspace-mcp --tools gmail drive calendar
```

> Run instantly without manual installation - you must configure OAuth credentials when using uvx. You can use either environment variables (recommended for production) or set the `GOOGLE_CLIENT_SECRET_PATH` (or legacy `GOOGLE_CLIENT_SECRETS`) environment variable to point to your `client_secret.json` file.

```bash
# Set OAuth credentials via environment variables (recommended)
export GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"

# Run the same linter that git hooks invoke automatically
uv run ruff check .

# Execute the full test suite (async fixtures require pytest-asyncio)
uv run pytest
```

- `uv sync --group test` installs only the testing stack if you need a slimmer environment.
- `uv run main.py --transport streamable-http` launches the server with your checked-out code for manual verification.
- Ruff is part of the `dev` group because pre-push hooks call `ruff check` automatically—run it locally before committing to avoid hook failures.

</details>

### OAuth 2.1 Support (Multi-User Bearer Token Authentication)

The server includes OAuth 2.1 support for bearer token authentication, enabling multi-user session management. **OAuth 2.1 automatically reuses your existing `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` credentials** - no additional configuration needed!

**When to use OAuth 2.1:**
- Multiple users accessing the same MCP server instance
- Need for bearer token authentication instead of passing user emails
- Building web applications or APIs on top of the MCP server
- Production environments requiring secure session management
- Browser-based clients requiring CORS support

**⚠️ Important: OAuth 2.1 and Single-User Mode are mutually exclusive**

OAuth 2.1 mode (`MCP_ENABLE_OAUTH21=true`) cannot be used together with the `--single-user` flag:
- **Single-user mode**: For legacy clients that pass user emails in tool calls
- **OAuth 2.1 mode**: For modern multi-user scenarios with bearer token authentication

Choose one authentication method - using both will result in a startup error.

**Enabling OAuth 2.1:**
To enable OAuth 2.1, set the `MCP_ENABLE_OAUTH21` environment variable to `true`.

```bash
# OAuth 2.1 requires HTTP transport mode
export MCP_ENABLE_OAUTH21=true
uv run main.py --transport streamable-http
```

If `MCP_ENABLE_OAUTH21` is not set to `true`, the server will use legacy authentication, which is suitable for clients that do not support OAuth 2.1.

<details>
<summary>🔐 <b>How the FastMCP GoogleProvider handles OAuth</b> <sub><sup>← Advanced OAuth 2.1 details</sup></sub></summary>

FastMCP ships a native `GoogleProvider` that we now rely on directly. It solves the two tricky parts of using Google OAuth with MCP clients:

1.  **Dynamic Client Registration**: Google still doesn't support OAuth 2.1 DCR, but the FastMCP provider exposes the full DCR surface and forwards registrations to Google using your fixed credentials. MCP clients register as usual and the provider hands them your Google client ID/secret under the hood.

2.  **CORS & Browser Compatibility**: The provider includes an OAuth proxy that serves all discovery, authorization, and token endpoints with proper CORS headers. We no longer maintain custom `/oauth2/*` routes—the provider handles the upstream exchanges securely and advertises the correct metadata to clients.

The result is a leaner server that still enables any OAuth 2.1 compliant client (including browser-based ones) to authenticate through Google without bespoke code.

</details>

### Stateless Mode (Container-Friendly)

The server supports a stateless mode designed for containerized environments where file system writes should be avoided:

**Enabling Stateless Mode:**
```bash
# Stateless mode requires OAuth 2.1 to be enabled
export MCP_ENABLE_OAUTH21=true
export WORKSPACE_MCP_STATELESS_MODE=true
uv run main.py --transport streamable-http
```

**Key Features:**
- **No file system writes**: Credentials are never written to disk
- **No debug logs**: File-based logging is completely disabled
- **Memory-only sessions**: All tokens stored in memory via OAuth 2.1 session store
- **Container-ready**: Perfect for Docker, Kubernetes, and serverless deployments
- **Token per request**: Each request must include a valid Bearer token

**Requirements:**
- Must be used with `MCP_ENABLE_OAUTH21=true`
- Incompatible with single-user mode
- Clients must handle OAuth flow and send valid tokens with each request

This mode is ideal for:
- Cloud deployments where persistent storage is unavailable
- Multi-tenant environments requiring strict isolation
- Containerized applications with read-only filesystems
- Serverless functions and ephemeral compute environments

**MCP Inspector**: No additional configuration needed with desktop OAuth client.

**Claude Code**: No additional configuration needed with desktop OAuth client.

### OAuth Proxy Storage Backends

The server supports pluggable storage backends for OAuth proxy state management via FastMCP 2.13.0+. Choose a backend based on your deployment needs.

**Available Backends:**

| Backend | Best For | Persistence | Multi-Server |
|---------|----------|-------------|--------------|
| Memory | Development, testing | ❌ | ❌ |
| Disk | Single-server production | ✅ | ❌ |
| Valkey/Redis | Distributed production | ✅ | ✅ |

**Configuration:**

```bash
# Memory storage (fast, no persistence)
export WORKSPACE_MCP_OAUTH_PROXY_STORAGE_BACKEND=memory

# Disk storage (persists across restarts)
export WORKSPACE_MCP_OAUTH_PROXY_STORAGE_BACKEND=disk
export WORKSPACE_MCP_OAUTH_PROXY_DISK_DIRECTORY=~/.fastmcp/oauth-proxy

# Valkey/Redis storage (distributed, multi-server)
export WORKSPACE_MCP_OAUTH_PROXY_STORAGE_BACKEND=valkey
export WORKSPACE_MCP_OAUTH_PROXY_VALKEY_HOST=redis.example.com
export WORKSPACE_MCP_OAUTH_PROXY_VALKEY_PORT=6379
```

> Valkey support is optional. Install `workspace-mcp[valkey]` (or `py-key-value-aio[valkey]`) only if you enable the Valkey backend.
> Windows: building `valkey-glide` from source requires MSVC C++ build tools with C11 support. If you see `aws-lc-sys` C11 errors, set `CFLAGS=/std:c11`.

<details>
<summary>🔐 <b>Valkey/Redis Configuration Options</b></summary>

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_HOST` | localhost | Valkey/Redis host |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_PORT` | 6379 | Port (6380 auto-enables TLS) |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_DB` | 0 | Database number |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_USE_TLS` | auto | Enable TLS (auto if port 6380) |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_USERNAME` | - | Authentication username |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_PASSWORD` | - | Authentication password |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_REQUEST_TIMEOUT_MS` | 5000 | Request timeout for remote hosts |
| `WORKSPACE_MCP_OAUTH_PROXY_VALKEY_CONNECTION_TIMEOUT_MS` | 10000 | Connection timeout for remote hosts |

**Encryption:** Disk and Valkey storage are encrypted with Fernet. The encryption key is derived from `FASTMCP_SERVER_AUTH_GOOGLE_JWT_SIGNING_KEY` if set, otherwise from `GOOGLE_OAUTH_CLIENT_SECRET`.

</details>

### External OAuth 2.1 Provider Mode

The server supports an external OAuth 2.1 provider mode for scenarios where authentication is handled by an external system. In this mode, the MCP server does not manage the OAuth flow itself but expects valid bearer tokens in the Authorization header of tool calls.

**Enabling External OAuth 2.1 Provider Mode:**
```bash
# External OAuth provider mode requires OAuth 2.1 to be enabled
export MCP_ENABLE_OAUTH21=true
export EXTERNAL_OAUTH21_PROVIDER=true
uv run main.py --transport streamable-http
```

**How It Works:**
- **Protocol-level auth disabled**: MCP handshake (`initialize`) and `tools/list` do not require authentication
- **Tool-level auth required**: All tool calls must include `Authorization: Bearer <token>` header
- **External OAuth flow**: Your external system handles the OAuth flow and obtains Google access tokens
- **Token validation**: Server validates bearer tokens via Google's tokeninfo API
- **Multi-user support**: Each request is authenticated independently based on its bearer token

**Key Features:**
- **No local OAuth flow**: Server does not provide OAuth callback endpoints or manage OAuth state
- **Bearer token only**: All authentication via Authorization headers
- **Stateless by design**: Works seamlessly with `WORKSPACE_MCP_STATELESS_MODE=true`
- **External identity providers**: Integrate with your existing authentication infrastructure
- **Tool discovery**: Clients can list available tools without authentication

**Requirements:**
- Must be used with `MCP_ENABLE_OAUTH21=true`
- OAuth credentials still required for token validation (`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`)
- External system must obtain valid Google OAuth access tokens (ya29.*)
- Each tool call request must include valid bearer token

**Use Cases:**
- Integrating with existing authentication systems
- Custom OAuth flows managed by your application
- API gateways that handle authentication upstream
- Multi-tenant SaaS applications with centralized auth
- Mobile or web apps with their own OAuth implementation


### VS Code MCP Client Support

> **✅ Recommended**: VS Code MCP extension properly supports the full MCP specification. **Always use HTTP transport mode** for proper OAuth 2.1 authentication.

<details>
<summary>🆚 <b>VS Code Configuration</b> <sub><sup>← Setup for VS Code MCP extension</sup></sub></summary>

```json
{
    "servers": {
        "google-workspace": {
            "url": "http://localhost:8000/mcp/",
            "type": "http"
        }
    }
}
```

*Note: Make sure to start the server with `--transport streamable-http` when using VS Code MCP.*
</details>

### Claude Code MCP Client Support

> **✅ Recommended**: Claude Code is a modern MCP client that properly supports the full MCP specification. **Always use HTTP transport mode** with Claude Code for proper OAuth 2.1 authentication and multi-user support.

<details>
<summary>🆚 <b>Claude Code Configuration</b> <sub><sup>← Setup for Claude Code MCP support</sup></sub></summary>

```bash
# Start the server in HTTP mode first
uv run main.py --transport streamable-http

# Then add to Claude Code
claude mcp add --transport http workspace-mcp http://localhost:8000/mcp
```
</details>

#### Reverse Proxy Setup

If you're running the MCP server behind a reverse proxy (nginx, Apache, Cloudflare, etc.), you have two configuration options:

**Problem**: When behind a reverse proxy, the server constructs OAuth URLs using internal ports (e.g., `http://localhost:8000`) but external clients need the public URL (e.g., `https://your-domain.com`).

**Solution 1**: Set `WORKSPACE_EXTERNAL_URL` for all OAuth endpoints:
```bash
# This configures all OAuth endpoints to use your external URL
export WORKSPACE_EXTERNAL_URL="https://your-domain.com"
```

**Solution 2**: Set `GOOGLE_OAUTH_REDIRECT_URI` for just the callback:
```bash
# This only overrides the OAuth callback URL
export GOOGLE_OAUTH_REDIRECT_URI="https://your-domain.com/oauth2callback"
```

You also have options for:
| `OAUTH_CUSTOM_REDIRECT_URIS` *(optional)* | Comma-separated list of additional redirect URIs |
| `OAUTH_ALLOWED_ORIGINS` *(optional)* | Comma-separated list of additional CORS origins |

**Important**:
- Use `WORKSPACE_EXTERNAL_URL` when all OAuth endpoints should use the external URL (recommended for reverse proxy setups)
- Use `GOOGLE_OAUTH_REDIRECT_URI` when you only need to override the callback URL
- The redirect URI must exactly match what's configured in your Google Cloud Console
- Your reverse proxy must forward OAuth-related requests (`/oauth2callback`, `/oauth2/*`, `/.well-known/*`) to the MCP server

<details>
<summary>🚀 <b>Advanced uvx Commands</b> <sub><sup>← More startup options</sup></sub></summary>

```bash
# Configure credentials first (see Credential Configuration section)

# Start with specific tools only
uvx workspace-mcp --tools gmail drive calendar tasks

# Start in HTTP mode for debugging
uvx workspace-mcp --transport streamable-http
```

*Requires Python 3.11+ and [uvx](https://github.com/astral-sh/uv). The package is available on [PyPI](https://pypi.org/project/workspace-mcp).*

### Development Installation

For development or customization:

```bash
git clone https://github.com/taylorwilsdon/google_workspace_mcp.git
cd google_workspace_mcp
uv run main.py
```

### Fork Development Setup

If you're working with a **fork** of this repository (recommended for custom enhancements):

```bash
# Clone your fork
git clone https://github.com/your-username/google_workspace_mcp.git
cd google_workspace_mcp

# Add upstream remote to stay updated with original repository
git remote add upstream https://github.com/taylorwilsdon/google_workspace_mcp.git

# Verify remote configuration
git remote -v
# Should show:
# origin    https://github.com/your-username/google_workspace_mcp.git (fetch/push)
# upstream  https://github.com/taylorwilsdon/google_workspace_mcp.git (fetch/push)

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Critical: Wrapper Scripts for Fork Development

**Forks require wrapper scripts** to work with Claude Desktop because:
- Python needs to run from the project directory for local imports
- Claude Desktop doesn't inherit your shell's PATH configuration
- Each server needs proper OAuth port configuration

Create the essential `google_workspace_mcp_wrapper_oauth_fix.sh`:

```bash
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Add uv to PATH - adjust for your system
export PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:$PATH"

PORT="$1"
shift

# Critical: Sync OAuth ports
export WORKSPACE_MCP_PORT="$PORT"
export OAUTH_CALLBACK_PORT="$PORT"

TOOLS_ARGS=""
[ $# -gt 0 ] && TOOLS_ARGS="--tools $*"

UV_PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
exec $UV_PATH run main.py $TOOLS_ARGS
```

Make it executable:
```bash
chmod +x google_workspace_mcp_wrapper_oauth_fix.sh
```

#### Fork Development Workflow

**Daily Development:**
```bash
# Test changes locally using wrapper
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive

# Commit changes
git add .
git commit -m "Your enhancement description"
git push origin main  # Pushes to YOUR fork
```

**Staying Updated:**
```bash
# Fetch and merge updates from original repository
git fetch upstream
git merge upstream/main
git push origin main  # Update your fork
```

**Security Note for Forks:**
- OAuth credentials are automatically excluded from version control via `.gitignore`
- Use environment variables or local `client_secret.json` files (never commit credentials!)
- See `CLAUDE.md` for detailed fork development guidance and Claude Desktop configuration

---

### 📦 Quick Clone & Use (TL;DR)

For users who just want to clone and start using the MCP server immediately:

```bash
# 1. Clone and setup
git clone https://github.com/hashslingers/google_workspace_mcp.git
cd google_workspace_mcp
curl -LsSf https://astral.sh/uv/install.sh | sh
chmod +x google_workspace_mcp_wrapper_oauth_fix.sh

# 2. Test it works
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive
```

Then add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google_sheets": {
      "command": "/full/path/to/google_workspace_mcp/google_workspace_mcp_wrapper_oauth_fix.sh",
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
```

Add more servers on different ports as needed: slides (8001), docs (8002), gmail/chat (8003), calendar/tasks (8004), forms (8005).

---

### 🖥️ Setting Up on a New Computer (Including Cloud/Remote Machines)

Whether you're setting up on a new local machine, remote server, or cloud computer, follow these steps to clone and configure the MCP server.

#### 1. Clone the Repository

```bash
# Clone the hashslingers fork (or your fork)
git clone https://github.com/hashslingers/google_workspace_mcp.git
cd google_workspace_mcp

# Optional: Add upstream remote to sync with original repository
git remote add upstream https://github.com/taylorwilsdon/google_workspace_mcp.git
```

#### 2. Install uv (Python Package Manager)

```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation and note the path
which uv
# Common locations:
# - $HOME/.local/bin/uv (most common)
# - /opt/homebrew/bin/uv (Homebrew on Apple Silicon)
# - /usr/local/bin/uv (Homebrew on Intel Macs)
```

#### 3. Verify/Update Wrapper Script

The wrapper script automatically checks multiple common `uv` locations. If your `uv` is in a non-standard location:

```bash
# Find your uv location
which uv

# If needed, add your custom path to the wrapper script
# Edit google_workspace_mcp_wrapper_oauth_fix.sh around line 42:
UV_LOCATIONS=(
    "$HOME/.local/bin/uv"
    "/your/custom/path/to/uv"  # Add your path here if different
    "/Library/Frameworks/Python.framework/Versions/3.12/bin/uv"
    "/opt/homebrew/bin/uv"
    "/usr/local/bin/uv"
)

# Make wrapper executable
chmod +x google_workspace_mcp_wrapper_oauth_fix.sh
```

#### 4. Configure OAuth Credentials

**For Local/Development Machines:**

Set environment variables in your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
export USER_GOOGLE_EMAIL="your-email@gmail.com"
export OAUTHLIB_INSECURE_TRANSPORT="1"  # Development only
```

**For Remote/Cloud Computers:**

Create a `.env` file in the project directory (this is gitignored):

```bash
# Create .env file
cat > .env << 'EOF'
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
USER_GOOGLE_EMAIL=your-email@gmail.com
OAUTHLIB_INSECURE_TRANSPORT=1
EOF

# Or export them directly in your session
export GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
```

#### 5. Configure Claude Desktop (Local Machines)

Edit your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google_sheets": {
      "command": "/full/path/to/google_workspace_mcp/google_workspace_mcp_wrapper_oauth_fix.sh",
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
```

**Important**: Use absolute paths in the Claude Desktop config, not `~` or relative paths.

#### 6. Cloud/Remote Computer Considerations

**SSH Port Forwarding for OAuth Callback:**

Since OAuth requires a browser redirect to `http://localhost:8000/oauth2callback`, use SSH tunneling when working on remote machines:

```bash
# On your local machine, connect with port forwarding
ssh -L 8000:localhost:8000 user@remote-server

# Now the OAuth callback from your browser will forward to the remote server
```

**Running in HTTP Mode (Alternative):**

For remote servers, you might want to expose the MCP server via HTTP:

```bash
# On remote server
uv run main.py --transport streamable-http --tools gmail drive calendar

# Access via mcp-remote from local Claude Desktop
# In claude_desktop_config.json:
{
  "mcpServers": {
    "google_workspace": {
      "command": "npx",
      "args": ["mcp-remote", "http://your-server-ip:8000/mcp"]
    }
  }
}
```

**Docker Deployment on Cloud:**

```bash
# Build and run with docker
docker build -t workspace-mcp .
docker run -p 8000:8000 \
  -e GOOGLE_OAUTH_CLIENT_ID="your-client-id" \
  -e GOOGLE_OAUTH_CLIENT_SECRET="your-secret" \
  -e OAUTHLIB_INSECURE_TRANSPORT=1 \
  workspace-mcp --transport streamable-http
```

#### 7. Test the Setup

```bash
# Test the wrapper script can find uv
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive 2>&1 | grep "Found uv"
# Should output: [MCP-WRAPPER ...] Found uv at: /path/to/uv

# Test the server starts
./google_workspace_mcp_wrapper_oauth_fix.sh 8000 sheets drive
# Should see FastMCP banner if successful

# Test from Claude Desktop
# Restart Claude Desktop and try: "List my Google spreadsheets"
```

#### Troubleshooting New Installations

**"uv executable not found"**
```bash
# Verify uv installation
which uv
uv --version

# If not found, reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or ~/.zshrc
```

**"Port 8000 already in use"**
```bash
# Check what's using the port
lsof -i :8000

# Kill existing process or use different port
./google_workspace_mcp_wrapper_oauth_fix.sh 8001 sheets drive
# Update Claude Desktop config to match new port
```

**OAuth callback fails on remote machine**
```bash
# Ensure SSH port forwarding is active
ssh -L 8000:localhost:8000 user@remote-server

# Or use ngrok for temporary public URL
ngrok http 8000
# Update GOOGLE_OAUTH_REDIRECT_URI to ngrok URL
```

---

### Prerequisites

- **Python 3.11+**
- **[uvx](https://github.com/astral-sh/uv)** (for instant installation) or [uv](https://github.com/astral-sh/uv) (for development)
- **Google Cloud Project** with OAuth 2.0 credentials

### Configuration

1. **Google Cloud Setup**:
   - Create OAuth 2.0 credentials (web application) in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable APIs: Calendar, Drive, Gmail, Docs, Sheets, Slides, Forms, Tasks, Chat
   - Add redirect URI: `http://localhost:8000/oauth2callback`
   - Configure credentials using one of these methods:

     **Option A: Environment Variables (Recommended for Production)**
     ```bash
     export GOOGLE_OAUTH_CLIENT_ID="your-client-id.apps.googleusercontent.com"
     export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret"
     export GOOGLE_OAUTH_REDIRECT_URI="http://localhost:8000/oauth2callback"  # Optional
     ```

     **Option B: File-based (Traditional)**
     - Download credentials as `client_secret.json` in project root
     - To use a different location, set `GOOGLE_CLIENT_SECRET_PATH` (or legacy `GOOGLE_CLIENT_SECRETS`) environment variable with the file path

   **Credential Loading Priority**:
   1. Environment variables (`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`)
   2. File specified by `GOOGLE_CLIENT_SECRET_PATH` or `GOOGLE_CLIENT_SECRETS` environment variable
   3. Default file (`client_secret.json` in project root)

   **Why Environment Variables?**
   - ✅ Containerized deployments (Docker, Kubernetes)
   - ✅ Cloud platforms (Heroku, Railway, etc.)
   - ✅ CI/CD pipelines
   - ✅ No secrets in version control
   - ✅ Easy credential rotation

2. **Environment**:
   ```bash
   export OAUTHLIB_INSECURE_TRANSPORT=1  # Development only
   export USER_GOOGLE_EMAIL=your.email@gmail.com  # Optional: Default email for auth - use this for single user setups and you won't need to set your email in system prompt for magic auth
   ```

3. **Server Configuration**:
   The server's base URL and port can be customized using environment variables:
   - `WORKSPACE_MCP_BASE_URI`: Sets the base URI for the server (default: http://localhost). This affects the `server_url` used to construct the default `OAUTH_REDIRECT_URI` if `GOOGLE_OAUTH_REDIRECT_URI` is not set.
   - `WORKSPACE_MCP_PORT`: Sets the port the server listens on (default: 8000). This affects the server_url, port, and OAUTH_REDIRECT_URI.
   - `USER_GOOGLE_EMAIL`: Optional default email for authentication flows. If set, the LLM won't need to specify your email when calling `start_google_auth`.
   - `GOOGLE_OAUTH_REDIRECT_URI`: Sets an override for OAuth redirect specifically, must include a full address (i.e. include port if necessary). Use this if you want to run your OAuth redirect separately from the MCP. This is not recommended outside of very specific cases

### Start the Server

```bash
# Default (stdio mode for MCP clients)
uv run main.py

# HTTP mode (for web interfaces and debugging)
uv run main.py --transport streamable-http

# Single-user mode (simplified authentication)
uv run main.py --single-user

# Selective tool registration (only register specific tools)
uv run main.py --tools gmail drive calendar tasks
uv run main.py --tools sheets docs
uv run main.py --single-user --tools gmail  # Can combine with other flags

# Docker
docker build -t workspace-mcp .
docker run -p 8000:8000 -v $(pwd):/app workspace-mcp --transport streamable-http
```

**Available Tools for `--tools` flag**: `gmail`, `drive`, `calendar`, `docs`, `sheets`, `forms`, `tasks`, `chat`

### Connect to Claude Desktop

The server supports two transport modes:

#### Stdio Mode (Default - Recommended for Claude Desktop)

**Guided Setup (Recommended if not using DXT)**

```bash
python install_claude.py
```

This script automatically:
- Prompts you for your Google OAuth credentials (Client ID and Secret)
- Creates the Claude Desktop config file in the correct location
- Sets up all necessary environment variables
- No manual file editing required!

After running the script, just restart Claude Desktop and you're ready to go.

**Manual Claude Configuration (Alternative)**
1. Open Claude Desktop Settings → Developer → Edit Config
   1. **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   2. **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "google_workspace": {
         "command": "uvx",
         "args": ["workspace-mcp"],
         "env": {
           "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
           "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret",
           "OAUTHLIB_INSECURE_TRANSPORT": "1"
         }
       }
     }
   }
   ```

**Get Google OAuth Credentials** (if you don't have them):
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project and enable APIs: Calendar, Drive, Gmail, Docs, Sheets, Slides, Forms, Tasks, Chat
- Create OAuth 2.0 Client ID (Web application) with redirect URI: `http://localhost:8000/oauth2callback`

**Development Installation (For Contributors)**:
```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/repo/google_workspace_mcp",
        "main.py"
      ],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    }
  }
}
```

#### HTTP Mode (For debugging or web interfaces)
If you need to use HTTP mode with Claude Desktop:

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

*Note: Make sure to start the server with `--transport streamable-http` when using HTTP mode.*

### First-Time Authentication

The server features **transport-aware OAuth callback handling**:

- **Stdio Mode**: Automatically starts a minimal HTTP server on port 8000 for OAuth callbacks
- **HTTP Mode**: Uses the existing FastAPI server for OAuth callbacks
- **Same OAuth Flow**: Both modes use `http://localhost:8000/oauth2callback` for consistency

When calling a tool:
1. Server returns authorization URL
2. Open URL in browser and authorize
3. Server handles OAuth callback automatically (on port 8000 in both modes)
4. Retry the original request

---

## 🧰 Available Tools

> **Note**: All tools support automatic authentication via `@require_google_service()` decorators with 30-minute service caching.

### 📅 Google Calendar ([`calendar_tools.py`](gcalendar/calendar_tools.py))

| Tool | Description |
|------|-------------|
| `list_calendars` | List accessible calendars |
| `get_events` | Retrieve events with time range filtering |
| `get_event` | Fetch detailed information of a single event by ID |
| `create_event` | Create events (all-day or timed) with optional Drive file attachments |
| `modify_event` | Update existing events |
| `delete_event` | Remove events |

### 📁 Google Drive ([`drive_tools.py`](gdrive/drive_tools.py))

| Tool | Description |
|------|-------------|
| `search_drive_files` | Search files with query syntax |
| `get_drive_file_content` | Read file content (supports Office formats) |
| `list_drive_items` | List folder contents |
| `create_drive_file` | Create new files or fetch content from public URLs |

### 📧 Gmail ([`gmail_tools.py`](gmail/gmail_tools.py))

| Tool | Description |
|------|-------------|
| `search_gmail_messages` | Search with Gmail operators |
| `get_gmail_message_content` | Retrieve message content |
| `send_gmail_message` | Send emails |
| `draft_gmail_message` | Create drafts |

### 📝 Google Docs ([`docs_tools.py`](gdocs/docs_tools.py))

| Tool | Description |
|------|-------------|
| `search_docs` | Find documents by name |
| `get_doc_content` | Extract document text |
| `list_docs_in_folder` | List docs in folder |
| `create_doc` | Create new documents |
| `read_doc_comments` | Read all comments and replies |
| `create_doc_comment` | Create new comments |
| `reply_to_comment` | Reply to existing comments |
| `resolve_comment` | Resolve comments |

### 📊 Google Sheets ([`sheets_tools.py`](gsheets/sheets_tools.py))

| Tool | Description |
|------|-------------|
| `list_spreadsheets` | List accessible spreadsheets |
| `get_spreadsheet_info` | Get spreadsheet metadata |
| `read_sheet_values` | Read cell ranges |
| `modify_sheet_values` | Write/update/clear cells |
| `create_spreadsheet` | Create new spreadsheets |
| `create_sheet` | Add sheets to existing files |
| `read_sheet_comments` | Read all comments and replies |
| `create_sheet_comment` | Create new comments |
| `reply_to_sheet_comment` | Reply to existing comments |
| `resolve_sheet_comment` | Resolve comments |

### 🖼️ Google Slides ([`slides_tools.py`](gslides/slides_tools.py))

| Tool | Description |
|------|-------------|
| `create_presentation` | Create new presentations |
| `get_presentation` | Retrieve presentation details |
| `batch_update_presentation` | Apply multiple updates at once |
| `get_page` | Get specific slide information |
| `get_page_thumbnail` | Generate slide thumbnails |
| `read_presentation_comments` | Read all comments and replies |
| `create_presentation_comment` | Create new comments |
| `reply_to_presentation_comment` | Reply to existing comments |
| `resolve_presentation_comment` | Resolve comments |

### 📝 Google Forms ([`forms_tools.py`](gforms/forms_tools.py))

| Tool | Description |
|------|-------------|
| `create_form` | Create new forms with title and description |
| `get_form` | Retrieve form details, questions, and URLs |
| `set_publish_settings` | Configure form template and authentication settings |
| `get_form_response` | Get individual form response details |
| `list_form_responses` | List all responses to a form with pagination |

### ✓ Google Tasks ([`tasks_tools.py`](gtasks/tasks_tools.py))

| Tool | Description |
|------|-------------|
| `list_task_lists` | List all task lists with pagination support |
| `get_task_list` | Retrieve details of a specific task list |
| `create_task_list` | Create new task lists with custom titles |
| `update_task_list` | Modify existing task list titles |
| `delete_task_list` | Remove task lists and all contained tasks |
| `list_tasks` | List tasks in a specific list with filtering options |
| `get_task` | Retrieve detailed information about a specific task |
| `create_task` | Create new tasks with title, notes, due dates, and hierarchy |
| `update_task` | Modify task properties including title, notes, status, and due dates |
| `delete_task` | Remove tasks from task lists |
| `move_task` | Reposition tasks within lists or move between lists |
| `clear_completed_tasks` | Hide all completed tasks from a list |

### 💬 Google Chat ([`chat_tools.py`](gchat/chat_tools.py))

| Tool | Description |
|------|-------------|
| `list_spaces` | List chat spaces/rooms |
| `get_messages` | Retrieve space messages |
| `send_message` | Send messages to spaces |
| `search_messages` | Search across chat history |

---

## 🛠️ Development

### Project Structure

```
google_workspace_mcp/
├── auth/              # Authentication system with decorators
├── core/              # MCP server and utilities
├── g{service}/        # Service-specific tools
├── main.py            # Server entry point
├── client_secret.json # OAuth credentials (not committed)
└── pyproject.toml     # Dependencies
```

### Adding New Tools

```python
from auth.service_decorator import require_google_service

@require_google_service("drive", "drive_read")  # Service + scope group
async def your_new_tool(service, param1: str, param2: int = 10):
    """Tool description"""
    # service is automatically injected and cached
    result = service.files().list().execute()
    return result  # Return native Python objects
```

### Architecture Highlights

- **Service Caching**: 30-minute TTL reduces authentication overhead
- **Scope Management**: Centralized in `SCOPE_GROUPS` for easy maintenance
- **Error Handling**: Native exceptions instead of manual error construction
- **Multi-Service Support**: `@require_multiple_services()` for complex tools

---

## 🔒 Security

- **Credentials**: Never commit `client_secret.json` or `.credentials/` directory
- **OAuth Callback**: Uses `http://localhost:8000/oauth2callback` for development (requires `OAUTHLIB_INSECURE_TRANSPORT=1`)
- **Transport-Aware Callbacks**: Stdio mode starts a minimal HTTP server only for OAuth, ensuring callbacks work in all modes
- **Production**: Use HTTPS for callback URIs and configure accordingly
- **Network Exposure**: Consider authentication when using `mcpo` over networks
- **Scope Minimization**: Tools request only necessary permissions

---

## 🌐 Integration with Open WebUI

To use this server as a tool provider within Open WebUI:

### 1. Create MCPO Configuration

Create a file named `config.json` with the following structure to have `mcpo` make the streamable HTTP endpoint available as an OpenAPI spec tool:

```json
{
  "mcpServers": {
    "google_workspace": {
      "type": "streamablehttp",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### 2. Start the MCPO Server

```bash
mcpo --port 8001 --config config.json --api-key "your-optional-secret-key"
```

This command starts the `mcpo` proxy, serving your active (assuming port 8000) Google Workspace MCP on port 8001.

### 3. Configure Open WebUI

1. Navigate to your Open WebUI settings
2. Go to **"Connections"** → **"Tools"**
3. Click **"Add Tool"**
4. Enter the **Server URL**: `http://localhost:8001/google_workspace` (matching the mcpo base URL and server name from config.json)
5. If you used an `--api-key` with mcpo, enter it as the **API Key**
6. Save the configuration

The Google Workspace tools should now be available when interacting with models in Open WebUI.

---

## 📄 License

MIT License - see `LICENSE` file for details.

---

<div align="center">
<img width="810" alt="Gmail Integration" src="https://github.com/user-attachments/assets/656cea40-1f66-40c1-b94c-5a2c900c969d" />
<img width="810" alt="Calendar Management" src="https://github.com/user-attachments/assets/d3c2a834-fcca-4dc5-8990-6d6dc1d96048" />
<img width="842" alt="Batch Emails" src="https://github.com/user-attachments/assets/0876c789-7bcc-4414-a144-6c3f0aaffc06" />
</div>
