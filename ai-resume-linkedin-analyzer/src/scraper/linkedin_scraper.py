"""
LinkedIn Job Scraper
Extracts job postings from LinkedIn with anti-detection measures
"""

import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger

from src.scraper.browser_manager import BrowserManager
from src.scraper.job_parser import JobParser
from src.scraper.anti_detection import AntiDetection
from src.scraper.selectors import LinkedInSelectors
from src.models.job import Job


@dataclass
class SearchParams:
    """LinkedIn job search parameters"""
    keywords: str
    location: str = ""
    experience_level: Optional[List[str]] = None  # Entry, Mid-Senior, Director, Executive
    job_type: Optional[List[str]] = None  # Full-time, Part-time, Contract, Internship
    remote: bool = False
    posted_within: str = "week"  # day, week, month
    max_results: int = 25


class LinkedInScraper:
    """Scrapes job postings from LinkedIn"""
    
    def __init__(self, email: str, password: str, headless: bool = True):
        """
        Initialize LinkedIn scraper
        
        Args:
            email: LinkedIn account email
            password: LinkedIn account password
            headless: Run browser in headless mode
        """
        self.email = email
        self.password = password
        self.headless = headless
        self.browser_manager = BrowserManager(headless=headless)
        self.job_parser = JobParser()
        self.anti_detection = AntiDetection()
        self.driver: Optional[webdriver.Chrome] = None
        self.is_logged_in = False
        
    def __enter__(self):
        """Context manager entry"""
        self.driver = self.browser_manager.get_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def login(self) -> bool:
        """
        Login to LinkedIn
        
        Returns:
            bool: True if login successful
        """
        try:
            logger.info("Attempting to login to LinkedIn")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Human-like typing
            self.anti_detection.human_type(
                self.driver.find_element(By.ID, "username"),
                self.email
            )
            time.sleep(random.uniform(0.5, 1.5))
            
            self.anti_detection.human_type(
                self.driver.find_element(By.ID, "password"),
                self.password
            )
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            login_button = self.driver.find_element(
                By.CSS_SELECTOR,
                LinkedInSelectors.LOGIN_BUTTON
            )
            self.anti_detection.human_click(login_button)
            
            # Wait for redirect to feed
            time.sleep(5)
            
            # Check if login successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                logger.info("Successfully logged in to LinkedIn")
                self.is_logged_in = True
                return True
            else:
                logger.error("Login failed - unexpected redirect")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False
    
    def search_jobs(self, params: SearchParams) -> List[Job]:
        """
        Search for jobs on LinkedIn
        
        Args:
            params: Search parameters
            
        Returns:
            List of Job objects
        """
        if not self.is_logged_in:
            if not self.login():
                logger.error("Cannot search jobs - login failed")
                return []
        
        jobs = []
        
        try:
            # Build search URL
            search_url = self._build_search_url(params)
            logger.info(f"Searching jobs: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(random.uniform(2, 4))
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, LinkedInSelectors.JOB_CARD)
                )
            )
            
            # Scroll and collect job cards
            job_cards = self._collect_job_cards(params.max_results)
            logger.info(f"Found {len(job_cards)} job cards")
            
            # Parse each job
            for idx, card in enumerate(job_cards):
                try:
                    logger.info(f"Parsing job {idx + 1}/{len(job_cards)}")
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                    
                    # Random delay between parsing jobs
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    logger.error(f"Error parsing job card: {str(e)}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs")
            
        except Exception as e:
            logger.error(f"Error searching jobs: {str(e)}")
        
        return jobs
    
    def _build_search_url(self, params: SearchParams) -> str:
        """Build LinkedIn job search URL with parameters"""
        base_url = "https://www.linkedin.com/jobs/search/?"
        
        # Basic parameters
        url_params = [
            f"keywords={params.keywords.replace(' ', '%20')}",
        ]
        
        if params.location:
            url_params.append(f"location={params.location.replace(' ', '%20')}")
        
        # Experience level filters
        if params.experience_level:
            exp_mapping = {
                "Entry": "2",
                "Mid-Senior": "3,4",
                "Director": "5",
                "Executive": "6"
            }
            exp_values = []
            for level in params.experience_level:
                if level in exp_mapping:
                    exp_values.append(exp_mapping[level])
            if exp_values:
                url_params.append(f"f_E={','.join(exp_values)}")
        
        # Job type filters
        if params.job_type:
            type_mapping = {
                "Full-time": "F",
                "Part-time": "P",
                "Contract": "C",
                "Internship": "I"
            }
            type_values = []
            for jtype in params.job_type:
                if jtype in type_mapping:
                    type_values.append(type_mapping[jtype])
            if type_values:
                url_params.append(f"f_JT={','.join(type_values)}")
        
        # Remote filter
        if params.remote:
            url_params.append("f_WT=2")
        
        # Posted within filter
        time_mapping = {
            "day": "r86400",
            "week": "r604800",
            "month": "r2592000"
        }
        if params.posted_within in time_mapping:
            url_params.append(f"f_TPR={time_mapping[params.posted_within]}")
        
        return base_url + "&".join(url_params)
    
    def _collect_job_cards(self, max_results: int) -> List:
        """Collect job card elements by scrolling"""
        job_cards = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while len(job_cards) < max_results:
            # Get current job cards
            cards = self.driver.find_elements(
                By.CSS_SELECTOR,
                LinkedInSelectors.JOB_CARD
            )
            job_cards = list(set(cards))  # Remove duplicates
            
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            
            # Check if reached bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        return job_cards[:max_results]
    
    def _parse_job_card(self, card_element) -> Optional[Job]:
        """Parse a single job card element"""
        try:
            # Click on job card to load details
            self.anti_detection.human_click(card_element)
            time.sleep(random.uniform(1, 2))
            
            # Wait for job details to load
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, LinkedInSelectors.JOB_DETAILS)
                )
            )
            
            # Extract job information using JobParser
            job_data = self.job_parser.parse_job_page(self.driver)
            
            if job_data:
                return Job(**job_data)
            
        except Exception as e:
            logger.error(f"Error parsing job card: {str(e)}")
        
        return None
    
    def close(self):
        """Close browser and cleanup"""
        if self.driver:
            self.browser_manager.close_driver()
            self.driver = None
            logger.info("Scraper closed")