# src/ai_resume_analyzer/api/routes/search.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from src.ai_resume_analyzer.embeddings.encoder import Encoder
from src.ai_resume_analyzer.embeddings.faiss_index import load_index, search

router = APIRouter()

class Query(BaseModel):
    query: str
    k: int = 5

@router.post("/")
def do_search(q: Query):
    index = load_index("models/faiss.index")
    enc = Encoder()
    emb = enc.encode([q.query])[0]
    hits = search(index, emb, k=q.k)
    # map hits to metadata if available
    import json
    meta_path = "models/faiss.index.records.json"
    meta_list = []
    try:
        meta_list = json.load(open(meta_path, "r", encoding="utf-8"))
    except Exception:
        meta_list = []
    out = []
    for idx, sc in hits:
        meta = meta_list[idx] if idx < len(meta_list) else {"id": idx}
        out.append({"idx": idx, "score": sc, "meta": meta})
    return {"query": q.query, "results": out}
