# src/ai_resume_analyzer/embeddings/faiss_index.py
import json
import os
import numpy as np
from typing import List, Tuple

_HAS_FAISS = False
try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False
from sklearn.metrics.pairwise import cosine_similarity

def build_index(embeddings: np.ndarray, ids: List[str], index_path: str, use_ivf: bool = False):
    """
    embeddings: (n, dim) float32, assumed normalized if using inner product as cosine
    ids: list of ids (len == n)
    """
    os.makedirs(os.path.dirname(index_path) or ".", exist_ok=True)
    meta_path = index_path + ".meta.json"
    if _HAS_FAISS:
        dim = embeddings.shape[1]
        if use_ivf:
            nlist = max(1, int(np.sqrt(len(embeddings))))
            quantizer = faiss.IndexFlatIP(dim)
            index = faiss.IndexIVFFlat(quantizer, dim, nlist, faiss.METRIC_INNER_PRODUCT)
            index.train(embeddings)
            index.add(embeddings)
        else:
            index = faiss.IndexFlatIP(embeddings.shape[1])
            index.add(embeddings)
        faiss.write_index(index, index_path)
        # save metadata
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({"ids": ids}, f, ensure_ascii=False)
        return True
    else:
        # fallback: save numpy arrays for brute-force
        np.save(index_path + ".emb.npy", embeddings)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({"ids": ids}, f, ensure_ascii=False)
        return False

def load_index(index_path: str):
    meta_path = index_path + ".meta.json"
    if _HAS_FAISS and os.path.exists(index_path):
        index = faiss.read_index(index_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return {"type": "faiss", "index": index, "ids": meta.get("ids", [])}
    elif os.path.exists(index_path + ".emb.npy"):
        emb = np.load(index_path + ".emb.npy")
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return {"type": "npy", "emb": emb, "ids": meta.get("ids", [])}
    else:
        raise FileNotFoundError("Index not found")

def search(index_obj, query_emb: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
    """
    returns list of tuples (idx, score) where idx is index into ids list
    """
    if index_obj["type"] == "faiss":
        index = index_obj["index"]
        if query_emb.ndim == 1:
            q = query_emb.reshape(1, -1).astype("float32")
        else:
            q = query_emb.astype("float32")
        D, I = index.search(q, k)
        # D are inner product scores (for normalized vectors equals cosine)
        res = []
        for i, row in enumerate(I):
            res.append([(int(idx), float(D[i][j])) for j, idx in enumerate(row) if idx != -1])
        return res[0]
    else:
        emb = index_obj["emb"]
        # cosine similarity
        if query_emb.ndim == 1:
            q = query_emb.reshape(1, -1)
        else:
            q = query_emb
        sims = cosine_similarity(q, emb)[0]
        idxs = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i])) for i in idxs]
