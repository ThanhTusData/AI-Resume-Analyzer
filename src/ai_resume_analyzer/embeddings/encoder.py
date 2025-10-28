# src/ai_resume_analyzer/embeddings/encoder.py
from typing import List, Optional
import numpy as np

# Try sentence-transformers; fallback to sklearn TfidfVectorizer
try:
    from sentence_transformers import SentenceTransformer
    _HAS_ST = True
except Exception:
    _HAS_ST = False

from sklearn.feature_extraction.text import TfidfVectorizer

class Encoder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", normalize: bool = True):
        self.normalize = normalize
        self.model_name = model_name
        self._model = None
        self._tfidf = None
        if _HAS_ST:
            try:
                self._model = SentenceTransformer(model_name)
            except Exception:
                self._model = None

    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        texts = ["" if t is None else t for t in texts]
        if self._model is not None:
            embs = self._model.encode(texts, batch_size=batch_size, show_progress_bar=False, convert_to_numpy=True)
            embs = embs.astype("float32")
        else:
            # TF-IDF fallback: create dense embeddings (not ideal but works for tests)
            if self._tfidf is None:
                self._tfidf = TfidfVectorizer(max_features=2048)
                self._tfidf.fit(texts)
            embs = self._tfidf.transform(texts).toarray().astype("float32")
        if self.normalize:
            # L2 normalize
            norms = np.linalg.norm(embs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            embs = embs / norms
        return embs
