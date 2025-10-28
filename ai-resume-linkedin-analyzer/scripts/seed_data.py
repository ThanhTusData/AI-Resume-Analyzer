import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger

from src.models.resume import Resume, FileType
from src.models.job import Job, JobType, ExperienceLevel
from src.database.resume_repository import ResumeRepository
from src.database.job_repository import JobRepository


def seed_resumes(repo: ResumeRepository, count: int = 5):
    """Seed sample resumes"""
    logger.info(f"Seeding {count} sample resumes...")
    
    sample_resumes = [
        {
            "filename": "john_doe_resume.pdf",
            "skills": ["Python", "Django", "PostgreSQL", "AWS", "Docker"],
            "summary": "Senior Software Engineer with 5+ years of experience",
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020-2023",
                    "description": "Led development of microservices architecture"
                }
            ]
        },
        {
            "filename": "jane_smith_resume.pdf",
            "skills": ["Machine Learning", "Python", "TensorFlow", "SQL", "Data Analysis"],
            "summary": "Data Scientist passionate about ML and AI",
            "experience": [
                {
                    "title": "Data Scientist",
                    "company": "AI Solutions",
                    "duration": "2019-2023",
                    "description": "Built predictive models for customer analytics"
                }
            ]
        },
        {
            "filename": "bob_johnson_resume.pdf",
            "skills": ["React", "Node.js", "JavaScript", "MongoDB", "AWS"],
            "summary": "Full-stack Developer with focus on modern web technologies",
            "experience": [
                {
                    "title": "Full Stack Developer",
                    "company": "Web Innovations",
                    "duration": "2018-2023",
                    "description": "Developed responsive web applications"
                }
            ]
        }
    ]
    
    for i, data in enumerate(sample_resumes[:count]):
        resume = Resume(
            filename=data["filename"],
            file_type=FileType.PDF,
            skills=data["skills"],
            summary=data["summary"],
            experience=data["experience"],
            raw_text=f"Sample resume content for {data['filename']}",
            word_count=random.randint(300, 800),
            upload_date=datetime.now() - timedelta(days=random.randint(1, 30)),
            analysis_completed=True,
            overall_score=random.uniform(60, 95)
        )
        
        repo.save_resume(resume)
        logger.info(f"Created resume: {resume.filename}")


def seed_jobs(repo: JobRepository, count: int = 10):
    """Seed sample jobs"""
    logger.info(f"Seeding {count} sample jobs...")
    
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "company": "Tech Giants Inc",
            "location": "San Francisco, CA",
            "remote": True,
            "description": "Looking for experienced Python developer",
            "required_skills": ["Python", "Django", "PostgreSQL", "AWS"],
            "job_type": JobType.FULL_TIME,
            "experience_level": ExperienceLevel.SENIOR
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Innovations",
            "location": "New York, NY",
            "remote": False,
            "description": "Build cutting-edge ML models",
            "required_skills": ["Python", "TensorFlow", "Machine Learning", "SQL"],
            "job_type": JobType.FULL_TIME,
            "experience_level": ExperienceLevel.MID
        },
        {
            "title": "Full Stack Developer",
            "company": "Startup XYZ",
            "location": "Austin, TX",
            "remote": True,
            "description": "Join our growing team",
            "required_skills": ["React", "Node.js", "MongoDB", "AWS"],
            "job_type": JobType.FULL_TIME,
            "experience_level": ExperienceLevel.MID
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "location": "Boston, MA",
            "remote": True,
            "description": "Analyze complex datasets",
            "required_skills": ["Python", "R", "SQL", "Data Analysis", "Statistics"],
            "job_type": JobType.FULL_TIME,
            "experience_level": ExperienceLevel.SENIOR
        },
        {
            "title": "DevOps Engineer",
            "company": "Cloud Services Co",
            "location": "Seattle, WA",
            "remote": True,
            "description": "Manage cloud infrastructure",
            "required_skills": ["AWS", "Docker", "Kubernetes", "Python", "Linux"],
            "job_type": JobType.FULL_TIME,
            "experience_level": ExperienceLevel.MID
        }
    ]
    
    for i, data in enumerate(sample_jobs[:count]):
        job = Job(
            title=data["title"],
            company=data["company"],
            location=data["location"],
            remote=data["remote"],
            description=data["description"],
            required_skills=data["required_skills"],
            job_type=data["job_type"],
            experience_level=data["experience_level"],
            posted_date=datetime.now() - timedelta(days=random.randint(1, 14)),
            salary_min=random.randint(80000, 120000),
            salary_max=random.randint(120000, 180000)
        )
        
        repo.save_job(job)
        logger.info(f"Created job: {job.title} at {job.company}")


def main():
    """Main seeding function"""
    logger.info("=" * 50)
    logger.info("Starting database seeding")
    logger.info("=" * 50)
    
    resume_repo = ResumeRepository()
    job_repo = JobRepository()
    
    # Seed data
    seed_resumes(resume_repo, count=5)
    seed_jobs(job_repo, count=10)
    
    logger.info("=" * 50)
    logger.info("✅ Database seeding completed!")
    logger.info(f"Total resumes: {resume_repo.count_all()}")
    logger.info(f"Total jobs: {job_repo.count_all()}")
    logger.info("=" * 50)


if __name__ == "__main__":
    logger.add("logs/seed_data.log", rotation="10 MB")
    main()