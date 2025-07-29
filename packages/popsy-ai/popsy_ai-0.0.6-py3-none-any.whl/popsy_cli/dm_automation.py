#!/usr/bin/env python3
"""
Enhanced Reddit DM automation that uses API instead of CSV files
"""

import time
import random
import os

from camoufox import Camoufox
from browserforge.fingerprints import Screen

import logging

# Import Thread type for type hints
from popsy_cli.api import Thread

logger = logging.getLogger(__name__)


class BrowserDMSender:
    """Browser automation for sending DMs"""

    def __init__(self, headless: bool = False):
        self.browser_context = None
        self.browser = None
        self.page = None
        self.headless = headless
        self.constrains = Screen(max_width=1680, max_height=1050)

    def setup_browser(self):
        """Setup the browser with persistent context"""
        # Create user data directory to persist login
        if not os.path.exists('browser_data'):
            os.makedirs('browser_data')

        # Create the Camoufox context manager
        self.browser_context = Camoufox(
            headless=self.headless,
            humanize=True,  # Enable human-like cursor movement
            os='macos',     # Use macOS fingerprint for MacBook
            locale='en-US', # Set locale automatically
            geoip=True,     # Auto-detect geolocation based on IP
            screen=self.constrains,
            persistent_context=True,
            user_data_dir='browser_data'  # Persist login and browser data
        )

        # Enter the context manager to get the actual browser object
        self.browser = self.browser_context.__enter__()
        self.page = self.browser.new_page()
        self.page.goto("https://www.reddit.com")

        input("Press Enter to continue after logging in (Just press enter if already logged in)")

    def send_dm_to_user(self, username: str, message: str) -> tuple[bool, str]:
        """
        Send a DM to a specific user

        Returns:
            tuple: (success: bool, error_message: str)
        """
        try:
            logger.info(f"Sending DM to {username}")

            self.page.goto(f'https://www.reddit.com/{username}/')
            time.sleep(random.uniform(4, 5))

            self.page.click('a[aria-label="Open chat"]')
            time.sleep(random.uniform(4, 5))

            self.page.keyboard.type(message)
            time.sleep(random.uniform(4, 5))

            self.page.keyboard.press('Enter')
            time.sleep(random.uniform(4, 5))

            # Check if daily limit is reached
            element_exists = self.page.query_selector('.theme-rpl.hasIcon.hasAction') is not None

            if element_exists:
                error_msg = "Daily DM limit reached"
                logger.warning(error_msg)
                return False, error_msg

            logger.info(f"Successfully sent DM to {username}")

            # Add delay between DMs
            delay = random.uniform(3, 5)  # 3, 5 seconds between DMs
            logger.info(f"Waiting {delay:.1f} seconds before next action...")
            time.sleep(delay)

            return True, None

        except Exception as e:
            error_msg = f"Failed to send DM to {username}: {e}"
            logger.error(error_msg)
            return False, str(e)

    def close(self):
        """Close the browser"""
        if self.browser_context:
            try:
                self.browser_context.__exit__(None, None, None)
            except Exception as e:
                logger.warning(f"Error closing browser: {e}")
            finally:
                self.browser_context = None
                self.browser = None
                self.page = None


def create_browser_dm_callback(browser_sender: BrowserDMSender):
    """
    Create a callback function for browser-based DM sending

    Args:
        browser_sender: BrowserDMSender instance

    Returns:
        Callback function compatible with process_threads_for_dm
    """
    def browser_dm_callback(thread: Thread) -> tuple[bool, str]:
        """Callback function for sending DMs via browser automation"""
        if not thread.suggested_dm:
            return False, "No suggested DM available"

        return browser_sender.send_dm_to_user(thread.author, thread.suggested_dm)

    return browser_dm_callback
