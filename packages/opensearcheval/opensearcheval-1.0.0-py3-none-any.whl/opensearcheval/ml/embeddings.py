import numpy as np
import logging
from typing import List, Dict, Any, Optional, Union
import mlx.core as mx
import os
import json
import httpx
import asyncio

logger = logging.getLogger(__name__)

class EmbeddingModel:
    """Base class for embedding models"""
    
    def __init__(self, model_name: str, dimension: int):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the model
            dimension: Dimension of the embeddings
        """
        self.model_name = model_name
        self.dimension = dimension
        logger.info(f"Initialized embedding model: {model_name} with dimension: {dimension}")
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text
        
        Args:
            text: Input text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        raise NotImplementedError("Subclasses must implement embed method")
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Cosine similarity score
        """
        return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
    
    def batch_similarity(self, query_embedding: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate similarities between a query embedding and multiple document embeddings
        
        Args:
            query_embedding: Query embedding
            doc_embeddings: Document embeddings
            
        Returns:
            Array of similarity scores
        """
        # Normalize embeddings
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        
        # Calculate dot products
        similarities = np.dot(doc_norms, query_norm)
        
        return similarities


class MLXEmbeddingModel(EmbeddingModel):
    """Embedding model using MLX"""
    
    def __init__(self, model_path: str):
        """
        Initialize the MLX embedding model
        
        Args:
            model_path: Path to model weights and config
        """
        # Load model configuration
        config_path = os.path.join(model_path, "config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        dimension = config.get("dimension", 768)
        model_name = config.get("model_name", "mlx_embedding_model")
        
        super().__init__(model_name, dimension)
        
        try:
            # Import and initialize the model
            from mlx.nn import TransformerEncoder, Embedding, Linear, LayerNorm
            
            # Define model architecture
            vocab_size = config.get("vocab_size", 30522)
            num_layers = config.get("num_layers", 12)
            num_heads = config.get("num_heads", 12)
            hidden_dim = config.get("hidden_dim", 768)
            
            # Create tokenizer
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(config.get("tokenizer_name", "bert-base-uncased"))
            
            # Create model components
            self.embedding = Embedding(vocab_size, hidden_dim)
            self.encoder = TransformerEncoder(num_layers, hidden_dim, num_heads)
            self.pooler = Linear(hidden_dim, hidden_dim)
            self.layer_norm = LayerNorm(hidden_dim)
            
            # Load weights
            weights_path = os.path.join(model_path, "weights.npz")
            weights = mx.load(weights_path)
            
            # Assign weights
            for name, param in weights.items():
                if name.startswith("embedding"):
                    self.embedding.update({name.replace("embedding.", ""): param})
                elif name.startswith("encoder"):
                    self.encoder.update({name.replace("encoder.", ""): param})
                elif name.startswith("pooler"):
                    self.pooler.update({name.replace("pooler.", ""): param})
                elif name.startswith("layer_norm"):
                    self.layer_norm.update({name.replace("layer_norm.", ""): param})
            
            logger.info(f"Loaded MLX embedding model from {model_path}")
        except Exception as e:
            logger.error(f"Error loading MLX embedding model: {str(e)}")
            raise
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text using MLX
        
        Args:
            text: Input text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        try:
            # Ensure text is a list
            if isinstance(text, str):
                texts = [text]
            else:
                texts = text
            
            # Tokenize
            inputs = self.tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="np"
            )
            
            # Convert to MLX arrays
            input_ids = mx.array(inputs["input_ids"])
            attention_mask = mx.array(inputs["attention_mask"])
            
            # Forward pass
            embeddings = self.embedding(input_ids)
            embeddings = self.encoder(embeddings, attention_mask)
            
            # Mean pooling
            mask_expanded = attention_mask.reshape(attention_mask.shape[0], attention_mask.shape[1], 1)
            sum_embeddings = mx.sum(embeddings * mask_expanded, axis=1)
            sum_mask = mx.sum(mask_expanded, axis=1)
            embeddings = sum_embeddings / sum_mask
            
            # Layer norm and pooler
            embeddings = self.layer_norm(embeddings)
            embeddings = self.pooler(embeddings)
            
            # Convert to numpy
            np_embeddings = embeddings.numpy()
            
            # Return single embedding or batch
            if len(texts) == 1:
                return np_embeddings[0]
            else:
                return np_embeddings
        
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            # Return zeros as fallback
            if isinstance(text, str):
                return np.zeros(self.dimension)
            else:
                return np.zeros((len(text), self.dimension))


class ApiEmbeddingModel(EmbeddingModel):
    """Embedding model using an API (like OpenAI)"""
    
    def __init__(self, model_name: str, api_key: str, api_url: str, dimension: int = 1536):
        """
        Initialize the API embedding model
        
        Args:
            model_name: Name of the embedding model
            api_key: API key
            api_url: API endpoint URL
            dimension: Dimension of the embeddings
        """
        super().__init__(model_name, dimension)
        self.api_key = api_key
        self.api_url = api_url
    
    async def async_embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text using API (async version)
        
        Args:
            text: Input text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        try:
            # Ensure text is a list
            if isinstance(text, str):
                texts = [text]
            else:
                texts = text
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    json={
                        "model": self.model_name,
                        "input": texts
                    },
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    logger.error(f"API error: {response.status_code} - {response.text}")
                    raise Exception(f"API error: {response.status_code}")
                
                result = response.json()
                
                # Extract embeddings
                embeddings = []
                for item in result.get("data", []):
                    embedding = item.get("embedding", [])
                    embeddings.append(embedding)
                
                # Convert to numpy array
                np_embeddings = np.array(embeddings, dtype=np.float32)
                
                # Return single embedding or batch
                if len(texts) == 1:
                    return np_embeddings[0]
                else:
                    return np_embeddings
        
        except Exception as e:
            logger.error(f"Error generating embeddings via API: {str(e)}")
            # Return zeros as fallback
            if isinstance(text, str):
                return np.zeros(self.dimension)
            else:
                return np.zeros((len(text), self.dimension))
    
    def embed(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text using API (sync wrapper)
        
        Args:
            text: Input text or list of texts
            
        Returns:
            Numpy array of embeddings
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.async_embed(text))


def create_embedding_model(config: Dict[str, Any]) -> EmbeddingModel:
    """
    Factory function to create an embedding model based on configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        EmbeddingModel instance
    """
    model_type = config.get("type", "mlx")
    
    if model_type == "mlx":
        model_path = config.get("model_path")
        if not model_path:
            raise ValueError("model_path is required for MLX embedding model")
        
        return MLXEmbeddingModel(model_path)
    
    elif model_type == "api":
        model_name = config.get("model_name", "text-embedding-ada-002")
        api_key = config.get("api_key")
        api_url = config.get("api_url", "https://api.openai.com/v1/embeddings")
        dimension = config.get("dimension", 1536)
        
        if not api_key:
            raise ValueError("api_key is required for API embedding model")
        
        return ApiEmbeddingModel(model_name, api_key, api_url, dimension)
    
    else:
        raise ValueError(f"Unsupported embedding model type: {model_type}")