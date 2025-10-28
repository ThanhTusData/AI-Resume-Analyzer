"""
Match Result Model
Stores job-resume matching results
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid
import json

from src.models.job import Job


@dataclass
class MatchResult:
    """
    Match result between resume and job
    
    Attributes:
        match_id: Unique identifier
        resume_id: ID of matched resume
        job: Job object
        overall_score: Overall match score (0-100)
        skills_match_score: Skills matching score
        experience_match_score: Experience matching score
        education_match_score: Education matching score
        semantic_similarity_score: Semantic similarity score
        location_match_score: Location matching score
        matched_skills: List of matched skills
        missing_skills: List of missing skills
        explanation: Human-readable explanation
        confidence_level: Confidence level
        matched_date: When match was created
    """
    
    # Identifiers
    match_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resume_id: str = ""
    job: Optional[Job] = None
    
    # Scores (0-100 scale)
    overall_score: float = 0.0
    skills_match_score: float = 0.0
    experience_match_score: float = 0.0
    education_match_score: float = 0.0
    semantic_similarity_score: float = 0.0
    location_match_score: float = 0.0
    
    # Details
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    explanation: str = ""
    confidence_level: str = "Medium"
    
    # Metadata
    matched_date: datetime = field(default_factory=datetime.now)
    
    def is_strong_match(self, threshold: float = 75.0) -> bool:
        """Check if this is a strong match"""
        return self.overall_score >= threshold
    
    def is_good_match(self, threshold: float = 60.0) -> bool:
        """Check if this is a good match"""
        return self.overall_score >= threshold
    
    def get_match_percentage(self) -> str:
        """Get formatted match percentage"""
        return f"{self.overall_score:.1f}%"
    
    def get_skills_gap(self) -> int:
        """Get number of missing skills"""
        return len(self.missing_skills)
    
    def get_skills_match_ratio(self) -> float:
        """Get ratio of matched to total skills"""
        total = len(self.matched_skills) + len(self.missing_skills)
        if total == 0:
            return 0.0
        return len(self.matched_skills) / total
    
    def get_confidence_emoji(self) -> str:
        """Get emoji for confidence level"""
        emojis = {
            'Very High': '🟢',
            'High': '🟢',
            'Medium': '🟡',
            'Low': '🔴',
            'Very Low': '🔴'
        }
        return emojis.get(self.confidence_level, '⚪')
    
    def get_score_breakdown(self) -> dict:
        """Get detailed score breakdown"""
        return {
            'skills': self.skills_match_score,
            'experience': self.experience_match_score,
            'education': self.education_match_score,
            'semantic': self.semantic_similarity_score,
            'location': self.location_match_score,
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'match_id': self.match_id,
            'resume_id': self.resume_id,
            'job': self.job.to_dict() if self.job else None,
            'overall_score': self.overall_score,
            'skills_match_score': self.skills_match_score,
            'experience_match_score': self.experience_match_score,
            'education_match_score': self.education_match_score,
            'semantic_similarity_score': self.semantic_similarity_score,
            'location_match_score': self.location_match_score,
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'explanation': self.explanation,
            'confidence_level': self.confidence_level,
            'matched_date': self.matched_date.isoformat(),
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"MatchResult(id={self.match_id[:8]}..., score={self.overall_score:.1f}%)"
    
    def __str__(self) -> str:
        """Human-readable string"""
        job_title = self.job.title if self.job else "Unknown"
        return f"Match: {job_title} - {self.overall_score:.1f}% ({self.confidence_level})"
