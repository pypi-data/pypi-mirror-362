"""
MLP Model for Federated Learning Client using scikit-learn
"""
from sklearn.neural_network import MLPClassifier
from sklearn.base import clone
import joblib
import pickle
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import logging
import numpy as np

logger = logging.getLogger(__name__)


class MLPModel:
    """
    Multi-Layer Perceptron for binary classification in federated learning using scikit-learn.
    """

    def __init__(self, hidden_layer_sizes: tuple = (64, 32), max_iter: int = 1000, random_state: int = 42):
        """
        Initialize MLP model using scikit-learn MLPClassifier.

        Args:
            hidden_layer_sizes: Tuple of hidden layer sizes (default: (64, 32))
            max_iter: Maximum number of iterations for training
            random_state: Random state for reproducibility
        """
        self.hidden_layer_sizes = hidden_layer_sizes
        self.max_iter = max_iter
        self.random_state = random_state

        # Initialize the MLPClassifier
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            activation='relu',
            solver='adam',
            alpha=0.0001,  # L2 regularization
            batch_size='auto',
            learning_rate='constant',
            learning_rate_init=0.001,
            max_iter=max_iter,
            shuffle=True,
            random_state=random_state,
            tol=1e-4,
            verbose=False,
            warm_start=False,
            momentum=0.9,
            nesterovs_momentum=True,
            early_stopping=True,
            validation_fraction=0.1,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-8,
            n_iter_no_change=10
        )

        self.is_fitted = False
        self.feature_count = None
        self.classes_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'MLPModel':
        """
        Train the MLP model.

        Args:
            X: Training features of shape (n_samples, n_features)
            y: Training labels of shape (n_samples,)

        Returns:
            Self for method chaining
        """
        self.model.fit(X, y)
        self.is_fitted = True
        self.feature_count = X.shape[1]
        self.classes_ = self.model.classes_
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on input data.

        Args:
            X: Input features of shape (n_samples, n_features)

        Returns:
            Predicted labels of shape (n_samples,)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities.

        Args:
            X: Input features of shape (n_samples, n_features)

        Returns:
            Class probabilities of shape (n_samples, n_classes)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict_proba(X)
    
    def get_model_weights(self) -> Dict[str, Any]:
        """
        Get model weights and parameters as a dictionary.

        Returns:
            Dictionary containing model parameters
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before extracting weights")

        return {
            'coefs_': [coef.copy() for coef in self.model.coefs_],
            'intercepts_': [intercept.copy() for intercept in self.model.intercepts_],
            'classes_': self.model.classes_.copy(),
            'n_features_in_': self.model.n_features_in_,
            'n_layers_': self.model.n_layers_,
            'n_outputs_': self.model.n_outputs_
        }

    def set_model_weights(self, weights: Dict[str, Any]):
        """
        Set model weights from a dictionary.

        Args:
            weights: Dictionary containing model parameters
        """
        if not self.is_fitted:
            # Create a dummy fit to initialize the model structure
            dummy_X = np.random.random((10, weights['n_features_in_']))
            dummy_y = np.random.randint(0, len(weights['classes_']), 10)
            self.model.fit(dummy_X, dummy_y)

        # Set the weights
        self.model.coefs_ = [coef.copy() for coef in weights['coefs_']]
        self.model.intercepts_ = [intercept.copy() for intercept in weights['intercepts_']]
        self.model.classes_ = weights['classes_'].copy()
        self.model.n_features_in_ = weights['n_features_in_']
        self.model.n_layers_ = weights['n_layers_']
        self.model.n_outputs_ = weights['n_outputs_']

        self.is_fitted = True
        self.feature_count = weights['n_features_in_']
        self.classes_ = weights['classes_']

    def save_model(self, filepath: str):
        """
        Save model to file using joblib.

        Args:
            filepath: Path to save the model
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        model_data = {
            'model': self.model,
            'hidden_layer_sizes': self.hidden_layer_sizes,
            'max_iter': self.max_iter,
            'random_state': self.random_state,
            'is_fitted': self.is_fitted,
            'feature_count': self.feature_count,
            'classes_': self.classes_
        }

        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")

    @classmethod
    def load_model(cls, filepath: str) -> 'MLPModel':
        """
        Load model from file.

        Args:
            filepath: Path to the saved model

        Returns:
            Loaded MLPModel instance
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")

        model_data = joblib.load(filepath)

        # Create model instance
        model_instance = cls(
            hidden_layer_sizes=model_data['hidden_layer_sizes'],
            max_iter=model_data['max_iter'],
            random_state=model_data['random_state']
        )

        # Load the fitted model
        model_instance.model = model_data['model']
        model_instance.is_fitted = model_data['is_fitted']
        model_instance.feature_count = model_data['feature_count']
        model_instance.classes_ = model_data['classes_']

        logger.info(f"Model loaded from {filepath}")
        return model_instance
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model architecture information.

        Returns:
            Dictionary containing model info
        """
        if not self.is_fitted:
            return {
                'hidden_layer_sizes': self.hidden_layer_sizes,
                'max_iter': self.max_iter,
                'random_state': self.random_state,
                'is_fitted': False,
                'feature_count': None,
                'n_classes': None,
                'total_parameters': None
            }

        # Calculate total parameters
        total_params = 0
        layer_sizes = [self.feature_count] + list(self.hidden_layer_sizes) + [len(self.classes_)]

        for i in range(len(layer_sizes) - 1):
            # Weights + biases
            total_params += layer_sizes[i] * layer_sizes[i + 1] + layer_sizes[i + 1]

        return {
            'hidden_layer_sizes': self.hidden_layer_sizes,
            'max_iter': self.max_iter,
            'random_state': self.random_state,
            'is_fitted': self.is_fitted,
            'feature_count': self.feature_count,
            'n_classes': len(self.classes_) if self.classes_ is not None else None,
            'classes': self.classes_.tolist() if self.classes_ is not None else None,
            'total_parameters': total_params,
            'n_layers': self.model.n_layers_ if self.is_fitted else None,
            'loss': getattr(self.model, 'loss_', None),
            'n_iter': getattr(self.model, 'n_iter_', None)
        }

    def get_training_history(self) -> Dict[str, Any]:
        """
        Get training history and convergence information.

        Returns:
            Dictionary containing training history
        """
        if not self.is_fitted:
            return {'error': 'Model not fitted yet'}

        return {
            'loss_curve': getattr(self.model, 'loss_curve_', []),
            'validation_scores': getattr(self.model, 'validation_scores_', []),
            'best_loss': getattr(self.model, 'best_loss_', None),
            'best_validation_score': getattr(self.model, 'best_validation_score_', None),
            'n_iter': getattr(self.model, 'n_iter_', None),
            'converged': getattr(self.model, 'n_iter_', 0) < self.max_iter
        }


def create_model(hidden_layer_sizes: tuple = (64, 32), max_iter: int = 1000, random_state: int = 42) -> MLPModel:
    """
    Factory function to create an MLP model.

    Args:
        hidden_layer_sizes: Tuple of hidden layer sizes
        max_iter: Maximum number of iterations
        random_state: Random state for reproducibility

    Returns:
        MLPModel instance
    """
    return MLPModel(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter, random_state=random_state)
