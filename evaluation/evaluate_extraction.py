# evaluation/evaluate_extraction.py
import argparse
import json
from pathlib import Path

def evaluate(labels_path, predictions_path, out_path):
    # labels: list of records with canonical fields; predictions same format
    labels = json.load(open(labels_path, "r", encoding="utf-8"))
    preds = json.load(open(predictions_path, "r", encoding="utf-8"))
    # Simple precision/recall on emails and phones as example
    tp_email = 0
    total_pred_email = 0
    total_true_email = 0
    for l, p in zip(labels, preds):
        true_emails = set(l.get("emails", []))
        pred_emails = set(p.get("emails", []))
        tp_email += len(true_emails & pred_emails)
        total_pred_email += len(pred_emails)
        total_true_email += len(true_emails)
    precision = tp_email / total_pred_email if total_pred_email else 0.0
    recall = tp_email / total_true_email if total_true_email else 0.0
    out = {"email_precision": precision, "email_recall": recall}
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("Wrote extraction eval to", out_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--labels", required=True)
    p.add_argument("--preds", required=True)
    p.add_argument("--out", default="evaluation/results_extraction.json")
    args = p.parse_args()
    evaluate(args.labels, args.preds, args.out)
