"""
Authenticated MCP server - STDIO transport with session-based authentication
This version handles the Azure AD + session cookie authentication flow
Self-contained version with all dependencies merged
"""
from fastmcp import FastMCP
import httpx
import json
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict
import re
import logging
import sys
import argparse
import os
import requests
from pathlib import Path

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)  # Send logs to stderr so they don't interfere with STDIO MCP protocol
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# MERGED: CookieAuth class (from cookie_auth_minimal.py)
# ============================================================================

class CookieAuth:
    """Minimal cookie authentication using cached credentials"""
    
    def __init__(self, cache_file=None):
        # Use Windows cache file location by default (for WSL cross-compatibility)
        if cache_file is None:
            windows_cache = "/mnt/c/Users/z0052v7s/.teamcenter_easy_auth_cache.json"
            linux_cache = os.path.expanduser("~/.teamcenter_easy_auth_cache.json")
            
            # Prefer Windows cache if available, fallback to standard location
            if os.path.exists(windows_cache):
                cache_file = windows_cache
            else:
                cache_file = linux_cache
        
        self.cache_file = cache_file
        self.auth_cookie = None
        self.cookie_expiry = None
        self.user_info = None
        self._load_cache()
    
    def _load_cache(self):
        """Load cached auth cookie if available and not expired"""
        try:
            cache_path = Path(self.cache_file)
            if cache_path.exists():
                with open(cache_path, 'r') as f:
                    cache = json.load(f)
                
                # Check expiry
                expiry_str = cache.get('expiry')
                if expiry_str:
                    expiry = datetime.fromisoformat(expiry_str)
                    if expiry > datetime.now():
                        self.auth_cookie = cache.get('cookie')
                        self.cookie_expiry = expiry
                        self.user_info = cache.get('user_info', {})
                        logger.info(f"Loaded valid cookie, expires: {expiry}")
                        return True
                    else:
                        logger.warning(f"Cached cookie expired: {expiry}")
                else:
                    logger.warning("No expiry found in cache")
            else:
                logger.info(f"Cache file not found: {cache_path}")
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
        
        return False
    
    def has_valid_cookie(self):
        """Check if we have a valid authentication cookie"""
        if not self.auth_cookie or not self.cookie_expiry:
            return False
        
        # Check if still valid (with small buffer)
        return datetime.now() < self.cookie_expiry
    
    def get_auth_headers(self):
        """Get authentication headers for API requests"""
        if self.has_valid_cookie():
            return {
                "Cookie": f"codesess={self.auth_cookie}",
                "Content-Type": "application/json"
            }
        else:
            raise Exception("No valid authentication cookie available")
    
    def get_user_info(self):
        """Get user information from cache"""
        return self.user_info or {}

# ============================================================================
# MERGED: TeamCenterAuthSession class (from teamcenter_auth_session.py)
# ============================================================================

