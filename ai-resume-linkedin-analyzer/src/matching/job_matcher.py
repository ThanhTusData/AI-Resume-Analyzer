"""
Job Matching Engine
Matches resumes with jobs using semantic similarity and scoring
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from loguru import logger

from src.matching.embeddings import EmbeddingGenerator
from src.matching.vector_store import VectorStore
from src.matching.similarity_scorer import SimilarityScorer
from src.matching.ranking_algorithm import RankingAlgorithm
from src.models.resume import Resume
from src.models.job import Job
from src.models.match_result import MatchResult


@dataclass
class MatchingConfig:
    """Configuration for job matching"""
    similarity_threshold: float = 0.7
    top_k: int = 10
    weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.weights is None:
            self.weights = {
                'skills': 0.35,
                'experience': 0.25,
                'education': 0.15,
                'semantic': 0.25
            }


class JobMatcher:
    """Matches resumes with relevant jobs"""
    
    def __init__(self, config: Optional[MatchingConfig] = None):
        """
        Initialize job matcher
        
        Args:
            config: Matching configuration
        """
        self.config = config or MatchingConfig()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.similarity_scorer = SimilarityScorer()
        self.ranker = RankingAlgorithm()
        
        logger.info("Job matcher initialized")
    
    def match_resume_to_jobs(
        self,
        resume: Resume,
        jobs: List[Job],
        top_k: Optional[int] = None
    ) -> List[MatchResult]:
        """
        Match a resume against multiple jobs
        
        Args:
            resume: Resume to match
            jobs: List of jobs to match against
            top_k: Number of top matches to return
            
        Returns:
            List of MatchResult objects sorted by score
        """
        if not jobs:
            logger.warning("No jobs provided for matching")
            return []
        
        top_k = top_k or self.config.top_k
        
        logger.info(f"Matching resume against {len(jobs)} jobs")
        
        # Generate resume embedding
        resume_embedding = self._generate_resume_embedding(resume)
        
        # Generate job embeddings and store
        job_embeddings = []
        for job in jobs:
            embedding = self._generate_job_embedding(job)
            job_embeddings.append(embedding)
        
        # Calculate matches
        matches = []
        for idx, (job, job_embedding) in enumerate(zip(jobs, job_embeddings)):
            try:
                match_result = self._calculate_match(
                    resume,
                    resume_embedding,
                    job,
                    job_embedding
                )
                matches.append(match_result)
                
                if (idx + 1) % 10 == 0:
                    logger.info(f"Processed {idx + 1}/{len(jobs)} jobs")
                    
            except Exception as e:
                logger.error(f"Error matching job {job.title}: {str(e)}")
                continue
        
        # Rank and filter matches
        ranked_matches = self.ranker.rank_matches(matches, self.config.weights)
        
        # Filter by threshold
        filtered_matches = [
            m for m in ranked_matches
            if m.overall_score >= self.config.similarity_threshold * 100
        ]
        
        logger.info(f"Found {len(filtered_matches)} matches above threshold")
        
        return filtered_matches[:top_k]
    
    def find_similar_jobs(
        self,
        target_job: Job,
        job_pool: List[Job],
        top_k: int = 5
    ) -> List[Tuple[Job, float]]:
        """
        Find jobs similar to a target job
        
        Args:
            target_job: Job to find similar matches for
            job_pool: Pool of jobs to search
            top_k: Number of similar jobs to return
            
        Returns:
            List of (Job, similarity_score) tuples
        """
        target_embedding = self._generate_job_embedding(target_job)
        
        similarities = []
        for job in job_pool:
            if job.job_id == target_job.job_id:
                continue
            
            job_embedding = self._generate_job_embedding(job)
            similarity = self.similarity_scorer.cosine_similarity(
                target_embedding,
                job_embedding
            )
            similarities.append((job, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def _generate_resume_embedding(self, resume: Resume) -> np.ndarray:
        """Generate embedding vector for resume"""
        # Prepare resume text for embedding
        resume_text = self._prepare_resume_for_embedding(resume)
        
        # Generate embedding
        embedding = self.embedding_gen.generate_embedding(resume_text)
        
        return embedding
    
    def _generate_job_embedding(self, job: Job) -> np.ndarray:
        """Generate embedding vector for job"""
        # Prepare job text for embedding
        job_text = self._prepare_job_for_embedding(job)
        
        # Generate embedding
        embedding = self.embedding_gen.generate_embedding(job_text)
        
        return embedding
    
    def _calculate_match(
        self,
        resume: Resume,
        resume_embedding: np.ndarray,
        job: Job,
        job_embedding: np.ndarray
    ) -> MatchResult:
        """Calculate comprehensive match between resume and job"""
        
        # 1. Semantic similarity using embeddings
        semantic_score = self.similarity_scorer.cosine_similarity(
            resume_embedding,
            job_embedding
        )
        
        # 2. Skills match
        skills_score = self._calculate_skills_match(resume.skills, job.required_skills)
        
        # 3. Experience match
        experience_score = self._calculate_experience_match(resume, job)
        
        # 4. Education match
        education_score = self._calculate_education_match(resume, job)
        
        # 5. Location match
        location_score = self._calculate_location_match(resume, job)
        
        # Calculate weighted overall score
        overall_score = (
            semantic_score * self.config.weights['semantic'] +
            skills_score * self.config.weights['skills'] +
            experience_score * self.config.weights['experience'] +
            education_score * self.config.weights['education']
        ) * 100  # Convert to 0-100 scale
        
        # Generate match explanation
        explanation = self._generate_match_explanation(
            skills_score,
            experience_score,
            education_score,
            semantic_score
        )
        
        # Identify missing skills
        missing_skills = self._identify_missing_skills(
            resume.skills,
            job.required_skills
        )
        
        return MatchResult(
            resume_id=resume.resume_id,
            job=job,
            overall_score=overall_score,
            skills_match_score=skills_score * 100,
            experience_match_score=experience_score * 100,
            education_match_score=education_score * 100,
            semantic_similarity_score=semantic_score * 100,
            location_match_score=location_score * 100,
            matched_skills=self._get_matched_skills(resume.skills, job.required_skills),
            missing_skills=missing_skills,
            explanation=explanation,
            confidence_level=self._calculate_confidence(overall_score)
        )
    
    def _prepare_resume_for_embedding(self, resume: Resume) -> str:
        """Prepare resume text optimized for embedding"""
        parts = []
        
        if resume.summary:
            parts.append(f"Summary: {resume.summary}")
        
        if resume.skills:
            parts.append(f"Skills: {', '.join(resume.skills)}")
        
        if resume.experience:
            exp_texts = []
            for exp in resume.experience:
                exp_text = f"{exp.get('title', '')} at {exp.get('company', '')}"
                if exp.get('description'):
                    exp_text += f". {exp['description']}"
                exp_texts.append(exp_text)
            parts.append(f"Experience: {' '.join(exp_texts)}")
        
        if resume.education:
            edu_texts = [
                f"{e.get('degree', '')} from {e.get('institution', '')}"
                for e in resume.education
            ]
            parts.append(f"Education: {' '.join(edu_texts)}")
        
        return " ".join(parts)
    
    def _prepare_job_for_embedding(self, job: Job) -> str:
        """Prepare job text optimized for embedding"""
        parts = [
            f"Title: {job.title}",
            f"Company: {job.company}"
        ]
        
        if job.description:
            parts.append(f"Description: {job.description}")
        
        if job.required_skills:
            parts.append(f"Required Skills: {', '.join(job.required_skills)}")
        
        if job.requirements:
            parts.append(f"Requirements: {job.requirements}")
        
        return " ".join(parts)
    
    def _calculate_skills_match(
        self,
        resume_skills: List[str],
        required_skills: List[str]
    ) -> float:
        """Calculate skills match score (0-1)"""
        if not required_skills:
            return 1.0
        
        if not resume_skills:
            return 0.0
        
        # Normalize skills to lowercase for comparison
        resume_skills_lower = {s.lower() for s in resume_skills}
        required_skills_lower = {s.lower() for s in required_skills}
        
        # Calculate exact matches
        exact_matches = resume_skills_lower.intersection(required_skills_lower)
        
        # Calculate partial matches (fuzzy matching)
        partial_matches = 0
        for req_skill in required_skills_lower:
            if req_skill not in exact_matches:
                for res_skill in resume_skills_lower:
                    if req_skill in res_skill or res_skill in req_skill:
                        partial_matches += 0.5
                        break
        
        total_matches = len(exact_matches) + partial_matches
        match_ratio = total_matches / len(required_skills_lower)
        
        return min(match_ratio, 1.0)
    
    def _calculate_experience_match(self, resume: Resume, job: Job) -> float:
        """Calculate experience match score (0-1)"""
        if not job.experience_required:
            return 1.0
        
        # Simple years of experience comparison
        resume_years = len(resume.experience) * 2  # Approximate
        required_years = self._parse_experience_years(job.experience_required)
        
        if resume_years >= required_years:
            return 1.0
        elif resume_years >= required_years * 0.7:
            return 0.8
        elif resume_years >= required_years * 0.5:
            return 0.6
        else:
            return 0.4
    
    def _calculate_education_match(self, resume: Resume, job: Job) -> float:
        """Calculate education match score (0-1)"""
        if not job.education_required:
            return 1.0
        
        if not resume.education:
            return 0.5
        
        # Simple degree level comparison
        degree_levels = {
            'phd': 5, 'doctorate': 5,
            'master': 4, 'mba': 4,
            'bachelor': 3, 'bachelors': 3,
            'associate': 2,
            'high school': 1
        }
        
        resume_level = 0
        for edu in resume.education:
            degree = edu.get('degree', '').lower()
            for key, level in degree_levels.items():
                if key in degree:
                    resume_level = max(resume_level, level)
        
        required_level = 0
        req_edu_lower = job.education_required.lower()
        for key, level in degree_levels.items():
            if key in req_edu_lower:
                required_level = level
                break
        
        if resume_level >= required_level:
            return 1.0
        elif resume_level >= required_level - 1:
            return 0.7
        else:
            return 0.5
    
    def _calculate_location_match(self, resume: Resume, job: Job) -> float:
        """Calculate location match score (0-1)"""
        if job.remote:
            return 1.0
        
        # Simplified location matching
        return 0.8  # Default moderate match
    
    def _parse_experience_years(self, exp_text: str) -> int:
        """Parse required years of experience from text"""
        import re
        matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', exp_text.lower())
        if matches:
            return int(matches[0])
        return 0
    
    def _get_matched_skills(
        self,
        resume_skills: List[str],
        required_skills: List[str]
    ) -> List[str]:
        """Get list of matched skills"""
        resume_skills_lower = {s.lower(): s for s in resume_skills}
        required_skills_lower = {s.lower() for s in required_skills}
        
        matched = []
        for req_skill_lower in required_skills_lower:
            if req_skill_lower in resume_skills_lower:
                matched.append(resume_skills_lower[req_skill_lower])
        
        return matched
    
    def _identify_missing_skills(
        self,
        resume_skills: List[str],
        required_skills: List[str]
    ) -> List[str]:
        """Identify skills missing from resume"""
        resume_skills_lower = {s.lower() for s in resume_skills}
        required_skills_lower = {s.lower(): s for s in required_skills}
        
        missing = []
        for req_skill_lower, req_skill in required_skills_lower.items():
            if req_skill_lower not in resume_skills_lower:
                # Check for partial matches
                found_partial = False
                for res_skill_lower in resume_skills_lower:
                    if req_skill_lower in res_skill_lower or res_skill_lower in req_skill_lower:
                        found_partial = True
                        break
                
                if not found_partial:
                    missing.append(req_skill)
        
        return missing
    
    def _generate_match_explanation(
        self,
        skills_score: float,
        experience_score: float,
        education_score: float,
        semantic_score: float
    ) -> str:
        """Generate human-readable match explanation"""
        explanations = []
        
        if skills_score >= 0.8:
            explanations.append("Excellent skills match")
        elif skills_score >= 0.6:
            explanations.append("Good skills match")
        else:
            explanations.append("Skills match needs improvement")
        
        if experience_score >= 0.8:
            explanations.append("Strong experience alignment")
        elif experience_score >= 0.6:
            explanations.append("Moderate experience match")
        
        if education_score >= 0.8:
            explanations.append("Education requirements met")
        
        if semantic_score >= 0.7:
            explanations.append("High semantic similarity")
        
        return ". ".join(explanations) + "."
    
    def _calculate_confidence(self, overall_score: float) -> str:
        """Calculate confidence level for match"""
        if overall_score >= 85:
            return "Very High"
        elif overall_score >= 75:
            return "High"
        elif overall_score >= 60:
            return "Medium"
        else:
            return "Low"