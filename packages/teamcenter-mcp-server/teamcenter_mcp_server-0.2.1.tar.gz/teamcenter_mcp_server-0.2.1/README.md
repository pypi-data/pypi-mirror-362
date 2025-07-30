# Teamcenter MCP Server

Universal MCP server for integrating AI assistants with Teamcenter Knowledge Base APIs with Azure AD authentication support.

📦 **Live on PyPI:** https://pypi.org/project/teamcenter-mcp-server/

## ✨ What's New in v0.2.0
- 🔐 **Azure AD Authentication** - Connect to real Teamcenter APIs
- 🔄 **Hybrid Mode** - Seamless switching between localhost mock and production
- 🌍 **Environment Variables** - Configure via `TEAMCENTER_API_HOST`
- 🛡️ **Secure** - Uses cached Azure AD cookies, no secrets in code

## Quick Start (Just Copy & Paste)

### 🚀 Production Mode (Azure AD)
Add to `~/.continue/config.json`:
```json
{
  "experimental": {
    "modelContextProtocolServers": [{
      "transport": {
        "type": "stdio",
        "command": "uvx",
        "args": ["teamcenter-mcp-server@0.2.0"],
        "env": {
          "TEAMCENTER_API_HOST": "https://codesentinel.azurewebsites.net"
        }
      }
    }]
  }
}
```

### 🔧 Development Mode (Localhost Mock)
Add to `~/.continue/config.json`:
```json
{
  "experimental": {
    "modelContextProtocolServers": [{
      "transport": {
        "type": "stdio",
        "command": "uvx",
        "args": ["teamcenter-mcp-server-test@0.1.2"]
      }
    }]
  }
}
```

### VS Code (Production)
Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "teamcenter": {
      "type": "stdio",
      "command": "uvx",
      "args": ["teamcenter-mcp-server@0.2.0"],
      "env": {
        "TEAMCENTER_API_HOST": "https://codesentinel.azurewebsites.net"
      }
    }
  }
}
```

### JetBrains IDEs (Production)
Add to `~/.mcp.json`:
```json
{
  "mcpServers": {
    "teamcenter": {
      "command": "uvx",
      "args": ["teamcenter-mcp-server@0.2.0"],
      "env": {
        "TEAMCENTER_API_HOST": "https://codesentinel.azurewebsites.net"
      }
    }
  }
}
```

## 🔐 Azure AD Authentication Setup

### Prerequisites
1. **Authenticate first** using the working Python client:
   ```bash
   # Run this once to cache Azure AD credentials
   python /path/to/easy_auth_client.py ask "test"
   ```

2. **Verify authentication** works:
   ```bash
   # Check for cached cookie
   ls ~/.teamcenter_easy_auth_cache.json
   ```

### Environment Variables
- `TEAMCENTER_API_HOST`: API endpoint URL
  - Production: `https://codesentinel.azurewebsites.net`
  - Development: `http://localhost:8000` (default)

## 📦 Version History
- **v0.2.0** (Latest) - Azure AD authentication + hybrid mode
- **v0.1.2** - Azure AD authentication + hybrid mode
- **v0.1.1** - Localhost mock only (legacy)

## Usage

**→ [See USAGE.md for copy & paste examples](USAGE.md) ←**

Quick examples:
- **VS Code**: `@workspace get Teamcenter API documentation for part creation`
- **Continue.dev**: `@MCP search for PLM workflow integration documentation`

## Production Setup

Replace `http://localhost:8000` with your real Teamcenter API:
```json
"args": ["teamcenter-mcp-server", "--base-url", "https://teamcenter.yourcompany.com"]
```

## Testing

### Quick Test
```bash
uvx teamcenter-mcp-server --version
```

### Demo/Development Setup

Start mock API server:
```bash
git clone https://github.com/your-repo/mock-api
cd mock-api
uv run uvicorn main:app --reload
```

Server runs on `http://localhost:8000` - use this URL in configs above.

---

## Development (Advanced)

<details>
<summary>Click for development setup</summary>

### Installation
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Build Package
```bash
uv build
```

### Run Tests
```bash
uv run pytest tests/ -v
```

### Publishing to PyPI
**→ [See DEVELOPER.md for release instructions](DEVELOPER.md) ←**

### Files Overview
- `auth_mcp_stdio_v2.py`: Main MCP server with optimized imports
- `main.py`: Mock API server for development
- `pyproject.toml`: Package configuration

</details>