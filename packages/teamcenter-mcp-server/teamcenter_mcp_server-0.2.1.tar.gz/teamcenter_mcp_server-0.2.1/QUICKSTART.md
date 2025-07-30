# Quick Start Guide - Teamcenter MCP Server

## ⚠️ IMPORTANT: Authentication Required

This MCP server requires authentication to access the Teamcenter Knowledge Base. You need either:
1. A web session cookie (easiest)
2. Azure AD credentials (more complex)

## Step 1: Install

```bash
pip install teamcenter-mcp-server
# or
uvx teamcenter-mcp-server
```

## Step 2: Get Authentication

### Option A: Web Cookie (Recommended for Quick Start)

1. Go to https://codesentinel.azurewebsites.net
2. Login with your Siemens credentials
3. Open Developer Tools (F12)
4. Go to Application → Cookies
5. Find and copy the `codesess` cookie value

### Option B: Azure AD Token

You need these values from your administrator:
- `AZURE_CLIENT_ID` - Your app's client ID
- `AZURE_TENANT_ID` - Your Azure AD tenant ID

```bash
# Set environment variables
export AZURE_CLIENT_ID="get-from-your-admin"
export AZURE_TENANT_ID="get-from-your-admin"

# Run the auth helper
teamcenter-auth-helper
```

## Step 3: Configure VS Code / Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "tools": [
    {
      "type": "mcp",
      "title": "Teamcenter KB",
      "transport": {
        "type": "stdio",
        "command": "teamcenter-mcp-server",
        "env": {
          "TEAMCENTER_API_HOST": "https://codesentinel.azurewebsites.net",
          "CODESESS_COOKIE": "paste-your-cookie-here"
        }
      }
    }
  ]
}
```

## Step 4: Test It

Ask your AI assistant:
- "Search Teamcenter KB for: How to create a BOM?"
- "What file processes JSON requests for updating classes?"

## Troubleshooting

### "Authentication failed"
- Your cookie may have expired (they last ~1 hour)
- Get a fresh cookie from the web app

### "No Azure credentials"
- Contact your Siemens IT administrator for:
  - Client ID (looks like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
  - Tenant ID (looks like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

### Need Help?
- PyPI Package: https://pypi.org/project/teamcenter-mcp-server/
- Full docs: https://github.com/your-repo/teamcenter-mcp-server
- Report issues: https://github.com/your-repo/teamcenter-mcp-server/issues