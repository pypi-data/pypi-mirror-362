"""
MCP server for CodeSentinel API with Azure AD authentication
Optimized for fast imports and real production use
"""
from fastmcp import FastMCP
import httpx
import json
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging
import sys
import os

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)  # Send logs to stderr so they don't interfere with STDIO MCP protocol
    ]
)
logger = logging.getLogger(__name__)

# Create MCP server instance with name
mcp = FastMCP("teamcenter-mcp-server")
mcp.version = "0.2.1"  # Set version as attribute

class AuthSession:
    """Manages authentication for CodeSentinel API"""
    
    def __init__(self):
        self.session_cookie: Optional[str] = None
        self.expires_at: Optional[datetime] = None
        self.base_url = os.getenv("TEAMCENTER_API_HOST", "http://127.0.0.1:8000")
        self.auth_mode = "production" if "azurewebsites.net" in self.base_url else "mock"
        
        # Azure AD config from environment (NO DEFAULTS!)
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        
        logger.info(f"🔧 AuthSession initialized - Mode: {self.auth_mode}, Base URL: {self.base_url}")
    
    def is_session_valid(self) -> bool:
        """Check if current session is still valid (with 5-minute buffer)"""
        if not self.session_cookie or not self.expires_at:
            return False
        
        buffer_time = timedelta(minutes=5)
        return datetime.now() < (self.expires_at - buffer_time)
    
    async def authenticate(self) -> Optional[str]:
        """Authenticate and return session ID"""
        if self.is_session_valid():
            logger.debug("✅ Using existing valid session")
            return self.session_cookie
        
        if self.auth_mode == "mock":
            return await self._mock_authenticate()
        else:
            return await self._azure_authenticate()
    
    async def _mock_authenticate(self) -> Optional[str]:
        """Mock authentication for local development"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/login",
                    headers={"Authorization": "Bearer mock_token"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.session_cookie = data["session_id"]
                    self.expires_at = datetime.fromisoformat(data["expires_at"])
                    logger.info(f"✅ Mock auth successful: {self.session_cookie[:8]}...")
                    return self.session_cookie
        except Exception as e:
            logger.error(f"❌ Mock auth failed: {e}")
            # Use fallback mock session
            self.session_cookie = "mock_session_12345"
            self.expires_at = datetime.now() + timedelta(hours=1)
            return self.session_cookie
    
    async def _azure_authenticate(self) -> Optional[str]:
        """Azure AD authentication for production"""
        # First check if we have a direct cookie
        codesess_cookie = os.getenv("CODESESS_COOKIE")
        if codesess_cookie:
            logger.info("🍪 Using CODESESS_COOKIE from environment")
            self.session_cookie = codesess_cookie
            self.expires_at = datetime.now() + timedelta(minutes=55)
            logger.info(f"✅ Cookie auth successful: {self.session_cookie[:8]}...")
            return self.session_cookie
        
        # Otherwise, check if we have a bearer token in environment
        bearer_token = os.getenv("AZURE_BEARER_TOKEN")
        if not bearer_token:
            logger.error("❌ No CODESESS_COOKIE or AZURE_BEARER_TOKEN environment variable set")
            logger.info("💡 To authenticate: Set CODESESS_COOKIE or AZURE_BEARER_TOKEN")
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/login",
                    headers={
                        "Authorization": f"Bearer {bearer_token}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Auth failed: {response.status_code} {response.text}")
                    return None
                
                # Extract session cookie from Set-Cookie header
                set_cookie = response.headers.get("set-cookie", "")
                if "codesess=" in set_cookie:
                    import re
                    match = re.search(r'codesess=([^;]+)', set_cookie)
                    if match:
                        self.session_cookie = match.group(1)
                        self.expires_at = datetime.now() + timedelta(minutes=55)
                        logger.info(f"✅ Azure AD auth successful: {self.session_cookie[:8]}...")
                        return self.session_cookie
                
                logger.error("❌ No session cookie in response")
                return None
                
        except Exception as e:
            logger.error(f"❌ Azure AD auth failed: {e}")
            return None
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for authenticated requests"""
        if self.session_cookie:
            return {"Cookie": f"codesess={self.session_cookie}"}
        return {}

