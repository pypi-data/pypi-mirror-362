#!/usr/bin/env python3
"""
Federated Learning Client CLI
Main entry point for the federated learning client application.
"""
import typer
from pathlib import Path
from typing import Optional
import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import sys

# Import our modules
from .train import train_model
from .evaluate import evaluate_model, compare_models
from .sync import download_model, upload_model, full_sync
from .auth import get_authenticated_session

# Setup
app = typer.Typer(
    name="federated-client",
    help="Federated Learning Client CLI - Train, evaluate, and sync ML models",
    rich_markup_mode="rich"
)
console = Console()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('federated_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print application banner."""
    banner = Text("🤖 Federated Learning Client", style="bold blue")
    subtitle = Text("Train, Evaluate, and Sync ML Models", style="italic cyan")
    
    panel_content = f"{banner}\n{subtitle}"
    console.print(Panel(panel_content, border_style="blue", padding=(1, 2)))


@app.command()
def train(
    data: str = typer.Argument(..., help="Path to training CSV file"),
    model: str = typer.Option("./models/local_model.pkl", "--model", "-m", help="Path to save/load model"),
    max_iter: int = typer.Option(1000, "--max-iter", "-i", help="Maximum number of training iterations"),
    hidden_layers: str = typer.Option("64,32", "--hidden", "-h", help="Hidden layer sizes (comma-separated)"),
    target_column: Optional[str] = typer.Option(None, "--target", "-t", help="Name of target column"),
    log_file: Optional[str] = typer.Option("./logs/training.log", "--log", "-l", help="Path to save training log"),
    round_num: Optional[int] = typer.Option(None, "--round-num", help="Federated learning round number")
):
    """
    Train MLP model locally on given CSV file using scikit-learn.

    Example:
        python cli.py train ./data/client1.csv --max-iter 1000 --model ./models/client1_model.pkl
    """
    print_banner()
    console.print(f"[bold green]🚀 Starting Local Training[/bold green]")
    console.print(f"Data: {data}")
    console.print(f"Model: {model}")
    console.print(f"Max Iterations: {max_iter}")

    # Parse hidden layers
    try:
        hidden_layer_sizes = tuple(map(int, hidden_layers.split(',')))
        console.print(f"Hidden Layers: {hidden_layer_sizes}")
    except ValueError:
        console.print(f"[red]❌ Error: Invalid hidden layers format. Use comma-separated integers (e.g., '64,32')[/red]")
        raise typer.Exit(1)

    try:
        # Validate input file
        if not Path(data).exists():
            console.print(f"[red]❌ Error: Data file not found: {data}[/red]")
            raise typer.Exit(1)

        # Train model
        results = train_model(
            data_path=data,
            model_save_path=model,
            max_iter=max_iter,
            hidden_layer_sizes=hidden_layer_sizes,
            target_column=target_column,
            log_path=log_file,
            round_num=round_num
        )

        # Display results summary
        metrics = results['training_metrics']
        console.print(f"\n[bold green]✅ Training Completed Successfully![/bold green]")
        console.print(f"Training Accuracy: {metrics['train_accuracy']:.4f} ({metrics['train_accuracy']*100:.2f}%)")
        console.print(f"Validation Accuracy: {metrics['val_accuracy']:.4f} ({metrics['val_accuracy']*100:.2f}%)")
        console.print(f"Iterations: {metrics['actual_iterations']}/{max_iter}")
        console.print(f"Converged: {metrics['converged']}")
        console.print(f"Model saved to: {model}")

        if log_file:
            console.print(f"Training log saved to: {log_file}")

    except Exception as e:
        console.print(f"[red]❌ Training failed: {str(e)}[/red]")
        logger.error(f"Training failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def evaluate(
    model: str = typer.Argument(..., help="Path to trained model file"),
    test_data: str = typer.Argument(..., help="Path to test CSV file"),
    target_column: Optional[str] = typer.Option(None, "--target", "-t", help="Name of target column"),
    save_results: bool = typer.Option(False, "--save", "-s", help="Save evaluation results to file"),
    results_path: Optional[str] = typer.Option("./results/evaluation_results.txt", "--output", "-o", help="Path to save results")
):
    """
    Evaluate trained model on test dataset.
    
    Example:
        python cli.py evaluate ./models/client1_model.pth ./data/test.csv --save
    """
    print_banner()
    console.print(f"[bold blue]📊 Starting Model Evaluation[/bold blue]")
    console.print(f"Model: {model}")
    console.print(f"Test Data: {test_data}")
    
    try:
        # Validate input files
        if not Path(model).exists():
            console.print(f"[red]❌ Error: Model file not found: {model}[/red]")
            raise typer.Exit(1)
        
        if not Path(test_data).exists():
            console.print(f"[red]❌ Error: Test data file not found: {test_data}[/red]")
            raise typer.Exit(1)
        
        # Evaluate model
        results = evaluate_model(
            model_path=model,
            test_data_path=test_data,
            target_column=target_column,
            save_results=save_results,
            results_path=results_path if save_results else None
        )
        
        # Display summary
        metrics = results['evaluation_metrics']
        console.print(f"\n[bold green]✅ Evaluation Completed![/bold green]")
        console.print(f"Test Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        console.print(f"Test Samples: {metrics['num_samples']:,}")
        
        if save_results:
            console.print(f"Results saved to: {results_path}")
        
    except Exception as e:
        console.print(f"[red]❌ Evaluation failed: {str(e)}[/red]")
        logger.error(f"Evaluation failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def sync(
    url_or_path: str = typer.Argument(..., help="HTTP URL or local path to download global model from"),
    model: str = typer.Option("./models/global_model.pkl", "--model", "-m", help="Local path to save downloaded model"),
    client_id: Optional[str] = typer.Option("client_001", "--client-id", "-c", help="Client identifier"),
    timeout: int = typer.Option(30, "--timeout", help="Download timeout in seconds")
):
    """
    Download the latest global model from HTTP URL or copy from local path.

    Examples:
        # Download from HTTP URL
        fl-client sync https://server.com/global_model.pkl

        # Copy from local path
        fl-client sync /path/to/shared/model.pkl
    """
    print_banner()
    console.print(f"[bold cyan]🔄 Syncing with Global Model[/bold cyan]")
    console.print(f"Source: {url_or_path}")
    console.print(f"Local Model Path: {model}")
    console.print(f"Client ID: {client_id}")

    try:
        # Download global model (no authentication required for downloads)
        success = download_model(url_or_path, model, client_id)

        if success:
            console.print(f"[bold green]✅ Global model downloaded successfully![/bold green]")
            console.print(f"Model saved to: {model}")
        else:
            console.print(f"[red]❌ Failed to download global model[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]❌ Sync failed: {str(e)}[/red]")
        logger.error(f"Sync failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def upload(
    model: str = typer.Argument(..., help="Path to local model file to upload"),
    server_url: str = typer.Argument(..., help="Server endpoint URL for uploading"),
    client_id: Optional[str] = typer.Option("client_001", "--client-id", "-c", help="Client identifier"),
    round_num: Optional[int] = typer.Option(None, "--round", "-r", help="Current federated learning round number"),
    timeout: int = typer.Option(30, "--timeout", help="Upload timeout in seconds"),
    firebase_config: Optional[str] = typer.Option(None, "--firebase-config", help="Firebase configuration file"),
    metadata: Optional[str] = typer.Option(None, "--metadata", help="JSON metadata to include with upload")
):
    """
    Upload local model weights to server endpoint (requires Firebase authentication).

    Examples:
        # Upload to HTTP server
        fl-client upload ./models/local_model.pkl https://server.com/upload --round 5
    """
    print_banner()
    console.print(f"[bold yellow]📤 Uploading Local Model[/bold yellow]")
    console.print(f"Model: {model}")
    console.print(f"Destination: {server_url}")
    console.print(f"Client ID: {client_id}")
    console.print(f"Round: {round_num}")

    try:
        # Validate model file
        if not Path(model).exists():
            console.print(f"[red]❌ Error: Model file not found: {model}[/red]")
            raise typer.Exit(1)

        # Parse metadata if provided
        upload_metadata = None
        if metadata:
            try:
                import json
                upload_metadata = json.loads(metadata)
            except json.JSONDecodeError:
                console.print(f"[red]❌ Error: Invalid JSON metadata: {metadata}[/red]")
                raise typer.Exit(1)

        # Authentication is required for uploads
        console.print("[yellow]🔐 Authentication required for model uploads[/yellow]")
        auth_session = get_authenticated_session(firebase_config, require_auth=True)
        if not auth_session or not auth_session.is_authenticated():
            console.print("[red]❌ Authentication failed. Please run 'fl-client login' first[/red]")
            raise typer.Exit(1)

        auth_token = auth_session.get_auth_token()
        console.print(f"[green]🔐 Authenticated as: {auth_session.get_user_info()['email']}[/green]")

        # Upload model
        success = upload_model(model, server_url, round_num, client_id, auth_token, upload_metadata)

        if success:
            console.print(f"[bold green]✅ Model uploaded successfully![/bold green]")
        else:
            console.print(f"[red]❌ Failed to upload model[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]❌ Upload failed: {str(e)}[/red]")
        logger.error(f"Upload failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def full_sync_cmd(
    server_url: str = typer.Argument(..., help="Base server URL for federated learning"),
    model: str = typer.Option("./models/federated_model.pkl", "--model", "-m", help="Local model path"),
    client_id: Optional[str] = typer.Option("client_001", "--client-id", "-c", help="Client identifier"),
    round_num: Optional[int] = typer.Option(None, "--round", "-r", help="Current round number"),
    upload_after: bool = typer.Option(False, "--upload-after", help="Upload local model after downloading global model")
):
    """
    Perform complete synchronization with federated learning server.
    
    Example:
        python cli.py full-sync https://federated-server.com --round 3 --upload-after
    """
    print_banner()
    console.print(f"[bold magenta]🔄 Full Synchronization[/bold magenta]")
    console.print(f"Server: {server_url}")
    console.print(f"Model: {model}")
    console.print(f"Client ID: {client_id}")
    console.print(f"Round: {round_num}")
    console.print(f"Upload After Download: {upload_after}")
    
    try:
        # Perform full sync
        results = full_sync(server_url, model, round_num, client_id, upload_after)
        
        # Display results
        if results['download_success']:
            console.print("[green]✅ Download: Success[/green]")
        else:
            console.print("[red]❌ Download: Failed[/red]")
        
        if upload_after:
            if results['upload_success']:
                console.print("[green]✅ Upload: Success[/green]")
            else:
                console.print("[red]❌ Upload: Failed[/red]")
        
        if results['errors']:
            console.print(f"[yellow]⚠️  Errors: {', '.join(results['errors'])}[/yellow]")
        
        if results['download_success'] and (not upload_after or results['upload_success']):
            console.print("[bold green]✅ Full synchronization completed successfully![/bold green]")
        else:
            console.print("[red]❌ Synchronization failed[/red]")
            raise typer.Exit(1)
        
    except Exception as e:
        console.print(f"[red]❌ Full sync failed: {str(e)}[/red]")
        logger.error(f"Full sync failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def compare(
    models: list[str] = typer.Argument(..., help="Paths to model files to compare"),
    test_data: str = typer.Option(..., "--test-data", "-d", help="Path to test CSV file"),
    target_column: Optional[str] = typer.Option(None, "--target", "-t", help="Name of target column")
):
    """
    Compare multiple models on the same test dataset.
    
    Example:
        python cli.py compare model1.pth model2.pth model3.pth --test-data ./data/test.csv
    """
    print_banner()
    console.print(f"[bold purple]📈 Comparing Models[/bold purple]")
    console.print(f"Models: {', '.join(models)}")
    console.print(f"Test Data: {test_data}")
    
    try:
        # Validate files
        for model_path in models:
            if not Path(model_path).exists():
                console.print(f"[red]❌ Error: Model file not found: {model_path}[/red]")
                raise typer.Exit(1)
        
        if not Path(test_data).exists():
            console.print(f"[red]❌ Error: Test data file not found: {test_data}[/red]")
            raise typer.Exit(1)
        
        # Compare models
        compare_models(models, test_data, target_column)

        console.print(f"[bold green]✅ Model comparison completed![/bold green]")
        console.print(f"Compared {len(models)} models on {test_data}")
        
    except Exception as e:
        console.print(f"[red]❌ Comparison failed: {str(e)}[/red]")
        logger.error(f"Comparison failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def login(
    firebase_config: Optional[str] = typer.Option(None, "--firebase-config", help="Firebase configuration file"),
    email: Optional[str] = typer.Option(None, "--email", help="Email address for authentication")
):
    """
    Authenticate with Firebase for secure operations.

    Example:
        python cli.py login --email user@example.com
    """
    print_banner()
    console.print(f"[bold blue]🔐 Firebase Authentication[/bold blue]")

    try:
        auth_session = get_authenticated_session(firebase_config, require_auth=False)
        if not auth_session:
            console.print("[red]❌ Failed to initialize authentication[/red]")
            raise typer.Exit(1)

        # Check if already authenticated
        if auth_session.is_authenticated():
            user_info = auth_session.get_user_info()
            console.print(f"[green]✅ Already authenticated as: {user_info['email']}[/green]")
            return

        # Authenticate
        success = auth_session.authenticate_with_email_password(email)
        if success:
            console.print("[green]✅ Authentication successful![/green]")
        else:
            console.print("[red]❌ Authentication failed[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]❌ Login failed: {str(e)}[/red]")
        logger.error(f"Login failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def logout():
    """
    Logout and clear saved authentication.

    Example:
        python cli.py logout
    """
    print_banner()
    console.print(f"[bold blue]🔓 Logout[/bold blue]")

    try:
        from auth import FirebaseAuth
        auth = FirebaseAuth()
        auth.logout()

    except Exception as e:
        console.print(f"[red]❌ Logout failed: {str(e)}[/red]")
        logger.error(f"Logout failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def setup_config():
    """
    Create example configuration files for Supabase and Firebase.

    Example:
        python cli.py setup-config
    """
    print_banner()
    console.print(f"[bold blue]⚙️  Setting up Configuration Files[/bold blue]")

    try:
        # Create example configuration files without initializing clients

        # Create Supabase config example
        supabase_example = {
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

        import json
        with open("supabase_config.example.json", 'w') as f:
            json.dump(supabase_example, f, indent=2)

        # Create Firebase config example
        firebase_example = {
            "apiKey": "your-firebase-api-key",
            "authDomain": "your-project.firebaseapp.com",
            "projectId": "your-firebase-project-id",
            "storageBucket": "your-project.appspot.com",
            "messagingSenderId": "123456789",
            "appId": "1:123456789:web:abcdef123456"
        }

        with open("firebase_config.example.json", 'w') as f:
            json.dump(firebase_example, f, indent=2)

        console.print(f"[green]✅ Example configuration created at: supabase_config.example.json[/green]")
        console.print(f"[green]✅ Example configuration created at: firebase_config.example.json[/green]")
        console.print("[yellow]Please update the configuration files with your actual Supabase and Firebase credentials.[/yellow]")

    except Exception as e:
        console.print(f"[red]❌ Setup failed: {str(e)}[/red]")
        logger.error(f"Setup failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def info():
    """Display information about the federated learning client."""
    print_banner()

    info_text = """
    [bold blue]Self-Contained Federated Learning Client[/bold blue]

    [green]✅ Works out-of-the-box - no external service setup required![/green]

    [cyan]Available Commands:[/cyan]
    • [green]train[/green]        - Train MLP model locally on CSV data
    • [green]evaluate[/green]     - Evaluate trained model on test dataset
    • [green]sync[/green]         - Download global model from HTTP URL or copy from local path
    • [green]upload[/green]       - Upload local model weights to server (requires Firebase auth)
    • [green]full-sync[/green]    - Complete sync cycle with server
    • [green]compare[/green]      - Compare multiple models on test data
    • [green]login[/green]        - Authenticate with Firebase (only needed for uploads)
    • [green]logout[/green]       - Clear saved authentication
    • [green]setup-config[/green] - Create example configuration files (optional)

    [cyan]Model Architecture:[/cyan]
    • Multi-Layer Perceptron (MLP) with scikit-learn
    • Configurable hidden layers with ReLU activation
    • Binary classification support
    • Automatic feature scaling and preprocessing

    [cyan]Data Processing:[/cyan]
    • CSV file support with pandas
    • Automatic missing value handling
    • Feature normalization with StandardScaler
    • Label encoding for categorical targets

    [cyan]Storage & Sync:[/cyan]
    • Local file storage and HTTP downloads (no external services required)
    • Firebase Authentication for uploads only (optional)
    • Works with any HTTP endpoint for model sync
    • Local model copying and sharing

    [cyan]Quick Start (No Setup Required):[/cyan]
    1. fl-client train ./data/sample.csv --rounds 10
    2. fl-client evaluate ./models/local_model.pkl ./data/test.csv
    3. fl-client sync https://server.com/model.pkl  # Download from HTTP
    4. fl-client sync /shared/path/model.pkl        # Copy from local path

    [yellow]For uploads only:[/yellow] fl-client login (requires Firebase config)

    For detailed help: fl-client [COMMAND] --help
    """

    console.print(Panel(info_text, border_style="blue", padding=(1, 2)))


def main():
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()
