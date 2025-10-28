from typing import List, Dict
from dataclasses import dataclass
import numpy as np
from loguru import logger

from src.models.match_result import MatchResult


@dataclass
class RankingWeights:
    """Weights for ranking algorithm"""
    skills: float = 0.35
    experience: float = 0.25
    education: float = 0.15
    semantic: float = 0.25


class RankingAlgorithm:
    """Advanced ranking algorithm for job matches"""
    
    def __init__(self):
        """Initialize ranking algorithm"""
        self.default_weights = RankingWeights()
    
    def rank_matches(
        self,
        matches: List[MatchResult],
        custom_weights: Dict[str, float] = None
    ) -> List[MatchResult]:
        """
        Rank matches using weighted scoring
        
        Args:
            matches: List of match results
            custom_weights: Optional custom weights
            
        Returns:
            Sorted list of matches
        """
        if not matches:
            return []
        
        weights = self._get_weights(custom_weights)
        
        # Calculate final scores
        for match in matches:
            match.overall_score = self._calculate_weighted_score(match, weights)
        
        # Sort by score (descending)
        ranked = sorted(matches, key=lambda x: x.overall_score, reverse=True)
        
        logger.info(f"Ranked {len(ranked)} matches")
        return ranked
    
    def _get_weights(self, custom_weights: Dict[str, float] = None) -> RankingWeights:
        """Get weights (custom or default)"""
        if not custom_weights:
            return self.default_weights
        
        return RankingWeights(
            skills=custom_weights.get('skills', self.default_weights.skills),
            experience=custom_weights.get('experience', self.default_weights.experience),
            education=custom_weights.get('education', self.default_weights.education),
            semantic=custom_weights.get('semantic', self.default_weights.semantic)
        )
    
    def _calculate_weighted_score(
        self,
        match: MatchResult,
        weights: RankingWeights
    ) -> float:
        """Calculate weighted score for a match"""
        score = (
            match.skills_match_score * weights.skills +
            match.experience_match_score * weights.experience +
            match.education_match_score * weights.education +
            match.semantic_similarity_score * weights.semantic
        )
        
        # Ensure score is in 0-100 range
        return max(0.0, min(100.0, score))
    
    def rank_by_component(
        self,
        matches: List[MatchResult],
        component: str = 'skills'
    ) -> List[MatchResult]:
        """
        Rank matches by specific component
        
        Args:
            matches: List of matches
            component: Component to rank by (skills, experience, education, semantic)
            
        Returns:
            Sorted matches
        """
        component_map = {
            'skills': lambda m: m.skills_match_score,
            'experience': lambda m: m.experience_match_score,
            'education': lambda m: m.education_match_score,
            'semantic': lambda m: m.semantic_similarity_score,
            'overall': lambda m: m.overall_score
        }
        
        if component not in component_map:
            logger.warning(f"Unknown component: {component}, using overall")
            component = 'overall'
        
        return sorted(matches, key=component_map[component], reverse=True)
    
    def get_top_k(
        self,
        matches: List[MatchResult],
        k: int = 10,
        threshold: float = 0.0
    ) -> List[MatchResult]:
        """
        Get top K matches above threshold
        
        Args:
            matches: List of matches
            k: Number of top matches
            threshold: Minimum score threshold
            
        Returns:
            Top K matches
        """
        filtered = [m for m in matches if m.overall_score >= threshold]
        ranked = self.rank_matches(filtered)
        return ranked[:k]