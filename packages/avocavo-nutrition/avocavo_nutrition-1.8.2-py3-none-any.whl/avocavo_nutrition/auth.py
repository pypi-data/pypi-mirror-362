"""
Authentication module for Avocavo Nutrition API
Handles user login, logout, and API key management
Supports both email/password and OAuth browser login
"""

import os
import json
import keyring
import requests
import webbrowser
import time
from typing import Optional, Dict, List
from pathlib import Path
from .models import Account
from .exceptions import ApiError, AuthenticationError


class AuthManager:
    """Manages authentication and API key storage"""
    
    SERVICE_NAME = "avocavo-nutrition"
    CONFIG_DIR = Path.home() / ".avocavo"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self, base_url: str = "https://app.avocavo.app"):
        self.base_url = base_url.rstrip('/')
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
    
    def login(self, email: str = None, password: str = None, provider: str = "google") -> Dict:
        """
        Login with email/password or OAuth browser login
        
        Args:
            email: User email (for email/password login)
            password: User password (for email/password login)
            provider: OAuth provider ("google" or "github") for browser login
            
        Returns:
            Dictionary with user info and API key
            
        Raises:
            AuthenticationError: If login fails
        """
        # If email and password provided, use traditional login
        if email and password:
            return self._login_with_password(email, password)
        
        # Otherwise use OAuth browser login
        return self._login_with_oauth(provider)
        
    def _prompt_for_provider(self) -> str:
        """Prompt user to choose OAuth provider"""
        print("\n🔐 Choose OAuth Provider:")
        print("1. Google")
        print("2. GitHub")
        
        while True:
            choice = input("Enter choice (1-2): ").strip()
            if choice == "1":
                return "google"
            elif choice == "2":
                return "github"
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
                continue
    
    def _login_with_password(self, email: str, password: str) -> Dict:
        """Traditional email/password login"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=30
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid email or password")
            elif response.status_code != 200:
                raise AuthenticationError(f"Login failed: {response.status_code}")
            
            data = response.json()
            
            if not data.get('success'):
                raise AuthenticationError(data.get('error', 'Login failed'))
            
            # Extract user info and API key
            user_info = data.get('user', {})
            api_key = user_info.get('api_key')
            
            if not api_key:
                raise AuthenticationError("No API key received")
            
            # Store API key securely
            self._store_api_key(email, api_key)
            
            # Store user config
            self._store_user_config({
                'email': email,
                'user_id': user_info.get('id'),
                'api_tier': user_info.get('api_tier', 'developer'),
                'logged_in_at': data.get('timestamp'),
                'login_method': 'password'
            })
            
            return {
                'success': True,
                'email': email,
                'api_tier': user_info.get('api_tier'),
                'api_key': api_key[:12] + "...",  # Masked for display
                'message': 'Successfully logged in'
            }
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")
    
    def _login_with_oauth(self, provider: str) -> Dict:
        """OAuth browser login with Google or GitHub"""
        try:
            print(f"🔐 Initiating {provider.title()} OAuth login...")
            
            # Step 1: Initiate OAuth flow
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/login",
                    json={"provider": provider},
                    timeout=30
                )
            except requests.exceptions.SSLError:
                # Fallback for SSL certificate issues
                print("⚠️  SSL certificate issue detected, using fallback...")
                response = requests.post(
                    f"{self.base_url}/api/auth/login",
                    json={"provider": provider},
                    timeout=30,
                    verify=False
                )
            
            if response.status_code != 200:
                data = response.json() if response.content else {}
                raise AuthenticationError(data.get('error', f'Failed to initiate {provider} login'))
            
            auth_data = response.json()
            if not auth_data.get('success'):
                raise AuthenticationError(auth_data.get('error', 'OAuth initiation failed'))
            
            session_id = auth_data.get('session_id')
            oauth_url = auth_data.get('oauth_url')
            
            if not session_id or not oauth_url:
                raise AuthenticationError("Invalid OAuth response from server")
            
            # Step 2: Open browser for user authentication
            print(f"🌐 Opening browser for {provider.title()} authentication...")
            print(f"📋 If browser doesn't open automatically, visit: {oauth_url}")
            
            try:
                webbrowser.open(oauth_url)
            except Exception:
                print("⚠️  Could not open browser automatically")
            
            # Step 3: Poll for completion
            print("⏳ Waiting for authentication to complete...")
            max_attempts = 60  # 5 minutes timeout
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    try:
                        status_response = requests.get(
                            f"{self.base_url}/api/auth/status/{session_id}",
                            timeout=10
                        )
                    except requests.exceptions.SSLError:
                        # Fallback for SSL certificate issues
                        status_response = requests.get(
                            f"{self.base_url}/api/auth/status/{session_id}",
                            timeout=10,
                            verify=False
                        )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        
                        if status_data.get('status') in ['completed', 'retrieved']:
                            # Success! Store JWT token for identity
                            jwt_token = status_data.get('jwt_token')
                            user_email = status_data.get('user_email')
                            
                            if jwt_token and user_email:
                                # Store JWT token for identity and key management
                                self._store_jwt_token(user_email, jwt_token)
                                
                                # Store user config
                                self._store_user_config({
                                    'email': user_email,
                                    'api_tier': 'developer',  # Default for OAuth users
                                    'logged_in_at': time.time(),
                                    'login_method': 'oauth',
                                    'oauth_provider': provider
                                })
                                
                                print(f"✅ Login successful! Welcome {user_email}")
                                print("💡 Use av.create_api_key() to create an API key for making requests")
                                
                                # Break out of the polling loop
                                return {
                                    'success': True,
                                    'email': user_email,
                                    'api_tier': 'developer',
                                    'provider': provider,
                                    'message': f'{provider.title()} OAuth login successful'
                                }
                            else:
                                raise AuthenticationError("Invalid response from OAuth completion")
                        
                        elif status_data.get('status') == 'error':
                            raise AuthenticationError(status_data.get('error', 'OAuth authentication failed'))
                        
                        # Still pending, continue polling
                        if attempt == 0:
                            print("👆 Please complete authentication in your browser...")
                        elif attempt % 10 == 0:  # Show progress every 10 attempts
                            print("⏳ Still waiting for authentication...")
                    
                    elif status_response.status_code == 404:
                        print(f"❌ Session not found (404). Attempt {attempt + 1}/{max_attempts}")
                        raise AuthenticationError("OAuth session expired. Please try again.")
                    elif status_response.status_code == 410:
                        # Session already retrieved, this is expected
                        print(f"❌ Session already used (410). Attempt {attempt + 1}/{max_attempts}")
                        raise AuthenticationError("OAuth session already used. Please try again.")
                    else:
                        print(f"❌ Unexpected status code: {status_response.status_code}. Response: {status_response.text[:200]}")
                
                except requests.exceptions.RequestException:
                    pass  # Network issues, continue trying
                
                time.sleep(5)  # Wait 5 seconds between polls
                attempt += 1
            
            raise AuthenticationError("OAuth login timed out. Please try again.")
            
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"OAuth login failed: {str(e)}")
    
    def logout(self) -> Dict:
        """
        Logout current user and clear stored credentials
        
        Returns:
            Success message
        """
        config = self._load_user_config()
        
        if config and config.get('email'):
            # Remove stored API key
            try:
                keyring.delete_password(self.SERVICE_NAME, config['email'])
            except keyring.errors.PasswordDeleteError:
                pass  # Key was already removed
        
        # Remove config file
        if self.config_file.exists():
            self.config_file.unlink()
        
        return {
            'success': True,
            'message': 'Successfully logged out'
        }
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Get current logged-in user info
        
        Returns:
            User info dictionary or None if not logged in
        """
        config = self._load_user_config()
        
        if not config or not config.get('email'):
            return None
        
        # For OAuth users, check if we have a JWT session
        if config.get('login_method') == 'oauth':
            jwt_token = self._get_jwt_token(config['email'])
            if jwt_token:
                return {
                    'email': config['email'],
                    'api_tier': config.get('api_tier'),
                    'user_id': config.get('user_id'),
                    'logged_in_at': config.get('logged_in_at'),
                    'login_method': 'oauth',
                    'provider': config.get('oauth_provider'),
                    'has_jwt': True
                }
        
        # For password users, check for API key
        api_key = self._get_api_key(config['email'])
        if api_key:
            return {
                'email': config['email'],
                'api_tier': config.get('api_tier'),
                'user_id': config.get('user_id'),
                'api_key': api_key,
                'logged_in_at': config.get('logged_in_at'),
                'login_method': 'password'
            }
        
        return None
    
    def get_api_key(self) -> Optional[str]:
        """
        Get stored API key for current user
        
        Returns:
            Selected API key for nutrition calls, or JWT token if no API key selected
        """
        config = self._load_user_config()
        if not config or not config.get('email'):
            return None
        
        # If user has selected an API key, return that for nutrition calls
        if config.get('selected_api_key'):
            return config['selected_api_key']
        
        # Otherwise return JWT token (for API key management operations)
        return self._get_api_key(config['email'])
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        return self.get_current_user() is not None
    
    def get_jwt_auth_headers(self) -> Dict[str, str]:
        """Get JWT authentication headers for API key management"""
        config = self._load_user_config()
        if not config or not config.get('email'):
            raise AuthenticationError("Not logged in. Please login first.")
        
        jwt_token = self._get_jwt_token(config['email'])
        if not jwt_token:
            raise AuthenticationError("No JWT token found. Please login again.")
        
        return {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
    
    def list_api_keys(self) -> Dict:
        """
        List all API keys for the authenticated user
        
        Returns:
            Dictionary with list of API keys and usage information
        """
        try:
            headers = self.get_jwt_auth_headers()
            response = requests.get(f"{self.base_url}/api/auth/keys", headers=headers, timeout=30, verify=False)
            
            if response.status_code == 401:
                raise AuthenticationError("Session expired. Please login again.")
            elif response.status_code != 200:
                raise AuthenticationError(f"Failed to list API keys: {response.status_code}")
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")
    
    def create_api_key(self, name: str = "Python Package Key", description: str = None, environment: str = "development") -> Dict:
        """
        Create a new API key
        
        Args:
            name: Name for the API key
            description: Optional description
            environment: Environment tag (development, staging, production)
            
        Returns:
            Dictionary with new API key information (full key shown only once)
        """
        try:
            headers = self.get_jwt_auth_headers()
            data = {
                "key_name": name,
                "description": description or "Created via Python package",
                "environment": environment
            }
            
            response = requests.post(f"{self.base_url}/api/auth/keys", json=data, headers=headers, timeout=30, verify=False)
            
            if response.status_code == 401:
                raise AuthenticationError("Session expired. Please login again.")
            elif response.status_code not in [200, 201]:
                error_data = response.json() if response.content else {}
                raise AuthenticationError(error_data.get('error', f'Failed to create API key: {response.status_code}'))
            
            result = response.json()
            
            # Automatically store the new API key for use
            if result.get('key', {}).get('api_key'):
                config = self._load_user_config()
                if config and config.get('email'):
                    self._store_api_key(config['email'], result['key']['api_key'])
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")
    
    def switch_to_api_key(self, api_key: str) -> Dict:
        """
        Switch to using a specific API key
        
        Args:
            api_key: The API key to switch to
            
        Returns:
            Success confirmation
        """
        config = self._load_user_config()
        if not config or not config.get('email'):
            raise AuthenticationError("Not logged in. Please login first.")
        
        # Store the API key
        self._store_api_key(config['email'], api_key)
        
        return {
            'success': True,
            'message': f'Switched to API key: {api_key[:12]}...',
            'api_key_preview': f'{api_key[:12]}...'
        }
    
    def delete_api_key(self, key_id: int) -> Dict:
        """
        Delete (deactivate) an API key
        
        Args:
            key_id: ID of the key to delete
            
        Returns:
            Dictionary with deletion confirmation
        """
        try:
            headers = self.get_jwt_auth_headers()
            response = requests.delete(f"{self.base_url}/api/auth/keys/{key_id}", headers=headers, timeout=30, verify=False)
            
            if response.status_code == 401:
                raise AuthenticationError("Session expired. Please login again.")
            elif response.status_code != 200:
                error_data = response.json() if response.content else {}
                raise AuthenticationError(error_data.get('error', f'Failed to delete API key: {response.status_code}'))
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")
    
    def _store_api_key(self, email: str, api_key: str) -> None:
        """Store API key securely using keyring"""
        try:
            keyring.set_password(self.SERVICE_NAME, email, api_key)
        except Exception as e:
            # Fallback to config file if keyring fails
            print(f"Warning: Could not store API key securely: {e}")
            config = self._load_user_config() or {}
            config['api_key_fallback'] = api_key
            self._store_user_config(config)
    
    def _store_jwt_token(self, email: str, jwt_token: str) -> None:
        """Store JWT token securely using keyring"""
        try:
            keyring.set_password(self.SERVICE_NAME, f"jwt_{email}", jwt_token)
        except Exception as e:
            # Fallback to config file if keyring fails
            print(f"Warning: Could not store JWT token securely: {e}")
            config = self._load_user_config() or {}
            config['jwt_token_fallback'] = jwt_token
            self._store_user_config(config)
    
    def _get_api_key(self, email: str) -> Optional[str]:
        """Retrieve API key securely"""
        try:
            return keyring.get_password(self.SERVICE_NAME, email)
        except Exception:
            # Fallback to config file
            config = self._load_user_config()
            return config.get('api_key_fallback') if config else None
    
    def _get_jwt_token(self, email: str) -> Optional[str]:
        """Retrieve JWT token securely"""
        try:
            return keyring.get_password(self.SERVICE_NAME, f"jwt_{email}")
        except Exception:
            # Fallback to config file
            config = self._load_user_config()
            return config.get('jwt_token_fallback') if config else None
    
    def list_api_keys(self) -> Dict:
        """List all API keys for the current user using JWT authentication"""
        config = self._load_user_config()
        if not config or not config.get('email'):
            raise AuthenticationError("Not logged in")
        
        email = config['email']
        jwt_token = self._get_jwt_token(email)
        
        if not jwt_token:
            raise AuthenticationError("No valid session. Please login again.")
        
        try:
            response = self._make_jwt_request('GET', '/api/auth/keys', jwt_token)
            if response.get('success'):
                return response  # Return full response with 'keys', 'success', 'total'
            else:
                raise AuthenticationError(response.get('error', 'Failed to list API keys'))
        except Exception as e:
            raise AuthenticationError(f"Failed to list API keys: {str(e)}")
    
    def switch_api_key(self, key_id: int = None) -> str:
        """
        Switch to use a specific API key for nutrition calls
        
        Args:
            key_id: ID of the key to switch to. If None, will show interactive selection.
            
        Returns:
            The full API key value that can be used for nutrition calls
            
        Example:
            # Interactive selection
            api_key = auth.switch_api_key()
            
            # Direct key ID
            api_key = auth.switch_api_key(123)
        """
        try:
            config = self._load_user_config()
            if not config or not config.get('email'):
                raise AuthenticationError("Not logged in. Please login first.")
            
            jwt_token = self._get_jwt_token(config['email'])
            if not jwt_token:
                raise AuthenticationError("JWT token not found. Please login again.")
            
            # If no key_id provided, user needs to select from available keys
            if key_id is None:
                keys_response = self.list_api_keys()
                keys = keys_response.get('keys', [])
                
                if not keys:
                    raise AuthenticationError("No API keys found. Please create an API key first.")
                
                print("Available API keys:")
                for i, key in enumerate(keys, 1):
                    status = "🟢 ACTIVE" if key.get('is_active') else "🔴 INACTIVE"
                    usage = key.get('usage', {})
                    usage_str = f"{usage.get('current_month', 0)}/{usage.get('limit', 'unlimited')}"
                    
                    print(f"   [{i}] {key.get('key_name', 'Unnamed')}: {key.get('api_key', 'N/A')} ({status}) Usage: {usage_str}")
                
                while True:
                    try:
                        choice = input("Select an API key (enter number): ").strip()
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(keys):
                            key_id = keys[choice_idx]['id']
                            break
                        else:
                            print(f"Please enter a number between 1 and {len(keys)}")
                    except (ValueError, KeyboardInterrupt):
                        raise AuthenticationError("API key selection cancelled")
            
            # Now reveal the full API key using the key_id
            response = self._make_jwt_request('POST', f'/api/auth/keys/{key_id}/reveal', jwt_token)
            
            if response.get('success'):
                full_api_key = response.get('api_key')
                key_name = response.get('key_name', 'Unknown')
                
                # Store the selected API key for future use
                config = self._load_user_config()
                config['selected_api_key'] = full_api_key
                config['selected_key_name'] = key_name
                config['selected_key_id'] = key_id
                self._store_user_config(config)
                
                print(f"✅ Switched to API key: {key_name}")
                return full_api_key
            else:
                raise AuthenticationError(response.get('error', 'Failed to reveal API key'))
                
        except Exception as e:
            raise AuthenticationError(f"Failed to switch API key: {str(e)}")
    
# Removed duplicate create_api_key method - using the one above with environment parameter
    
    def _make_jwt_request(self, method: str, endpoint: str, jwt_token: str, data: Dict = None):
        """Make authenticated request using JWT token"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, verify=False)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, verify=False)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Request failed: {str(e)}")
    
    def _store_user_config(self, config: Dict) -> None:
        """Store user configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _load_user_config(self) -> Optional[Dict]:
        """Load user configuration"""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None


# Global auth manager instance
_auth_manager = AuthManager()


def login(email: str = None, password: str = None, provider: str = "google", base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Login to Avocavo and store API key securely
    
    Args:
        email: Your email (for email/password login)
        password: Your password (for email/password login)
        provider: OAuth provider ("google" or "github") for browser login
        base_url: API base URL (defaults to production)
        
    Returns:
        Login result with user info
        
    Examples:
        import avocavo_nutrition as av
        
        # OAuth browser login (recommended)
        result = av.login()                    # Google OAuth (default)
        result = av.login(provider="google")   # Google OAuth (explicit)
        result = av.login(provider="github")   # GitHub OAuth
        
        # Email/password login (legacy)
        result = av.login("user@example.com", "password")
        
        if result['success']:
            print(f"Logged in as {result['email']}")
            
            # Now you can use the API without passing API key
            nutrition = av.analyze_ingredient("2 cups flour")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.login(email, password, provider)


def logout() -> Dict:
    """
    Logout and clear stored credentials
    
    Returns:
        Logout confirmation
        
    Example:
        result = av.logout()
        print(result['message'])  # "Successfully logged out"
    """
    return _auth_manager.logout()


def get_current_user() -> Optional[Dict]:
    """
    Get current logged-in user information
    
    Returns:
        User info dictionary or None if not logged in
        
    Example:
        user = av.get_current_user()
        if user:
            print(f"Logged in as: {user['email']}")
            print(f"Plan: {user['api_tier']}")
        else:
            print("Not logged in")
    """
    return _auth_manager.get_current_user()


def get_stored_api_key() -> Optional[str]:
    """
    Get stored API key for the current user
    
    Returns:
        API key or None if not logged in
    """
    return _auth_manager.get_api_key()


def is_logged_in() -> bool:
    """
    Check if user is currently logged in
    
    Returns:
        True if logged in, False otherwise
    """
    return _auth_manager.is_logged_in()


# For backwards compatibility with environment variables
def get_api_key_from_env() -> Optional[str]:
    """Get API key from environment variable"""
    return os.environ.get('AVOCAVO_API_KEY')


def get_api_key() -> Optional[str]:
    """
    Get API key from storage or environment
    Priority: logged-in user > environment variable
    """
    # First try logged-in user
    stored_key = get_stored_api_key()
    if stored_key:
        return stored_key
    
    # Fallback to environment variable
    return get_api_key_from_env()


def list_api_keys(base_url: str = "https://app.avocavo.app") -> Dict:
    """
    List all API keys for the authenticated user
    
    Args:
        base_url: API base URL
        
    Returns:
        Dictionary with list of API keys and usage information
        
    Example:
        keys = av.list_api_keys()
        for key in keys['keys']:
            print(f"{key['key_name']}: {key['monthly_usage']}/{key['monthly_limit']}")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.list_api_keys()


def switch_api_key(key_id: int = None, base_url: str = "https://app.avocavo.app") -> str:
    """
    Switch to use a specific API key for nutrition calls
    
    Args:
        key_id: ID of the key to switch to. If None, will show interactive selection.
        base_url: API base URL
        
    Returns:
        The full API key value that can be used for nutrition calls
        
    Example:
        import avocavo_nutrition as av
        
        # First login with OAuth
        av.login()
        
        # Interactive selection of API key
        av.switch_api_key()
        
        # Now nutrition calls will use the selected API key
        result = av.analyze_ingredient("1 cup rice")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.switch_api_key(key_id)


def create_api_key(name: str = "Python Package Key", description: str = None, environment: str = "development", base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Create a new API key and automatically switch to it
    
    Args:
        name: Name for the API key
        description: Optional description
        environment: Environment tag (development, staging, production)
        base_url: API base URL
        
    Returns:
        Dictionary with new API key information (full key shown only once)
        
    Example:
        import avocavo_nutrition as av
        
        # First login with OAuth
        av.login()
        
        # Create and switch to new API key
        result = av.create_api_key("My App Key", 
                                 description="API key for my application",
                                 environment="production")
        
        print(f"Created key: {result['key']['api_key']}")
        
        # Now you can use the nutrition API
        nutrition = av.analyze_ingredient("2 cups flour")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.create_api_key(name, description, environment)


def switch_to_api_key(api_key: str, base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Switch to using a specific API key
    
    Args:
        api_key: The API key to switch to
        base_url: API base URL
        
    Returns:
        Success confirmation
        
    Example:
        av.switch_to_api_key("sk_prod_abc123...")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.switch_to_api_key(api_key)


def delete_api_key(key_id: int, base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Delete (deactivate) an API key
    
    Args:
        key_id: ID of the key to delete
        base_url: API base URL
        
    Returns:
        Dictionary with deletion confirmation
        
    Example:
        av.delete_api_key(123)
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.delete_api_key(key_id)


if __name__ == "__main__":
    # Demo authentication
    print("🔐 Avocavo Nutrition API Authentication")
    print("=" * 40)
    
    user = get_current_user()
    if user:
        print(f"✅ Logged in as: {user['email']}")
        print(f"📊 Plan: {user['api_tier']}")
        print(f"🔑 API Key: {user.get('api_key', '')[:12]}...")
    else:
        print("❌ Not logged in")
        print("\nTo login:")
        print("  import avocavo_nutrition as av")
        print('  av.login("your@email.com", "password")')