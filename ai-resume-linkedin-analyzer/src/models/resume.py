"""
Resume Data Model
Complete resume data structure with validation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import uuid
import json


class FileType(Enum):
    """Supported resume file types"""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    TXT = "txt"
    IMAGE = "image"


@dataclass
class Resume:
    """
    Resume data model with complete information
    
    Attributes:
        resume_id: Unique identifier
        filename: Original filename
        file_type: Type of resume file
        upload_date: When resume was uploaded
        personal_info: Personal information dictionary
        summary: Professional summary
        experience: List of work experiences
        education: List of education entries
        skills: List of skills
        certifications: List of certifications
        projects: List of projects
        languages: List of languages spoken
        raw_text: Raw extracted text
        word_count: Total word count
        page_count: Number of pages
        parsed_date: When resume was parsed
        analysis_completed: Whether AI analysis is done
        analysis_date: When analysis was completed
        overall_score: Overall resume score (0-100)
    """
    
    # Identifiers
    resume_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    filename: str = ""
    file_type: FileType = FileType.PDF
    upload_date: datetime = field(default_factory=datetime.now)
    
    # Personal Information
    personal_info: Dict[str, str] = field(default_factory=dict)
    
    # Content Sections
    summary: str = ""
    experience: List[Dict[str, any]] = field(default_factory=list)
    education: List[Dict[str, any]] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    projects: List[Dict[str, any]] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    
    # Metadata
    raw_text: str = ""
    word_count: int = 0
    page_count: int = 1
    parsed_date: Optional[datetime] = None
    
    # Analysis Results
    analysis_completed: bool = False
    analysis_date: Optional[datetime] = None
    overall_score: float = 0.0
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Convert file_type to enum if string
        if isinstance(self.file_type, str):
            self.file_type = FileType(self.file_type)
        
        # Initialize personal_info with default structure
        if not self.personal_info:
            self.personal_info = {
                'name': '',
                'email': '',
                'phone': '',
                'location': '',
                'linkedin': '',
                'github': '',
                'website': '',
                'portfolio': ''
            }
    
    def get_full_name(self) -> str:
        """Get full name from personal info"""
        return self.personal_info.get('name', 'Unknown')
    
    def get_email(self) -> str:
        """Get email address"""
        return self.personal_info.get('email', '')
    
    def get_phone(self) -> str:
        """Get phone number"""
        return self.personal_info.get('phone', '')
    
    def get_location(self) -> str:
        """Get location"""
        return self.personal_info.get('location', '')
    
    def get_total_experience_years(self) -> float:
        """
        Calculate total years of experience
        
        Returns:
            Approximate years of experience
        """
        if not self.experience:
            return 0.0
        
        # Simplified calculation: assume 2.5 years per position
        return len(self.experience) * 2.5
    
    def get_highest_degree(self) -> str:
        """
        Get highest educational degree
        
        Returns:
            Highest degree or empty string
        """
        if not self.education:
            return ""
        
        degree_hierarchy = {
            'phd': 5, 'doctorate': 5, 'doctoral': 5,
            'master': 4, 'masters': 4, 'mba': 4, 'ms': 4, 'ma': 4,
            'bachelor': 3, 'bachelors': 3, 'bs': 3, 'ba': 3,
            'associate': 2,
            'diploma': 1, 'certificate': 1
        }
        
        highest = ('', 0)
        for edu in self.education:
            degree = edu.get('degree', '').lower()
            for key, level in degree_hierarchy.items():
                if key in degree and level > highest[1]:
                    highest = (edu.get('degree', ''), level)
        
        return highest[0]
    
    def get_skill_count(self) -> int:
        """Get total number of skills"""
        return len(self.skills)
    
    def has_certification(self, cert_name: str) -> bool:
        """Check if resume has specific certification"""
        return any(cert_name.lower() in cert.lower() for cert in self.certifications)
    
    def is_analyzed(self) -> bool:
        """Check if resume has been analyzed"""
        return self.analysis_completed
    
    def to_dict(self) -> Dict:
        """
        Convert resume to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'resume_id': self.resume_id,
            'filename': self.filename,
            'file_type': self.file_type.value,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'personal_info': self.personal_info,
            'summary': self.summary,
            'experience': self.experience,
            'education': self.education,
            'skills': self.skills,
            'certifications': self.certifications,
            'projects': self.projects,
            'languages': self.languages,
            'word_count': self.word_count,
            'page_count': self.page_count,
            'parsed_date': self.parsed_date.isoformat() if self.parsed_date else None,
            'analysis_completed': self.analysis_completed,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'overall_score': self.overall_score,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Resume':
        """
        Create Resume from dictionary
        
        Args:
            data: Dictionary with resume data
            
        Returns:
            Resume instance
        """
        # Handle datetime fields
        if isinstance(data.get('upload_date'), str):
            data['upload_date'] = datetime.fromisoformat(data['upload_date'])
        
        if isinstance(data.get('parsed_date'), str):
            data['parsed_date'] = datetime.fromisoformat(data['parsed_date'])
        
        if isinstance(data.get('analysis_date'), str):
            data['analysis_date'] = datetime.fromisoformat(data['analysis_date'])
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"Resume(id={self.resume_id[:8]}..., name={self.get_full_name()}, score={self.overall_score:.1f})"
    
    def __str__(self) -> str:
        """Human-readable string"""
        return f"{self.get_full_name()} - {self.filename} (Score: {self.overall_score:.1f}/100)"
