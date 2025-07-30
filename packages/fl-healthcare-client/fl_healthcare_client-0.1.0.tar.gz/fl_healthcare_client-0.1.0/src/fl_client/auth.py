"""
Firebase Authentication module for Federated Learning CLI Client
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import getpass
from rich.console import Console
from rich.prompt import Prompt, Confirm
import requests

logger = logging.getLogger(__name__)
console = Console()


class FirebaseAuth:
    """Handle Firebase Authentication for CLI client."""
    
    def __init__(self, config_file: str = None):
        """
        Initialize Firebase Authentication.
        
        Args:
            config_file: Optional path to Firebase config file
        """
        self.config_file = config_file or "firebase_config.json"
        self.firebase_config = None
        self.auth_token = None
        self.user_info = None
        self.token_file = Path.home() / ".federated_client" / "auth_token.json"
        
        self._load_config()
    
    def _load_config(self):
        """Load Firebase configuration."""
        # Try to load from config file
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    self.firebase_config = json.load(f)
                logger.info(f"Firebase config loaded from {self.config_file}")
            except Exception as e:
                logger.warning(f"Failed to load Firebase config: {e}")
        
        # Try environment variables
        if not self.firebase_config:
            env_config = {
                "apiKey": os.getenv('FIREBASE_API_KEY'),
                "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
                "projectId": os.getenv('FIREBASE_PROJECT_ID'),
            }
            
            if all(env_config.values()):
                self.firebase_config = env_config
                logger.info("Firebase config loaded from environment variables")
        
        if not self.firebase_config:
            logger.warning("Firebase configuration not found. Authentication will be limited.")
    
    def authenticate_with_email_password(self, email: str = None, password: str = None) -> bool:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email (will prompt if not provided)
            password: User password (will prompt if not provided)
            
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            if not self.firebase_config:
                console.print("[red]❌ Firebase configuration not available[/red]")
                return False
            
            # Get credentials if not provided
            if not email:
                email = Prompt.ask("Enter your email")
            
            if not password:
                password = getpass.getpass("Enter your password: ")
            
            console.print("[blue]🔐 Authenticating with Firebase...[/blue]")
            
            # Firebase REST API authentication
            auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            
            params = {
                "key": self.firebase_config["apiKey"]
            }
            
            response = requests.post(auth_url, json=payload, params=params)
            
            if response.status_code == 200:
                auth_data = response.json()
                self.auth_token = auth_data.get("idToken")
                self.user_info = {
                    "email": auth_data.get("email"),
                    "localId": auth_data.get("localId"),
                    "displayName": auth_data.get("displayName", ""),
                    "refreshToken": auth_data.get("refreshToken")
                }
                
                # Save token for future use
                self._save_token()
                
                console.print(f"[green]✅ Authentication successful! Welcome, {self.user_info['email']}[/green]")
                return True
            else:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "Authentication failed")
                console.print(f"[red]❌ Authentication failed: {error_message}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]❌ Authentication error: {str(e)}[/red]")
            logger.error(f"Authentication error: {e}")
            return False
    
    def load_saved_token(self) -> bool:
        """
        Load previously saved authentication token.
        
        Returns:
            True if token loaded and valid, False otherwise
        """
        try:
            if not self.token_file.exists():
                return False
            
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            
            self.auth_token = token_data.get("idToken")
            self.user_info = token_data.get("userInfo")
            
            if self.auth_token and self._verify_token():
                console.print(f"[green]✅ Loaded saved authentication for {self.user_info['email']}[/green]")
                return True
            else:
                # Token is invalid, remove it
                self.token_file.unlink(missing_ok=True)
                self.auth_token = None
                self.user_info = None
                return False
                
        except Exception as e:
            logger.warning(f"Failed to load saved token: {e}")
            return False
    
    def _verify_token(self) -> bool:
        """Verify if the current token is valid."""
        try:
            if not self.auth_token or not self.firebase_config:
                return False
            
            # Verify token with Firebase
            verify_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup"
            
            payload = {
                "idToken": self.auth_token
            }
            
            params = {
                "key": self.firebase_config["apiKey"]
            }
            
            response = requests.post(verify_url, json=payload, params=params)
            return response.status_code == 200
            
        except Exception as e:
            logger.warning(f"Token verification failed: {e}")
            return False
    
    def _save_token(self):
        """Save authentication token to file."""
        try:
            # Create directory if it doesn't exist
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            
            token_data = {
                "idToken": self.auth_token,
                "userInfo": self.user_info
            }
            
            with open(self.token_file, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            # Set restrictive permissions
            self.token_file.chmod(0o600)
            
        except Exception as e:
            logger.warning(f"Failed to save token: {e}")
    
    def logout(self):
        """Logout user and clear saved token."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            
            self.auth_token = None
            self.user_info = None
            
            console.print("[green]✅ Logged out successfully[/green]")
            
        except Exception as e:
            logger.warning(f"Logout error: {e}")
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return self.auth_token is not None and self._verify_token()
    
    def get_auth_token(self) -> Optional[str]:
        """Get current authentication token."""
        return self.auth_token
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information."""
        return self.user_info
    
    def require_authentication(self, allow_skip: bool = False) -> bool:
        """
        Ensure user is authenticated, prompt if necessary.
        
        Args:
            allow_skip: Whether to allow skipping authentication
            
        Returns:
            True if authenticated or skipped, False otherwise
        """
        # Try to load saved token first
        if self.load_saved_token():
            return True
        
        # Check if authentication is available
        if not self.firebase_config:
            if allow_skip:
                console.print("[yellow]⚠️  Firebase not configured. Proceeding without authentication.[/yellow]")
                return True
            else:
                console.print("[red]❌ Firebase authentication required but not configured[/red]")
                return False
        
        # Prompt for authentication
        console.print("[yellow]🔐 Authentication required for secure operations[/yellow]")
        
        if allow_skip:
            if not Confirm.ask("Do you want to authenticate now?", default=True):
                console.print("[yellow]⚠️  Proceeding without authentication[/yellow]")
                return True
        
        # Attempt authentication
        return self.authenticate_with_email_password()
    
    def create_example_config(self, output_path: str = "firebase_config.example.json"):
        """Create an example Firebase configuration file."""
        example_config = {
            "apiKey": "your-firebase-api-key",
            "authDomain": "your-project.firebaseapp.com",
            "projectId": "your-firebase-project-id",
            "storageBucket": "your-project.appspot.com",
            "messagingSenderId": "123456789",
            "appId": "1:123456789:web:abcdef123456"
        }
        
        with open(output_path, 'w') as f:
            json.dump(example_config, f, indent=2)
        
        console.print(f"[green]Example Firebase configuration created at: {output_path}[/green]")
        console.print("[yellow]Please update with your actual Firebase project configuration.[/yellow]")


def get_authenticated_session(config_file: str = None, require_auth: bool = False) -> Optional[FirebaseAuth]:
    """
    Get an authenticated Firebase session.
    
    Args:
        config_file: Optional Firebase config file path
        require_auth: Whether authentication is required
        
    Returns:
        FirebaseAuth instance if successful, None otherwise
    """
    try:
        auth = FirebaseAuth(config_file)
        
        if require_auth:
            if not auth.require_authentication(allow_skip=False):
                return None
        else:
            auth.require_authentication(allow_skip=True)
        
        return auth
        
    except Exception as e:
        logger.error(f"Failed to get authenticated session: {e}")
        return None
