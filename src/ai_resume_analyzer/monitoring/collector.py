# src/ai_resume_analyzer/monitoring/collector.py
import hashlib
import json
import os
import time
from typing import Dict

MON_DIR = os.environ.get("MONITORING_DIR", "monitoring")
os.makedirs(MON_DIR, exist_ok=True)
LOG_PATH = os.path.join(MON_DIR, "requests.log")

def _hash_text(text: str) -> str:
    # normalize and hash text; do not store original
    if text is None:
        text = ""
    s = text.strip().lower().encode("utf-8")
    return hashlib.sha256(s).hexdigest()

def record_inference(event: Dict):
    """
    event: dict containing non-PII metadata to record.
    Expected keys (example): {"route": "/analyze", "duration": 0.23, "num_tokens": 123}
    If you need to include text fingerprint, provide key 'text' -> will be hashed.
    """
    safe = {}
    safe.update({k: v for k, v in event.items() if k != "text"})
    if "text" in event:
        safe["text_fingerprint"] = _hash_text(event["text"])
    safe["ts"] = int(time.time())
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(safe, ensure_ascii=False) + "\n")
