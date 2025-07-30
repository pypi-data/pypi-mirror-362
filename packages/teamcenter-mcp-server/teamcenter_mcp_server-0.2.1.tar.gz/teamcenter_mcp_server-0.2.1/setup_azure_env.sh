#!/bin/bash
# Setup script for Azure AD environment
# This script helps configure your environment securely

echo "CodeSentinel MCP Server - Azure AD Setup"
echo "========================================"
echo ""
echo "This script will help you set up your environment variables securely."
echo "Your credentials will ONLY be stored in your local shell environment."
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  Warning: .env file found. Loading existing configuration..."
    source .env
fi

# API Host
if [ -z "$TEAMCENTER_API_HOST" ]; then
    echo "Enter API Host (press Enter for default: https://codesentinel.azurewebsites.net):"
    read -r api_host
    export TEAMCENTER_API_HOST="${api_host:-https://codesentinel.azurewebsites.net}"
else
    echo "✓ Using existing TEAMCENTER_API_HOST: $TEAMCENTER_API_HOST"
fi

# Client ID
if [ -z "$AZURE_CLIENT_ID" ]; then
    echo ""
    echo "Enter Azure AD Client ID (get from your administrator):"
    read -r client_id
    if [ -z "$client_id" ]; then
        echo "❌ Error: Client ID is required for Azure AD authentication"
        exit 1
    fi
    export AZURE_CLIENT_ID="$client_id"
else
    echo "✓ Using existing AZURE_CLIENT_ID"
fi

# Tenant ID
if [ -z "$AZURE_TENANT_ID" ]; then
    echo ""
    echo "Enter Azure AD Tenant ID (get from your administrator):"
    read -r tenant_id
    if [ -z "$tenant_id" ]; then
        echo "❌ Error: Tenant ID is required for Azure AD authentication"
        exit 1
    fi
    export AZURE_TENANT_ID="$tenant_id"
else
    echo "✓ Using existing AZURE_TENANT_ID"
fi

echo ""
echo "✅ Environment configured successfully!"
echo ""
echo "To get an authentication token, run:"
echo "  python get_azure_token.py"
echo ""
echo "To save this configuration for future sessions, add to your shell profile:"
echo "  export TEAMCENTER_API_HOST='$TEAMCENTER_API_HOST'"
echo "  export AZURE_CLIENT_ID='$AZURE_CLIENT_ID'"
echo "  export AZURE_TENANT_ID='$AZURE_TENANT_ID'"
echo ""
echo "⚠️  IMPORTANT: Never commit these values to version control!"