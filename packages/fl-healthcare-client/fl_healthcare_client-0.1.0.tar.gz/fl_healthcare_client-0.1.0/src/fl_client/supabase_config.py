"""
Supabase Configuration and Storage Handler for Federated Learning Client
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from supabase import create_client, Client
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
from rich.console import Console

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)
console = Console()


class SupabaseConfig:
    """Configuration handler for Supabase integration."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize Supabase configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file or "supabase_config.json"
        self.supabase_url = None
        self.supabase_key = None
        self.storage_bucket = None
        self.firebase_config = None
        self._supabase_client = None
        self._firebase_app = None
        
        self._load_config()
        self._init_supabase()
        self._init_firebase()
    
    def _load_config(self):
        """Load configuration from environment variables and config file."""
        # Try environment variables first
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.storage_bucket = os.getenv('SUPABASE_STORAGE_BUCKET', 'federated-models')
        
        # Load from config file if available
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                
                supabase_config = config_data.get('supabase', {})
                self.supabase_url = self.supabase_url or supabase_config.get('url')
                self.supabase_key = self.supabase_key or supabase_config.get('anon_key')
                self.storage_bucket = self.storage_bucket or supabase_config.get('storage_bucket', 'federated-models')
                
                # Firebase configuration
                self.firebase_config = config_data.get('firebase', {})
                
            except Exception as e:
                logger.warning(f"Failed to load config file {self.config_file}: {e}")
        
        # Validate required configuration
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase configuration missing. Please set SUPABASE_URL and SUPABASE_ANON_KEY "
                "environment variables or provide them in the config file."
            )
    
    def _init_supabase(self):
        """Initialize Supabase client."""
        try:
            self._supabase_client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    def _init_firebase(self):
        """Initialize Firebase Admin SDK for authentication."""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to load Firebase service account key
                firebase_key_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
                if firebase_key_path and Path(firebase_key_path).exists():
                    cred = credentials.Certificate(firebase_key_path)
                    self._firebase_app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized with service account")
                elif self.firebase_config:
                    # Use config from file
                    cred = credentials.Certificate(self.firebase_config)
                    self._firebase_app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK initialized from config file")
                else:
                    logger.warning("Firebase configuration not found. Authentication features will be limited.")
            else:
                self._firebase_app = firebase_admin.get_app()
                logger.info("Using existing Firebase app")
                
        except Exception as e:
            logger.warning(f"Firebase initialization failed: {e}. Authentication features will be limited.")
    
    @property
    def supabase(self) -> Client:
        """Get Supabase client instance."""
        if not self._supabase_client:
            raise RuntimeError("Supabase client not initialized")
        return self._supabase_client
    
    def verify_firebase_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token.
        
        Args:
            id_token: Firebase ID token to verify
            
        Returns:
            Decoded token data if valid, None otherwise
        """
        try:
            if not self._firebase_app:
                logger.warning("Firebase not initialized, cannot verify token")
                return None
            
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            return None
    
    def create_example_config(self, output_path: str = "supabase_config.example.json"):
        """Create an example configuration file."""
        example_config = {
            "supabase": {
                "url": "https://your-project.supabase.co",
                "anon_key": "your-anon-key-here",
                "storage_bucket": "federated-models"
            },
            "firebase": {
                "type": "service_account",
                "project_id": "your-firebase-project-id",
                "private_key_id": "your-private-key-id",
                "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
                "client_id": "your-client-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"
            },
            "federated_learning": {
                "client_id": "hospital_client_001",
                "model_storage_path": "models/global",
                "default_timeout": 30
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(example_config, f, indent=2)
        
        console.print(f"[green]Example configuration created at: {output_path}[/green]")
        console.print("[yellow]Please update the configuration with your actual Supabase and Firebase credentials.[/yellow]")


class SupabaseStorageHandler:
    """Handle Supabase Storage operations for federated learning models."""
    
    def __init__(self, config: SupabaseConfig):
        """
        Initialize storage handler.
        
        Args:
            config: SupabaseConfig instance
        """
        self.config = config
        self.supabase = config.supabase
        self.bucket_name = config.storage_bucket
    
    def upload_model(
        self,
        local_file_path: str,
        remote_file_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Upload model file to Supabase Storage.
        
        Args:
            local_file_path: Path to local model file
            remote_file_path: Remote path in storage bucket
            metadata: Optional metadata to attach to the file
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            local_path = Path(local_file_path)
            if not local_path.exists():
                logger.error(f"Local file not found: {local_file_path}")
                return False
            
            console.print(f"[blue]Uploading model to Supabase Storage: {remote_file_path}[/blue]")
            
            # Read file content
            with open(local_path, 'rb') as f:
                file_content = f.read()
            
            # Upload to Supabase Storage
            response = self.supabase.storage.from_(self.bucket_name).upload(
                path=remote_file_path,
                file=file_content,
                file_options={
                    "content-type": "application/octet-stream",
                    "upsert": "true"  # String instead of boolean
                }
            )
            
            # Check if upload was successful
            if hasattr(response, 'status_code'):
                success = response.status_code == 200
            else:
                # For newer Supabase client, check if response exists and has no error
                success = response is not None and not hasattr(response, 'error')

            if success:
                console.print(f"[green]✓ Model uploaded successfully to: {remote_file_path}[/green]")

                # Add metadata if provided
                if metadata:
                    self._update_file_metadata(remote_file_path, metadata)

                return True
            else:
                error_msg = getattr(response, 'error', 'Unknown upload error')
                logger.error(f"Upload failed: {error_msg}")
                return False
                
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            console.print(f"[red]✗ Upload failed: {str(e)}[/red]")
            return False
    
    def download_model(
        self,
        remote_file_path: str,
        local_file_path: str,
        use_signed_url: bool = True
    ) -> bool:
        """
        Download model file from Supabase Storage.
        
        Args:
            remote_file_path: Remote path in storage bucket
            local_file_path: Local path to save the file
            use_signed_url: Whether to use signed URL for download
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            console.print(f"[blue]Downloading model from Supabase Storage: {remote_file_path}[/blue]")
            
            # Create local directory if it doesn't exist
            local_path = Path(local_file_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            if use_signed_url:
                # Get signed URL for download
                response = self.supabase.storage.from_(self.bucket_name).create_signed_url(
                    path=remote_file_path,
                    expires_in=3600  # 1 hour
                )
                
                if 'signedURL' in response:
                    signed_url = response['signedURL']
                    
                    # Download using requests
                    import requests
                    download_response = requests.get(signed_url)
                    download_response.raise_for_status()
                    
                    with open(local_path, 'wb') as f:
                        f.write(download_response.content)
                else:
                    logger.error(f"Failed to get signed URL: {response}")
                    return False
            else:
                # Direct download
                response = self.supabase.storage.from_(self.bucket_name).download(remote_file_path)
                
                with open(local_path, 'wb') as f:
                    f.write(response)
            
            console.print(f"[green]✓ Model downloaded successfully to: {local_file_path}[/green]")
            return True
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            console.print(f"[red]✗ Download failed: {str(e)}[/red]")
            return False
    
    def list_models(self, path_prefix: str = "") -> list:
        """
        List available models in storage.
        
        Args:
            path_prefix: Optional path prefix to filter results
            
        Returns:
            List of file information dictionaries
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).list(path_prefix)
            return response
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def delete_model(self, remote_file_path: str) -> bool:
        """
        Delete model file from storage.
        
        Args:
            remote_file_path: Remote path of file to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            response = self.supabase.storage.from_(self.bucket_name).remove([remote_file_path])
            console.print(f"[green]✓ Model deleted: {remote_file_path}[/green]")
            return True
        except Exception as e:
            logger.error(f"Failed to delete model: {e}")
            console.print(f"[red]✗ Delete failed: {str(e)}[/red]")
            return False
    
    def _update_file_metadata(self, file_path: str, metadata: Dict[str, Any]):
        """Update file metadata (if supported by Supabase Storage)."""
        try:
            # Note: Supabase Storage metadata update might be limited
            # This is a placeholder for future metadata functionality
            logger.info(f"Metadata update requested for {file_path}: {metadata}")
        except Exception as e:
            logger.warning(f"Failed to update metadata: {e}")
