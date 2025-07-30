#!/usr/bin/env python3
"""
Authentication helper for CodeSentinel MCP Server

This script helps you get authentication credentials for the MCP server:
1. Azure AD token using device flow
2. Instructions for getting cookie from web app

Usage:
    python get_auth_token.py          # Interactive device flow
    python get_auth_token.py --help   # Show all options
"""
import sys
import os
import argparse

# Azure AD configuration from environment
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")

if not CLIENT_ID or not TENANT_ID:
    print("❌ Error: Azure AD configuration not found!")
    print("\nPlease set environment variables:")
    print("  export AZURE_CLIENT_ID='your-client-id'")
    print("  export AZURE_TENANT_ID='your-tenant-id'")
    print("\nContact your administrator for these values.")
    sys.exit(1)

SCOPES = [f"api://{CLIENT_ID}/.default"]

def get_token_device_flow():
    """Get token using device code flow (works everywhere)"""
    app = PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )
    
    # Check cache first
    accounts = app.get_accounts()
    if accounts:
        print("Found cached account, trying silent authentication...")
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            return result
    
    # Device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print("Failed to create device flow:", flow.get("error_description"))
        return None
    
    print("\n" + "="*60)
    print(flow['message'])
    print("="*60 + "\n")
    
    result = app.acquire_token_by_device_flow(flow)
    return result

def get_token_interactive():
    """Get token using interactive browser flow (requires GUI)"""
    app = PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )
    
    # Try interactive authentication
    result = app.acquire_token_interactive(
        scopes=SCOPES,
        prompt="select_account"
    )
    return result

def main():
    print("CodeSentinel Azure AD Authentication")
    print("=" * 40)
    
    # Try device code flow (works in SSH/headless)
    result = get_token_device_flow()
    
    if result and "access_token" in result:
        token = result["access_token"]
        
        print("\n✅ Authentication successful!")
        print(f"\nAccess token (first 50 chars): {token[:50]}...")
        print(f"\nFull token length: {len(token)} characters")
        
        # Save to file for easy use
        with open(".azure_token", "w") as f:
            f.write(token)
        print("\n💾 Token saved to .azure_token file")
        
        # Show how to use it
        print("\n📋 To use with MCP server:")
        print(f"export AZURE_BEARER_TOKEN='{token}'")
        print("\nOr read from file:")
        print("export AZURE_BEARER_TOKEN=$(cat .azure_token)")
        
        # Show token info
        if "id_token_claims" in result:
            claims = result["id_token_claims"]
            print(f"\n👤 Authenticated as: {claims.get('name', claims.get('preferred_username', 'Unknown'))}")
            print(f"📧 Email: {claims.get('email', claims.get('upn', 'Not available'))}")
        
    else:
        print("\n❌ Authentication failed!")
        if result:
            print(f"Error: {result.get('error')}")
            print(f"Description: {result.get('error_description')}")
        sys.exit(1)

def main():
    """Main entry point for the auth helper"""
    # Check if msal is available
    try:
        from msal import PublicClientApplication
        run_azure_auth()
    except ImportError:
        print("❌ MSAL not installed. Showing alternative authentication methods...")
        show_alternatives()

def show_alternatives():
    """Show alternative authentication methods when MSAL is not available"""
    print("\n" + "="*60)
    print("Authentication Options for Teamcenter MCP Server")
    print("="*60)
    
    print("\n1. Web Cookie (Easiest):")
    print("   - Go to https://codesentinel.azurewebsites.net")
    print("   - Login with your Siemens credentials")
    print("   - Open DevTools (F12) → Application → Cookies")
    print("   - Copy the 'codesess' cookie value")
    print("\n   Then set: export CODESESS_COOKIE='your-cookie-value'")
    
    print("\n2. Install MSAL for Azure AD authentication:")
    print("   pip install msal")
    print("   Then run this command again")
    
    print("\n3. Get help from your administrator for Azure AD credentials")
    print("="*60)

def run_azure_auth():
    """Run the Azure AD authentication flow"""
    from msal import PublicClientApplication
    import json
    
    # Azure AD configuration from environment
    CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    TENANT_ID = os.getenv("AZURE_TENANT_ID")
    
    if not CLIENT_ID or not TENANT_ID:
        print("❌ Error: Azure AD configuration not found!")
        print("\nPlease set environment variables:")
        print("  export AZURE_CLIENT_ID='your-client-id'")
        print("  export AZURE_TENANT_ID='your-tenant-id'")
        print("\nContact your administrator for these values.")
        sys.exit(1)
    
    SCOPES = [f"api://{CLIENT_ID}/.default"]
    
    # Run the device flow authentication
    result = get_token_device_flow()
    
    if result and "access_token" in result:
        token = result["access_token"]
        
        print("\n✅ Authentication successful!")
        print(f"\nAccess token (first 50 chars): {token[:50]}...")
        
        # Save to file for easy use
        with open(".azure_token", "w") as f:
            f.write(token)
        print("\n💾 Token saved to .azure_token file")
        
        print("\n📋 To use with MCP server:")
        print(f"export AZURE_BEARER_TOKEN='{token}'")
    else:
        print("\n❌ Authentication failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()