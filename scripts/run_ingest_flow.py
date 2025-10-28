# scripts/run_ingest_flow.py
import argparse
from pathlib import Path
from flows.ingest_flow import ingest_from_urls

def load_urls(path):
    p = Path(path)
    if not p.exists():
        return []
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--urls", default="data/samples/urls.txt")
    p.add_argument("--use-prefect", action="store_true")
    args = p.parse_args()
    urls = load_urls(args.urls)
    if not urls:
        print("No URLs provided.")
    else:
        print(f"Running ingest for {len(urls)} urls")
        ingest_from_urls(urls, scraper_conf=None)
