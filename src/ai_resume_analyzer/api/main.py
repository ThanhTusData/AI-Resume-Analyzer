# src/ai_resume_analyzer/api/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from .routes import health, analyze, search

import os
import logging
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

# prometheus client
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="AI Resume Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics - basic
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency (s)", ["endpoint"])

# Sentry init (if DSN provided)
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", 0.0)))
    # wrap app with Sentry ASGI middleware automatically below after routes added


# include existing routers
app.include_router(health.router, prefix="")
app.include_router(analyze.router, prefix="/analyze")
app.include_router(search.router, prefix="/search")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    import time
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        # let Sentry capture if configured
        logger.exception("Unhandled exception in request")
        raise
    latency = time.time() - start
    endpoint = request.url.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=str(response.status_code)).inc()
    return response


@app.get("/metrics")
def metrics():
    """
    Prometheus plain-text metrics endpoint. Scrape only aggregated metrics (no PII).
    """
    data = generate_latest()
    return PlainTextResponse(content=data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
def startup():
    logger.info("Starting AI Resume Analyzer API")
    # Optionally load heavy singletons in background if desired (encoder/index)
    # Avoid loading models unnecessarily in unit tests.

# If Sentry configured, wrap app
if SENTRY_DSN:
    app.add_middleware(SentryAsgiMiddleware)
