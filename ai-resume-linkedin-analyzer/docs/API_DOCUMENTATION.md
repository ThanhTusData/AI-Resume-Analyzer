# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. In production, implement JWT-based authentication.

## Endpoints

### Health Check

#### GET `/health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "ai_service": "available",
    "scraper": "configured"
  }
}
```

---

### Resume Endpoints

#### POST `/api/resumes/upload`
Upload and parse a resume.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF, DOCX, TXT, or image)

**Response:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "john_doe_resume.pdf",
  "message": "Resume uploaded and parsed successfully",
  "status": "success"
}
```

**Errors:**
- 400: Unsupported file type
- 500: Processing error

---

#### POST `/api/resumes/analyze`
Analyze a resume with AI.

**Request:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "analysis_depth": "standard"
}
```

**Response:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall_score": 85.5,
  "strengths": [
    "Strong technical skills",
    "Clear career progression",
    "Quantifiable achievements"
  ],
  "weaknesses": [
    "Missing soft skills",
    "Could use more metrics"
  ],
  "improvements": [
    "Add leadership examples",
    "Include team size managed"
  ],
  "suggested_job_titles": [
    "Senior Software Engineer",
    "Tech Lead",
    "Engineering Manager"
  ],
  "ats_score": 78.0,
  "processing_time": 12.5,
  "status": "success"
}
```

---

#### GET `/api/resumes/{resume_id}`
Get resume details.

**Response:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "john_doe_resume.pdf",
  "skills": ["Python", "Django", "AWS"],
  "experience": [...],
  "education": [...],
  "overall_score": 85.5
}
```

---

#### GET `/api/resumes`
List all resumes.

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 10): Maximum records to return

**Response:**
```json
{
  "total": 25,
  "resumes": [...]
}
```

---

#### DELETE `/api/resumes/{resume_id}`
Delete a resume.

**Response:**
```json
{
  "message": "Resume deleted successfully"
}
```

---

### Job Endpoints

#### GET `/api/jobs`
List jobs with filters.

**Query Parameters:**
- `skip` (int): Pagination offset
- `limit` (int): Results per page
- `keywords` (string): Search keywords
- `location` (string): Location filter
- `remote` (boolean): Remote only

**Response:**
```json
{
  "total": 150,
  "jobs": [
    {
      "job_id": "...",
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "remote": true,
      "required_skills": ["Python", "Django", "AWS"]
    }
  ]
}
```

---

#### GET `/api/jobs/{job_id}`
Get job details.

---

#### POST `/api/jobs`
Create a new job posting.

**Request:**
```json
{
  "title": "Senior Software Engineer",
  "company": "Tech Inc",
  "location": "Remote",
  "description": "...",
  "required_skills": ["Python", "AWS"],
  "job_type": "Full-time",
  "remote": true
}
```

---

### Matching Endpoints

#### POST `/api/matching`
Match resume with jobs.

**Request:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_ids": ["job-id-1", "job-id-2"],
  "top_k": 10,
  "similarity_threshold": 0.7
}
```

**Response:**
```json
{
  "resume_id": "550e8400-e29b-41d4-a716-446655440000",
  "matches_count": 8,
  "matches": [
    {
      "job": {...},
      "overall_score": 87.5,
      "skills_match_score": 90.0,
      "matched_skills": ["Python", "AWS"],
      "missing_skills": ["Kubernetes"],
      "confidence_level": "High"
    }
  ],
  "status": "success"
}
```

---

#### GET `/api/matching/similar/{job_id}`
Find similar jobs.

**Query Parameters:**
- `top_k` (int, default: 5): Number of similar jobs

---

### Statistics Endpoint

#### GET `/api/stats`
Get application statistics.

**Response:**
```json
{
  "total_resumes": 125,
  "total_jobs": 450,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message",
  "status": "error"
}
```

### HTTP Status Codes
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

---

## Rate Limiting

- 60 requests per minute per IP
- 1000 requests per hour per IP