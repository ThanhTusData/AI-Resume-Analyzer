"""
Job Parser
Extracts job information from LinkedIn pages
"""

import re
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger

from src.scraper.selectors import LinkedInSelectors
from src.scraper.anti_detection import AntiDetection


class JobParser:
    """Parse job information from LinkedIn pages"""
    
    def __init__(self):
        """Initialize job parser"""
        self.selectors = LinkedInSelectors()
        self.anti_detection = AntiDetection()
    
    def parse_job_page(self, driver: webdriver.Chrome) -> Optional[Dict]:
        """
        Parse job details from current page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            Dictionary with job information
        """
        try:
            job_data = {
                'title': self._extract_title(driver),
                'company': self._extract_company(driver),
                'location': self._extract_location(driver),
                'description': self._extract_description(driver),
                'requirements': self._extract_requirements(driver),
                'responsibilities': '',
                'remote': self._check_remote(driver),
                'job_type': self._extract_job_type(driver),
                'experience_level': self._extract_experience_level(driver),
                'experience_required': self._extract_experience_required(driver),
                'education_required': self._extract_education_required(driver),
                'required_skills': self._extract_skills(driver),
                'salary_min': None,
                'salary_max': None,
                'posted_date': self._extract_posted_date(driver),
                'applicant_count': self._extract_applicant_count(driver),
                'url': driver.current_url
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job page: {str(e)}")
            return None
    
    def _extract_title(self, driver: webdriver.Chrome) -> str:
        """Extract job title"""
        try:
            selectors = [
                self.selectors.JOB_DETAILS_TITLE,
                "h1.t-24",
                "h2.t-24"
            ]
            
            for selector in selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    return element.text.strip()
                except:
                    continue
            
            return ""
        except Exception:
            return ""
    
    def _extract_company(self, driver: webdriver.Chrome) -> str:
        """Extract company name"""
        try:
            selectors = [
                self.selectors.JOB_DETAILS_COMPANY,
                "a.ember-view.job-card-container__link",
                "span.jobs-unified-top-card__company-name"
            ]
            
            for selector in selectors:
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    return element.text.strip()
                except:
                    continue
            
            return ""
        except Exception:
            return ""
    
    def _extract_location(self, driver: webdriver.Chrome) -> str:
        """Extract job location"""
        try:
            element = driver.find_element(
                By.CSS_SELECTOR,
                self.selectors.JOB_DETAILS_LOCATION
            )
            return element.text.strip()
        except Exception:
            return ""
    
    def _extract_description(self, driver: webdriver.Chrome) -> str:
        """Extract job description"""
        try:
            # Click 'Show more' if available
            try:
                show_more = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors.SHOW_MORE_BUTTON))
                )
                self.anti_detection.human_click(show_more, driver)
                self.anti_detection.random_delay(0.5, 1.0)
            except:
                pass
            
            element = driver.find_element(
                By.CSS_SELECTOR,
                self.selectors.JOB_DESCRIPTION
            )
            return element.text.strip()
        except Exception:
            return ""
    
    def _extract_requirements(self, driver: webdriver.Chrome) -> str:
        """Extract job requirements"""
        description = self._extract_description(driver)
        
        # Try to extract requirements section
        keywords = ['requirements', 'qualifications', 'must have', 'required', 'you have']
        lines = description.split('\n')
        
        req_lines = []
        in_requirements = False
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if line starts requirements section
            if any(kw in line_lower for kw in keywords):
                in_requirements = True
                req_lines.append(line)
                continue
            
            # Check if we've moved to a new section
            if in_requirements and line and line[0].isupper() and ':' in line:
                if not any(kw in line_lower for kw in keywords):
                    break
            
            if in_requirements:
                req_lines.append(line)
        
        return '\n'.join(req_lines) if req_lines else description[:500]
    
    def _check_remote(self, driver: webdriver.Chrome) -> bool:
        """Check if job is remote"""
        try:
            page_text = driver.page_source.lower()
            remote_keywords = ['remote', 'work from home', 'wfh', 'hybrid', 'telecommute']
            return any(keyword in page_text for keyword in remote_keywords)
        except Exception:
            return False
    
    def _extract_job_type(self, driver: webdriver.Chrome) -> Optional[str]:
        """Extract job type"""
        try:
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "span.jobs-unified-top-card__job-insight-text"
            )
            
            job_types = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']
            
            for element in elements:
                text = element.text.strip()
                for job_type in job_types:
                    if job_type.lower() in text.lower():
                        return job_type
            
            return None
        except Exception:
            return None
    
    def _extract_experience_level(self, driver: webdriver.Chrome) -> Optional[str]:
        """Extract experience level"""
        try:
            elements = driver.find_elements(
                By.CSS_SELECTOR,
                "span.jobs-unified-top-card__job-insight-text"
            )
            
            levels = ['Entry level', 'Mid-Senior level', 'Director', 'Executive', 'Associate']
            
            for element in elements:
                text = element.text.strip()
                for level in levels:
                    if level.lower() in text.lower():
                        return level
            
            return None
        except Exception:
            return None
    
    def _extract_experience_required(self, driver: webdriver.Chrome) -> str:
        """Extract required years of experience"""
        try:
            description = self._extract_description(driver)
            
            # Look for patterns like "5+ years", "3-5 years", etc.
            patterns = [
                r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(\d+)\s*to\s*(\d+)\s*(?:years?|yrs?)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, description.lower())
                if match:
                    return match.group(0)
            
            return ""
        except Exception:
            return ""
    
    def _extract_education_required(self, driver: webdriver.Chrome) -> str:
        """Extract education requirements"""
        try:
            description = self._extract_description(driver)
            
            degrees = ['PhD', 'Doctorate', "Master's", 'Masters', "Bachelor's", 'Bachelors', 'MBA', 'BS', 'MS', 'BA', 'MA']
            
            for degree in degrees:
                if degree.lower() in description.lower():
                    return degree
            
            return ""
        except Exception:
            return ""
    
    def _extract_skills(self, driver: webdriver.Chrome) -> List[str]:
        """Extract required skills"""
        try:
            description = self._extract_description(driver)
            
            # Common skill patterns
            skill_keywords = [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Ruby', 'PHP',
                'SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
                'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring',
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
                'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'NLP',
                'Agile', 'Scrum', 'DevOps', 'Microservices', 'REST API', 'GraphQL'
            ]
            
            found_skills = []
            description_lower = description.lower()
            
            for skill in skill_keywords:
                if skill.lower() in description_lower:
                    found_skills.append(skill)
            
            return found_skills[:15]  # Limit to top 15
            
        except Exception:
            return []
    
    def _extract_posted_date(self, driver: webdriver.Chrome) -> Optional[str]:
        """Extract job posted date"""
        try:
            element = driver.find_element(
                By.CSS_SELECTOR,
                self.selectors.JOB_POSTED_DATE
            )
            return element.text.strip()
        except Exception:
            return None
    
    def _extract_applicant_count(self, driver: webdriver.Chrome) -> int:
        """Extract number of applicants"""
        try:
            element = driver.find_element(
                By.CSS_SELECTOR,
                self.selectors.APPLICANT_COUNT
            )
            text = element.text.strip()
            
            # Extract number from text like "50 applicants"
            match = re.search(r'(\d+)', text)
            if match:
                return int(match.group(1))
            
            return 0
        except Exception:
            return 0