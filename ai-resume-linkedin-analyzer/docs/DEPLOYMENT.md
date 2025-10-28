# Deployment Guide

## Prerequisites

- Python 3.9+
- Docker & Docker Compose
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (optional)
- API keys for OpenAI/Google AI

## Local Development

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/yourusername/ai-resume-linkedin-analyzer.git
cd ai-resume-linkedin-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### 3. Initialize Database

```bash
python scripts/init_db.py
python scripts/seed_data.py  # Optional: add sample data
```

### 4. Run Application

```bash
# Streamlit app
streamlit run app/main.py

# FastAPI (optional)
uvicorn api.main:app --reload
```

---

## Docker Deployment

### 1. Build Images

```bash
docker-compose build
```

### 2. Start Services

```bash
docker-compose up -d
```

### 3. Verify Deployment

```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Applications

- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

---

## Production Deployment

### Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

### AWS (EC2)

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Open ports: 22, 80, 443, 8501, 8000

2. **SSH and Setup**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone your-repo
cd ai-resume-linkedin-analyzer
docker-compose up -d
```

3. **Setup Nginx (optional)**
```bash
sudo apt install nginx
# Configure reverse proxy
```

### Google Cloud Platform (Cloud Run)

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/resume-analyzer

# Deploy
gcloud run deploy resume-analyzer \
  --image gcr.io/PROJECT_ID/resume-analyzer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Environment Variables

### Required
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Optional
```
GOOGLE_API_KEY=...
REDIS_URL=redis://localhost:6379
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...
```

---

## Monitoring

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check database
docker-compose exec postgres pg_isready
```

### Logs

```bash
# View application logs
docker-compose logs -f streamlit

# View all logs
docker-compose logs -f
```

---

## Backup & Recovery

### Database Backup

```bash
# Backup
docker-compose exec postgres pg_dump -U postgres resume_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres resume_db < backup.sql
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
```bash
# Find and kill process
lsof -ti:8501 | xargs kill -9
```

2. **Database connection error**
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check network connectivity

3. **API key errors**
- Verify keys in .env
- Check API quotas
- Validate key formats
