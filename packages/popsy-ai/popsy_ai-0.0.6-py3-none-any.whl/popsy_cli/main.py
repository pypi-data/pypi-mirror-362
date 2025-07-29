#!/usr/bin/env python3
"""
CLI entry point for Reddit DM automation using Popsy API
"""

import argparse
import json
import logging
import os
import sys
from importlib import metadata

from popsy_cli.api import (
    PopsyAPIClient,
    parse_threads_response,
    process_threads_for_dm,
    process_threads_for_comment,
    setup_logging,
    show_configuration
)

# Import browser automation functionality
try:
    from popsy_cli.dm_automation import BrowserDMSender, create_browser_dm_callback
    BROWSER_AVAILABLE = True
except ImportError as e:
    BROWSER_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"Browser automation not available: {e}")

logger = logging.getLogger(__name__)


def get_version():
    """Get the version of the CLI package"""
    try:
        return metadata.version("popsy-ai")
    except metadata.PackageNotFoundError:
        return "unknown"


def cmd_version(args):
    """Handle version command"""
    version = get_version()
    print(f"popsy-ai version {version}")


def cmd_run(args):
    """Handle run command"""
    # Setup logging based on verbosity
    setup_logging(verbose=args.verbose, debug=args.debug)

    # Load configuration from file if it exists
    config = {}
    if os.path.exists(args.config):
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {args.config}")
        except Exception as e:
            logger.warning(f"Failed to load config file: {e}")

    # Override config with command line arguments (only if explicitly provided)
    token = args.token or config.get('token') or os.getenv('POPSY_API_TOKEN')
    base_url = args.base_url or config.get('base_url') or 'https://app.popsy.ai'

    # Handle other config values with proper precedence: CLI args -> config file -> defaults
    # Define defaults here instead of in parser
    defaults = {
        'min_relevancy': 0,
        'max_threads': 100,
        'page_size': 100,
        'sort_by': 'by_date',
        'mode': 'dm',
        'show_new': False,
        'hide_already_dmed': True,
        'queued': True,
        'browser': True,
        'headless': False
    }

    def get_effective_value(arg_name, arg_value, config_key=None):
        """Get effective value: CLI arg (if provided) -> config -> default"""
        config_key = config_key or arg_name
        default_value = defaults.get(arg_name)

        # If CLI arg is provided (not None), use it
        if arg_value is not None:
            return arg_value
        # Otherwise use config value or default
        return config.get(config_key, default_value)

    def get_effective_bool_value(arg_name, arg_value, config_key=None):
        """Get effective boolean value for store_true actions"""
        config_key = config_key or arg_name
        default_value = defaults.get(arg_name)

        # For store_true actions, if the flag was passed, it's True
        # If not passed, check config then default
        if arg_value:  # Flag was passed on CLI
            return True
        # Otherwise use config value or default
        return config.get(config_key, default_value)

    min_relevancy = get_effective_value('min_relevancy', args.min_relevancy)
    max_threads = get_effective_value('max_threads', args.max_threads)
    page_size = get_effective_value('page_size', args.page_size)
    sort_by = get_effective_value('sort_by', args.sort_by)
    mode = get_effective_value('mode', args.mode)
    show_new = get_effective_bool_value('show_new', args.show_new)
    use_browser = get_effective_bool_value('browser', args.browser)
    headless = get_effective_bool_value('headless', args.headless)
    queued = get_effective_bool_value('queued', args.queued)

    # Handle hide_already_dmed with override logic
    hide_already_dmed = get_effective_bool_value('hide_already_dmed', args.hide_already_dmed)
    if args.show_already_dmed:
        hide_already_dmed = False

    # Validate browser automation requirements
    if use_browser and not BROWSER_AVAILABLE:
        logger.error("Browser automation requested but dependencies not available. Install camoufox and browserforge.")
        return

    # Browser mode only works with DM mode
    if use_browser and mode != 'dm':
        logger.error("Browser automation is only available for DM mode (--mode dm)")
        return

    # Show configuration if verbose mode is enabled
    if args.verbose or args.debug:
        effective_values = {
            'token': '[REDACTED]' if token else 'Not set',
            'base_url': base_url,
            'min_relevancy': min_relevancy,
            'max_threads': max_threads,
            'page_size': page_size,
            'sort_by': sort_by,
            'mode': mode,
            'show_new': show_new,
            'hide_already_dmed': hide_already_dmed,
            'queued': queued,
            'use_browser': use_browser,
            'headless': headless,
        }
        show_configuration(config, vars(args), effective_values)

    if not token:
        logger.error("No API token provided. Use --token, config file, or POPSY_API_TOKEN env var")
        return

    automation_type = "BROWSER AUTOMATION" if use_browser else "API SIMULATION"
    logger.info("=" * 80)
    logger.info(f"REDDIT {mode.upper()} AUTOMATION - {automation_type}")
    logger.info("=" * 80)
    logger.info(f"Base URL: {base_url}")
    logger.info(f"Min Relevancy: {min_relevancy}")
    logger.info(f"Max Threads: {max_threads}")
    logger.info(f"Mode: {mode}")
    logger.info(f"Queued: {queued}")
    logger.info(f"Hide Already DMed: {hide_already_dmed}")
    logger.info(f"Use Browser: {use_browser}")
    if use_browser:
        logger.info(f"Headless Mode: {headless}")
    logger.info(f"Dry Run: {args.dry_run}")
    logger.info("=" * 80)
    # Setup browser automation if requested
    browser_sender = None
    dm_callback = None

    with PopsyAPIClient(base_url=base_url, token=token) as api_client:
        try:
            threads_data = api_client.fetch_threads(
                subreddit_id=args.subreddit_id,
                dm_sent=args.dm_sent,
                comment_sent=args.comment_sent,
                dm_queued=True if queued and mode == 'dm' else False,
                comment_queued=True if queued and mode == 'comment' else False,
                show_deleted=args.show_deleted,
                show_new=show_new,
                min_relevancy=min_relevancy,
                page_size=page_size,
                sort_by=sort_by,
                hide_already_dmed=hide_already_dmed
            )

            if not threads_data:
                logger.warning("No threads data received")
                return

            threads = parse_threads_response(threads_data)

            if not threads:
                logger.info("No threads found matching criteria")
                return

            # Limit to max_threads
            threads = threads[:max_threads]

            logger.info(f"Found {len(threads)} threads to process")

            if mode == 'dm':
                if use_browser and not args.dry_run:
                    logger.info("Setting up browser for DM automation...")
                    browser_sender = BrowserDMSender(headless=headless)
                    browser_sender.setup_browser()
                    dm_callback = create_browser_dm_callback(browser_sender)
                    logger.info("Browser automation ready!")

                processed_count, failed_count = process_threads_for_dm(
                    api_client,
                    threads,
                    dm_sender_callback=dm_callback,
                    dry_run=args.dry_run
                )
            else:  # comment mode
                if use_browser:
                    logger.warning("Browser automation not supported for comment mode, falling back to simulation")

                processed_count, failed_count = process_threads_for_comment(
                    api_client,
                    threads,
                    dry_run=args.dry_run
                )

            logger.info("=" * 80)
            logger.info(f"COMPLETED: Processed {processed_count} threads, {failed_count} failed")
            logger.info("=" * 80)

        except Exception as e:
            logger.error(f"Error in main execution: {e}")
        finally:
            # Clean up browser if it was used
            if browser_sender:
                logger.info("Closing browser...")
                browser_sender.close()


