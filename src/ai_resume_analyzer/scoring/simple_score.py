# src/ai_resume_analyzer/scoring/simple_score.py
from typing import Tuple, Dict
import re

def simple_score(record: dict, jd_text: str) -> Tuple[float, Dict]:
    """
    Very lightweight rule-based scoring:
    - match count of keywords extracted from jd_text vs resume raw_text
    Returns score in [0,1] and explanation dict
    """
    def words(s: str):
        return [w.lower() for w in re.findall(r"\\w+", s or "")]

    jd_words = set(words(jd_text)) if jd_text else set()
    resume_words = set(words(record.get("raw_text", "")))

    if not jd_words:
        return 0.0, {"reason": "no_jd_text"}

    common = jd_words.intersection(resume_words)
    match_count = len(common)
    score = min(1.0, match_count / max(1.0, len(jd_words)))
    explain = {"jd_term_count": len(jd_words), "matched_terms": list(common)[:30], "match_count": match_count}
    return float(score), explain
