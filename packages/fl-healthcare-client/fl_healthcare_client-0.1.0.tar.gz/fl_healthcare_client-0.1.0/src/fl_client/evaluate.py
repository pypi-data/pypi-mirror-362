"""
Evaluation logic for Federated Learning Client using scikit-learn
"""
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path
import logging
from typing import Dict, Any, Tuple, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .model import MLPModel
from .train import DataPreprocessor

logger = logging.getLogger(__name__)
console = Console()


class ModelEvaluator:
    """Handle model evaluation for federated learning using scikit-learn."""

    def __init__(self, model: MLPModel):
        self.model = model
    
    def evaluate_on_data(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Dict[str, Any]:
        """
        Evaluate model on given data using scikit-learn.

        Args:
            X: Feature array
            y: Label array

        Returns:
            Dictionary containing evaluation metrics
        """
        if not self.model.is_fitted:
            raise ValueError("Model must be fitted before evaluation")

        # Make predictions
        y_pred = self.model.predict(X)
        y_pred_proba = self.model.predict_proba(X)

        # Calculate metrics
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y, y_pred, average='weighted', zero_division=0)

        # Confusion matrix
        cm = confusion_matrix(y, y_pred)

        # Classification report
        class_report = classification_report(y, y_pred, output_dict=True, zero_division=0)

        # Calculate log loss (cross-entropy) if probabilities are available
        try:
            from sklearn.metrics import log_loss
            loss = log_loss(y, y_pred_proba)
        except:
            loss = None

        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'loss': loss,
            'confusion_matrix': cm,
            'classification_report': class_report,
            'predictions': y_pred,
            'prediction_probabilities': y_pred_proba,
            'true_labels': y,
            'num_samples': len(y)
        }
    
    def print_evaluation_results(self, metrics: Dict[str, Any], title: str = "Model Evaluation Results"):
        """
        Print evaluation results in a formatted way.
        
        Args:
            metrics: Dictionary containing evaluation metrics
            title: Title for the results display
        """
        # Create main metrics table
        table = Table(title="Performance Metrics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        
        table.add_row("Accuracy", f"{metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        table.add_row("Precision", f"{metrics['precision']:.4f}")
        table.add_row("Recall", f"{metrics['recall']:.4f}")
        table.add_row("F1-Score", f"{metrics['f1_score']:.4f}")
        table.add_row("Loss", f"{metrics['loss']:.4f}")
        table.add_row("Samples", str(metrics['num_samples']))
        
        console.print(Panel(table, title=title, border_style="blue"))
        
        # Print confusion matrix
        cm = metrics['confusion_matrix']
        console.print("\n[bold]Confusion Matrix:[/bold]")
        cm_table = Table(show_header=True, header_style="bold yellow")
        cm_table.add_column("True\\Pred", style="cyan")
        
        # Add columns for each class
        for i in range(cm.shape[1]):
            cm_table.add_column(f"Class {i}", style="white")
        
        # Add rows
        for i in range(cm.shape[0]):
            row = [f"Class {i}"] + [str(cm[i, j]) for j in range(cm.shape[1])]
            cm_table.add_row(*row)
        
        console.print(cm_table)
        
        # Print per-class metrics
        class_report = metrics['classification_report']
        if 'macro avg' in class_report:
            console.print("\n[bold]Per-Class Metrics:[/bold]")
            class_table = Table(show_header=True, header_style="bold green")
            class_table.add_column("Class", style="cyan")
            class_table.add_column("Precision", style="white")
            class_table.add_column("Recall", style="white")
            class_table.add_column("F1-Score", style="white")
            class_table.add_column("Support", style="white")
            
            for class_name, metrics_dict in class_report.items():
                if class_name not in ['accuracy', 'macro avg', 'weighted avg']:
                    class_table.add_row(
                        f"Class {class_name}",
                        f"{metrics_dict['precision']:.3f}",
                        f"{metrics_dict['recall']:.3f}",
                        f"{metrics_dict['f1-score']:.3f}",
                        str(int(metrics_dict['support']))
                    )
            
            console.print(class_table)


def evaluate_model(
    model_path: str,
    test_data_path: str,
    target_column: str = None,
    save_results: bool = False,
    results_path: str = None
) -> Dict[str, Any]:
    """
    Main evaluation function for federated learning client using scikit-learn.

    Args:
        model_path: Path to saved model
        test_data_path: Path to test CSV file
        target_column: Name of target column
        save_results: Whether to save results to file
        results_path: Path to save evaluation results

    Returns:
        Dictionary containing evaluation results
    """
    # Check if model exists
    model_file = Path(model_path)
    if not model_file.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Load model
    console.print(f"[blue]Loading model from {model_path}[/blue]")
    model = MLPModel.load_model(model_path)

    # Display model info
    model_info = model.get_model_info()
    console.print(f"[green]Model loaded successfully![/green]")
    console.print(f"Hidden layers: {model_info['hidden_layer_sizes']}")
    console.print(f"Total parameters: {model_info['total_parameters']:,}")
    console.print(f"Training iterations: {model_info['n_iter']}")

    # Preprocess test data
    console.print(f"[blue]Loading and preprocessing test data from {test_data_path}[/blue]")
    preprocessor = DataPreprocessor()
    X_test, y_test = preprocessor.preprocess_data(test_data_path, target_column)

    # Verify input size matches
    if X_test.shape[1] != model_info['feature_count']:
        raise ValueError(
            f"Input size mismatch: model expects {model_info['feature_count']} features, "
            f"but test data has {X_test.shape[1]} features"
        )

    # Evaluate model
    console.print("[blue]Evaluating model...[/blue]")
    evaluator = ModelEvaluator(model)
    evaluation_results = evaluator.evaluate_on_data(X_test, y_test)

    # Display results
    evaluator.print_evaluation_results(evaluation_results, "Test Set Evaluation")

    # Save results if requested
    if save_results and results_path:
        save_evaluation_results(evaluation_results, results_path, model_info)
        console.print(f"[green]Evaluation results saved to {results_path}[/green]")

    return {
        'evaluation_metrics': evaluation_results,
        'model_info': model_info,
        'test_data_shape': X_test.shape
    }


def save_evaluation_results(
    results: Dict[str, Any],
    results_path: str,
    model_info: Dict[str, Any]
):
    """
    Save evaluation results to file.
    
    Args:
        results: Evaluation results dictionary
        results_path: Path to save results
        model_info: Model information dictionary
    """
    results_file = Path(results_path)
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_file, 'w') as f:
        f.write("=== Federated Learning Client - Model Evaluation Results ===\n\n")
        
        # Model info
        f.write("Model Information:\n")
        f.write(f"  Feature Count: {model_info.get('feature_count', 'N/A')}\n")
        f.write(f"  Hidden Layers: {model_info['hidden_layer_sizes']}\n")
        f.write(f"  Number of Classes: {model_info.get('n_classes', 'N/A')}\n")
        f.write(f"  Total Parameters: {model_info['total_parameters']:,}\n")
        f.write(f"  Training Iterations: {model_info.get('n_iter', 'N/A')}\n")
        f.write(f"  Model Fitted: {model_info['is_fitted']}\n\n")
        
        # Performance metrics
        f.write("Performance Metrics:\n")
        f.write(f"  Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)\n")
        f.write(f"  Precision: {results['precision']:.4f}\n")
        f.write(f"  Recall: {results['recall']:.4f}\n")
        f.write(f"  F1-Score: {results['f1_score']:.4f}\n")
        f.write(f"  Loss: {results['loss']:.4f}\n")
        f.write(f"  Number of Samples: {results['num_samples']}\n\n")
        
        # Confusion matrix
        f.write("Confusion Matrix:\n")
        cm = results['confusion_matrix']
        for i in range(cm.shape[0]):
            f.write(f"  {cm[i].tolist()}\n")
        f.write("\n")
        
        # Classification report
        f.write("Classification Report:\n")
        class_report = results['classification_report']
        for class_name, metrics in class_report.items():
            if isinstance(metrics, dict):
                f.write(f"  {class_name}:\n")
                for metric_name, value in metrics.items():
                    f.write(f"    {metric_name}: {value:.4f}\n")
            else:
                f.write(f"  {class_name}: {metrics:.4f}\n")


def compare_models(
    model_paths: list,
    test_data_path: str,
    target_column: str = None
) -> Dict[str, Any]:
    """
    Compare multiple models on the same test dataset.

    Args:
        model_paths: List of paths to saved models
        test_data_path: Path to test CSV file
        target_column: Name of target column

    Returns:
        Dictionary containing comparison results
    """
    console.print("[blue]Comparing multiple models...[/blue]")
    
    # Preprocess test data once
    preprocessor = DataPreprocessor()
    X_test, y_test = preprocessor.preprocess_data(test_data_path, target_column)
    
    # Setup device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    comparison_results = {}
    
    for i, model_path in enumerate(model_paths):
        console.print(f"\n[yellow]Evaluating Model {i+1}: {model_path}[/yellow]")
        
        try:
            # Load and evaluate model
            model = MLPModel.load_model(model_path)
            evaluator = ModelEvaluator(model)
            results = evaluator.evaluate_on_data(X_test, y_test)
            
            comparison_results[f"Model_{i+1}"] = {
                'path': model_path,
                'results': results,
                'model_info': model.get_model_info()
            }
            
            console.print(f"Accuracy: {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
            
        except Exception as e:
            console.print(f"[red]Error evaluating {model_path}: {str(e)}[/red]")
            comparison_results[f"Model_{i+1}"] = {
                'path': model_path,
                'error': str(e)
            }
    
    # Display comparison table
    if len(comparison_results) > 1:
        console.print("\n[bold]Model Comparison Summary:[/bold]")
        comp_table = Table(show_header=True, header_style="bold blue")
        comp_table.add_column("Model", style="cyan")
        comp_table.add_column("Accuracy", style="green")
        comp_table.add_column("Precision", style="white")
        comp_table.add_column("Recall", style="white")
        comp_table.add_column("F1-Score", style="white")
        
        for model_name, data in comparison_results.items():
            if 'results' in data:
                results = data['results']
                comp_table.add_row(
                    model_name,
                    f"{results['accuracy']:.4f}",
                    f"{results['precision']:.4f}",
                    f"{results['recall']:.4f}",
                    f"{results['f1_score']:.4f}"
                )
            else:
                comp_table.add_row(model_name, "Error", "Error", "Error", "Error")
        
        console.print(comp_table)
    
    return comparison_results
