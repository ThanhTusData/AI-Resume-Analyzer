# scripts/build_faiss_index.py
import json
from pathlib import Path
import argparse
import numpy as np
from src.ai_resume_analyzer.embeddings.encoder import Encoder
from src.ai_resume_analyzer.embeddings.faiss_index import build_index

DATA = Path("data/processed")
OUT = Path("models")
OUT.mkdir(parents=True, exist_ok=True)

def collect_text_for_embedding(rec: dict) -> str:
    # combine fields: summary + skills + experiences descriptions
    parts = []
    if rec.get("summary"):
        parts.append(rec["summary"])
    if rec.get("skills"):
        parts.append(" ".join(rec["skills"]))
    if rec.get("experiences"):
        parts.append(" ".join([e.get("description","") for e in rec["experiences"]]))
    if rec.get("raw_text"):
        parts.append(rec["raw_text"][:4000])  # limit size
    return "\n".join(parts)

def main(input_dir: str, model_name: str, out_index: str, batch_size: int):
    input_dir = Path(input_dir)
    files = sorted(list(input_dir.glob("*.json")))
    if not files:
        print("No processed JSON found. Run scripts/generate_fake_processed.py or place files in data/processed/")
        return
    ids = []
    texts = []
    metadatas = []
    for f in files:
        rec = json.load(open(f, "r", encoding="utf-8"))
        ids.append(rec.get("id", f.stem))
        texts.append(collect_text_for_embedding(rec))
        metadatas.append({"id": rec.get("id", f.stem), "name": rec.get("name"), "emails": rec.get("emails", [])})
    enc = Encoder(model_name=model_name)
    embs = enc.encode(texts, batch_size=batch_size)
    out_index_path = out_index
    built = build_index(embs.astype("float32"), ids, out_index_path)
    # save metadata file used by index builder is out_index.meta.json
    # save also human readable metadata
    with open(out_index_path + ".records.json", "w", encoding="utf-8") as f:
        json.dump(metadatas, f, ensure_ascii=False, indent=2)
    print(f"Index created at {out_index_path} (faiss: {built})")
    print(f"Records metadata written to {out_index_path}.records.json")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="data/processed")
    p.add_argument("--model", default="all-MiniLM-L6-v2")
    p.add_argument("--out", default="models/faiss.index")
    p.add_argument("--batch_size", type=int, default=32)
    args = p.parse_args()
    main(args.input, args.model, args.out, args.batch_size)
