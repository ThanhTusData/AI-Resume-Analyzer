"""
Pytest Configuration
Fixtures and test setup
"""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def test_data_dir():
    """Get test data directory"""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing"""
    return """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567
    
    EXPERIENCE
    Senior Software Engineer at Tech Corp (2020-2023)
    - Developed microservices using Python and Django
    - Led team of 5 engineers
    
    EDUCATION
    Bachelor of Science in Computer Science
    MIT University, 2019
    
    SKILLS
    Python, Django, AWS, Docker, Machine Learning
    """


@pytest.fixture
def sample_job_data():
    """Sample job data for testing"""
    return {
        "title": "Senior Python Developer",
        "company": "Tech Giants Inc",
        "location": "San Francisco, CA",
        "remote": True,
        "description": "Looking for Python developer",
        "required_skills": ["Python", "Django", "AWS"]
    }
