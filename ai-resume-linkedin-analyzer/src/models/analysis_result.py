"""
Analysis Result Model
Stores resume analysis results from AI
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
import uuid
import json


@dataclass
class AnalysisResult:
    """
    Resume analysis result from AI
    
    Attributes:
        analysis_id: Unique identifier
        resume_id: ID of analyzed resume
        overall_score: Overall resume score
        ats_score: ATS compatibility score
        content_score: Content quality score
        formatting_score: Formatting quality score
        strengths: List of resume strengths
        weaknesses: List of resume weaknesses
        improvements: List of improvement suggestions
        suggested_job_titles: Recommended job titles
        skill_analysis: Detailed skill analysis
        experience_analysis: Experience analysis
        education_analysis: Education analysis
        extracted_keywords: Keywords found in resume
        missing_keywords: Missing important keywords
        summary: Executive summary
        analysis_date: When analysis was performed
        ai_model_used: AI model used for analysis
        processing_time: Time taken for analysis
    """
    
    # Identifiers
    analysis_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resume_id: str = ""
    
    # Scores (0-100 scale)
    overall_score: float = 0.0
    ats_score: float = 0.0
    content_score: float = 0.0
    formatting_score: float = 0.0
    
    # Insights
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    suggested_job_titles: List[str] = field(default_factory=list)
    
    # Detailed Analysis
    skill_analysis: Dict[str, any] = field(default_factory=dict)
    experience_analysis: Dict[str, any] = field(default_factory=dict)
    education_analysis: Dict[str, any] = field(default_factory=dict)
    
    # Keywords
    extracted_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    
    # Summary
    summary: str = ""
    
    # Metadata
    analysis_date: datetime = field(default_factory=datetime.now)
    ai_model_used: str = "gpt-4"
    processing_time: float = 0.0
    
    def is_excellent(self, threshold: float = 85.0) -> bool:
        """Check if resume is excellent"""
        return self.overall_score >= threshold
    
    def is_good(self, threshold: float = 70.0) -> bool:
        """Check if resume is good"""
        return self.overall_score >= threshold
    
    def needs_improvement(self, threshold: float = 60.0) -> bool:
        """Check if resume needs improvement"""
        return self.overall_score < threshold
    
    def get_score_category(self) -> str:
        """Get score category"""
        if self.overall_score >= 85:
            return "Excellent"
        elif self.overall_score >= 70:
            return "Good"
        elif self.overall_score >= 60:
            return "Average"
        else:
            return "Needs Improvement"
    
    def get_top_strengths(self, n: int = 3) -> List[str]:
        """Get top N strengths"""
        return self.strengths[:n]
    
    def get_top_weaknesses(self, n: int = 3) -> List[str]:
        """Get top N weaknesses"""
        return self.weaknesses[:n]
    
    def get_priority_improvements(self, n: int = 5) -> List[str]:
        """Get priority improvements"""
        return self.improvements[:n]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'analysis_id': self.analysis_id,
            'resume_id': self.resume_id,
            'overall_score': self.overall_score,
            'ats_score': self.ats_score,
            'content_score': self.content_score,
            'formatting_score': self.formatting_score,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'improvements': self.improvements,
            'suggested_job_titles': self.suggested_job_titles,
            'skill_analysis': self.skill_analysis,
            'experience_analysis': self.experience_analysis,
            'education_analysis': self.education_analysis,
            'extracted_keywords': self.extracted_keywords,
            'missing_keywords': self.missing_keywords,
            'summary': self.summary,
            'analysis_date': self.analysis_date.isoformat(),
            'ai_model_used': self.ai_model_used,
            'processing_time': self.processing_time,
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"AnalysisResult(id={self.analysis_id[:8]}..., score={self.overall_score:.1f})"
    
    def __str__(self) -> str:
        """Human-readable string"""
        return f"Analysis: {self.overall_score:.1f}/100 ({self.get_score_category()})"