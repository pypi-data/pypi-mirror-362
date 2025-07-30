"""
Easeon - A Python package manager with virtual environment support.

Simplified Client API Example:
    ```python
    from easeon import EaseonInstaller

    # Create an installer with default settings
    installer = EaseonInstaller(
        auto_create_venv=True,
        env_name="myenv",
        use_test_pypi=False,
        use_test_pypi_easeon=False,
        log_destination="console"  # or path to log file
    )

    # Install packages
    installer.get_list(['numpy', 'pandas']).install()

    # Or from a requirements.txt file
    installer.get_txt('requirements.txt').install()
    
    # Or from a CSV file
    installer.get_csv('packages.csv').install()
    ```
"""
import logging
import sys
from typing import List, Optional, Union
from pathlib import Path

# Import core functionality
from easeon.core.easeon_installer import EaseonInstaller as _EaseonInstaller
from easeon.core.python_lib_installer import PythonLibInstaller
from easeon.core.easeon_utils import (
    install_packages_from_txt,
    install_packages_from_list,
    search_pypi
)

# Import logging helper
from easeon.logging_helper import setup_logging as _setup_logging
from easeon.paths import get_log_file_path

# Define public API
__version__ = '1.0.0'

# Create a simplified EaseonInstaller class that extends the core one
class EaseonInstaller(_EaseonInstaller):
    """A simplified interface for the Easeon package manager.
    
    This class provides a more convenient API for common package management tasks.
    All methods return self to enable method chaining.
    """
    
    def install(self) -> None:
        """Install all packages that have been added to the installer.
        
        Returns:
            None
        """
        python_executable = self._get_python_executable()
        self.manager.install(python_executable=python_executable)
        
    def get_list(self, packages: List[str]) -> 'EaseonInstaller':
        """Set the list of packages to be installed.
        
        Args:
            packages: List of package specifications (e.g., ["numpy==1.23.0", "pandas>=1.0.0"])
            
        Returns:
            Self for method chaining
        """
        self.logger.info(f"Setting package list with {len(packages)} packages")
        self.manager.clear()  # Clear any existing packages
        for pkg_spec in packages:
            pkg_spec = pkg_spec.strip()
            if not pkg_spec or pkg_spec.startswith('#'):
                continue
                
            # Add the package specification as is
            self.manager.add_package(pkg_spec)
            
        return self
    
    def get_txt(self, path: str) -> 'EaseonInstaller':
        """Set packages from a text file.
        
        Args:
            path: Path to the text file containing package specifications (one per line)
            
        Returns:
            Self for method chaining
        """
        self.logger.info(f"Loading packages from text file: {path}")
        with open(path, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        return self.get_list(packages)
    
    def get_csv(self, path: str) -> 'EaseonInstaller':
        """Set packages from a CSV file.
        
        Args:
            path: Path to the CSV file containing package specifications (first column)
            
        Returns:
            Self for method chaining
        """
        self.logger.info(f"Loading packages from CSV file: {path}")
        import csv
        packages = []
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip() and not row[0].strip().startswith('#'):
                    packages.append(row[0].strip())
        
        return self.get_list(packages)
        
    def get_logs(self) -> str:
        """Retrieve the contents of the log file.
        
        Returns:
            str: The contents of the log file, or an error message if the log file cannot be read.
        """
        try:
            log_file = self.log_files[0] if hasattr(self, 'log_files') and self.log_files else None
            if not log_file:
                return "No log file path available"
                
            log_path = Path(log_file)
            if not log_path.exists():
                return f"Log file not found at: {log_path}"
                
            with open(log_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error reading log file: {e}", exc_info=True)
            return f"Error reading log file: {str(e)}"

# Update __all__ to include the simplified API
__all__ = [
    "EaseonInstaller",
    "PythonLibInstaller",
    "install_packages_from_txt",
    "install_packages_from_list",
    "search_pypi",
    "setup_logging",
    "__version__"
]

def setup_logging(
    log_destination: Optional[Union[str, Path]] = None, 
    console: bool = True, 
    log_level: int = logging.INFO
) -> None:
    """
    Set up logging for the Easeon package.
    
    Args:
        log_destination: Path to the log file, 'console' for console only, 
                        or None for default location.
        console: Whether to log to console.
        log_level: Logging level (default: logging.INFO)
    """
    _setup_logging(
        log_file=str(log_destination) if log_destination and str(log_destination).lower() != 'console' else None,
        console=console,
        log_level=log_level
    )
    
    # Log the initialization
    logger = logging.getLogger(__name__)
    logger.info(f"Easeon v{__version__} initialized")
    if log_destination and str(log_destination).lower() != 'console':
        logger.info(f"Log file: {Path(log_destination).resolve()}")
    elif log_destination is None:
        logger.info(f"Log file: {get_log_file_path()}")

# Initialize logging only if not already configured
if not logging.getLogger().hasHandlers():
    setup_logging(console=False)
