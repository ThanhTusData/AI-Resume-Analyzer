# AI Resume Analyzer

**Short description**

AI Resume Analyzer is an end-to-end toolkit that collects, parses, analyzes, and semantically searches resumes and professional profiles (e.g., LinkedIn) using modern NLP, embeddings, and vector search. It helps HR and recruiting teams automate CV parsing, rank and match candidates against job descriptions, and monitor the quality and drift of candidate data.

---

## Table of contents
- Project overview
- Business value
- High-level architecture & directory layout
- Tools & why we use them
- Quickstart (install & run)
- API endpoints & sample usage
- Scripts & utilities
- Testing & CI
- Observability & monitoring
- Security, privacy & scraping policy
- Roadmap & upgrade suggestions
- Troubleshooting
- Contributing, license & contact

---

# Project overview

AI Resume Analyzer is designed to reduce manual time spent on resume screening by automating extraction, normalization and semantic search of candidate profiles. The system accepts resumes in multiple formats (PDF, DOCX, images with OCR), normalizes fields (name, contact, skills, job history, education), computes semantic embeddings for each candidate, and supports nearest-neighbor search (via FAISS) to find best-matching candidates for a given job description or query.

# Business value

- **Faster screening**: automates the first-round triage so recruiters focus on higher-value interviewing tasks.
- **Better matching**: semantic search finds candidates who match the meaning of a job description, not only exact keywords.
- **Scalable indexing**: FAISS allows fast approximate nearest-neighbor queries on large candidate pools.
- **Data-driven recruiting**: metrics and monitoring enable teams to measure sourcing quality, coverage, and drift over time.
- **Auditability**: extraction and scoring outputs are logged for traceability.

---

# High-level architecture & repository layout

This project follows a modular layout: parsers, analyzers, embedding/indexing, API, orchestration scripts, monitoring, and tests. Example top-level layout:

```
ai-resume-analyzer/
├─ app.py
├─ src/
│  ├─ parsers/                # pdf/docx/ocr parsers and parser factory
│  ├─ embeddings/             # encoder + vector utilities
│  ├─ index/                  # faiss index builder & loader
│  ├─ api/                    # FastAPI/Flask endpoints
│  ├─ scoring/                # candidate scoring & ranking
│  ├─ scraper/                # LinkedIn / profile scrapers (playwright/selenium)
│  ├─ monitoring/             # metrics collector, drift detector
│  └─ utils/                  # common helpers
├─ scripts/                   # ingest, build_index, data generators
├─ tests/                     # pytest tests
├─ docker/                    # Dockerfiles and compose manifests
├─ requirements.txt
├─ .env.example
└─ POLICIES/                  # SCRAPING_POLICY.md, PRIVACY.md
```

> Note: adapt the exact paths to your repository if they differ.

---

# Tools used & their role in the project

- **Python**: primary language for parsers, model inference, API and scripts (fast to iterate and has rich NLP ecosystem).
- **FastAPI / Flask**: production-ready HTTP API frameworks to expose analyze/search endpoints.
- **Playwright / Selenium**: optional scrapers to collect public profiles when no API is available; use with legal policy.
- **pdfplumber / python-docx / pytesseract**: robust parsing of PDF/DOCX and OCR for image-based resumes.
- **spaCy / Hugging Face Transformers**: NER and token-level processing for better field extraction and optional fine-tuning.
- **Sentence Transformers / OpenAI embeddings**: to convert text into dense vectors for semantic similarity.
- **FAISS**: fast similarity search for nearest-neighbor queries on dense vectors.
- **Docker & docker-compose**: containerize services for consistent development and production deployments.
- **Prometheus & Grafana**: metrics collection and dashboards for observability and drift monitoring.
- **pytest & pre-commit**: automated tests and code quality gates for safer changes.

---

# Quickstart — local development

> These commands assume the repository root contains `requirements.txt`, `.env.example` and a `docker` folder. Adjust paths if needed.

