"""
Resume Repository
Database operations for resumes
"""

from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Session
from loguru import logger

from src.database.db_manager import Base, get_session
from src.models.resume import Resume, FileType


class ResumeDB(Base):
    """Resume database model"""
    __tablename__ = "resumes"
    
    # Primary key
    resume_id = Column(String, primary_key=True, index=True)
    
    # Basic info
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.now, index=True)
    
    # Personal info (stored as JSON)
    personal_info = Column(JSON, default=dict)
    
    # Content sections (stored as JSON)
    summary = Column(Text)
    experience = Column(JSON, default=list)
    education = Column(JSON, default=list)
    skills = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    languages = Column(JSON, default=list)
    
    # Metadata
    raw_text = Column(Text)
    word_count = Column(Integer, default=0)
    page_count = Column(Integer, default=1)
    parsed_date = Column(DateTime)
    
    # Analysis results
    analysis_completed = Column(Boolean, default=False, index=True)
    analysis_date = Column(DateTime)
    overall_score = Column(Float, default=0.0, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ResumeRepository:
    """Repository for resume database operations"""
    
    def __init__(self):
        """Initialize repository"""
        self.session: Optional[Session] = None
    
    def get_session(self) -> Session:
        """Get or create database session"""
        if self.session is None:
            self.session = get_session()
        return self.session
    
    def save_resume(self, resume: Resume) -> bool:
        """
        Save or update resume
        
        Args:
            resume: Resume object to save
            
        Returns:
            True if successful
        """
        try:
            session = self.get_session()
            
            # Check if exists
            existing = session.query(ResumeDB).filter(
                ResumeDB.resume_id == resume.resume_id
            ).first()
            
            if existing:
                # Update existing
                self._update_resume_db(existing, resume)
                logger.info(f"Updated resume: {resume.resume_id}")
            else:
                # Create new
                resume_db = self._resume_to_db(resume)
                session.add(resume_db)
                logger.info(f"Created new resume: {resume.resume_id}")
            
            session.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to save resume: {str(e)}")
            session.rollback()
            return False
    
    def get_resume(self, resume_id: str) -> Optional[Resume]:
        """
        Get resume by ID
        
        Args:
            resume_id: Resume ID
            
        Returns:
            Resume object or None
        """
        try:
            session = self.get_session()
            resume_db = session.query(ResumeDB).filter(
                ResumeDB.resume_id == resume_id
            ).first()
            
            if resume_db:
                return self._db_to_resume(resume_db)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get resume: {str(e)}")
            return None
    
    def get_all_resumes(self, skip: int = 0, limit: int = 100) -> List[Resume]:
        """
        Get all resumes with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of Resume objects
        """
        try:
            session = self.get_session()
            resumes_db = session.query(ResumeDB).order_by(
                ResumeDB.upload_date.desc()
            ).offset(skip).limit(limit).all()
            
            return [self._db_to_resume(r) for r in resumes_db]
            
        except Exception as e:
            logger.error(f"Failed to get all resumes: {str(e)}")
            return []
    
    def get_recent_resumes(self, limit: int = 10, days: int = 30) -> List[Resume]:
        """
        Get recent resumes
        
        Args:
            limit: Maximum number of resumes
            days: Number of days to look back
            
        Returns:
            List of Resume objects
        """
        try:
            session = self.get_session()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            resumes_db = session.query(ResumeDB).filter(
                ResumeDB.upload_date >= cutoff_date
            ).order_by(
                ResumeDB.upload_date.desc()
            ).limit(limit).all()
            
            return [self._db_to_resume(r) for r in resumes_db]
            
        except Exception as e:
            logger.error(f"Failed to get recent resumes: {str(e)}")
            return []
    
    def get_analyzed_resumes(self, skip: int = 0, limit: int = 100) -> List[Resume]:
        """Get only analyzed resumes"""
        try:
            session = self.get_session()
            resumes_db = session.query(ResumeDB).filter(
                ResumeDB.analysis_completed == True
            ).order_by(
                ResumeDB.overall_score.desc()
            ).offset(skip).limit(limit).all()
            
            return [self._db_to_resume(r) for r in resumes_db]
            
        except Exception as e:
            logger.error(f"Failed to get analyzed resumes: {str(e)}")
            return []
    
    def get_top_resumes(self, limit: int = 10, min_score: float = 70.0) -> List[Resume]:
        """
        Get top scoring resumes
        
        Args:
            limit: Maximum number of resumes
            min_score: Minimum score threshold
            
        Returns:
            List of top Resume objects
        """
        try:
            session = self.get_session()
            resumes_db = session.query(ResumeDB).filter(
                ResumeDB.overall_score >= min_score
            ).order_by(
                ResumeDB.overall_score.desc()
            ).limit(limit).all()
            
            return [self._db_to_resume(r) for r in resumes_db]
            
        except Exception as e:
            logger.error(f"Failed to get top resumes: {str(e)}")
            return []
    
    def search_resumes(self, query: str, limit: int = 50) -> List[Resume]:
        """
        Search resumes by filename or content
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching Resume objects
        """
        try:
            session = self.get_session()
            resumes_db = session.query(ResumeDB).filter(
                (ResumeDB.filename.ilike(f"%{query}%")) |
                (ResumeDB.raw_text.ilike(f"%{query}%"))
            ).limit(limit).all()
            
            return [self._db_to_resume(r) for r in resumes_db]
            
        except Exception as e:
            logger.error(f"Failed to search resumes: {str(e)}")
            return []
    
    def delete_resume(self, resume_id: str) -> bool:
        """
        Delete resume
        
        Args:
            resume_id: Resume ID
            
        Returns:
            True if successful
        """
        try:
            session = self.get_session()
            deleted = session.query(ResumeDB).filter(
                ResumeDB.resume_id == resume_id
            ).delete()
            session.commit()
            
            if deleted:
                logger.info(f"Deleted resume: {resume_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete resume: {str(e)}")
            session.rollback()
            return False
    
    def count_all(self) -> int:
        """Count all resumes"""
        try:
            session = self.get_session()
            return session.query(ResumeDB).count()
        except Exception:
            return 0
    
    def count_analyzed(self) -> int:
        """Count analyzed resumes"""
        try:
            session = self.get_session()
            return session.query(ResumeDB).filter(
                ResumeDB.analysis_completed == True
            ).count()
        except Exception:
            return 0
    
    def get_statistics(self) -> dict:
        """Get resume statistics"""
        try:
            session = self.get_session()
            
            total = session.query(ResumeDB).count()
            analyzed = session.query(ResumeDB).filter(
                ResumeDB.analysis_completed == True
            ).count()
            
            avg_score = session.query(ResumeDB).filter(
                ResumeDB.overall_score > 0
            ).with_entities(ResumeDB.overall_score).all()
            
            avg_score_value = sum(s[0] for s in avg_score) / len(avg_score) if avg_score else 0
            
            return {
                'total': total,
                'analyzed': analyzed,
                'unanalyzed': total - analyzed,
                'avg_score': avg_score_value
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    def _resume_to_db(self, resume: Resume) -> ResumeDB:
        """Convert Resume to ResumeDB"""
        return ResumeDB(
            resume_id=resume.resume_id,
            filename=resume.filename,
            file_type=resume.file_type.value,
            upload_date=resume.upload_date,
            personal_info=resume.personal_info,
            summary=resume.summary,
            experience=resume.experience,
            education=resume.education,
            skills=resume.skills,
            certifications=resume.certifications,
            projects=resume.projects,
            languages=resume.languages,
            raw_text=resume.raw_text,
            word_count=resume.word_count,
            page_count=resume.page_count,
            parsed_date=resume.parsed_date,
            analysis_completed=resume.analysis_completed,
            analysis_date=resume.analysis_date,
            overall_score=resume.overall_score
        )
    
    def _db_to_resume(self, resume_db: ResumeDB) -> Resume:
        """Convert ResumeDB to Resume"""
        return Resume(
            resume_id=resume_db.resume_id,
            filename=resume_db.filename,
            file_type=FileType(resume_db.file_type),
            upload_date=resume_db.upload_date,
            personal_info=resume_db.personal_info or {},
            summary=resume_db.summary or "",
            experience=resume_db.experience or [],
            education=resume_db.education or [],
            skills=resume_db.skills or [],
            certifications=resume_db.certifications or [],
            projects=resume_db.projects or [],
            languages=resume_db.languages or [],
            raw_text=resume_db.raw_text or "",
            word_count=resume_db.word_count or 0,
            page_count=resume_db.page_count or 1,
            parsed_date=resume_db.parsed_date,
            analysis_completed=resume_db.analysis_completed,
            analysis_date=resume_db.analysis_date,
            overall_score=resume_db.overall_score
        )
    
    def _update_resume_db(self, resume_db: ResumeDB, resume: Resume):
        """Update ResumeDB with Resume data"""
        resume_db.filename = resume.filename
        resume_db.file_type = resume.file_type.value
        resume_db.personal_info = resume.personal_info
        resume_db.summary = resume.summary
        resume_db.experience = resume.experience
        resume_db.education = resume.education
        resume_db.skills = resume.skills
        resume_db.certifications = resume.certifications
        resume_db.projects = resume.projects
        resume_db.languages = resume.languages
        resume_db.raw_text = resume.raw_text
        resume_db.word_count = resume.word_count
        resume_db.page_count = resume.page_count
        resume_db.analysis_completed = resume.analysis_completed
        resume_db.analysis_date = resume.analysis_date
        resume_db.overall_score = resume.overall_score
        resume_db.updated_at = datetime.now()