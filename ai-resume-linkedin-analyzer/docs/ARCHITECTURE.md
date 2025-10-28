# System Architecture

## Overview

The AI Resume & LinkedIn Analyzer is built with a modular, scalable architecture that separates concerns into distinct layers.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Streamlit    │  │   Streamlit    │  │   Streamlit    │   │
│  │     Pages      │  │   Components   │  │   Dashboard    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Layer (Optional)                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   FastAPI      │  │   Endpoints    │  │   Middleware   │   │
│  │   Routes       │  │   & Schemas    │  │   (CORS/Auth)  │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   Scraper      │  │   Parsers      │  │   Extractors   │   │
│  │   (Selenium)   │  │   (PDF/DOCX)   │  │   (NLP/NER)    │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  AI Analyzer   │  │  Job Matcher   │  │   Embeddings   │   │
│  │  (LLM Client)  │  │  (FAISS/Cos)   │  │   (OpenAI)     │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   PostgreSQL   │  │     Redis      │  │  Vector Store  │   │
│  │   (SQLAlchemy) │  │    (Cache)     │  │    (FAISS)     │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      External Services                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │   OpenAI API   │  │   Google AI    │  │   LinkedIn     │   │
│  │   (GPT-4)      │  │   (Gemini)     │  │   (Scraping)   │   │
│  └────────────────┘  └────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer

#### Streamlit Application
- **Main App**: Entry point and navigation
- **Pages**: Modular pages for different features
  - LinkedIn Scraper
  - Resume Analyzer
  - Job Matching
  - Analytics Dashboard
- **Components**: Reusable UI elements

### 2. API Layer (Optional)

#### FastAPI Backend
- RESTful API endpoints
- Request validation with Pydantic
- Async support for better performance
- OpenAPI documentation (Swagger/ReDoc)

### 3. Business Logic Layer

#### Scraper Module
- **LinkedIn Scraper**: Automated job extraction
- **Browser Manager**: Selenium WebDriver management
- **Anti-Detection**: Human-like behavior simulation
- **Job Parser**: HTML parsing and data extraction

#### Parser Module
- **PDF Parser**: Extract text from PDFs
- **DOCX Parser**: Parse Word documents
- **Image Parser**: OCR for images (Tesseract)
- **TXT Parser**: Plain text processing

#### Extractor Module
- **Text Cleaner**: Text preprocessing
- **Skill Extractor**: Identify technical and soft skills
- **Experience Extractor**: Parse work history
- **Education Extractor**: Extract educational background

#### AI Analyzer Module
- **LLM Client**: Unified interface for AI providers
- **Resume Analyzer**: Comprehensive resume analysis
- **Prompt Templates**: Optimized prompts for different analyses

#### Matching Module
- **Embedding Generator**: Convert text to vectors
- **Vector Store**: FAISS-based similarity search
- **Job Matcher**: Match resumes with jobs
- **Ranking Algorithm**: Score and rank matches

### 4. Data Layer

#### Database
- **PostgreSQL**: Primary data store
- **SQLAlchemy ORM**: Database abstraction
- **Repositories**: Data access patterns

#### Caching
- **Redis**: Session and result caching
- **In-memory**: Temporary data storage

#### Vector Storage
- **FAISS**: Efficient similarity search
- **Embeddings**: Semantic representations

### 5. External Services

#### AI Services
- OpenAI GPT-4 for text analysis
- Google Gemini as alternative
- Anthropic Claude (optional)

#### Data Sources
- LinkedIn for job postings
- Public APIs (future)

## Data Flow

### Resume Analysis Flow
```
1. User uploads resume → 2. File validation → 3. Parser selection
   ↓
4. Text extraction → 5. Information extraction → 6. AI analysis
   ↓
7. Store results → 8. Display insights
```

### Job Scraping Flow
```
1. User inputs search params → 2. Browser initialization → 3. LinkedIn login
   ↓
4. Job search → 5. Parse job cards → 6. Extract details
   ↓
7. Store in database → 8. Display results
```

### Job Matching Flow
```
1. Select resume + jobs → 2. Generate embeddings → 3. Calculate similarity
   ↓
4. Component scoring → 5. Weighted ranking → 6. Display matches
```

## Technology Stack

### Frontend
- Streamlit 1.31+
- Plotly for visualizations
- Pandas for data manipulation

### Backend
- FastAPI 0.109+
- Uvicorn ASGI server
- SQLAlchemy ORM

### AI/ML
- OpenAI API (GPT-4)
- Google Generative AI
- spaCy (NER)
- Sentence Transformers
- FAISS (vector search)

### Scraping
- Selenium 4.17+
- BeautifulSoup4
- WebDriver Manager

### Database
- PostgreSQL 15+
- Redis 7+
- SQLite (development)

### Infrastructure
- Docker & Docker Compose
- Nginx (reverse proxy)
- Prometheus & Grafana (monitoring)

## Security Considerations

1. **API Keys**: Stored in environment variables
2. **Authentication**: JWT for API access
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Sanitize all inputs
5. **CORS**: Controlled cross-origin requests

## Scalability

### Horizontal Scaling
- Stateless design allows multiple instances
- Load balancing with Nginx
- Session management with Redis

### Vertical Scaling
- Async processing with Celery
- Database connection pooling
- Caching strategies

## Monitoring & Logging

- **Loguru**: Structured logging
- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Sentry**: Error tracking
