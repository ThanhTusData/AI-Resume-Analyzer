# SCRAPING_POLICY (draft)

1. Respect robots.txt: Always check target domain's robots.txt. If disallowed, DO NOT SCRAPE.
2. Rate limiting: Default throttle_seconds=1.0. Do not exceed polite rate (>=1s).
3. No credential sharing: Never store or commit API keys, tokens, or account credentials.
4. PII handling: Extracted personal data (emails, phones) must be stored encrypted and access-restricted.
5. Retention: Raw HTML must be retained only for debugging (configurable, default: 7 days).
6. Legal: Verify Terms of Service of targets; prefer official APIs (LinkedIn API) over scraping.
7. Security: Rotate proxies & user-agents responsibly; avoid evasion methods that violate law/ToS.
