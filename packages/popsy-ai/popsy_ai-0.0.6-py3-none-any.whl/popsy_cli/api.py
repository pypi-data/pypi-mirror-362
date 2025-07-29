#!/usr/bin/env python3
"""
CLI API client for Reddit DM automation using Popsy API
"""

import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import csv

import requests
from dataclasses import dataclass

# Configure basic logging (will be updated in main based on args)
logger = logging.getLogger(__name__)


@dataclass
class Thread:
    """Thread data structure matching the API response"""
    id: int
    title: str
    url: str
    author: str
    content: str
    score: int
    reasoning: str
    suggested_dm: Optional[str] = None
    suggested_comment: Optional[str] = None
    subreddit_name: str = ""
    created_at: str = ""


class PopsyAPIClient:
    """API client for Popsy Reddit automation"""

    def __init__(self, base_url: str = "https://app.popsy.ai", token: str = None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization"""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def fetch_threads(self,
                     subreddit_id: Optional[int] = None,
                     dm_sent: bool = False,
                     comment_sent: bool = False,
                     dm_queued: bool = False,
                     comment_queued: bool = False,
                     show_deleted: bool = False,
                     show_new: bool = True,
                     min_relevancy: Optional[int] = None,
                     page: int = 1,
                     page_size: int = 50,
                     sort_by: str = "by_date",
                     hide_already_dmed: bool = True) -> Dict:
        """Fetch threads from the API with filters"""

        params = {
            'page': page,
            'page_size': page_size,
            'sort_by': sort_by
        }

        if subreddit_id:
            params['subreddit_id'] = subreddit_id
        if dm_sent:
            params['dm_sent'] = 'true'
        if comment_sent:
            params['comment_sent'] = 'true'
        if dm_queued:
            params['dm_queued'] = 'true'
        if comment_queued:
            params['comment_queued'] = 'true'
        if show_deleted:
            params['show_deleted'] = 'true'
        if show_new:
            params['show_new'] = 'true'
        if min_relevancy is not None:
            params['min_relevancy'] = min_relevancy
        if hide_already_dmed:
            params['hide_already_dmed'] = 'true'

        url = f"{self.base_url}/api/threads"

        try:
            logger.debug(f"Making GET request to: {url}")
            logger.debug(f"Request params: {params}")
            logger.debug(f"Request headers: {self._get_headers()}")

            response = self.session.get(url, params=params, headers=self._get_headers())

            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Response data: {data}")
                logger.debug(f"Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                # API returns data under 'items' key, not 'results'
                items = data.get('items', [])
                logger.info(f"Fetched {len(items)} threads")
                return data
            else:
                logger.error(f"Failed to fetch threads: {response.status_code} - {response.text}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching threads: {e}")
            return {}

    def mark_thread_as_seen(self, thread_id: int) -> bool:
        """Mark a thread as seen"""
        url = f"{self.base_url}/api/threads/{thread_id}/seen"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Marked thread {thread_id} as seen")
                return True
            else:
                logger.error(f"Failed to mark thread {thread_id} as seen: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error marking thread {thread_id} as seen: {e}")
            return False

    def mark_thread_as_closed(self, thread_id: int) -> bool:
        """Mark a thread as closed"""
        url = f"{self.base_url}/api/threads/{thread_id}/close"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Marked thread {thread_id} as closed")
                return True
            else:
                logger.error(f"Failed to mark thread {thread_id} as closed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error marking thread {thread_id} as closed: {e}")
            return False

    def send_dm(self, thread_id: int) -> bool:
        """Mark DM as sent for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/dm"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Marked DM as sent for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to mark DM as sent for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error marking DM as sent for thread {thread_id}: {e}")
            return False

    def send_comment(self, thread_id: int) -> bool:
        """Mark comment as sent for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/comment"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Marked comment as sent for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to mark comment as sent for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error marking comment as sent for thread {thread_id}: {e}")
            return False

    def queue_dm(self, thread_id: int) -> bool:
        """Queue a DM for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/queue-dm"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Queued DM for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to queue DM for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error queuing DM for thread {thread_id}: {e}")
            return False

    def unqueue_dm(self, thread_id: int) -> bool:
        """Unqueue a DM for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/unqueue-dm"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Unqueued DM for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to unqueue DM for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error unqueuing DM for thread {thread_id}: {e}")
            return False

    def queue_comment(self, thread_id: int) -> bool:
        """Queue a comment for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/queue-comment"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Queued comment for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to queue comment for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error queuing comment for thread {thread_id}: {e}")
            return False

    def unqueue_comment(self, thread_id: int) -> bool:
        """Unqueue a comment for a thread"""
        url = f"{self.base_url}/api/threads/{thread_id}/unqueue-comment"

        try:
            response = self.session.post(url, headers=self._get_headers())
            if response.status_code == 200:
                logger.info(f"Unqueued comment for thread {thread_id}")
                return True
            else:
                logger.error(f"Failed to unqueue comment for thread {thread_id}: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error unqueuing comment for thread {thread_id}: {e}")
            return False


