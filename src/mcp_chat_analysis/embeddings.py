from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import torch
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Handles generation of vector embeddings for text"""
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: Optional[str] = None,
        batch_size: int = 32,
        max_length: int = 512
    ):
        """
        Initialize the embedding generator
        
        Args:
            model_name: Name of the sentence-transformers model to use
            device: Device to run model on ('cpu', 'cuda', or None for auto)
            batch_size: Batch size for embedding generation
            max_length: Maximum sequence length
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_length = max_length
        
        # Determine device
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        
        # Load model
        logger.info(f"Loading model {model_name} on {device}")
        self.model = SentenceTransformer(model_name, device=device)
        
        # Cache model properties
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    async def generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        # Preprocess texts
        processed_texts = [
            self._preprocess_text(text) for text in texts
        ]
        
        # Generate embeddings in batches
        all_embeddings = []
        for i in range(0, len(processed_texts), self.batch_size):
            batch = processed_texts[i:i + self.batch_size]
            embeddings = self.model.encode(
                batch,
                batch_size=self.batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            all_embeddings.extend(embeddings.tolist())
        
        return all_embeddings
    
    async def generate_single(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        processed = self._preprocess_text(text)
        embedding = self.model.encode(
            processed,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        return embedding.tolist()
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text before embedding
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # Basic preprocessing
        text = text.strip()
        
        # Truncate if needed
        if len(text) > self.max_length:
            text = text[:self.max_length]
        
        return text
    
    async def compute_similarity(
        self,
        text1: str,
        text2: str,
        method: str = "cosine"
    ) -> float:
        """
        Compute similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            method: Similarity method ('cosine' or 'euclidean')
            
        Returns:
            Similarity score
        """
        # Generate embeddings
        emb1 = await self.generate_single(text1)
        emb2 = await self.generate_single(text2)
        
        # Convert to numpy arrays
        vec1 = np.array(emb1)
        vec2 = np.array(emb2)
        
        # Compute similarity
        if method == "cosine":
            similarity = np.dot(vec1, vec2) / (
                np.linalg.norm(vec1) * np.linalg.norm(vec2)
            )
        elif method == "euclidean":
            similarity = 1 / (1 + np.linalg.norm(vec1 - vec2))
        else:
            raise ValueError(f"Unknown similarity method: {method}")
        
        return float(similarity)
    
    async def find_similar_chunks(
        self,
        query: str,
        texts: List[str],
        threshold: float = 0.5,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find most similar text chunks to a query
        
        Args:
            query: Query text
            texts: List of texts to search
            threshold: Minimum similarity threshold
            top_k: Maximum number of results
            
        Returns:
            List of similar texts with scores
        """
        # Generate query embedding
        query_emb = await self.generate_single(query)
        
        # Generate embeddings for all texts
        chunk_embs = await self.generate(texts)
        
        # Compute similarities
        similarities = []
        for i, emb in enumerate(chunk_embs):
            score = np.dot(query_emb, emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(emb)
            )
            if score >= threshold:
                similarities.append({
                    "text": texts[i],
                    "score": float(score)
                })
        
        # Sort by score and return top_k
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:top_k]