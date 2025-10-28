# Privacy & Logging Policy (short)

- **Never** store raw resume text in logs or monitoring.
- Monitoring must only record hashed fingerprints (sha256 of normalized text) and aggregated numeric metadata (latency, sizes).
- Secrets (API keys) must not be committed. Use environment variables.
- For debugging only: create ephemeral dumps locally and remove before commit.
- Retention: monitoring logs should be rotated (not older than 90 days) — implement external rotation.
