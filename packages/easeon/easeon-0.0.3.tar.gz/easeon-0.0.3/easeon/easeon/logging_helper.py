"""
Logging configuration for the Easeon package.

This module provides a centralized logging configuration system that can be used
throughout the Easeon package. It supports logging to files, console, or both,
with configurable log levels and formatting.

Example:
    ```python
    from easeon.logging_helper import setup_logging
    
    # Basic setup with default log file
    setup_logging()
    
    # Custom log file and console output
    setup_logging(
        log_file="custom.log",
        console=True,
        log_level=logging.DEBUG
    )
    ```
"""
import os
import sys
import logging
from typing import Optional, Union
from pathlib import Path

from .paths import get_log_file_path


def setup_logging(
    log_file: Optional[Union[str, Path]] = None,
    console: bool = False,
    log_level: int = logging.INFO
) -> None:
    """
    Configure logging for the Easeon package.
    
    This function sets up logging with the specified configuration, including:
    - File logging (if log_file is provided)
    - Console logging (if console=True)
    - Log level filtering
    - Consistent log formatting
    
    Args:
        log_file: Path to the log file. If None, file logging is disabled.
        console: If True, enables logging to console.
        log_level: Minimum log level to capture (default: logging.INFO)
        
    Example:
        ```python
        # Basic setup with default log file
        setup_logging()
        
        # Log to a custom file and console
        setup_logging("app.log", console=True)
        
        # Debug-level logging
        setup_logging(console=True, log_level=logging.DEBUG)
        ```
        console: Whether to log to console (default: True)
    """
    try:
        # Get the default log file if none provided
        if log_file is None:
            log_file = str(get_log_file_path())
        
        # Clear any existing handlers to avoid duplicate logs
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Set log level
        root_logger.setLevel(log_level)
        
        # Create formatter with detailed information
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler for user feedback
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Configure file handler
        try:
            # Ensure directory exists
            log_path = Path(log_file).resolve()
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(
                str(log_path),
                mode='a',
                encoding='utf-8',
                delay=False
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            # Log the log file location
            root_logger.info(f"Logging to file: {log_path}")
            
            # Write a header if the file is new or empty
            if log_path.stat().st_size == 0:
                with log_path.open('a', encoding='utf-8') as f:
                    f.write('\n' + '=' * 80 + '\n')
                    f.write(f'Easeon Log - Started at: {logging.Formatter().formatTime(logging.LogRecord("root", logging.INFO, "", 0, "", (), None))}\n')
                    f.write('=' * 80 + '\n\n')
                    
        except Exception as e:
            print(f"❌ Failed to configure file logging: {e}", file=sys.stderr)
            if not console:
                # If console logging is disabled, we need at least one handler
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(log_level)
                console_handler.setFormatter(formatter)
                root_logger.addHandler(console_handler)
        
        # Log the start of the application
        root_logger.info("=" * 50)
        root_logger.info("Easeon application started")
        root_logger.info(f"Python version: {sys.version.split()[0]}")
        root_logger.info(f"Current working directory: {os.getcwd()}")
        root_logger.info(f"Log file: {log_path}" if 'log_path' in locals() else "Log file: Console only")
        root_logger.info("=" * 50)
        
    except Exception as e:
        print(f"❌ Critical error in logging setup: {e}", file=sys.stderr)
        # Fallback to basic config if all else fails
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        logging.error("Failed to configure advanced logging. Using basic configuration.")


# Set up logging when this module is imported
# This will be overridden if setup_logging() is called with different parameters
setup_logging(console=False)
