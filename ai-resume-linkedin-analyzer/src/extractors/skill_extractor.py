"""
Skill Extractor
Extracts skills from resume text
"""

import re
from typing import List, Dict
from loguru import logger


class SkillExtractor:
    """Extract skills from text"""
    
    def __init__(self):
        self.technical_skills = self._load_technical_skills()
        self.soft_skills = self._load_soft_skills()
    
    def extract(self, text: str) -> List[str]:
        """Extract skills from text"""
        skills = set()
        text_lower = text.lower()
        
        # Technical skills
        for skill in self.technical_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                skills.add(skill)
        
        # Soft skills
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                skills.add(skill)
        
        return sorted(list(skills))
    
    def categorize(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills"""
        technical = []
        soft = []
        
        tech_lower = {s.lower() for s in self.technical_skills}
        soft_lower = {s.lower() for s in self.soft_skills}
        
        for skill in skills:
            if skill.lower() in tech_lower:
                technical.append(skill)
            elif skill.lower() in soft_lower:
                soft.append(skill)
        
        return {'technical': technical, 'soft': soft}
    
    def _load_technical_skills(self) -> List[str]:
        """Load technical skills list"""
        return [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQL', 'NoSQL',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'NLP',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
        ]
    
    def _load_soft_skills(self) -> List[str]:
        """Load soft skills list"""
        return [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Time Management', 'Project Management',
            'Collaboration', 'Adaptability', 'Creativity',
        ]