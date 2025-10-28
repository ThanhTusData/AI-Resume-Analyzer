"""
Browser Manager
Manages Selenium WebDriver instances with anti-detection
"""

import time
import random
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger


class BrowserManager:
    """Manages browser instances for scraping"""
    
    def __init__(self, headless: bool = True, user_agent: Optional[str] = None):
        """
        Initialize browser manager
        
        Args:
            headless: Run browser in headless mode
            user_agent: Custom user agent string
        """
        self.headless = headless
        self.user_agent = user_agent or self._get_random_user_agent()
        self.driver: Optional[webdriver.Chrome] = None
        self.options = self._configure_options()
        
        logger.info(f"BrowserManager initialized (headless={headless})")
    
    def _get_random_user_agent(self) -> str:
        """Get a random realistic user agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        return random.choice(user_agents)
    
    def _configure_options(self) -> Options:
        """Configure Chrome options for anti-detection"""
        options = Options()
        
        # Headless mode
        if self.headless:
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
        
        # Anti-detection settings
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        options.add_argument(f'user-agent={self.user_agent}')
        
        # Window size
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        
        # Disable unnecessary features
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-default-apps')
        
        # Performance optimizations
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        
        # Disable images for faster loading (optional)
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.cookies": 1,
            "profile.managed_default_content_settings.javascript": 1,
            "profile.managed_default_content_settings.plugins": 1,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.media_stream": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        return options
    
    def get_driver(self) -> webdriver.Chrome:
        """
        Get or create Chrome WebDriver
        
        Returns:
            Chrome WebDriver instance
        """
        if self.driver is None:
            self.driver = self._create_driver()
        
        return self.driver
    
    def _create_driver(self) -> webdriver.Chrome:
        """Create a new Chrome WebDriver with anti-detection"""
        try:
            # Install and get ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # Create driver
            driver = webdriver.Chrome(service=service, options=self.options)
            
            # Set timeouts
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # Execute CDP commands to hide automation
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.user_agent
            })
            
            # Remove webdriver property
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Override plugins
            driver.execute_script(
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})"
            )
            
            # Override languages
            driver.execute_script(
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})"
            )
            
            logger.info("Chrome WebDriver created successfully")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {str(e)}")
            raise
    
    def close_driver(self):
        """Close and cleanup WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                logger.info("WebDriver closed")
            except Exception as e:
                logger.error(f"Error closing driver: {str(e)}")
    
    def restart_driver(self):
        """Restart the WebDriver"""
        logger.info("Restarting WebDriver")
        self.close_driver()
        time.sleep(random.uniform(2, 4))
        self.driver = self._create_driver()
    
    def clear_cookies(self):
        """Clear browser cookies"""
        if self.driver:
            self.driver.delete_all_cookies()
            logger.info("Cookies cleared")
    
    def take_screenshot(self, filename: str):
        """Take a screenshot"""
        if self.driver:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
    
    def __enter__(self):
        """Context manager entry"""
        self.get_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_driver()
