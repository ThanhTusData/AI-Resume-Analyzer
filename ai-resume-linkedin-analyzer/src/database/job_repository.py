"""
Job Repository
Database operations for jobs
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Session
from loguru import logger

from src.database.db_manager import Base, get_session
from src.models.job import Job, JobType, ExperienceLevel


class JobDB(Base):
    """Job database model"""
    __tablename__ = "jobs"
    
    # Primary key
    job_id = Column(String, primary_key=True, index=True)
    
    # Basic info
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, index=True)
    remote = Column(Boolean, default=False, index=True)
    
    # Job details
    description = Column(Text)
    requirements = Column(Text)
    responsibilities = Column(Text)
    
    # Classification
    job_type = Column(String, index=True)
    experience_level = Column(String, index=True)
    experience_required = Column(String)
    education_required = Column(String)
    
    # Skills (stored as JSON)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    
    # Compensation
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String, default="USD")
    
    # Metadata
    posted_date = Column(DateTime, index=True)
    scraped_date = Column(DateTime, default=datetime.now, index=True)
    url = Column(String)
    source = Column(String, default="LinkedIn", index=True)
    
    # Company info
    company_size = Column(String)
    industry = Column(String, index=True)
    company_description = Column(Text)
    
    # Application info
    applicant_count = Column(Integer, default=0)
    easy_apply = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class JobRepository:
    """Repository for job database operations"""
    
    def __init__(self):
        """Initialize repository"""
        self.session: Optional[Session] = None
    
    def get_session(self) -> Session:
        """Get or create database session"""
        if self.session is None:
            self.session = get_session()
        return self.session
    
    def save_job(self, job: Job) -> bool:
        """
        Save job to database
        
        Args:
            job: Job object to save
            
        Returns:
            True if successful
        """
        try:
            session = self.get_session()
            
            # Check if exists
            existing = session.query(JobDB).filter(
                JobDB.job_id == job.job_id
            ).first()
            
            if existing:
                logger.info(f"Job already exists: {job.job_id}")
                return False
            
            # Create new
            job_db = self._job_to_db(job)
            session.add(job_db)
            session.commit()
            
            logger.info(f"Saved new job: {job.job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save job: {str(e)}")
            session.rollback()
            return False
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        try:
            session = self.get_session()
            job_db = session.query(JobDB).filter(
                JobDB.job_id == job_id
            ).first()
            
            if job_db:
                return self._db_to_job(job_db)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get job: {str(e)}")
            return None
    
    def get_all_jobs(self, skip: int = 0, limit: int = 100) -> List[Job]:
        """Get all jobs with pagination"""
        try:
            session = self.get_session()
            jobs_db = session.query(JobDB).order_by(
                JobDB.scraped_date.desc()
            ).offset(skip).limit(limit).all()
            
            return [self._db_to_job(j) for j in jobs_db]
            
        except Exception as e:
            logger.error(f"Failed to get all jobs: {str(e)}")
            return []
    
    def get_recent_jobs(self, limit: int = 10, days: int = 7) -> List[Job]:
        """Get recent jobs"""
        try:
            session = self.get_session()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            jobs_db = session.query(JobDB).filter(
                JobDB.scraped_date >= cutoff_date
            ).order_by(
                JobDB.scraped_date.desc()
            ).limit(limit).all()
            
            return [self._db_to_job(j) for j in jobs_db]
            
        except Exception as e:
            logger.error(f"Failed to get recent jobs: {str(e)}")
            return []
    
    def search_jobs(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        remote: Optional[bool] = None,
        job_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Job]:
        """
        Search jobs with filters
        
        Args:
            keywords: Search keywords
            location: Location filter
            remote: Remote filter
            job_type: Job type filter
            limit: Maximum results
            
        Returns:
            List of matching Job objects
        """
        try:
            session = self.get_session()
            query = session.query(JobDB)
            
            if keywords:
                query = query.filter(
                    (JobDB.title.ilike(f"%{keywords}%")) |
                    (JobDB.description.ilike(f"%{keywords}%"))
                )
            
            if location:
                query = query.filter(JobDB.location.ilike(f"%{location}%"))
            
            if remote is not None:
                query = query.filter(JobDB.remote == remote)
            
            if job_type:
                query = query.filter(JobDB.job_type == job_type)
            
            jobs_db = query.order_by(JobDB.scraped_date.desc()).limit(limit).all()
            return [self._db_to_job(j) for j in jobs_db]
            
        except Exception as e:
            logger.error(f"Failed to search jobs: {str(e)}")
            return []
    
    def delete_job(self, job_id: str) -> bool:
        """Delete job"""
        try:
            session = self.get_session()
            deleted = session.query(JobDB).filter(
                JobDB.job_id == job_id
            ).delete()
            session.commit()
            
            if deleted:
                logger.info(f"Deleted job: {job_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete job: {str(e)}")
            session.rollback()
            return False
    
    def count_all(self) -> int:
        """Count all jobs"""
        try:
            session = self.get_session()
            return session.query(JobDB).count()
        except Exception:
            return 0
    
    def count_remote(self) -> int:
        """Count remote jobs"""
        try:
            session = self.get_session()
            return session.query(JobDB).filter(JobDB.remote == True).count()
        except Exception:
            return 0
    
    def get_statistics(self) -> dict:
        """Get job statistics"""
        try:
            session = self.get_session()
            
            total = session.query(JobDB).count()
            remote = session.query(JobDB).filter(JobDB.remote == True).count()
            
            return {
                'total': total,
                'remote': remote,
                'onsite': total - remote
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    def _job_to_db(self, job: Job) -> JobDB:
        """Convert Job to JobDB"""
        return JobDB(
            job_id=job.job_id,
            title=job.title,
            company=job.company,
            location=job.location,
            remote=job.remote,
            description=job.description,
            requirements=job.requirements,
            responsibilities=job.responsibilities,
            job_type=job.job_type.value if job.job_type else None,
            experience_level=job.experience_level.value if job.experience_level else None,
            experience_required=job.experience_required,
            education_required=job.education_required,
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            salary_currency=job.salary_currency,
            posted_date=job.posted_date,
            scraped_date=job.scraped_date,
            url=job.url,
            source=job.source,
            company_size=job.company_size,
            industry=job.industry,
            company_description=job.company_description,
            applicant_count=job.applicant_count,
            easy_apply=job.easy_apply
        )
    
    def _db_to_job(self, job_db: JobDB) -> Job:
        """Convert JobDB to Job"""
        return Job(
            job_id=job_db.job_id,
            title=job_db.title,
            company=job_db.company,
            location=job_db.location or "",
            remote=job_db.remote,
            description=job_db.description or "",
            requirements=job_db.requirements or "",
            responsibilities=job_db.responsibilities or "",
            job_type=JobType(job_db.job_type) if job_db.job_type else None,
            experience_level=ExperienceLevel(job_db.experience_level) if job_db.experience_level else None,
            experience_required=job_db.experience_required or "",
            education_required=job_db.education_required or "",
            required_skills=job_db.required_skills or [],
            preferred_skills=job_db.preferred_skills or [],
            salary_min=job_db.salary_min,
            salary_max=job_db.salary_max,
            salary_currency=job_db.salary_currency or "USD",
            posted_date=job_db.posted_date,
            scraped_date=job_db.scraped_date,
            url=job_db.url or "",
            source=job_db.source or "LinkedIn",
            company_size=job_db.company_size,
            industry=job_db.industry,
            company_description=job_db.company_description,
            applicant_count=job_db.applicant_count or 0,
            easy_apply=job_db.easy_apply
        )