# scripts/query_index.py
import argparse
import json
from src.ai_resume_analyzer.embeddings.encoder import Encoder
from src.ai_resume_analyzer.embeddings.faiss_index import load_index, search
import numpy as np

def main(index_path: str, model_name: str, k: int):
    idx_obj = load_index(index_path)
    records = json.load(open(index_path + ".records.json", "r", encoding="utf-8"))
    enc = Encoder(model_name=model_name)
    print("Enter job description (end with a blank line):")
    lines = []
    while True:
        try:
            l = input()
        except EOFError:
            break
        if l.strip() == "":
            break
        lines.append(l)
    jd = "\n".join(lines).strip()
    if not jd:
        print("Empty query")
        return
    q_emb = enc.encode([jd])[0]
    res = search(idx_obj, q_emb, k=k)
    print("Top results:")
    for idx, score in res:
        rec = records[idx] if idx < len(records) else {"id": "unknown"}
        print(f"- id={rec.get('id')} name={rec.get('name')} score={score:.4f} emails={rec.get('emails')}")
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--index", default="models/faiss.index")
    p.add_argument("--model", default="all-MiniLM-L6-v2")
    p.add_argument("--k", type=int, default=5)
    args = p.parse_args()
    main(args.index, args.model, args.k)
