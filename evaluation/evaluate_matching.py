# evaluation/evaluate_matching.py
import argparse
import json
from pathlib import Path
import numpy as np

def load_labels(path):
    return json.load(open(path, "r", encoding="utf-8"))

def evaluate(index_meta_path, labels_path, out_path, topk=5):
    # labels format expected: list of {"query": "...", "expected_ids": ["id1", "id2", ...]}
    labels = load_labels(labels_path)
    # load index metadata: records.json for mapping idx -> id
    metas = json.load(open(index_meta_path, "r", encoding="utf-8"))
    id_list = [m.get("id") for m in metas]
    results = []
    for q in labels:
        query = q["query"]
        expected = set(q.get("expected_ids", []))
        # we can't run the index here (offline) so assume we have a precomputed results file or call API
        # For skeleton, we will just return zero scores
        results.append({"query": query, "expected_count": len(expected), "matched": 0})
    out = {"n_queries": len(labels), "results": results}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Wrote evaluation to", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--index-meta", default="models/faiss.index.records.json")
    p.add_argument("--labels", required=True)
    p.add_argument("--out", default="evaluation/results_matching.json")
    args = p.parse_args()
    evaluate(args.index_meta, args.labels, args.out)
