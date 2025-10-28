# flows/ingest_flow.py
from pathlib import Path
import json
from prefect import flow, task, get_run_logger
from src.ai_resume_analyzer.scraper.playwright_linkedin import PlaywrightLinkedinScraper
from src.parsers.factory import parse_resume_to_record

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

@task
def fetch_url(scraper_conf: dict, url: str):
    logger = get_run_logger()
    scraper = PlaywrightLinkedinScraper(config=scraper_conf)
    try:
        raw = scraper.fetch(url)
        out_path = RAW_DIR / f"{url.replace('://','_').replace('/','_')}.html"
        out_path.write_text(raw.get("content",""), encoding="utf-8")
        logger.info("Saved raw %s", out_path)
        return {"url": url, "raw_path": str(out_path)}
    finally:
        scraper.close()

@task
def parse_raw_to_record(raw_meta: dict):
    logger = get_run_logger()
    raw_path = Path(raw_meta["raw_path"])
    # very generic: wrap as bytes and feed parse_resume_to_record (it handles bytes)
    with open(raw_path, "rb") as fh:
        rec = parse_resume_to_record(fh, filename=raw_path.name)
    # add source_url if any
    rec["source_url"] = raw_meta["url"]
    out = PROCESSED_DIR / (raw_path.stem + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    logger.info("Wrote processed record %s", out)
    return str(out)

@flow
def ingest_from_urls(urls: list, scraper_conf: dict = None):
    scraper_conf = scraper_conf or {}
    results = []
    for url in urls:
        raw_meta = fetch_url(scraper_conf, url)
        processed_path = parse_raw_to_record(raw_meta)
        results.append(processed_path)
    return results
