"""
Anti-Detection Techniques
Human-like behavior simulation
"""

import time
import random
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


class AntiDetection:
    """Anti-detection techniques for web scraping"""
    
    @staticmethod
    def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Random delay between actions
        
        Args:
            min_seconds: Minimum delay
            max_seconds: Maximum delay
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    def human_type(element: WebElement, text: str, typing_speed: float = 0.1):
        """
        Type text like a human with random delays
        
        Args:
            element: Input element
            text: Text to type
            typing_speed: Base typing speed (seconds per character)
        """
        element.clear()
        time.sleep(random.uniform(0.2, 0.5))
        
        for char in text:
            element.send_keys(char)
            # Random delay between keystrokes
            delay = random.uniform(typing_speed * 0.5, typing_speed * 1.5)
            time.sleep(delay)
        
        # Small delay after typing
        time.sleep(random.uniform(0.3, 0.7))
    
    @staticmethod
    def human_click(element: WebElement, driver: webdriver.Chrome = None):
        """
        Click element with human-like behavior
        
        Args:
            element: Element to click
            driver: WebDriver instance
        """
        try:
            # Try to move to element first
            if driver:
                actions = ActionChains(driver)
                actions.move_to_element(element)
                actions.pause(random.uniform(0.1, 0.3))
                actions.click()
                actions.perform()
            else:
                element.click()
        except Exception:
            # Fallback to JavaScript click
            if driver:
                driver.execute_script("arguments[0].click();", element)
            else:
                element.click()
        
        # Small delay after click
        time.sleep(random.uniform(0.3, 0.7))
    
    @staticmethod
    def random_scroll(driver: webdriver.Chrome, scroll_pause: float = 0.5):
        """
        Scroll page randomly to appear human
        
        Args:
            driver: WebDriver instance
            scroll_pause: Pause between scrolls
        """
        # Get page height
        page_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")
        
        # Scroll in random chunks
        current_position = 0
        while current_position < page_height:
            # Random scroll amount (200-500 pixels)
            scroll_amount = random.randint(200, 500)
            current_position += scroll_amount
            
            # Scroll
            driver.execute_script(f"window.scrollTo(0, {current_position});")
            
            # Random pause
            time.sleep(random.uniform(scroll_pause * 0.5, scroll_pause * 1.5))
            
            # Occasionally scroll back up a bit
            if random.random() < 0.1:
                scroll_back = random.randint(50, 150)
                current_position -= scroll_back
                driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.2, 0.5))
    
    @staticmethod
    def smooth_scroll_to_element(driver: webdriver.Chrome, element: WebElement):
        """
        Smoothly scroll to an element
        
        Args:
            driver: WebDriver instance
            element: Target element
        """
        # Get element position
        element_position = driver.execute_script(
            "return arguments[0].getBoundingClientRect().top + window.pageYOffset;",
            element
        )
        
        # Current scroll position
        current_position = driver.execute_script("return window.pageYOffset;")
        
        # Calculate steps
        distance = element_position - current_position
        steps = abs(int(distance / 100))
        
        # Smooth scroll
        for i in range(steps):
            step_position = current_position + (distance / steps * (i + 1))
            driver.execute_script(f"window.scrollTo(0, {step_position});")
            time.sleep(random.uniform(0.01, 0.03))
    
    @staticmethod
    def mouse_movement(driver: webdriver.Chrome, element: WebElement):
        """
        Move mouse to element in a human-like way
        
        Args:
            driver: WebDriver instance
            element: Target element
        """
        actions = ActionChains(driver)
        
        # Random movements before reaching target
        for _ in range(random.randint(1, 3)):
            random_x = random.randint(-50, 50)
            random_y = random.randint(-50, 50)
            actions.move_by_offset(random_x, random_y)
            actions.pause(random.uniform(0.05, 0.15))
        
        # Move to target
        actions.move_to_element(element)
        actions.pause(random.uniform(0.1, 0.3))
        actions.perform()
    
    @staticmethod
    def inject_noise():
        """Add random noise to timing patterns"""
        time.sleep(random.uniform(0.01, 0.05))
    
    @staticmethod
    def random_mouse_movement(driver: webdriver.Chrome, num_movements: int = 3):
        """
        Perform random mouse movements
        
        Args:
            driver: WebDriver instance
            num_movements: Number of random movements
        """
        actions = ActionChains(driver)
        
        for _ in range(num_movements):
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            actions.move_by_offset(x, y)
            actions.pause(random.uniform(0.1, 0.3))
        
        actions.perform()
    
    @staticmethod
    def simulate_reading(duration: float = 3.0):
        """
        Simulate reading by waiting
        
        Args:
            duration: Average reading duration
        """
        # Random reading time
        reading_time = random.uniform(duration * 0.7, duration * 1.3)
        time.sleep(reading_time)