def parse_threads_response(data: Dict) -> List[Thread]:
    """Parse API response into Thread objects"""
    threads = []

    # API might return data under 'items' or 'results' key
    items = data.get('items', [])
    logger.debug(f"Parsing response with {len(items)} items")
    for item in items:
        # Extract thread data from nested structure
        thread_data = item.get('thread', {})
        analysis = item.get('analysis', {})

        thread = Thread(
            id=analysis.get('id', 0),
            title=thread_data.get('title', ''),
            url=thread_data.get('url', ''),
            author=thread_data.get('author', ''),
            content=thread_data.get('content', ''),
            score=analysis.get('score', 0),
            reasoning=analysis.get('reasoning', ''),
            suggested_dm=analysis.get('suggested_dm'),
            suggested_comment=analysis.get('suggested_comment'),
            subreddit_name=item.get('subreddit_name', ''),
            created_at=thread_data.get('created_at', '')
        )
        threads.append(thread)

    return threads


def process_threads_for_dm(api_client: PopsyAPIClient,
                          threads: List[Thread],
                          dm_sender_callback=None,
                          dry_run: bool = False) -> tuple[int, int]:
    """
    Process threads for DM automation with configurable DM sending

    Args:
        api_client: API client instance
        threads: List of threads to process
        dm_sender_callback: Function to call for sending DMs.
                           Should accept (thread, api_client) and return (success: bool, error_msg: str)
                           If None, will simulate DM sending
        dry_run: If True, won't actually send DMs or mark threads

    Returns:
        tuple: (processed_count, failed_count)
    """
    processed_count = 0
    failed_count = 0

    # Create log file for this session
    log_filename = f"logs/sent_messages_{datetime.now().strftime('%Y-%m-%d')}.csv"
    if not os.path.exists(log_filename):
        with open(log_filename, 'w', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['Timestamp', 'Thread_ID', 'Username', 'Status', 'Score', 'Subreddit'])

    author_set = set()
    # Default simulation callback
    def simulate_dm_sending(thread):
        logger.info(f"SIMULATION: Would send DM to u/{thread.author}")
        logger.info(f"SIMULATION: Message: {thread.suggested_dm[:100]}...")
        time.sleep(1)  # Simulate processing time
        return True, None

    # Use provided callback or default to simulation
    dm_callback = dm_sender_callback or simulate_dm_sending

    for thread in threads:
        try:
            logger.info(f"Processing thread: {thread.title[:50]}... (ID: {thread.id})")
            logger.info(f"Author: u/{thread.author}")
            logger.info(f"Score: {thread.score}")
            logger.info(f"Subreddit: {thread.subreddit_name}")

            if not thread.suggested_dm:
                logger.warning(f"No suggested DM for thread {thread.id}, skipping")
                continue

            logger.info(f"Suggested DM: {thread.suggested_dm[:100]}...")

            if not dry_run:
                # Mark thread as seen first
                api_client.mark_thread_as_seen(thread.id)

                if thread.author in author_set:
                    logger.warning(f"Skipping because {thread.author} has already been DMed")
                    continue
                author_set.add(thread.author)

                # Send the DM using the callback
                dm_success, error_msg = dm_callback(thread)

                if dm_success:
                    # Mark DM as sent in API
                    api_client.send_dm(thread.id)

                    # Mark thread as closed
                    api_client.mark_thread_as_closed(thread.id)

                    processed_count += 1

                    # Log successful DM
                    with open(log_filename, 'a', newline='') as log_file:
                        log_writer = csv.writer(log_file)
                        log_writer.writerow([
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            thread.id,
                            thread.author,
                            'SUCCESS',
                            thread.score,
                            thread.subreddit_name
                        ])

                    logger.info(f"✅ Successfully processed thread {thread.id}")

                else:
                    failed_count += 1

                    # Log failed DM
                    with open(log_filename, 'a', newline='') as log_file:
                        log_writer = csv.writer(log_file)
                        log_writer.writerow([
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            thread.id,
                            thread.author,
                            f'FAILED: {error_msg or "Unknown error"}',
                            thread.score,
                            thread.subreddit_name
                        ])

                    logger.error(f"❌ Failed to process thread {thread.id}: {error_msg}")

                    # If we hit a daily limit, stop processing
                    if error_msg and "Daily" in error_msg and "limit" in error_msg:
                        logger.warning("Daily limit reached, stopping automation")
                        break

                # Add delay between processing threads
                time.sleep(2)

            else:
                logger.info("DRY RUN: Would process this thread")
                processed_count += 1

            print("-" * 80)

        except Exception as e:
            logger.error(f"Error processing thread {thread.id}: {e}")
            failed_count += 1
            continue

    return processed_count, failed_count


