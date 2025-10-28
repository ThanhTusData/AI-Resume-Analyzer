# scripts/ingest_sample.py
import os
import json
from pathlib import Path
from src.parsers.factory import parse_resume_to_record

DATA_SAMPLES = Path("data/samples")
DATA_PROCESSED = Path("data/processed")

def ensure_dirs():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

def ingest_folder(input_dir: Path = DATA_SAMPLES, output_dir: Path = DATA_PROCESSED):
    ensure_dirs()
    files = list(input_dir.glob("*"))
    if not files:
        print(f"No files found in {input_dir}. Please add sample resumes (pdf/docx/png/jpg).")
        return
    for f in files:
        try:
            with open(f, "rb") as fh:
                record = parse_resume_to_record(fh, filename=f.name)
            out_path = output_dir / (f.stem + ".json")
            with open(out_path, "w", encoding="utf-8") as out:
                json.dump(record, out, ensure_ascii=False, indent=2)
            print(f"[OK] Parsed {f.name} -> {out_path}")
        except Exception as e:
            print(f"[ERR] {f.name}: {e}")

if __name__ == "__main__":
    ingest_folder()
