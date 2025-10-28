# src/ai_resume_analyzer/scraper/playwright_linkedin.py
from typing import Dict, Any
import time
import logging

try:
    from playwright.sync_api import sync_playwright
except Exception as e:
    sync_playwright = None

from .base import BaseScraper

logger = logging.getLogger(__name__)

class PlaywrightLinkedinScraper(BaseScraper):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config=config)
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None
        self._start_playwright()

    def _start_playwright(self):
        if sync_playwright is None:
            raise RuntimeError("playwright not installed. pip install playwright && playwright install")
        self._pw = sync_playwright().start()
        browser_type = self.config.get("browser", "chromium")
        headless = self.config.get("headless", True)
        self._browser = getattr(self._pw, browser_type).launch(headless=headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()

    def fetch(self, url: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Fetch page and return basic dict. Does not attempt to log in.
        """
        if not self.respect_robots(url):
            return {"url": url, "status": 403, "content": "", "meta": {"error": "disallowed by robots"}}

        retries = self.config.get("max_retries", 2)
        throttle = self.config.get("throttle_seconds", 1.0)
        last_exc = None
        for attempt in range(1, retries + 1):
            try:
                self._page.goto(url, timeout=timeout * 1000)
                time.sleep(throttle)
                content = self._page.content()
                status = 200
                return {"url": url, "status": status, "content": content, "meta": {"attempt": attempt}}
            except Exception as e:
                last_exc = e
                logger.warning("fetch attempt %s failed for %s: %s", attempt, url, e)
                time.sleep(1 + attempt)
        return {"url": url, "status": 500, "content": "", "meta": {"error": str(last_exc)}}

    def parse_profile(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Very lightweight parse: return raw_text (page text) and metadata.
        Real parsing should be implemented by downstream parser.
        """
        html = raw.get("content", "") or ""
        # crude extraction: page innerText via JS for better text (but here fallback)
        try:
            inner_text = self._page.inner_text("body") if self._page else ""
        except Exception:
            inner_text = ""
        raw_text = inner_text or html
        return {
            "source_url": raw.get("url"),
            "raw_text": raw_text,
            "meta": raw.get("meta", {})
        }

    def close(self):
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._pw:
                self._pw.stop()
        except Exception:
            pass
