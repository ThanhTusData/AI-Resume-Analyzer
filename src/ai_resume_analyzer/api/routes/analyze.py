# src/ai_resume_analyzer/api/routes/analyze.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from src.parsers.factory import parse_resume_to_record
from src.ai_resume_analyzer.scoring.simple_score import simple_score
from src.ai_resume_analyzer.embeddings.encoder import Encoder
from src.ai_resume_analyzer.embeddings.faiss_index import load_index, search
import tempfile
import shutil
import os
import time
import logging

# monitoring collector (does hashing internally; does NOT store raw text)
from src.ai_resume_analyzer.monitoring.collector import record_inference

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

# Lazy singletons
_ENCODER = None
_INDEX = None

def get_encoder():
    global _ENCODER
    if _ENCODER is None:
        _ENCODER = Encoder()
    return _ENCODER

def get_index():
    global _INDEX
    if _INDEX is None:
        try:
            _INDEX = load_index("models/faiss.index")
        except Exception:
            _INDEX = None
    return _INDEX

@router.post("/")
async def analyze(file: Optional[UploadFile] = File(None), jd_text: Optional[str] = Form(None), k: int = Form(5)):
    start = time.time()
    if file is None and not jd_text:
        raise HTTPException(status_code=400, detail="Provide file or jd_text")
    # If file provided parse it
    if file is not None:
        content = await file.read()
        record = parse_resume_to_record(content, filename=file.filename)
    else:
        # create a synthetic record from jd_text for scoring
        record = {"source_file": "jd", "raw_text": jd_text, "name": "", "emails": [], "phones": [], "skills": [], "experiences": []}

    # compute simple score
    score, explain = simple_score(record, jd_text or "")

    # run vector search for similar profiles if index present
    idx_obj = get_index()
    matches = []
    if idx_obj is not None:
        enc = get_encoder()
        q_emb = enc.encode([jd_text or record.get("raw_text", "")])[0]
        try:
            hits = search(idx_obj, q_emb, k=k)
            # hits is list of tuples (idx, score) or list-of-list depending impl
            for idx, sc in hits:
                # load metadata list file if exists
                meta_path = "models/faiss.index.records.json"
                meta = {}
                try:
                    import json
                    meta_list = json.load(open(meta_path, "r", encoding="utf-8"))
                    meta = meta_list[idx] if idx < len(meta_list) else {}
                except Exception:
                    meta = {"id": str(idx)}
                matches.append({"idx": idx, "score": sc, "meta": meta})
        except Exception:
            matches = []

    duration = time.time() - start

    # Safe monitoring record: collector will hash the 'text' and will NOT persist raw text.
    try:
        record_inference({
            "route": "/analyze",
            "duration": float(duration),
            "num_matches": int(len(matches)),
            "num_emails": int(len(record.get("emails", [])) if isinstance(record.get("emails", []), list) else 0),
            # Pass only a small slice for fingerprinting; collector hashes it and does NOT store raw
            "text": (record.get("raw_text") or "")[:4000]
        })
    except Exception:
        # monitoring should never break main flow
        logger.exception("monitoring record failed")

    return {"record": record, "score": float(score), "explain": explain, "matches": matches}
