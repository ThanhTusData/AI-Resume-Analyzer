"""
Vector Store
FAISS-based vector storage for similarity search
"""

import numpy as np
from typing import List, Tuple, Optional
import pickle
from pathlib import Path
from loguru import logger


class VectorStore:
    """FAISS-based vector store"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = None
        self.metadata = []
        self._init_index()
    
    def _init_index(self):
        """Initialize FAISS index"""
        try:
            import faiss
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info(f"FAISS index initialized: dimension={self.dimension}")
        except ImportError:
            logger.error("FAISS not installed")
            raise
    
    def add_vectors(self, vectors: np.ndarray, metadata: Optional[List] = None):
        """Add vectors to store"""
        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)
        
        vectors = self._normalize_vectors(vectors)
        self.index.add(vectors)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([None] * len(vectors))
        
        logger.info(f"Added {len(vectors)} vectors. Total: {self.index.ntotal}")
    
    def search(self, query_vector: np.ndarray, k: int = 10) -> List[Tuple[float, any]]:
        """Search for similar vectors"""
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        
        query_vector = self._normalize_vectors(query_vector)
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            
            similarity = 1 - (dist / 2)
            
            if idx < len(self.metadata):
                results.append((similarity, self.metadata[idx]))
            else:
                results.append((similarity, idx))
        
        return results
    
    def _normalize_vectors(self, vectors: np.ndarray) -> np.ndarray:
        """Normalize vectors to unit length"""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors / norms
    
    def save(self, filepath: str):
        """Save vector store"""
        try:
            import faiss
            
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            faiss.write_index(self.index, str(path.with_suffix('.faiss')))
            
            with open(path.with_suffix('.metadata'), 'wb') as f:
                pickle.dump({
                    'metadata': self.metadata,
                    'dimension': self.dimension
                }, f)
            
            logger.info(f"Vector store saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save: {str(e)}")
            raise
    
    def load(self, filepath: str):
        """Load vector store"""
        try:
            import faiss
            
            path = Path(filepath)
            self.index = faiss.read_index(str(path.with_suffix('.faiss')))
            
            with open(path.with_suffix('.metadata'), 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.dimension = data['dimension']
            
            logger.info(f"Loaded {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Failed to load: {str(e)}")
            raise