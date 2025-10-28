# 🚀 AI Resume & LinkedIn Analyzer

A comprehensive AI-powered platform for analyzing resumes, scraping LinkedIn job postings, and intelligently matching candidates with relevant opportunities.

## ✨ Features

### 🔍 LinkedIn Job Scraper
- Automated job posting extraction from LinkedIn
- Anti-detection mechanisms for reliable scraping
- Session persistence and browser management
- Configurable search parameters (location, keywords, experience level)

### 📄 Resume Analyzer
- Multi-format support (PDF, DOCX, TXT, Images via OCR)
- AI-powered content analysis using OpenAI/Gemini
- Strength and weakness identification
- Skill extraction and categorization
- Education and experience parsing

### 🎯 Job Matching Engine
- Semantic similarity using embeddings (OpenAI/HuggingFace)
- FAISS vector database for efficient matching
- Intelligent ranking algorithm
- Personalized job recommendations

### 📊 Analytics Dashboard
- Visual insights into resume quality
- Match score distributions
- Skill gap analysis
- Career progression suggestions

## 🏗️ Architecture

```
Frontend: Streamlit (Multi-page app)
Backend: FastAPI (Optional REST API)
Scraping: Selenium/Playwright
Parsing: PyPDF2, python-docx, Tesseract OCR
AI: OpenAI GPT-4, Google Gemini
Vector Store: FAISS
Database: PostgreSQL/SQLite
Cache: Redis (Optional)
```

## 📦 Installation

### Prerequisites
- Python 3.9+
- Chrome/Chromium browser
- Tesseract OCR (for image processing)
- PostgreSQL (optional, SQLite by default)

### Quick Start

1. **Clone the repository**
```bash
git clone ...
cd ai-resume-linkedin-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

5. **Initialize database**
```bash
python scripts/init_db.py
```

6. **Run the application**
```bash
streamlit run app/main.py
```

### Docker Installation

```bash
docker-compose up -d
```

Access at: http://localhost:8501

## 🔑 Configuration

Create a `.env` file with:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

# LinkedIn Credentials (for scraping)
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/resume_db

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Application
DEBUG=True
LOG_LEVEL=INFO
```

## 🎮 Usage

### Resume Analysis
1. Navigate to **Resume Analyzer** page
2. Upload your resume (PDF, DOCX, or image)
3. Wait for AI analysis
4. Review strengths, weaknesses, and suggestions

### LinkedIn Job Scraping
1. Go to **LinkedIn Scraper** page
2. Enter search criteria (job title, location, etc.)
3. Start scraping
4. View and save results

### Job Matching
1. Visit **Job Matching** page
2. Select your analyzed resume
3. Match against scraped jobs
4. View ranked opportunities with scores

## 🧪 Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=src tests/
```

## 📚 API Documentation

If using FastAPI backend:

```bash
uvicorn api.main:app --reload
```

Visit: http://localhost:8000/docs

## 🛠️ Development

### Project Structure
```
app/          - Streamlit frontend
src/          - Core business logic
api/          - FastAPI backend (optional)
tests/        - Test suite
config/       - Configuration files
data/         - Data storage
```

### Key Modules
- `src/scraper/` - LinkedIn scraping engine
- `src/parsers/` - Resume parsing (PDF, DOCX, OCR)
- `src/extractors/` - Information extraction
- `src/ai_analyzer/` - AI-powered analysis
- `src/matching/` - Job matching algorithm

### Code Quality
```bash
# Format code
black .
isort .

# Lint
flake8 src/ app/
pylint src/ app/

# Type checking
mypy src/
```

## 🚀 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### AWS/GCP/Azure
See `docs/DEPLOYMENT.md` for detailed guides

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

See `CONTRIBUTING.md` for detailed guidelines.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Google for Gemini AI
- Streamlit for the amazing framework
- FAISS for vector similarity search

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Mobile app
- [ ] Chrome extension
- [ ] Advanced analytics
- [ ] Interview preparation module
- [ ] Salary negotiation insights
- [ ] Cover letter generator

## ⚠️ Disclaimer

This tool is for educational and personal use. Always comply with LinkedIn's Terms of Service and robots.txt when scraping. Use responsibly and ethically.
