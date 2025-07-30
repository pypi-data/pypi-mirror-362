"""
Training logic for Federated Learning Client using scikit-learn
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path
import logging
from typing import Tuple, Optional, Dict, Any
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Console
import time

from .model import MLPModel

logger = logging.getLogger(__name__)
console = Console()


class DataPreprocessor:
    """Handle data preprocessing for federated learning."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = None
        self.target_column = None
    
    def preprocess_data(self, data_path: str, target_column: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess CSV data for training.

        Args:
            data_path: Path to CSV file
            target_column: Name of target column (if None, assumes last column)

        Returns:
            Tuple of (features, labels) as numpy arrays
        """
        # Load data
        df = pd.read_csv(data_path)
        console.print(f"[green]Loaded data with shape: {df.shape}[/green]")

        # Handle missing values
        # For numeric columns, fill with mean
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

        # For categorical columns, fill with mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'unknown')

        # Determine target column
        if target_column is None:
            target_column = df.columns[-1]

        self.target_column = target_column

        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Store feature columns
        self.feature_columns = X.columns.tolist()

        # Encode categorical features
        for col in X.columns:
            if X[col].dtype == 'object':
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))

        # Normalize features
        X_scaled = self.scaler.fit_transform(X)

        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        console.print(f"[green]Preprocessed data: {X_scaled.shape[1]} features, {len(np.unique(y_encoded))} classes[/green]")

        return X_scaled, y_encoded
    
    def get_input_size(self) -> int:
        """Get the number of input features."""
        return len(self.feature_columns) if self.feature_columns else 0


class FederatedTrainer:
    """Handle federated learning training process using scikit-learn."""

    def __init__(self, model: MLPModel):
        self.model = model
        self.training_history = []
    
    def train_local_epochs(
        self,
        X: np.ndarray,
        y: np.ndarray,
        max_iter: int = 1000,
        validation_split: float = 0.2
    ) -> Dict[str, Any]:
        """
        Train model using scikit-learn MLPClassifier.

        Args:
            X: Feature array
            y: Label array
            max_iter: Maximum number of iterations for training
            validation_split: Fraction of data to use for validation

        Returns:
            Dictionary containing training metrics
        """
        start_time = time.time()

        # Split data into train/validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42, stratify=y
        )

        console.print(f"[blue]Training set: {X_train.shape[0]} samples[/blue]")
        console.print(f"[blue]Validation set: {X_val.shape[0]} samples[/blue]")

        # Update model max_iter if different
        if self.model.max_iter != max_iter:
            self.model.max_iter = max_iter
            self.model.model.max_iter = max_iter

        # Training with progress indication
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            task = progress.add_task(f"Training MLP (max_iter={max_iter})", total=None)

            # Fit the model
            self.model.fit(X_train, y_train)

            progress.update(task, completed=True)

        # Calculate training time
        training_time = time.time() - start_time

        # Evaluate on training and validation sets
        train_predictions = self.model.predict(X_train)
        val_predictions = self.model.predict(X_val)

        train_accuracy = accuracy_score(y_train, train_predictions)
        val_accuracy = accuracy_score(y_val, val_predictions)

        # Get training history from the model
        training_history = self.model.get_training_history()

        # Store training metrics
        training_metrics = {
            'max_iter': max_iter,
            'actual_iterations': training_history.get('n_iter', max_iter),
            'converged': training_history.get('converged', False),
            'training_time': training_time,
            'train_accuracy': train_accuracy,
            'val_accuracy': val_accuracy,
            'final_train_accuracy': train_accuracy,
            'final_val_accuracy': val_accuracy,
            'loss_curve': training_history.get('loss_curve', []),
            'validation_scores': training_history.get('validation_scores', []),
            'best_loss': training_history.get('best_loss', None),
            'best_validation_score': training_history.get('best_validation_score', None)
        }

        self.training_history.append(training_metrics)

        # Display results
        console.print(f"[green]Training completed![/green]")
        console.print(f"Training accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        console.print(f"Validation accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
        console.print(f"Iterations: {training_metrics['actual_iterations']}/{max_iter}")
        console.print(f"Converged: {training_metrics['converged']}")
        console.print(f"Training time: {training_time:.2f} seconds")

        return training_metrics
    
    def save_training_log(self, log_path: str, round_num: int = None):
        """
        Save training history to log file.

        Args:
            log_path: Path to save log file
            round_num: Round number for federated learning
        """
        log_path = Path(log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(log_path, 'a') as f:
            for i, metrics in enumerate(self.training_history):
                round_info = f"Round {round_num}, " if round_num is not None else ""
                f.write(
                    f"{round_info}Training Session {i+1}: "
                    f"Max_iter={metrics['max_iter']}, "
                    f"Actual_iter={metrics['actual_iterations']}, "
                    f"Train Acc={metrics['train_accuracy']:.4f}, "
                    f"Val Acc={metrics['val_accuracy']:.4f}, "
                    f"Converged={metrics['converged']}\n"
                )


def train_model(
    data_path: str,
    model_save_path: str,
    max_iter: int = 1000,
    hidden_layer_sizes: tuple = (64, 32),
    target_column: str = None,
    log_path: str = None,
    round_num: int = None
) -> Dict[str, Any]:
    """
    Main training function for federated learning client using scikit-learn.

    Args:
        data_path: Path to training CSV file
        model_save_path: Path to save trained model
        max_iter: Maximum number of iterations for training
        hidden_layer_sizes: Tuple of hidden layer sizes
        target_column: Name of target column
        log_path: Path to save training log
        round_num: Round number for federated learning

    Returns:
        Dictionary containing training results
    """
    console.print(f"[blue]Starting federated learning training[/blue]")

    # Preprocess data
    preprocessor = DataPreprocessor()
    X, y = preprocessor.preprocess_data(data_path, target_column)

    # Create or load model
    model_path = Path(model_save_path)
    if model_path.exists():
        console.print(f"[yellow]Loading existing model from {model_save_path}[/yellow]")
        model = MLPModel.load_model(model_save_path)
        # Update max_iter if different
        if model.max_iter != max_iter:
            model.max_iter = max_iter
            model.model.max_iter = max_iter
    else:
        console.print("[blue]Creating new model[/blue]")
        model = MLPModel(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter)

    # Train model
    trainer = FederatedTrainer(model)
    training_metrics = trainer.train_local_epochs(X, y, max_iter=max_iter)

    # Save model
    model.save_model(model_save_path)
    console.print(f"[green]Model saved to {model_save_path}[/green]")

    # Save training log
    if log_path:
        trainer.save_training_log(log_path, round_num)
        console.print(f"[green]Training log saved to {log_path}[/green]")

    return {
        'training_metrics': training_metrics,
        'model_info': model.get_model_info(),
        'data_shape': X.shape,
        'num_classes': len(np.unique(y)),
        'feature_count': X.shape[1]
    }
