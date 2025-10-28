"""
Experience Extractor
Extracts work experience from resume text
"""

import re
from typing import List, Dict, Optional
from loguru import logger


class ExperienceExtractor:
    """Extract work experience"""
    
    def __init__(self):
        self.date_patterns = [
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*-\s*(Present|Current)',
            r'([A-Z][a-z]+\s+\d{4})\s*-\s*([A-Z][a-z]+\s+\d{4})',
        ]
    
    def extract(self, text: str) -> List[Dict[str, str]]:
        """Extract experience from text"""
        experiences = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            for pattern in self.date_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    exp = self._extract_experience_block(lines, i)
                    if exp:
                        experiences.append(exp)
                    break
        
        return experiences
    
    def _extract_experience_block(self, lines: List[str], idx: int) -> Optional[Dict]:
        """Extract single experience block"""
        try:
            line = lines[idx].strip()
            
            title, company = self._extract_title_company(line)
            duration = self._extract_duration(line)
            
            description = []
            for i in range(idx + 1, min(idx + 10, len(lines))):
                desc_line = lines[i].strip()
                
                if any(re.search(p, desc_line) for p in self.date_patterns):
                    break
                
                if desc_line and len(desc_line) >= 10:
                    description.append(desc_line)
            
            return {
                'title': title,
                'company': company,
                'duration': duration,
                'description': ' '.join(description)
            }
        except:
            return None
    
    def _extract_title_company(self, line: str) -> tuple:
        """Extract title and company"""
        for indicator in ['at', 'with', '@', '|', '-']:
            if indicator in line:
                parts = line.split(indicator, 1)
                if len(parts) == 2:
                    return parts[0].strip(), parts[1].strip()
        
        return line, ""
    
    def _extract_duration(self, line: str) -> str:
        """Extract duration"""
        for pattern in self.date_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(0)
        return ""