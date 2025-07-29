#!/usr/bin/env python3
"""
WebDriver Manager
Unified WebDriver setup and management for all scraping operations.
"""

import logging
import os
import time
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class WebDriverManager:
    """Unified WebDriver manager with consistent setup and teardown."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize WebDriver manager with configuration."""
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.default_timeout = config.get('timeout', 30)
        self.headless = config.get('headless', True)
        self.user_agent = config.get('user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    def setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome WebDriver with optimal configuration."""
        try:
            chrome_options = Options()

            # Core options for stability
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument(f"--user-agent={self.user_agent}")

            # Anti-detection options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Performance optimization
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript") if self.config.get('disable_js', False) else None

            # Memory management
            chrome_options.add_argument("--memory-pressure-off")
            chrome_options.add_argument("--max_old_space_size=4096")

            # Setup service
            service = Service(ChromeDriverManager().install())

            # Create driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Execute anti-detection script
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            # Set timeouts
            self.driver.implicitly_wait(self.default_timeout)
            self.driver.set_page_load_timeout(self.default_timeout)

            logger.info("WebDriver initialized successfully")
            return self.driver

        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {e}")
            raise WebDriverException(f"WebDriver setup failed: {e}")

    def navigate_to(self, url: str, wait_for_element: Optional[str] = None) -> bool:
        """Navigate to URL with optional element wait."""
        try:
            if not self.driver:
                self.setup_driver()

            if not self.driver:
                logger.error("Failed to initialize WebDriver")
                return False

            logger.info(f"Navigating to: {url}")
            self.driver.get(url)

            # Wait for specific element if provided
            if wait_for_element:
                WebDriverWait(self.driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
                )
                logger.info(f"Successfully loaded page with element: {wait_for_element}")
            else:
                # Wait for body to load
                WebDriverWait(self.driver, self.default_timeout).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                logger.info("Page loaded successfully")

            return True

        except TimeoutException:
            logger.warning(f"Timeout waiting for page to load: {url}")
            return False
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False

    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Wait for element to be present."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return False

            wait_time = timeout or self.default_timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except TimeoutException:
            logger.warning(f"Element not found within {wait_time}s: {selector}")
            return False

    def click_element(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Click element with wait."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return False

            wait_time = timeout or self.default_timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            element.click()
            logger.info(f"Clicked element: {selector}")
            return True
        except TimeoutException:
            logger.warning(f"Element not clickable within {wait_time}s: {selector}")
            return False
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            return False

    def scroll_to_bottom(self, pause_time: float = 2.0) -> None:
        """Scroll to bottom of page with pause."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return

            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(pause_time)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            logger.info("Scrolled to bottom of page")

        except Exception as e:
            logger.error(f"Failed to scroll to bottom: {e}")

    def handle_iframe(self, iframe_selector: str) -> bool:
        """Switch to iframe context."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return False

            iframe = self.driver.find_element(By.CSS_SELECTOR, iframe_selector)
            self.driver.switch_to.frame(iframe)
            logger.info(f"Switched to iframe: {iframe_selector}")
            return True
        except Exception as e:
            logger.error(f"Failed to switch to iframe {iframe_selector}: {e}")
            return False

    def switch_to_default_content(self) -> None:
        """Switch back to default content."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return

            self.driver.switch_to.default_content()
            logger.info("Switched back to default content")
        except Exception as e:
            logger.error(f"Failed to switch to default content: {e}")

    def take_screenshot(self, filename: str) -> bool:
        """Take screenshot for debugging."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return False

            screenshot_path = os.path.join("logs", "screenshots", filename)
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False

    def get_page_source(self) -> str:
        """Get current page source."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return ""

            return self.driver.page_source
        except Exception as e:
            logger.error(f"Failed to get page source: {e}")
            return ""

    def execute_script(self, script: str) -> Any:
        """Execute JavaScript."""
        try:
            if not self.driver:
                logger.error("WebDriver not initialized")
                return None

            return self.driver.execute_script(script)
        except Exception as e:
            logger.error(f"Failed to execute script: {e}")
            return None

    def quit(self) -> None:
        """Quit WebDriver safely."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("WebDriver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting WebDriver: {e}")

    def __enter__(self) -> "WebDriverManager":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """Context manager exit."""
        self.quit()