# Global auth session
auth_session = AuthSession()

@mcp.tool()
async def search(search_query: str, topNDocuments: int = 5) -> str:
    """Search the Teamcenter Knowledge Base for technical information
    
    Args:
        search_query: The search query to find relevant documents
        topNDocuments: Number of top documents to return (default: 5)
    
    Returns:
        Streaming response with search results and citations
    """
    logger.info(f"🔍 Search request: '{search_query}' (top {topNDocuments})")
    
    # Ensure we're authenticated
    session_id = await auth_session.authenticate()
    if not session_id:
        return json.dumps({
            "error": "Authentication failed. Please check your credentials.",
            "details": "Set AZURE_BEARER_TOKEN environment variable for production use"
        })
    
    try:
        # Make the search request with streaming
        url = f"{auth_session.base_url}/stream"
        params = {
            "search_query": search_query,
            "topNDocuments": topNDocuments
        }
        
        async with httpx.AsyncClient() as client:
            # Use event stream for real API, regular JSON for mock
            if auth_session.auth_mode == "production":
                headers = auth_session.get_headers()
                headers["Accept"] = "text/event-stream"
            else:
                headers = auth_session.get_headers()
            
            response = await client.get(
                url,
                params=params,
                headers=headers,
                timeout=60.0  # Real API can be slow
            )
            
            if response.status_code != 200:
                logger.error(f"❌ Search failed: {response.status_code}")
                return json.dumps({
                    "error": f"Search failed with status {response.status_code}",
                    "details": response.text
                })
            
            # For production, we'd parse SSE stream here
            # For now, return the response content
            content = response.text
            logger.info(f"✅ Search completed successfully")
            return content
            
    except Exception as e:
        logger.error(f"❌ Search error: {e}")
        return json.dumps({
            "error": "Search request failed",
            "details": str(e)
        })

@mcp.tool()
async def health_check() -> str:
    """Check the health status of the Teamcenter API connection
    
    Returns:
        JSON with connection status and session information
    """
    logger.info("🏥 Health check requested")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{auth_session.base_url}/health",
                timeout=10.0
            )
            
            health_status = {
                "api_status": "healthy" if response.status_code == 200 else "unhealthy",
                "api_url": auth_session.base_url,
                "auth_mode": auth_session.auth_mode,
                "session_valid": auth_session.is_session_valid(),
                "response_code": response.status_code
            }
            
            if auth_session.is_session_valid():
                health_status["session_expires_at"] = auth_session.expires_at.isoformat()
            
            logger.info(f"✅ Health check completed: {health_status['api_status']}")
            return json.dumps(health_status, indent=2)
            
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return json.dumps({
            "api_status": "error",
            "error": str(e),
            "api_url": auth_session.base_url
        }, indent=2)

@mcp.tool()
async def session_info() -> str:
    """Get current session information and authentication status
    
    Returns:
        JSON with session details and authentication configuration
    """
    logger.info("🔐 Session info requested")
    
    info = {
        "auth_mode": auth_session.auth_mode,
        "api_url": auth_session.base_url,
        "session_valid": auth_session.is_session_valid(),
        "session_cookie_present": bool(auth_session.session_cookie)
    }
    
    if auth_session.auth_mode == "production":
        info["azure_config"] = {
            "client_id": auth_session.client_id,
            "tenant_id": auth_session.tenant_id,
            "bearer_token_set": bool(os.getenv("AZURE_BEARER_TOKEN")),
            "codesess_cookie_set": bool(os.getenv("CODESESS_COOKIE"))
        }
    
    if auth_session.is_session_valid() and auth_session.expires_at:
        info["expires_at"] = auth_session.expires_at.isoformat()
        info["expires_in_minutes"] = int((auth_session.expires_at - datetime.now()).total_seconds() / 60)
    
    return json.dumps(info, indent=2)

def main():
    """Main entry point for the MCP server"""
    logger.info(f"🚀 Starting Teamcenter MCP Server v{mcp.version}")
    logger.info(f"📍 API Host: {auth_session.base_url}")
    logger.info(f"🔧 Auth Mode: {auth_session.auth_mode}")
    
    # Run with STDIO transport - VS Code will manage this process
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()