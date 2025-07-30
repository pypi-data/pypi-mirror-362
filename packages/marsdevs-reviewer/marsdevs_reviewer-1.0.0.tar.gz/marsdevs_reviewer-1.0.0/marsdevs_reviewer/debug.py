"""
Debug utilities for MarsDevs Code Reviewer
"""

import os
import sys
import logging
import functools
import time
from typing import Any, Callable


# Configure logging based on environment
def setup_logging():
    """Setup logging configuration based on environment variables."""
    log_level = os.environ.get('MARSDEVS_LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if os.environ.get('MARSDEVS_DEBUG'):
        log_level = 'DEBUG'
        log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        stream=sys.stderr
    )
    
    return logging.getLogger('marsdevs_reviewer')


# Create logger instance
logger = setup_logging()


def debug_mode() -> bool:
    """Check if debug mode is enabled."""
    return bool(os.environ.get('MARSDEVS_DEBUG'))


def profile_time(func: Callable) -> Callable:
    """Decorator to profile function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not debug_mode():
            return func(*args, **kwargs)
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.debug(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    
    return wrapper


def log_api_request(url: str, headers: dict, data: dict):
    """Log API request details in debug mode."""
    if not debug_mode():
        return
    
    logger.debug(f"API Request to: {url}")
    logger.debug(f"Headers: {{k: v for k, v in headers.items() if k != 'x-api-key'}}")
    logger.debug(f"Data size: {len(str(data))} chars")
    
    if os.environ.get('MARSDEVS_DEBUG_VERBOSE'):
        logger.debug(f"Full data: {data}")


def log_api_response(response):
    """Log API response details in debug mode."""
    if not debug_mode():
        return
    
    logger.debug(f"API Response status: {response.status_code}")
    logger.debug(f"Response size: {len(response.text)} chars")
    
    if os.environ.get('MARSDEVS_DEBUG_VERBOSE'):
        logger.debug(f"Response content: {response.text[:1000]}...")


def debug_git_state():
    """Log current git state for debugging."""
    if not debug_mode():
        return
    
    import subprocess
    
    try:
        # Get git status
        status = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True
        )
        logger.debug(f"Git status:\n{status.stdout}")
        
        # Get staged files
        staged = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True
        )
        logger.debug(f"Staged files:\n{staged.stdout}")
        
    except Exception as e:
        logger.debug(f"Failed to get git state: {e}")


def debug_conventions(conventions_context: str, similar_files: dict):
    """Log convention analysis details."""
    if not debug_mode():
        return
    
    logger.debug(f"Found {len(similar_files)} files with similar extensions")
    for staged, similar in similar_files.items():
        logger.debug(f"  {staged} -> {len(similar)} similar files")
    
    logger.debug(f"Conventions context size: {len(conventions_context)} chars")
    
    if os.environ.get('MARSDEVS_DEBUG_VERBOSE'):
        logger.debug("Full conventions context:")
        logger.debug(conventions_context[:2000] + "..." if len(conventions_context) > 2000 else conventions_context)


def create_debug_report(error: Exception = None) -> str:
    """Create a debug report for troubleshooting."""
    import platform
    import subprocess
    
    report = []
    report.append("=== MarsDevs Debug Report ===")
    report.append(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Python: {sys.version}")
    report.append(f"Platform: {platform.platform()}")
    report.append(f"Working directory: {os.getcwd()}")
    
    # Environment variables
    report.append("\nEnvironment:")
    report.append(f"  ANTHROPIC_API_KEY: {'Set' if os.environ.get('ANTHROPIC_API_KEY') else 'Not set'}")
    report.append(f"  MARSDEVS_DEBUG: {os.environ.get('MARSDEVS_DEBUG', 'Not set')}")
    report.append(f"  MARSDEVS_LOG_LEVEL: {os.environ.get('MARSDEVS_LOG_LEVEL', 'Not set')}")
    
    # Git info
    try:
        git_version = subprocess.run(['git', '--version'], capture_output=True, text=True)
        report.append(f"\nGit version: {git_version.stdout.strip()}")
        
        git_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
        report.append(f"Git root: {git_root.stdout.strip()}")
    except:
        report.append("\nGit: Not available or not in a repository")
    
    # Package info
    try:
        import marsdevs_reviewer
        report.append(f"\nPackage version: {marsdevs_reviewer.__version__}")
        report.append(f"Package location: {os.path.dirname(marsdevs_reviewer.__file__)}")
    except:
        report.append("\nPackage: Failed to import")
    
    # Error info
    if error:
        report.append(f"\nError: {type(error).__name__}: {str(error)}")
        import traceback
        report.append("Traceback:")
        report.append(traceback.format_exc())
    
    return "\n".join(report)


# Export utilities
__all__ = [
    'logger',
    'debug_mode',
    'profile_time',
    'log_api_request',
    'log_api_response',
    'debug_git_state',
    'debug_conventions',
    'create_debug_report'
]