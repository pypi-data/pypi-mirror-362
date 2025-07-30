import mlx.core as mx
import mlx.nn as nn
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import logging
import os

from opensearcheval.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class SearchRankingModel(nn.Module):
    """Neural ranking model for search results using MLX"""
    
    def __init__(self, 
                 embedding_dim: int = 768, 
                 hidden_dim: int = 256, 
                 dropout: float = 0.1):
        super().__init__()
        
        # Layers for the model
        self.query_encoder = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        self.doc_encoder = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim)
        )
        
        self.scorer = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1)
        )
        
        logger.info(f"Initialized SearchRankingModel with embedding_dim={embedding_dim}, hidden_dim={hidden_dim}")
    
    def __call__(self, query_emb: mx.array, doc_emb: mx.array) -> mx.array:
        """
        Forward pass of the ranking model
        
        Args:
            query_emb: Query embedding tensor [batch_size, embedding_dim]
            doc_emb: Document embedding tensor [batch_size, embedding_dim]
            
        Returns:
            Relevance scores [batch_size, 1]
        """
        # Encode query and document
        q_enc = self.query_encoder(query_emb)
        d_enc = self.doc_encoder(doc_emb)
        
        # Concatenate encoded representations
        combined = mx.concatenate([q_enc, d_enc], axis=1)
        
        # Compute relevance score
        scores = self.scorer(combined)
        
        return scores
    
    def save(self, path: str):
        """Save model weights to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mx.save(path, self.parameters())
        logger.info(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load model weights from file"""
        params = mx.load(path)
        self.update(params)
        logger.info(f"Model loaded from {path}")


class ClickThroughRatePredictor(nn.Module):
    """Model to predict click-through rate for search results using MLX"""
    
    def __init__(self, 
                 feature_dim: int = 20, 
                 hidden_dims: List[int] = [64, 32], 
                 dropout: float = 0.2):
        super().__init__()
        
        layers = []
        prev_dim = feature_dim
        
        # Create hidden layers
        for dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = dim
        
        # Output layer
        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.model = nn.Sequential(*layers)
        
        logger.info(f"Initialized ClickThroughRatePredictor with feature_dim={feature_dim}, hidden_dims={hidden_dims}")
    
    def __call__(self, features: mx.array) -> mx.array:
        """
        Forward pass to predict CTR
        
        Args:
            features: Feature tensor [batch_size, feature_dim]
            
        Returns:
            Predicted CTR values [batch_size, 1]
        """
        return self.model(features)
    
    def save(self, path: str):
        """Save model weights to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        mx.save(path, self.parameters())
        logger.info(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load model weights from file"""
        params = mx.load(path)
        self.update(params)
        logger.info(f"Model loaded from {path}")


def extract_features(query: str, document: Dict[str, Any], position: int) -> List[float]:
    """
    Extract features for CTR prediction
    
    Args:
        query: Search query
        document: Document information
        position: Position in search results
        
    Returns:
        Feature vector
    """
    # This is a simplified version - in a real system this would be more complex
    features = [
        float(position),  # Position in results
        float(len(query)),  # Query length
        float(len(document.get("title", ""))),  # Title length
        float(len(document.get("snippet", ""))),  # Snippet length
        float(document.get("score", 0.0)),  # Document score
        # Add more features as needed
    ]
    
    # Pad to feature_dim if needed
    feature_dim = 20
    if len(features) < feature_dim:
        features.extend([0.0] * (feature_dim - len(features)))
    
    return features


def train_ctr_model(training_data: List[Dict[str, Any]], 
                    validation_data: Optional[List[Dict[str, Any]]] = None,
                    epochs: int = 10,
                    batch_size: int = 64,
                    learning_rate: float = 0.001,
                    model_path: Optional[str] = None) -> ClickThroughRatePredictor:
    """
    Train a CTR prediction model
    
    Args:
        training_data: List of training examples with features and labels
        validation_data: Optional validation data
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate
        model_path: Path to save the trained model
        
    Returns:
        Trained CTR model
    """
    # Initialize model
    model = ClickThroughRatePredictor()
    
    # Prepare optimizer
    optimizer = mx.optimizer.Adam(learning_rate=learning_rate)
    
    # Extract features and labels
    X_train = mx.array([ex["features"] for ex in training_data])
    y_train = mx.array([[ex["clicked"]] for ex in training_data])
    
    if validation_data:
        X_val = mx.array([ex["features"] for ex in validation_data])
        y_val = mx.array([[ex["clicked"]] for ex in validation_data])
    
    # Training loop
    for epoch in range(epochs):
        # Shuffle data
        indices = np.random.permutation(len(X_train))
        X_shuffled = X_train[indices]
        y_shuffled = y_train[indices]
        
        total_loss = 0.0
        num_batches = (len(X_train) + batch_size - 1) // batch_size
        
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, len(X_train))
            
            X_batch = X_shuffled[start_idx:end_idx]
            y_batch = y_shuffled[start_idx:end_idx]
            
            def loss_fn(params):
                model.update(params)
                y_pred = model(X_batch)
                # Binary cross-entropy loss
                loss = -mx.mean(y_batch * mx.log(y_pred + 1e-10) + 
                              (1 - y_batch) * mx.log(1 - y_pred + 1e-10))
                return loss
            
            # Compute loss and gradients
            loss, grads = mx.value_and_grad(loss_fn)(model.parameters())
            
            # Update parameters
            optimizer.update(model, grads)
            
            total_loss += loss.item()
        
        avg_loss = total_loss / num_batches
        logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        # Validation
        if validation_data:
            with mx.NoGrad():
                y_pred = model(X_val)
                val_loss = -mx.mean(y_val * mx.log(y_pred + 1e-10) + 
                                 (1 - y_val) * mx.log(1 - y_pred + 1e-10))
                logger.info(f"Validation Loss: {val_loss.item():.4f}")
    
    # Save model if path is provided
    if model_path:
        model.save(model_path)
    
    return model