class TeamCenterAuthSession:
    """Hybrid authentication session supporting mock and production modes"""
    
    def __init__(self, base_url: Optional[str] = None):
        # Environment variable takes precedence, then parameter, then default
        self.base_url = base_url or os.getenv("TEAMCENTER_API_HOST", "http://127.0.0.1:8000")
        self.base_url = self.base_url.rstrip('/')  # Remove trailing slash
        
        # Session state
        self.session_cookie: Optional[str] = None
        self.expires_at: Optional[datetime] = None
        
        # Determine authentication mode based on URL
        if self.base_url.startswith("https://codesentinel"):
            self.auth_mode = "cookie"
            self._init_cookie_auth()
        else:
            self.auth_mode = "mock"
            self._init_mock_auth()
        
        logger.info(f"🔧 AuthSession initialized: mode={self.auth_mode}, url={self.base_url}")
    
    def _init_cookie_auth(self):
        """Initialize cookie-based authentication for production"""
        try:
            self.cookie_auth = CookieAuth()
            if not self.cookie_auth.has_valid_cookie():
                logger.warning("No valid cookie found for production mode")
                logger.info("💡 Run 'python easy_auth_client.py ask \"test\"' to authenticate")
                logger.info("🔄 Falling back to mock mode")
                self._fallback_to_mock()
            else:
                # Use the cached cookie for session
                self.session_cookie = self.cookie_auth.auth_cookie
                self.expires_at = self.cookie_auth.cookie_expiry
                logger.info(f"✅ Cookie auth initialized, expires: {self.expires_at}")
        except Exception as e:
            logger.error(f"Cookie auth initialization failed: {e}")
            logger.info("🔄 Falling back to mock mode")
            self._fallback_to_mock()
    
    def _init_mock_auth(self):
        """Initialize mock authentication for localhost"""
        # Create a real session with the mock server
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/login",
                headers={"Authorization": "Bearer mock_token"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.session_cookie = data["session_id"]
                self.expires_at = datetime.fromisoformat(data["expires_at"])
                logger.info(f"🔧 Mock auth initialized with session: {self.session_cookie[:8]}...")
            else:
                # Fallback to basic mock
                self.session_cookie = "mock_session_cookie"
                self.expires_at = datetime.now() + timedelta(hours=1)
                logger.warning("🔧 Mock auth fallback - couldn't create session")
        except Exception as e:
            # Fallback to basic mock  
            self.session_cookie = "mock_session_cookie"
            self.expires_at = datetime.now() + timedelta(hours=1)
            logger.warning(f"🔧 Mock auth fallback due to error: {e}")
    
    def _fallback_to_mock(self):
        """Fallback to mock mode when production auth fails"""
        self.auth_mode = "mock"
        self.base_url = "http://127.0.0.1:8000"
        self._init_mock_auth()
    
    def is_session_valid(self) -> bool:
        """Check if current session is still valid (with 5-minute buffer)"""
        if not self.session_cookie or not self.expires_at:
            logger.debug("🔍 Session invalid: missing cookie or expiry")
            return False
        
        # Check expiry with 5-minute buffer (like the real client)
        buffer_time = timedelta(minutes=5)
        is_valid = datetime.now() < (self.expires_at - buffer_time)
        logger.debug(f"🔍 Session validity check: {is_valid}, expires at {self.expires_at}")
        return is_valid
    
    async def authenticate(self) -> Optional[str]:
        """Authenticate and return session ID"""
        if self.auth_mode == "mock":
            # Mock authentication always succeeds
            logger.info("🔧 Mock authentication successful")
            return self.session_cookie
        
        elif self.auth_mode == "cookie":
            if self.is_session_valid():
                logger.info("✅ Using existing valid session")
                return self.session_cookie
            else:
                logger.warning("❌ Session invalid or expired")
                # For now, don't try to refresh - require manual re-auth
                logger.info("💡 Run 'python easy_auth_client.py ask \"test\"' to re-authenticate")
                return None
        
        return None
    
    async def make_authenticated_request(self, endpoint: str, method: str = "GET", 
                                       data: Optional[Dict] = None, 
                                       params: Optional[Dict] = None,
                                       stream: bool = False) -> Optional[requests.Response]:
        """Make authenticated request to the API"""
        # Ensure we have a valid session
        session_id = await self.authenticate()
        if not session_id:
            raise Exception("Authentication failed - no valid session")
        
        # Prepare headers
        if self.auth_mode == "cookie":
            headers = {
                "Cookie": f"codesess={self.session_cookie}",
                "Content-Type": "application/json"
            }
        else:  # mock mode
            headers = {
                "Cookie": f"codesess={self.session_cookie}",
                "Content-Type": "application/json"
            }
        
        # Construct URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"🌐 {method} {url} (mode: {self.auth_mode})")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, stream=stream, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, params=params, stream=stream, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log response status
            logger.debug(f"📊 Response: {response.status_code}")
            
            # Handle authentication errors
            if response.status_code == 401:
                logger.warning("🔒 Authentication failed (401)")
                if self.auth_mode == "cookie":
                    logger.info("💡 Cookie might be expired - run easy_auth_client.py")
                raise Exception("Authentication failed - 401 Unauthorized")
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"🔥 Request failed: {e}")
            return None
    
    def get_auth_status(self) -> Dict:
        """Get authentication status for debugging"""
        return {
            "auth_mode": self.auth_mode,
            "base_url": self.base_url,
            "is_session_valid": self.is_session_valid(),
            "session_cookie_length": len(self.session_cookie) if self.session_cookie else 0,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

# ============================================================================
# ORIGINAL: MCP Server Implementation
# ============================================================================

# Global auth session - will be initialized in main()
auth_session = None

# Global MCP instance - will be initialized in main()
mcp = None

async def teamcenter_search(search_query: str, 
                           topNDocuments: int = 5, 
                           sessionID: str = "default",
                           llm: str = "gpt-4o-mini",
                           language: str = "english") -> str:
    """
    Search Teamcenter knowledge base for technical information and documentation with streaming response
    
    Args:
        search_query: The search query to process
        topNDocuments: Number of top documents to retrieve (1-20)
        sessionID: Session identifier for the request
        llm: Language model to use (gpt-4o-mini, gpt-4o, claude-3-5-sonnet-latest)
        language: Response language (english, german, chinese)
    
    Returns:
        Streaming response with search results and citations
    """
    global auth_session
    
    if not auth_session:
        logger.error("Auth session not initialized")
        return "Error: Authentication session not available"
    
    try:
        # Prepare query parameters
        params = {
            "search_query": search_query,
            "sessionID": sessionID,
            "topNDocuments": min(max(topNDocuments, 1), 20),  # Clamp between 1-20
            "llm": llm,
            "language": language,
            "subfolder": ""  # Default subfolder
        }
        
        logger.info(f"🔍 Searching: {search_query[:50]}... (session: {sessionID[:8]}...)")
        
        # Make streaming request to the search endpoint
        response = await auth_session.make_authenticated_request(
            endpoint="stream", 
            method="GET",
            params=params  # Pass the query parameters!
        )
        
        if response is None:
            return "Error: Failed to connect to Teamcenter API"
        
        if response.status_code != 200:
            logger.error(f"Search failed: {response.status_code} - {response.text}")
            return f"Error: Search failed with status {response.status_code}"
        
        # For now, return non-streaming response
        # TODO: Implement proper streaming when MCP supports it
        response_text = response.text
        logger.info(f"✅ Search completed, response length: {len(response_text)}")
        
        return response_text
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"Error during search: {str(e)}"

async def teamcenter_health_check() -> str:
    """
    Check the health status of the Teamcenter API connection
    
    Returns:
        Health status information
    """
    global auth_session
    
    if not auth_session:
        return "Error: Authentication session not available"
    
    try:
        logger.info("🏥 Performing health check")
        
        # Call the health endpoint
        response = await auth_session.make_authenticated_request(endpoint="health")
        
        if response is None:
            return "❌ Health check failed: No response from API"
        
        if response.status_code == 200:
            health_data = response.json() if response.text else {"status": "ok"}
            logger.info("✅ Health check passed")
            return f"✅ Teamcenter API is healthy: {json.dumps(health_data, indent=2)}"
        else:
            logger.warning(f"Health check returned status {response.status_code}")
            return f"⚠️ Health check status: {response.status_code} - {response.text}"
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return f"❌ Health check failed: {str(e)}"

async def teamcenter_session_info() -> str:
    """
    Get information about the current authentication session
    
    Returns:
        Session information and authentication status
    """
    global auth_session
    
    if not auth_session:
        return "Error: Authentication session not available"
    
    try:
        auth_status = auth_session.get_auth_status()
        
        # Don't expose sensitive session cookie data
        safe_status = {
            "auth_mode": auth_status["auth_mode"],
            "base_url": auth_status["base_url"],
            "is_session_valid": auth_status["is_session_valid"],
            "expires_at": auth_status["expires_at"],
            "has_session_cookie": auth_status["session_cookie_length"] > 0
        }
        
        return f"📊 Session Status:\n{json.dumps(safe_status, indent=2)}"
        
    except Exception as e:
        logger.error(f"Session info error: {e}")
        return f"Error getting session info: {str(e)}"

def main():
    """Main entry point for the MCP server"""
    global auth_session, mcp
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Teamcenter MCP Server with Azure AD Authentication')
    parser.add_argument('--base-url', 
                       help='Base URL for the Teamcenter API (default: http://localhost:8000)')
    args = parser.parse_args()
    
    # Initialize FastMCP server
    mcp = FastMCP("Teamcenter Knowledge Base")
    
    # Register all the tools
    mcp.tool(teamcenter_search)
    mcp.tool(teamcenter_health_check) 
    mcp.tool(teamcenter_session_info)
    
    # Determine base URL from args, env var, or default
    base_url = args.base_url or os.environ.get('TEAMCENTER_API_URL') or os.environ.get('TEAMCENTER_API_HOST') or 'http://localhost:8000'
    
    # Initialize global auth session with hybrid authentication
    auth_session = TeamCenterAuthSession(base_url)
    
    # Use STDIO transport - VS Code will manage this process
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()