# src/ai_resume_analyzer/scraper/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseScraper(ABC):
    """
    Abstract scraper interface used by ingest flows.
    Implementations MUST respect robots.txt externally (configurable).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    @abstractmethod
    def fetch(self, url: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Fetch raw content for a URL.
        Return dict { 'url': url, 'status': int, 'content': bytes or str, 'meta': {...} }
        """
        raise NotImplementedError

    @abstractmethod
    def parse_profile(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw fetched content -> normalized record (may include raw_text, title, company, location, etc.)
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """Close resources (browser, sessions)."""
        raise NotImplementedError

    def respect_robots(self, url: str) -> bool:
        """
        Optional helper: check robots.txt usage. Default implementation returns True
        (caller should implement actual robots checking).
        """
        return True