def main():
    """Main CLI function with subcommands"""
    parser = argparse.ArgumentParser(
        description='Popsy AI CLI - Reddit DM automation using Popsy API',
        prog='popsy'
    )

    # Add global version option
    parser.add_argument('--version', action='version', version=f'%(prog)s {get_version()}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Version subcommand
    version_parser = subparsers.add_parser('version', help='Show version information')
    version_parser.set_defaults(func=cmd_version)

    # Run subcommand (main functionality)
    run_parser = subparsers.add_parser('run', help='Run Reddit Automation')
    run_parser.set_defaults(func=cmd_run)

    # Add all the run command arguments
    run_parser.add_argument('--token', type=str, help='API authentication token')
    run_parser.add_argument('--base-url', type=str,
                           help='Base URL of the API (default: https://app.popsy.ai)')
    run_parser.add_argument('--min-relevancy', type=int,
                           help='Minimum relevancy score (0-100, default: 90)')
    run_parser.add_argument('--subreddit-id', type=int,
                           help='Filter by specific subreddit ID')
    run_parser.add_argument('--page-size', type=int,
                           help='Number of threads to fetch per page (default: 50)')
    run_parser.add_argument('--max-threads', type=int,
                           help='Maximum number of threads to process (default: 100)')
    run_parser.add_argument('--dry-run', action='store_true',
                           help='Run without actually sending DMs or marking threads')
    run_parser.add_argument('--dm-sent', action='store_true',
                           help='Include sent threads')
    run_parser.add_argument('--comment-sent', action='store_true',
                           help='Include posted threads')
    run_parser.add_argument('--queued', action='store_true',
                           help='Include queued threads')
    run_parser.add_argument('--show-deleted', action='store_true',
                           help='Include deleted threads')
    run_parser.add_argument('--show-new', action='store_true',
                           help='Include new threads (default: False)')
    run_parser.add_argument('--hide-already-dmed', action='store_true',
                           help='Hide threads from authors already DMed (default: True)')
    run_parser.add_argument('--show-already-dmed', action='store_true',
                           help='Show threads from authors already DMed (overrides --hide-already-dmed)')
    run_parser.add_argument('--config', type=str, default='config.json',
                           help='Configuration file path (default: config.json)')
    run_parser.add_argument('--mode', type=str, choices=['dm', 'comment'],
                           help='Processing mode: dm or comment (default: dm)')
    run_parser.add_argument('--sort-by', type=str, choices=['by_relevancy', 'by_date'],
                           help='Sort threads by relevance or recency (default: by_date)')
    run_parser.add_argument('--verbose', '-v', action='store_true',
                           help='Enable verbose logging and show detailed configuration')
    run_parser.add_argument('--debug', action='store_true',
                           help='Enable debug logging (shows API requests/responses)')
    run_parser.add_argument('--browser', '--live', action='store_true',
                           help='Use live browser automation for sending DMs (requires camoufox)')
    run_parser.add_argument('--headless', action='store_true',
                           help='Run browser in headless mode (only with --browser)')
    run_parser.add_argument('--browser-delay', type=float, default=None,
                           help='Override delay between browser actions (seconds)')

    args = parser.parse_args()

    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute the appropriate command
    args.func(args)


if __name__ == "__main__":
    main()
