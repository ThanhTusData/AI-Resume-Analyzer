# tests/test_scraper_interface.py
from src.ai_resume_analyzer.scraper.base import BaseScraper
import pytest

class DummyScraper(BaseScraper):
    def fetch(self, url: str, timeout: int = 30):
        return {"url": url, "status": 200, "content": "<html><body>Hello</body></html>", "meta": {}}
    def parse_profile(self, raw):
        return {"raw_text": "Hello"}
    def close(self):
        pass

def test_dummy_scraper_interface():
    s = DummyScraper()
    r = s.fetch("http://example.com")
    assert r["status"] == 200
    parsed = s.parse_profile(r)
    assert "raw_text" in parsed
    s.close()
