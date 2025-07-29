#!/usr/bin/env python3
"""
Pagination Manager
Unified pagination handling for directory scraping.
"""

import logging
import time
from typing import Optional, Dict, Any, Generator
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class PaginationManager:
    """Handles pagination patterns for directory scraping."""

    def __init__(self, driver_manager: Any, config: Dict[str, Any]):
        """Initialize pagination manager."""
        self.driver_manager = driver_manager
        self.config = config
        self.max_pages = config.get('max_pages', 10)
        self.page_delay = config.get('page_delay', 3.0)
        self.current_page = 1

        # Common pagination selectors
        self.pagination_selectors = config.get('pagination_selectors', {
            'next_button': [
                'a[aria-label*="Next"]',
                'button[aria-label*="Next"]',
                '.next-page',
                '.pagination-next',
                '[data-action="next"]',
                'a:contains("Next")',
                'button:contains("Next")',
                '.btn-next',
                '.page-next'
            ],
            'load_more': [
                'button:contains("Load More")',
                'button:contains("Show More")',
                '.load-more',
                '.show-more',
                '[data-action="load-more"]',
                '.btn-load-more',
                '.pagination-load-more'
            ],
            'page_numbers': [
                '.pagination a',
                '.page-numbers a',
                '.pager a',
                '[data-page]'
            ]
        })

    def detect_pagination_type(self) -> str:
        """Detect the type of pagination on current page."""
        driver = self.driver_manager.driver

        # Check for load more button
        for selector in self.pagination_selectors['load_more']:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and any(el.is_displayed() for el in elements):
                    logger.info(f"Detected load more pagination: {selector}")
                    return 'load_more'
            except Exception:
                continue

        # Check for next button
        for selector in self.pagination_selectors['next_button']:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and any(el.is_displayed() for el in elements):
                    logger.info(f"Detected next button pagination: {selector}")
                    return 'next_button'
            except Exception:
                continue

        # Check for page numbers
        for selector in self.pagination_selectors['page_numbers']:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 1:  # Multiple page links
                    logger.info(f"Detected numbered pagination: {selector}")
                    return 'page_numbers'
            except Exception:
                continue

        # Check for infinite scroll
        if self._has_infinite_scroll():
            logger.info("Detected infinite scroll pagination")
            return 'infinite_scroll'

        logger.info("No pagination detected")
        return 'none'

    def _has_infinite_scroll(self) -> bool:
        """Check if page has infinite scroll."""
        try:
            driver = self.driver_manager.driver
            initial_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll back up to reset position
            driver.execute_script("window.scrollTo(0, 0);")

            return bool(new_height > initial_height)
        except Exception:
            return False

    def paginate_all_pages(self) -> Generator[int, None, None]:
        """Generator that yields page numbers while paginating through all pages."""
        pagination_type = self.detect_pagination_type()

        if pagination_type == 'none':
            yield 1
            return

        logger.info(f"Starting pagination with type: {pagination_type}")

        # Yield first page
        yield 1

        if pagination_type == 'load_more':
            yield from self._paginate_load_more()
        elif pagination_type == 'next_button':
            yield from self._paginate_next_button()
        elif pagination_type == 'page_numbers':
            yield from self._paginate_page_numbers()
        elif pagination_type == 'infinite_scroll':
            yield from self._paginate_infinite_scroll()

    def _paginate_load_more(self) -> Generator[int, None, None]:
        """Handle load more button pagination."""
        page_count = 1

        while page_count < self.max_pages:
            load_more_clicked = False

            # Try each load more selector
            for selector in self.pagination_selectors['load_more']:
                if self.driver_manager.click_element(selector, timeout=5):
                    load_more_clicked = True
                    break

            if not load_more_clicked:
                logger.info("No more load more buttons found")
                break

            # Wait for new content to load
            time.sleep(self.page_delay)
            page_count += 1

            logger.info(f"Loaded more content - page {page_count}")
            yield page_count

    def _paginate_next_button(self) -> Generator[int, None, None]:
        """Handle next button pagination."""
        page_count = 1

        while page_count < self.max_pages:
            next_clicked = False

            # Try each next button selector
            for selector in self.pagination_selectors['next_button']:
                if self.driver_manager.click_element(selector, timeout=5):
                    next_clicked = True
                    break

            if not next_clicked:
                logger.info("No more next buttons found")
                break

            # Wait for new page to load
            time.sleep(self.page_delay)
            page_count += 1

            logger.info(f"Navigated to page {page_count}")
            yield page_count

    def _paginate_page_numbers(self) -> Generator[int, None, None]:
        """Handle numbered pagination."""
        driver = self.driver_manager.driver
        page_count = 1

        while page_count < self.max_pages:
            # Find next page number
            next_page = page_count + 1
            page_found = False

            for selector in self.pagination_selectors['page_numbers']:
                try:
                    page_links = driver.find_elements(By.CSS_SELECTOR, selector)

                    for link in page_links:
                        if (link.text.strip() == str(next_page) or
                            link.get_attribute('data-page') == str(next_page)):
                            link.click()
                            page_found = True
                            break

                    if page_found:
                        break

                except Exception as e:
                    logger.debug(f"Error with page selector {selector}: {e}")
                    continue

            if not page_found:
                logger.info(f"Page {next_page} not found")
                break

            # Wait for new page to load
            time.sleep(self.page_delay)
            page_count += 1

            logger.info(f"Navigated to page {page_count}")
            yield page_count

    def _paginate_infinite_scroll(self) -> Generator[int, None, None]:
        """Handle infinite scroll pagination."""
        driver = self.driver_manager.driver
        page_count = 1

        while page_count < self.max_pages:
            # Get current scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content
            time.sleep(self.page_delay)

            # Check if new content loaded
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                logger.info("No more content to load via infinite scroll")
                break

            page_count += 1
            logger.info(f"Loaded infinite scroll content - page {page_count}")
            yield page_count

    def navigate_to_page(self, page_number: int) -> bool:
        """Navigate directly to a specific page number."""
        try:
            driver = self.driver_manager.driver

            # Try to find and click the specific page number
            for selector in self.pagination_selectors['page_numbers']:
                try:
                    page_links = driver.find_elements(By.CSS_SELECTOR, selector)

                    for link in page_links:
                        if (link.text.strip() == str(page_number) or
                            link.get_attribute('data-page') == str(page_number)):
                            link.click()
                            time.sleep(self.page_delay)
                            self.current_page = page_number
                            logger.info(f"Successfully navigated to page {page_number}")
                            return True

                except Exception as e:
                    logger.debug(f"Error with page navigation selector {selector}: {e}")
                    continue

            logger.warning(f"Could not navigate to page {page_number}")
            return False

        except Exception as e:
            logger.error(f"Error navigating to page {page_number}: {e}")
            return False

    def get_total_pages(self) -> Optional[int]:
        """Try to determine total number of pages."""
        try:
            driver = self.driver_manager.driver

            # Look for pagination info text
            pagination_info_selectors = [
                '.pagination-info',
                '.page-info',
                '.results-info',
                '[class*="total"]',
                '[class*="count"]'
            ]

            for selector in pagination_info_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text
                        # Look for patterns like "Page 1 of 10" or "1-20 of 200"
                        import re
                        patterns = [
                            r'Page \d+ of (\d+)',
                            r'of (\d+) pages',
                            r'(\d+) pages total'
                        ]

                        for pattern in patterns:
                            match = re.search(pattern, text, re.IGNORECASE)
                            if match:
                                total_pages = int(match.group(1))
                                logger.info(f"Found total pages: {total_pages}")
                                return total_pages

                except Exception:
                    continue

            # Try to count page number links
            for selector in self.pagination_selectors['page_numbers']:
                try:
                    page_links = driver.find_elements(By.CSS_SELECTOR, selector)
                    if page_links:
                        # Find the highest page number
                        max_page = 0
                        for link in page_links:
                            try:
                                page_num = int(link.text.strip())
                                max_page = max(max_page, page_num)
                            except (ValueError, AttributeError):
                                continue

                        if max_page > 0:
                            logger.info(f"Estimated total pages from links: {max_page}")
                            return max_page

                except Exception:
                    continue

            logger.info("Could not determine total pages")
            return None

        except Exception as e:
            logger.error(f"Error determining total pages: {e}")
            return None

    def reset(self) -> None:
        """Reset pagination state."""
        self.current_page = 1
        logger.info("Pagination state reset")
