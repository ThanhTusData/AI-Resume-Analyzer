"""
Embeddings Generator
Generate text embeddings for similarity search
"""

import numpy as np
from typing import List
import openai
from loguru import logger


class EmbeddingGenerator:
    """Generate embeddings for text"""
    
    def __init__(self, provider: str = "openai", model: str = "text-embedding-3-small"):
        self.provider = provider
        self.model = model
        self.dimension = 1536
        
        if provider == "openai":
            from app.config import get_config
            config = get_config()
            openai.api_key = config.OPENAI_API_KEY
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        if not text or not text.strip():
            logger.warning("Empty text for embedding")
            return np.zeros(self.dimension)
        
        try:
            if self.provider == "openai":
                response = openai.embeddings.create(
                    model=self.model,
                    input=text[:8000]
                )
                embedding = response.data[0].embedding
                return np.array(embedding, dtype=np.float32)
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            return np.zeros(self.dimension)
    
    def generate_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        embeddings = [self.generate_embedding(text) for text in texts]
        return np.array(embeddings)