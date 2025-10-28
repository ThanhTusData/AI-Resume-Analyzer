"""
AI-Powered Resume Analyzer
Uses LLMs to analyze resumes and provide insights
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from loguru import logger

from src.ai_analyzer.llm_client import LLMClient
from src.ai_analyzer.prompt_templates import PromptTemplates
from src.models.resume import Resume
from src.models.analysis_result import AnalysisResult


@dataclass
class ResumeAnalysis:
    """Complete resume analysis results"""
    overall_score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    suggested_improvements: List[str]
    suggested_job_titles: List[str]
    skill_assessment: Dict[str, Dict[str, any]]
    experience_analysis: Dict[str, any]
    education_analysis: Dict[str, any]
    ats_compatibility: Dict[str, any]
    missing_keywords: List[str]
    formatting_suggestions: List[str]
    summary: str


class ResumeAnalyzer:
    """Analyzes resumes using AI"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize resume analyzer
        
        Args:
            llm_client: LLM client for AI analysis (creates default if None)
        """
        self.llm = llm_client or LLMClient()
        self.prompts = PromptTemplates()
    
    def analyze_resume(self, resume: Resume) -> ResumeAnalysis:
        """
        Perform comprehensive resume analysis
        
        Args:
            resume: Resume object to analyze
            
        Returns:
            ResumeAnalysis with complete insights
        """
        logger.info(f"Starting AI analysis for resume: {resume.filename}")
        
        # Prepare resume text
        resume_text = self._prepare_resume_text(resume)
        
        # Run parallel analyses
        analyses = {
            'overall': self._analyze_overall_quality(resume_text),
            'strengths': self._analyze_strengths(resume_text),
            'weaknesses': self._analyze_weaknesses(resume_text),
            'skills': self._analyze_skills(resume_text, resume.skills),
            'experience': self._analyze_experience(resume_text, resume.experience),
            'education': self._analyze_education(resume_text, resume.education),
            'ats': self._analyze_ats_compatibility(resume_text),
            'job_titles': self._suggest_job_titles(resume_text),
            'improvements': self._suggest_improvements(resume_text)
        }
        
        # Compile results
        analysis = ResumeAnalysis(
            overall_score=analyses['overall']['score'],
            strengths=analyses['strengths'],
            weaknesses=analyses['weaknesses'],
            suggested_improvements=analyses['improvements'],
            suggested_job_titles=analyses['job_titles'],
            skill_assessment=analyses['skills'],
            experience_analysis=analyses['experience'],
            education_analysis=analyses['education'],
            ats_compatibility=analyses['ats'],
            missing_keywords=analyses['ats'].get('missing_keywords', []),
            formatting_suggestions=analyses['overall'].get('formatting', []),
            summary=self._generate_summary(analyses)
        )
        
        logger.info(f"Analysis complete. Overall score: {analysis.overall_score}")
        return analysis
    
    def _prepare_resume_text(self, resume: Resume) -> str:
        """Prepare structured resume text for analysis"""
        sections = []
        
        if resume.personal_info:
            sections.append("=== PERSONAL INFORMATION ===")
            for key, value in resume.personal_info.items():
                if value:
                    sections.append(f"{key.title()}: {value}")
        
        if resume.summary:
            sections.append("\n=== SUMMARY ===")
            sections.append(resume.summary)
        
        if resume.experience:
            sections.append("\n=== WORK EXPERIENCE ===")
            for exp in resume.experience:
                sections.append(f"\n{exp.get('title', 'Position')} at {exp.get('company', 'Company')}")
                sections.append(f"Duration: {exp.get('duration', 'N/A')}")
                if exp.get('description'):
                    sections.append(f"Description: {exp['description']}")
        
        if resume.education:
            sections.append("\n=== EDUCATION ===")
            for edu in resume.education:
                sections.append(f"{edu.get('degree', 'Degree')} - {edu.get('institution', 'Institution')}")
                sections.append(f"Year: {edu.get('year', 'N/A')}")
        
        if resume.skills:
            sections.append("\n=== SKILLS ===")
            sections.append(", ".join(resume.skills))
        
        if resume.certifications:
            sections.append("\n=== CERTIFICATIONS ===")
            for cert in resume.certifications:
                sections.append(f"- {cert}")
        
        return "\n".join(sections)
    
    def _analyze_overall_quality(self, resume_text: str) -> Dict:
        """Analyze overall resume quality"""
        prompt = self.prompts.get_overall_analysis_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000
        )
        
        # Parse response
        score = self._extract_score(response)
        formatting = self._extract_list(response, "formatting")
        
        return {
            'score': score,
            'formatting': formatting,
            'raw_response': response
        }
    
    def _analyze_strengths(self, resume_text: str) -> List[str]:
        """Identify resume strengths"""
        prompt = self.prompts.get_strengths_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=800
        )
        
        return self._extract_list(response, "strengths")
    
    def _analyze_weaknesses(self, resume_text: str) -> List[str]:
        """Identify resume weaknesses"""
        prompt = self.prompts.get_weaknesses_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=800
        )
        
        return self._extract_list(response, "weaknesses")
    
    def _analyze_skills(self, resume_text: str, skills: List[str]) -> Dict:
        """Analyze skills comprehensively"""
        prompt = self.prompts.get_skills_analysis_prompt(resume_text, skills)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=1000
        )
        
        return {
            'technical_skills': self._categorize_skills(skills, 'technical'),
            'soft_skills': self._categorize_skills(skills, 'soft'),
            'proficiency_levels': self._assess_skill_levels(response),
            'trending_skills': self._identify_trending_skills(skills),
            'missing_skills': self._extract_list(response, "missing")
        }
    
    def _analyze_experience(self, resume_text: str, experience: List[Dict]) -> Dict:
        """Analyze work experience"""
        prompt = self.prompts.get_experience_analysis_prompt(resume_text, experience)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=1000
        )
        
        return {
            'total_years': self._calculate_years_experience(experience),
            'career_progression': self._assess_career_progression(experience),
            'achievements': self._extract_list(response, "achievements"),
            'gaps': self._identify_gaps(experience),
            'recommendations': self._extract_list(response, "recommendations")
        }
    
    def _analyze_education(self, resume_text: str, education: List[Dict]) -> Dict:
        """Analyze education background"""
        prompt = self.prompts.get_education_analysis_prompt(resume_text, education)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=600
        )
        
        return {
            'highest_degree': self._get_highest_degree(education),
            'relevance': self._extract_score(response),
            'recommendations': self._extract_list(response, "recommendations")
        }
    
    def _analyze_ats_compatibility(self, resume_text: str) -> Dict:
        """Analyze ATS (Applicant Tracking System) compatibility"""
        prompt = self.prompts.get_ats_analysis_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        return {
            'ats_score': self._extract_score(response),
            'keyword_density': self._analyze_keywords(resume_text),
            'missing_keywords': self._extract_list(response, "missing_keywords"),
            'format_issues': self._extract_list(response, "format_issues"),
            'improvements': self._extract_list(response, "ats_improvements")
        }
    
    def _suggest_job_titles(self, resume_text: str) -> List[str]:
        """Suggest suitable job titles"""
        prompt = self.prompts.get_job_title_suggestion_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.6,
            max_tokens=400
        )
        
        return self._extract_list(response, "job_titles")
    
    def _suggest_improvements(self, resume_text: str) -> List[str]:
        """Suggest resume improvements"""
        prompt = self.prompts.get_improvement_suggestions_prompt(resume_text)
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000
        )
        
        return self._extract_list(response, "improvements")
    
    def _generate_summary(self, analyses: Dict) -> str:
        """Generate executive summary of analysis"""
        summary_parts = [
            f"Overall Score: {analyses['overall']['score']}/100",
            f"\nKey Strengths: {', '.join(analyses['strengths'][:3])}",
            f"\nAreas for Improvement: {', '.join(analyses['weaknesses'][:3])}",
            f"\nATS Compatibility: {analyses['ats']['ats_score']}/100",
            f"\nRecommended Roles: {', '.join(analyses['job_titles'][:3])}"
        ]
        
        return "\n".join(summary_parts)
    
    # Helper methods
    def _extract_score(self, text: str) -> float:
        """Extract numerical score from text"""
        import re
        matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:/\s*100|%)', text)
        if matches:
            return float(matches[0])
        return 70.0  # Default score
    
    def _extract_list(self, text: str, section: str) -> List[str]:
        """Extract list items from text"""
        lines = text.split('\n')
        items = []
        in_section = False
        
        for line in lines:
            line = line.strip()
            if section.lower() in line.lower():
                in_section = True
                continue
            
            if in_section and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                item = line.lstrip('-•* ').strip()
                if item:
                    items.append(item)
            elif in_section and line and not any(line.startswith(x) for x in ['-', '•', '*', '#']):
                break
        
        return items[:10]  # Limit to top 10
    
    def _categorize_skills(self, skills: List[str], category: str) -> List[str]:
        """Categorize skills by type"""
        # Simplified categorization logic
        technical_keywords = ['python', 'java', 'sql', 'aws', 'docker', 'kubernetes', 'react', 'angular']
        soft_keywords = ['leadership', 'communication', 'teamwork', 'management', 'negotiation']
        
        if category == 'technical':
            return [s for s in skills if any(kw in s.lower() for kw in technical_keywords)]
        else:
            return [s for s in skills if any(kw in s.lower() for kw in soft_keywords)]
    
    def _assess_skill_levels(self, response: str) -> Dict[str, str]:
        """Assess proficiency levels for skills"""
        # Simplified assessment
        return {"assessment": "based_on_context"}
    
    def _identify_trending_skills(self, skills: List[str]) -> List[str]:
        """Identify trending/in-demand skills"""
        trending = ['AI', 'Machine Learning', 'Cloud', 'Kubernetes', 'React', 'Python', 'DevOps']
        return [s for s in skills if any(t.lower() in s.lower() for t in trending)]
    
    def _calculate_years_experience(self, experience: List[Dict]) -> float:
        """Calculate total years of experience"""
        # Simplified calculation
        return len(experience) * 2.5  # Approximate
    
    def _assess_career_progression(self, experience: List[Dict]) -> str:
        """Assess career progression trajectory"""
        if len(experience) >= 3:
            return "Strong upward trajectory"
        elif len(experience) >= 1:
            return "Moderate progression"
        return "Early career"
    
    def _identify_gaps(self, experience: List[Dict]) -> List[str]:
        """Identify employment gaps"""
        # Simplified gap detection
        return []
    
    def _get_highest_degree(self, education: List[Dict]) -> str:
        """Get highest educational degree"""
        if not education:
            return "Not specified"
        
        degrees = ['phd', 'doctorate', 'master', 'bachelor', 'associate']
        for degree in degrees:
            for edu in education:
                if degree in edu.get('degree', '').lower():
                    return edu.get('degree', 'Not specified')
        
        return education[0].get('degree', 'Not specified')
    
    def _analyze_keywords(self, text: str) -> Dict[str, int]:
        """Analyze keyword density"""
        words = text.lower().split()
        return {'total_words': len(words), 'unique_words': len(set(words))}