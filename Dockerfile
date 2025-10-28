# Dockerfile (multi-target)
# ---------- base stage ----------
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# system deps commonly needed (tesseract, poppler utils for pdf -> images)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for better security
RUN useradd -m appuser
USER appuser

# ---------- deps stage ----------
FROM base AS deps

# copy only requirements to leverage docker cache
COPY --chown=appuser:appuser requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

# ---------- api stage ----------
FROM deps AS api

# copy source
COPY --chown=appuser:appuser . /app

# expose port for uvicorn
EXPOSE 8000

# default command for API target (uvicorn)
CMD ["uvicorn", "src.ai_resume_analyzer.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---------- ui stage ----------
FROM deps AS ui

# copy source
COPY --chown=appuser:appuser . /app

# expose streamlit port
EXPOSE 8501

# streamlit config option if needed
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# default command for UI target (streamlit)
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"]
