"""
Education Extractor
Extracts education information
"""

import re
from typing import List, Dict, Optional


class EducationExtractor:
    """Extract education information"""
    
    def __init__(self):
        self.degree_keywords = [
            'Bachelor', 'Master', 'PhD', 'Doctorate', 'Associate',
            'B.S.', 'B.A.', 'M.S.', 'M.A.', 'MBA', 'Ph.D.',
        ]
        
        self.institution_keywords = [
            'University', 'College', 'Institute', 'School'
        ]
    
    def extract(self, text: str) -> List[Dict[str, str]]:
        """Extract education"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            for degree in self.degree_keywords:
                if degree.lower() in line.lower():
                    edu = self._extract_education_entry(lines, i)
                    if edu:
                        education.append(edu)
                    break
        
        return education
    
    def _extract_education_entry(self, lines: List[str], idx: int) -> Optional[Dict]:
        """Extract single education entry"""
        try:
            line = lines[idx].strip()
            
            degree = line
            institution = ""
            
            for keyword in self.institution_keywords:
                if keyword in line:
                    institution = line
                    break
            
            if not institution:
                for i in range(idx + 1, min(idx + 3, len(lines))):
                    next_line = lines[i].strip()
                    for keyword in self.institution_keywords:
                        if keyword in next_line:
                            institution = next_line
                            break
            
            year_match = re.search(r'\b(19|20)\d{2}\b', line)
            year = year_match.group(0) if year_match else ""
            
            return {
                'degree': degree,
                'institution': institution,
                'year': year,
                'field': ''
            }
        except:
            return None