def setup_logging(verbose: bool = False, debug: bool = False):
    """Setup logging based on verbosity level"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Determine log level
    if debug:
        log_level = logging.DEBUG
    elif verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/api_client_{datetime.now().strftime("%Y-%m-%d")}.log'),
            logging.StreamHandler()
        ],
        force=True  # Override any existing configuration
    )

    # Set requests logging level
    if debug:
        logging.getLogger("requests").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
    else:
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)


def show_configuration(config: dict, args_dict: dict, effective_values: dict = None):
    """Display current configuration in verbose mode"""
    logger.info("=" * 80)
    logger.info("CURRENT CONFIGURATION")
    logger.info("=" * 80)

    logger.info("Command Line Arguments:")
    for arg, value in args_dict.items():
        logger.info(f"  --{arg.replace('_', '-')}: {value}")

    logger.info("\nConfiguration File Settings:")
    if config:
        for key, value in config.items():
            # Don't log sensitive information
            if 'token' in key.lower() or 'password' in key.lower():
                logger.info(f"  {key}: [REDACTED]")
            else:
                logger.info(f"  {key}: {value}")
    else:
        logger.info("  No configuration file loaded")

    logger.info("\nEnvironment Variables:")
    env_vars = ['POPSY_API_TOKEN', 'BASE_URL']
    for env_var in env_vars:
        value = os.getenv(env_var)
        if value:
            if 'token' in env_var.lower():
                logger.info(f"  {env_var}: [REDACTED]")
            else:
                logger.info(f"  {env_var}: {value}")
        else:
            logger.info(f"  {env_var}: Not set")

    if effective_values:
        logger.info("\nEFFECTIVE VALUES (after precedence resolution):")
        for key, value in effective_values.items():
            if 'token' in key.lower() or 'password' in key.lower():
                logger.info(f"  {key}: [REDACTED]")
            else:
                logger.info(f"  {key}: {value}")

    logger.info("=" * 80)


def process_threads_for_comment(api_client: PopsyAPIClient,
                               threads: List[Thread],
                               comment_sender_callback=None,
                               dry_run: bool = False) -> tuple[int, int]:
    """
    Process threads for comment automation with configurable comment sending

    Args:
        api_client: API client instance
        threads: List of threads to process
        comment_sender_callback: Function to call for posting comments.
                                Should accept (thread, api_client) and return (success: bool, error_msg: str)
                                If None, will simulate comment posting
        dry_run: If True, won't actually post comments or mark threads

    Returns:
        tuple: (processed_count, failed_count)
    """
    processed_count = 0
    failed_count = 0

    # Create log file for this session
    log_filename = f"logs/sent_comments_{datetime.now().strftime('%Y-%m-%d')}.csv"
    if not os.path.exists(log_filename):
        with open(log_filename, 'w', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['Timestamp', 'Thread_ID', 'Thread_URL', 'Status', 'Score', 'Subreddit'])

    # Default simulation callback
    def simulate_comment_posting(thread):
        logger.info(f"SIMULATION: Would post comment on thread: {thread.url}")
        logger.info(f"SIMULATION: Comment: {thread.suggested_comment[:100]}...")
        time.sleep(1)  # Simulate processing time
        return True, None

    # Use provided callback or default to simulation
    comment_callback = comment_sender_callback or simulate_comment_posting

    for thread in threads:
        try:
            logger.info(f"Processing thread for comment: {thread.title[:50]}... (ID: {thread.id})")
            logger.info(f"Author: u/{thread.author}")
            logger.info(f"Score: {thread.score}")
            logger.info(f"Subreddit: {thread.subreddit_name}")

            if not thread.suggested_comment:
                logger.warning(f"No suggested comment for thread {thread.id}, skipping")
                continue

            logger.info(f"Suggested Comment: {thread.suggested_comment[:100]}...")

            if not dry_run:
                # Mark thread as seen first
                api_client.mark_thread_as_seen(thread.id)

                # Post the comment using the callback
                comment_success, error_msg = comment_callback(thread)

                if comment_success:
                    # Mark comment as sent in API
                    api_client.send_comment(thread.id)

                    # Mark thread as closed
                    api_client.mark_thread_as_closed(thread.id)

                    processed_count += 1

                    # Log successful comment
                    with open(log_filename, 'a', newline='') as log_file:
                        log_writer = csv.writer(log_file)
                        log_writer.writerow([
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            thread.id,
                            thread.url,
                            'SUCCESS',
                            thread.score,
                            thread.subreddit_name
                        ])

                    logger.info(f"✅ Successfully processed thread {thread.id}")

                else:
                    failed_count += 1

                    # Log failed comment
                    with open(log_filename, 'a', newline='') as log_file:
                        log_writer = csv.writer(log_file)
                        log_writer.writerow([
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            thread.id,
                            thread.url,
                            f'FAILED: {error_msg or "Unknown error"}',
                            thread.score,
                            thread.subreddit_name
                        ])

                    logger.error(f"❌ Failed to process thread {thread.id}: {error_msg}")

                    # If we hit a daily limit, stop processing
                    if error_msg and "Daily" in error_msg and "limit" in error_msg:
                        logger.warning("Daily limit reached, stopping automation")
                        break

                # Add delay between processing threads
                time.sleep(2)

            else:
                logger.info("DRY RUN: Would post comment and mark thread as processed")
                processed_count += 1

            print("-" * 80)

        except Exception as e:
            logger.error(f"Error processing thread {thread.id}: {e}")
            failed_count += 1
            continue

    return processed_count, failed_count