## 1) Clone the repo

```bash
git clone <repo-url>
cd ai-resume-analyzer
```

## 2) Prepare environment

Copy example env and set keys (embedding provider, DB endpoints, etc.)

```bash
cp .env.example .env
# edit .env with your API keys and paths
```

## 3) Install dependencies (venv)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Run app locally

Example using Uvicorn (FastAPI):

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Or run the legacy entrypoint if provided:

```bash
python app.py
```

## 5) Docker (recommended for parity)

```bash
docker compose up --build
```

## 6) Build FAISS index (sample)

```bash
python scripts/build_faiss_index.py --input data/candidates.jsonl --output data/candidates.faiss
```

## 7) Ingest sample data

```bash
python scripts/ingest_sample.py --source data/sample_resumes/
```

---

# API endpoints (examples)

> Adjust paths based on `src/api` implementation.

- `GET /health` — health and readiness checks
- `POST /analyze` — upload a resume file or raw text; returns extracted fields and a score
- `POST /search` — submit text or job description; returns top-N candidate matches (by vector similarity)

### Example: analyze

```bash
curl -X POST "http://localhost:8000/analyze" -F "file=@/path/to/CV.pdf"
```

Example response (schema idea):

```json
{
  "candidate_id": "uuid",
  "extracted": {
    "name": "",
    "email": "",
    "phones": [],
    "skills": ["python", "nlp"],
    "experiences": [{"company":"X","title":"Data Analyst","from":"2019","to":"2022"}],
  },
  "scores": {"match_score": 0.78, "skill_coverage": 0.6}
}
```

---

# Scripts & utilities

- `scripts/build_faiss_index.py` — create FAISS index from an embeddings file.
- `scripts/ingest_sample.py` — ingest sample resumes into the local DB and index.
- `scripts/generate_fake_data.py` — create synthetic candidate data for testing.
- `scripts/monitor_report.py` — run monitoring checks and produce a daily report.

---

# Testing & CI

Run unit & integration tests with pytest:

```bash
pytest -q
```

A sample CI workflow should run tests across supported Python versions and linting. Keep test coverage for parsers and index loading tight because they are risk points.

---

# Observability & monitoring

- Export metrics (request counts, latency, error rates, index size, vector ingestion rate) to Prometheus.
- Use a drift detector (statistical test or windowed embedding distribution checks) to detect changes in candidate profile distributions.
- Dashboards in Grafana to visualize hiring funnel metrics and quality of source channels.

---

# Security, privacy & scraping policy

- Keep collected personal data secure and encrypted at rest.
- Limit crawler/scraper rate and obey site `robots.txt` and terms-of-service.
- Store and display only necessary personal fields in the UI; add retention policies and deletion endpoints.
- Document and follow `POLICIES/SCRAPING_POLICY.md` and `POLICIES/PRIVACY.md` before running scrapers at scale.

---

# Roadmap & upgrade suggestions

**Short-term**
- Improve NER extraction with fine-tuned models for CV fields (dates, roles, company names).
- Add multilingual parsing support.
- Create a small admin UI for manual corrections and feedback labeling.

**Medium-term**
- Implement learning-to-rank for candidate ranking using historical hiring decisions as labels.
- Integrate with ATS platforms via webhooks and scheduled ETL.
- Add role-based access control and audit logs.

**Long-term**
- Privacy-preserving vector search (encrypted embeddings / secure enclaves).
- ML-driven anonymization for unbiased screening experiments.

---

# Troubleshooting

- **FAISS fails to load**: verify the FAISS library version and vector `dtype` (float32). Rebuild index if necessary.
- **OCR errors**: check image resolution and preprocessing (deskew, denoise).
- **Scraper blocked / CAPTCHA**: consider official APIs, human-in-the-loop, or rotate proxies responsibly following policy.
- **Slow search**: shard FAISS indices or use IVF+PQ for large datasets and warm up the index at service start.
