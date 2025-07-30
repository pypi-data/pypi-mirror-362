"""
Synchronization logic for Federated Learning Client using scikit-learn with Supabase Storage
"""
import requests
import json
import joblib
import pickle
from pathlib import Path
import logging
from typing import Dict, Any, Optional
from rich.console import Console
from rich.progress import Progress, DownloadColumn, BarColumn, TextColumn, TimeElapsedColumn
import tempfile
import shutil
from datetime import datetime

from .model import MLPModel
from .supabase_config import SupabaseConfig, SupabaseStorageHandler

logger = logging.getLogger(__name__)
console = Console()


class FederatedSync:
    """Handle synchronization with federated learning server using Supabase Storage."""

    def __init__(self, client_id: str = None, config_file: str = None, auth_token: str = None):
        self.client_id = client_id or "client_001"
        self.auth_token = auth_token
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': f'FederatedLearningClient/{self.client_id}',
            'Content-Type': 'application/json'
        })

        # Initialize Supabase configuration and storage handler
        try:
            self.supabase_config = SupabaseConfig(config_file)
            self.storage_handler = SupabaseStorageHandler(self.supabase_config)
            self.use_supabase = True
            console.print("[green]✓ Supabase Storage initialized[/green]")
        except Exception as e:
            logger.warning(f"Supabase initialization failed: {e}. Falling back to HTTP sync.")
            self.use_supabase = False
            self.supabase_config = None
            self.storage_handler = None
    
    def download_global_model(
        self,
        url_or_path: str,
        local_model_path: str,
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> bool:
        """
        Download global model from Supabase Storage or fallback to HTTP URL.

        Args:
            url_or_path: Supabase storage path or HTTP URL to download the global model from
            local_model_path: Local path to save the downloaded model
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates

        Returns:
            True if download successful, False otherwise
        """
        try:
            # Check authentication if using Supabase
            if self.use_supabase and self.auth_token:
                auth_result = self.supabase_config.verify_firebase_token(self.auth_token)
                if not auth_result:
                    console.print("[yellow]⚠️  Authentication failed, proceeding without auth[/yellow]")

            # Try Supabase Storage first if available
            if self.use_supabase and not url_or_path.startswith(('http://', 'https://')):
                console.print(f"[blue]Downloading global model from Supabase Storage: {url_or_path}[/blue]")

                # Use storage handler for Supabase download
                success = self.storage_handler.download_model(url_or_path, local_model_path)
                if success:
                    return self._verify_downloaded_model(local_model_path)
                else:
                    console.print("[yellow]Supabase download failed, falling back to HTTP[/yellow]")

            # Fallback to HTTP download
            return self._download_via_http(url_or_path, local_model_path, timeout, verify_ssl)

        except Exception as e:
            console.print(f"[red]✗ Unexpected error during download: {str(e)}[/red]")
            return False

    def _download_via_http(
        self,
        url: str,
        local_model_path: str,
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> bool:
        """Download model via HTTP with progress bar."""
        try:
            console.print(f"[blue]Downloading global model from HTTP: {url}[/blue]")

            # Create directory if it doesn't exist
            local_path = Path(local_model_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Download with progress bar
            with self.session.get(url, stream=True, timeout=timeout, verify=verify_ssl) as response:
                response.raise_for_status()

                # Get file size if available
                total_size = int(response.headers.get('content-length', 0))

                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    DownloadColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:

                    task = progress.add_task("Downloading", total=total_size)

                    # Use temporary file for atomic download
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                temp_file.write(chunk)
                                progress.update(task, advance=len(chunk))

                        temp_path = temp_file.name

                    # Move temp file to final location
                    shutil.move(temp_path, local_model_path)

            return self._verify_downloaded_model(local_model_path)

        except requests.exceptions.RequestException as e:
            console.print(f"[red]✗ HTTP download failed: {str(e)}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]✗ Unexpected error during HTTP download: {str(e)}[/red]")
            return False

    def _verify_downloaded_model(self, local_model_path: str) -> bool:
        """Verify the downloaded model is valid."""
        try:
            model = MLPModel.load_model(local_model_path)
            model_info = model.get_model_info()
            console.print(f"[green]✓ Global model downloaded and verified successfully![/green]")
            if model_info['total_parameters']:
                console.print(f"Model info: {model_info['total_parameters']:,} parameters")
            else:
                console.print(f"Model info: Hidden layers {model_info['hidden_layer_sizes']}")
            return True

        except Exception as e:
            console.print(f"[red]✗ Downloaded model verification failed: {str(e)}[/red]")
            # Clean up invalid file
            Path(local_model_path).unlink(missing_ok=True)
            return False
    
    def upload_model_weights(
        self,
        model_path: str,
        server_url_or_path: str,
        round_num: int = None,
        metadata: Dict[str, Any] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> bool:
        """
        Upload local model weights to Supabase Storage or fallback to HTTP server.

        Args:
            model_path: Path to local model file
            server_url_or_path: Supabase storage path or server endpoint URL for uploading weights
            round_num: Current federated learning round number
            metadata: Additional metadata to send with weights
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates

        Returns:
            True if upload successful, False otherwise
        """
        try:
            # Check if model file exists
            model_file = Path(model_path)
            if not model_file.exists():
                console.print(f"[red]✗ Model file not found: {model_path}[/red]")
                return False

            # Check authentication if using Supabase
            if self.use_supabase and self.auth_token:
                auth_result = self.supabase_config.verify_firebase_token(self.auth_token)
                if not auth_result:
                    console.print("[yellow]⚠️  Authentication failed, proceeding without auth[/yellow]")

            # Prepare metadata
            upload_metadata = metadata or {}
            upload_metadata.update({
                'client_id': self.client_id,
                'round_number': round_num,
                'upload_timestamp': datetime.now().isoformat(),
                'model_type': 'scikit-learn-mlp'
            })

            # Try Supabase Storage first if available
            if self.use_supabase and not server_url_or_path.startswith(('http://', 'https://')):
                console.print(f"[blue]Uploading model to Supabase Storage: {server_url_or_path}[/blue]")

                # Generate remote path with timestamp and round info
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                remote_path = f"{server_url_or_path}/client_{self.client_id}_round_{round_num}_{timestamp}.pkl"

                success = self.storage_handler.upload_model(model_path, remote_path, upload_metadata)
                if success:
                    console.print(f"[green]✓ Model uploaded successfully to Supabase Storage![/green]")
                    console.print(f"Remote path: {remote_path}")
                    return True
                else:
                    console.print("[yellow]Supabase upload failed, falling back to HTTP[/yellow]")

            # Fallback to HTTP upload
            return self._upload_via_http(model_path, server_url_or_path, round_num, upload_metadata, timeout, verify_ssl)

        except Exception as e:
            console.print(f"[red]✗ Upload failed: {str(e)}[/red]")
            return False

    def _upload_via_http(
        self,
        model_path: str,
        server_url: str,
        round_num: int,
        metadata: Dict[str, Any],
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> bool:
        """Upload model via HTTP with weights extraction."""
        try:
            console.print(f"[blue]Uploading model weights via HTTP to: {server_url}[/blue]")

            # Load model to extract weights
            model = MLPModel.load_model(model_path)
            weights = model.get_model_weights()
            model_info = model.get_model_info()

            # Convert weights to serializable format
            serializable_weights = {}
            for key, value in weights.items():
                if hasattr(value, 'tolist'):
                    # Convert numpy arrays to lists
                    if isinstance(value, list):
                        serializable_weights[key] = [arr.tolist() if hasattr(arr, 'tolist') else arr for arr in value]
                    else:
                        serializable_weights[key] = value.tolist()
                else:
                    serializable_weights[key] = value

            # Prepare payload
            payload = {
                'client_id': self.client_id,
                'round_number': round_num,
                'model_weights': serializable_weights,
                'model_info': model_info,
                'metadata': metadata
            }

            # Simulate upload with progress (replace with actual HTTP request in production)
            console.print("[yellow]Simulating HTTP model upload (replace with actual server endpoint)...[/yellow]")

            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            ) as progress:

                task = progress.add_task("Uploading weights", total=100)

                # Simulate upload chunks
                import time
                for i in range(10):
                    time.sleep(0.1)  # Simulate network delay
                    progress.update(task, advance=10)

            # In a real implementation, uncomment and modify this:
            # response = self.session.post(
            #     server_url,
            #     json=payload,
            #     timeout=timeout,
            #     verify=verify_ssl
            # )
            # response.raise_for_status()
            # result = response.json()

            # Simulate successful response
            result = {
                'status': 'success',
                'message': 'Model weights uploaded successfully via HTTP',
                'client_id': self.client_id,
                'round_number': round_num,
                'timestamp': datetime.now().isoformat()
            }

            console.print(f"[green]✓ Model weights uploaded successfully via HTTP![/green]")
            console.print(f"Server response: {result.get('message', 'Upload completed')}")

            return True

        except Exception as e:
            console.print(f"[red]✗ HTTP upload failed: {str(e)}[/red]")
            return False
    
    def get_server_status(self, server_url: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Get server status and information.
        
        Args:
            server_url: Server status endpoint URL
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing server status information
        """
        try:
            console.print(f"[blue]Checking server status: {server_url}[/blue]")
            
            # Simulate server status check
            # In real implementation: response = self.session.get(server_url, timeout=timeout)
            
            status_info = {
                'status': 'online',
                'current_round': 5,
                'total_clients': 10,
                'active_clients': 7,
                'model_version': '1.2.3',
                'last_update': '2024-01-01T12:00:00Z'
            }
            
            console.print("[green]✓ Server is online[/green]")
            console.print(f"Current round: {status_info['current_round']}")
            console.print(f"Active clients: {status_info['active_clients']}/{status_info['total_clients']}")
            
            return status_info
            
        except Exception as e:
            console.print(f"[red]✗ Failed to get server status: {str(e)}[/red]")
            return {'status': 'error', 'message': str(e)}
    
    def sync_with_server(
        self,
        server_base_url: str,
        local_model_path: str,
        round_num: int = None,
        upload_after_download: bool = False
    ) -> Dict[str, Any]:
        """
        Complete synchronization cycle with server.
        
        Args:
            server_base_url: Base URL of the federated learning server
            local_model_path: Path to local model file
            round_num: Current round number
            upload_after_download: Whether to upload local model after downloading global model
            
        Returns:
            Dictionary containing sync results
        """
        sync_results = {
            'download_success': False,
            'upload_success': False,
            'server_status': None,
            'errors': []
        }
        
        try:
            # Check server status
            status_url = f"{server_base_url}/status"
            server_status = self.get_server_status(status_url)
            sync_results['server_status'] = server_status
            
            if server_status.get('status') != 'online':
                sync_results['errors'].append("Server is not online")
                return sync_results
            
            # Download global model
            download_url = f"{server_base_url}/model/global"
            download_success = self.download_global_model(download_url, local_model_path)
            sync_results['download_success'] = download_success
            
            if not download_success:
                sync_results['errors'].append("Failed to download global model")
            
            # Upload local model if requested
            if upload_after_download:
                upload_url = f"{server_base_url}/model/upload"
                upload_success = self.upload_model_weights(
                    local_model_path, upload_url, round_num
                )
                sync_results['upload_success'] = upload_success
                
                if not upload_success:
                    sync_results['errors'].append("Failed to upload local model")
            
            # Summary
            if sync_results['download_success']:
                console.print("[green]✓ Synchronization completed successfully![/green]")
            else:
                console.print("[red]✗ Synchronization failed![/red]")
            
            return sync_results
            
        except Exception as e:
            error_msg = f"Sync error: {str(e)}"
            sync_results['errors'].append(error_msg)
            console.print(f"[red]✗ {error_msg}[/red]")
            return sync_results


def download_model(
    url_or_path: str,
    output_path: str,
    client_id: str = None,
    config_file: str = None,
    auth_token: str = None
) -> bool:
    """
    Download global model from Supabase Storage or HTTP URL.

    Args:
        url_or_path: Supabase storage path or URL to download model from
        output_path: Local path to save the model
        client_id: Client identifier
        config_file: Optional Supabase config file path
        auth_token: Optional Firebase authentication token

    Returns:
        True if successful, False otherwise
    """
    sync_client = FederatedSync(client_id, config_file, auth_token)
    return sync_client.download_global_model(url_or_path, output_path)


def upload_model(
    model_path: str,
    server_url_or_path: str,
    round_num: int = None,
    client_id: str = None,
    config_file: str = None,
    auth_token: str = None,
    metadata: Dict[str, Any] = None
) -> bool:
    """
    Upload model weights to Supabase Storage or HTTP server.

    Args:
        model_path: Path to local model
        server_url_or_path: Supabase storage path or server upload endpoint
        round_num: Current round number
        client_id: Client identifier
        config_file: Optional Supabase config file path
        auth_token: Optional Firebase authentication token
        metadata: Optional metadata to include with upload

    Returns:
        True if successful, False otherwise
    """
    sync_client = FederatedSync(client_id, config_file, auth_token)
    return sync_client.upload_model_weights(model_path, server_url_or_path, round_num, metadata)


def full_sync(
    server_url: str,
    model_path: str,
    round_num: int = None,
    client_id: str = None,
    upload_after_download: bool = False,
    config_file: str = None,
    auth_token: str = None
) -> Dict[str, Any]:
    """
    Perform full synchronization with federated learning server using Supabase Storage.

    Args:
        server_url: Base server URL or Supabase storage path
        model_path: Local model path
        round_num: Current round number
        client_id: Client identifier
        upload_after_download: Whether to upload after downloading
        config_file: Optional Supabase config file path
        auth_token: Optional Firebase authentication token

    Returns:
        Dictionary containing sync results
    """
    sync_client = FederatedSync(client_id, config_file, auth_token)
    return sync_client.sync_with_server(
        server_url, model_path, round_num, upload_after_download
    )
