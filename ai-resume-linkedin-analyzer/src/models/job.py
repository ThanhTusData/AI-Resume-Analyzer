"""
Job Data Model
Complete job posting data structure
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid
import json


class JobType(Enum):
    """Job types"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"
    VOLUNTEER = "Volunteer"


class ExperienceLevel(Enum):
    """Experience levels"""
    ENTRY = "Entry level"
    MID = "Mid-Senior level"
    SENIOR = "Senior level"
    DIRECTOR = "Director"
    EXECUTIVE = "Executive"
    ASSOCIATE = "Associate"


@dataclass
class Job:
    """
    Job posting data model
    
    Attributes:
        job_id: Unique identifier
        title: Job title
        company: Company name
        location: Job location
        remote: Whether job is remote
        description: Full job description
        requirements: Job requirements
        responsibilities: Job responsibilities
        job_type: Type of employment
        experience_level: Required experience level
        experience_required: Required years of experience
        education_required: Required education
        required_skills: List of required skills
        preferred_skills: List of preferred skills
        salary_min: Minimum salary
        salary_max: Maximum salary
        salary_currency: Salary currency
        posted_date: When job was posted
        scraped_date: When job was scraped
        url: Job posting URL
        source: Source platform (LinkedIn, etc)
        company_size: Company size range
        industry: Company industry
        company_description: About the company
        applicant_count: Number of applicants
        easy_apply: Whether easy apply is available
    """
    
    # Identifiers
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Basic Info
    title: str = ""
    company: str = ""
    location: str = ""
    remote: bool = False
    
    # Job Details
    description: str = ""
    requirements: str = ""
    responsibilities: str = ""
    
    # Classification
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    experience_required: str = ""
    education_required: str = ""
    
    # Skills
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    
    # Compensation
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "USD"
    
    # Metadata
    posted_date: Optional[datetime] = None
    scraped_date: datetime = field(default_factory=datetime.now)
    url: str = ""
    source: str = "LinkedIn"
    
    # Company Info
    company_size: Optional[str] = None
    industry: Optional[str] = None
    company_description: Optional[str] = None
    
    # Application Info
    applicant_count: int = 0
    easy_apply: bool = False
    
    def __post_init__(self):
        """Post-initialization processing"""
        # Convert enums if needed
        if isinstance(self.job_type, str):
            try:
                self.job_type = JobType(self.job_type)
            except ValueError:
                self.job_type = None
        
        if isinstance(self.experience_level, str):
            try:
                self.experience_level = ExperienceLevel(self.experience_level)
            except ValueError:
                self.experience_level = None
    
    def get_salary_range(self) -> str:
        """
        Get formatted salary range
        
        Returns:
            Formatted salary string
        """
        symbol = {'USD': '$', 'EUR': '€', 'GBP': '£', 'VND': '₫'}.get(self.salary_currency, '$')
        
        if self.salary_min and self.salary_max:
            if self.salary_currency == 'VND':
                return f"{self.salary_min:,.0f}{symbol} - {self.salary_max:,.0f}{symbol}"
            return f"{symbol}{self.salary_min:,.0f} - {symbol}{self.salary_max:,.0f}"
        elif self.salary_min:
            if self.salary_currency == 'VND':
                return f"{self.salary_min:,.0f}{symbol}+"
            return f"{symbol}{self.salary_min:,.0f}+"
        elif self.salary_max:
            if self.salary_currency == 'VND':
                return f"Up to {self.salary_max:,.0f}{symbol}"
            return f"Up to {symbol}{self.salary_max:,.0f}"
        
        return "Not specified"
    
    def is_remote_or_hybrid(self) -> bool:
        """Check if job is remote or hybrid"""
        return self.remote or 'hybrid' in self.location.lower()
    
    def days_since_posted(self) -> Optional[int]:
        """
        Calculate days since job was posted
        
        Returns:
            Number of days or None
        """
        if self.posted_date:
            delta = datetime.now() - self.posted_date
            return delta.days
        return None
    
    def get_skill_count(self) -> int:
        """Get total number of required skills"""
        return len(self.required_skills)
    
    def has_skill(self, skill: str) -> bool:
        """Check if job requires specific skill"""
        skill_lower = skill.lower()
        return any(skill_lower in s.lower() for s in self.required_skills)
    
    def is_recent(self, days: int = 7) -> bool:
        """Check if job was posted recently"""
        days_ago = self.days_since_posted()
        return days_ago is not None and days_ago <= days
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'job_id': self.job_id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'remote': self.remote,
            'description': self.description,
            'requirements': self.requirements,
            'responsibilities': self.responsibilities,
            'job_type': self.job_type.value if self.job_type else None,
            'experience_level': self.experience_level.value if self.experience_level else None,
            'experience_required': self.experience_required,
            'education_required': self.education_required,
            'required_skills': self.required_skills,
            'preferred_skills': self.preferred_skills,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'salary_currency': self.salary_currency,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'scraped_date': self.scraped_date.isoformat(),
            'url': self.url,
            'source': self.source,
            'company_size': self.company_size,
            'industry': self.industry,
            'company_description': self.company_description,
            'applicant_count': self.applicant_count,
            'easy_apply': self.easy_apply,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        """Create Job from dictionary"""
        # Handle datetime fields
        if isinstance(data.get('posted_date'), str):
            data['posted_date'] = datetime.fromisoformat(data['posted_date'])
        
        if isinstance(data.get('scraped_date'), str):
            data['scraped_date'] = datetime.fromisoformat(data['scraped_date'])
        
        return cls(**data)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"Job(id={self.job_id[:8]}..., title={self.title}, company={self.company})"
    
    def __str__(self) -> str:
        """Human-readable string"""
        location_str = "Remote" if self.remote else self.location
        return f"{self.title} at {self.company} ({location_str})"
