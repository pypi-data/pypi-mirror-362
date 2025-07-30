"""
Paths configuration for the Easeon package.

This module handles all path-related operations for the Easeon package,
including log file locations, configuration directories, and other file system paths.

Example:
    ```python
    from easeon.paths import get_logs_dir, get_log_file_path
    
    # Get the logs directory
    logs_dir = get_logs_dir()
    
    # Get the default log file path
    log_file = get_log_file_path()
    ```
"""
import os
import sys
from pathlib import Path
from typing import Optional

def get_logs_dir() -> Path:
    """
    Get the directory where log files should be stored.
    
    The location is platform-specific:
    - Windows: %APPDATA%\\Easeon\\logs
    - Unix/Linux/Mac: ~/.config/easeon/logs
    
    The directory will be created if it doesn't exist.
    
    Returns:
        Path: The path to the logs directory
        
    Example:
        ```python
        logs_dir = get_logs_dir()
        print(f"Logs are stored in: {logs_dir}")
        ```
    """
    if sys.platform == "win32":
        # Windows: %APPDATA%\Easeon\logs
        appdata = os.getenv('APPDATA', os.path.expanduser('~'))
        log_dir = Path(appdata) / 'Easeon' / 'logs'
    else:
        # Unix/Linux/Mac: ~/.config/easeon/logs
        log_dir = Path.home() / '.config' / 'easeon' / 'logs'
    
    # Create the directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def get_log_file_path() -> Path:
    """Get the path to the main log file."""
    return get_logs_dir() / 'easeon.log'
