import os
import json
import webbrowser
import threading
import time
import requests
import secrets
import base64
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import typer

class AuthCallbackHandler(BaseHTTPRequestHandler):
    def __init__(self, auth_code_queue, *args, **kwargs):
        self.auth_code_queue = auth_code_queue
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            auth_code = query_params['code'][0]
            self.auth_code_queue.put(auth_code)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
            <html>
            <head><title>Authentication Successful</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #22c55e;">✅ Authentication Successful!</h1>
                <p>You can now close this window and return to your terminal.</p>
                <script>setTimeout(() => window.close(), 3000);</script>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        else:
            # Send error response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            error_html = """
            <html>
            <head><title>Authentication Failed</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #ef4444;">❌ Authentication Failed</h1>
                <p>Please try again.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

class OAuthProvider:
    """Base class for OAuth providers"""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    def get_auth_url(self, state: str) -> str:
        """Get the authorization URL"""
        raise NotImplementedError
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        raise NotImplementedError
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from the provider"""
        raise NotImplementedError

class GoogleOAuth(OAuthProvider):
    """Google OAuth implementation"""
    
    def get_auth_url(self, state: str) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'access_type': 'offline'
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        response.raise_for_status()
        return response.json()

class GitHubOAuth(OAuthProvider):
    """GitHub OAuth implementation"""
    
    def get_auth_url(self, state: str) -> str:
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'read:user user:email',
            'state': state
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        
        headers = {'Accept': 'application/json'}
        response = requests.post('https://github.com/login/oauth/access_token', data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        response.raise_for_status()
        return response.json()

class AuthManager:
    def __init__(self):
        self.token_file = Path.home() / ".exponent" / "auth_token.json"
        self.token_file.parent.mkdir(exist_ok=True)
        self.providers = {}
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup OAuth providers based on environment variables"""
        # Load from .env file if it exists
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        redirect_uri = "http://localhost:8080"
        
        # Google OAuth
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        if google_client_id and google_client_secret:
            self.providers["google"] = GoogleOAuth(google_client_id, google_client_secret, redirect_uri)
        
        # GitHub OAuth
        github_client_id = os.getenv("GITHUB_CLIENT_ID")
        github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        if github_client_id and github_client_secret:
            self.providers["github"] = GitHubOAuth(github_client_id, github_client_secret, redirect_uri)
    
    def get_stored_token(self) -> Optional[Dict[str, Any]]:
        """Get stored authentication token."""
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    # Check if token is still valid
                    if self._is_token_valid(token_data):
                        return token_data
            except Exception:
                pass
        return None
    
    def _is_token_valid(self, token_data: Dict[str, Any]) -> bool:
        """Check if stored token is still valid."""
        # Check if token has expired
        if 'expires_at' in token_data:
            return time.time() < token_data['expires_at']
        return True
    
    def store_token(self, token_data: Dict[str, Any]):
        """Store authentication token."""
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
    
    def clear_token(self):
        """Clear stored authentication token."""
        if self.token_file.exists():
            self.token_file.unlink()
    
    def authenticate_user(self, provider: Optional[str] = None) -> bool:
        """Authenticate user using OAuth flow."""
        # Check for existing valid token
        stored_token = self.get_stored_token()
        if stored_token:
            typer.echo("✅ Already authenticated!")
            return True
        
        if not self.providers:
            typer.echo("❌ No OAuth providers configured!")
            typer.echo("Please set up your OAuth credentials:")
            typer.echo("  - GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET for Google")
            typer.echo("  - GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET for GitHub")
            return False
        
        # If no provider specified, let user choose
        if not provider:
            if len(self.providers) == 1:
                provider = list(self.providers.keys())[0]
            else:
                typer.echo("🔐 Choose your authentication provider:")
                for i, prov in enumerate(self.providers.keys(), 1):
                    typer.echo(f"  {i}. {prov.title()}")
                
                try:
                    choice = int(typer.prompt("Enter your choice", default=1))
                    provider = list(self.providers.keys())[choice - 1]
                except (ValueError, IndexError):
                    typer.echo("❌ Invalid choice")
                    return False
        
        if provider not in self.providers:
            typer.echo(f"❌ Provider '{provider}' not configured")
            return False
        
        return self._authenticate_with_provider(provider)
    
    def _authenticate_with_provider(self, provider: str) -> bool:
        """Authenticate with a specific OAuth provider"""
        oauth_provider = self.providers[provider]
        
        typer.echo(f"🔐 Authenticating with {provider.title()}...")
        typer.echo("Opening browser for authentication...")
        
        # Generate state for security
        state = secrets.token_urlsafe(32)
        
        # Start local server for OAuth callback
        from queue import Queue
        auth_code_queue = Queue()
        
        # Use port 8080 for OAuth callback
        port = 8080
        server = HTTPServer(('localhost', port), 
                          lambda *args, **kwargs: AuthCallbackHandler(auth_code_queue, *args, **kwargs))
        
        # Start server in background thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Get authorization URL
        auth_url = oauth_provider.get_auth_url(state)
        
        # Open browser
        webbrowser.open(auth_url)
        
        typer.echo("🌐 Browser opened. Please complete authentication...")
        
        # Wait for auth code
        try:
            auth_code = auth_code_queue.get(timeout=300)  # 5 minute timeout
        except:
            typer.echo("❌ Authentication timed out")
            server.shutdown()
            return False
        
        # Exchange code for token
        try:
            token_response = oauth_provider.exchange_code_for_token(auth_code)
            
            # Get user info
            access_token = token_response.get('access_token')
            if not access_token:
                typer.echo("❌ Failed to get access token")
                server.shutdown()
                return False
            
            user_info = oauth_provider.get_user_info(access_token)
            
            # Store token with user info
            token_data = {
                "access_token": access_token,
                "provider": provider,
                "user_id": user_info.get('id'),
                "email": user_info.get('email'),
                "name": user_info.get('name', user_info.get('login')),
                "expires_at": time.time() + token_response.get('expires_in', 3600),
                "token_type": token_response.get('token_type', 'Bearer'),
                "refresh_token": token_response.get('refresh_token')
            }
            
            self.store_token(token_data)
            
            typer.echo(f"✅ Authentication successful with {provider.title()}!")
            typer.echo(f"👤 Welcome, {token_data['name']}!")
            server.shutdown()
            return True
            
        except Exception as e:
            typer.echo(f"❌ Authentication failed: {e}")
            server.shutdown()
            return False
    
    def require_auth(self):
        """Decorator to require authentication for commands."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    if not self.authenticate_user():
                        raise typer.Exit(1)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.get_stored_token() is not None
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information."""
        token_data = self.get_stored_token()
        if token_data:
            return {
                "user_id": token_data.get("user_id"),
                "email": token_data.get("email"),
                "name": token_data.get("name"),
                "provider": token_data.get("provider"),
                "expires_at": token_data.get("expires_at")
            }
        return None

# Global auth manager instance
auth_manager = AuthManager() 