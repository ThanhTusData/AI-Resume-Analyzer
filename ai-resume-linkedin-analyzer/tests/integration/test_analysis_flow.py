"""
Integration Tests for Analysis Flow
"""

import pytest
from src.models.resume import Resume


@pytest.mark.integration
class TestAnalysisFlow:
    """Integration tests for analysis flow"""
    
    def test_resume_creation(self, sample_resume_text):
        """Test resume creation"""
        resume = Resume(
            filename="test.pdf",
            raw_text=sample_resume_text,
            skills=["Python", "Django"],
            word_count=len(sample_resume_text.split())
        )
        
        assert resume.filename == "test.pdf"
        assert len(resume.skills) == 2
        assert resume.word_count > 0
    
    def test_resume_methods(self):
        """Test resume methods"""
        resume = Resume(
            filename="test.pdf",
            personal_info={'name': 'John Doe'},
            experience=[{}, {}]
        )
        
        assert resume.get_full_name() == 'John Doe'
        assert resume.get_total_experience_years() == 5.0
