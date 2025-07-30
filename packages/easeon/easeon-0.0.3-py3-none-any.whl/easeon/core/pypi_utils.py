import logging
import sys
from typing import Optional
from packaging.version import parse
from easeon.core.pypi_search import PyPISearcher

logger = logging.getLogger(__name__)

class PyPIUtils:
    def __init__(self, test_mode: bool = False):
        """
        Initialize PyPI utilities
        
        Args:
            test_mode: If True, use TestPyPI instead of PyPI
        """
        self.logger = logging.getLogger(__name__)
        self.test_mode = test_mode
        self.pypi_search = PyPISearcher(use_testpypi=test_mode)

    def get_latest_version(self, package_name: str) -> Optional[str]:
        """Get the latest version of a package from PyPI or TestPyPI."""
        try:
            result = self.pypi_search.get_package_versions(package_name)
            if 'error' in result:
                logger.error(f"Failed to get package versions: {result['error']}")
                return None
            return result.get('latest')
        except Exception as e:
            logger.error(f"Failed to get latest version: {e}")
            return None

    def check_version_exists(self, package_name: str, version: str) -> bool:
        """Check if a specific version of a package exists on PyPI."""
        try:
            result = self.pypi_search.get_package_versions(package_name)
            if 'error' in result:
                logger.error(f"Failed to check version existence: {result['error']}")
                return False
            
            versions = result.get('versions', [])
            return version in versions
        except Exception as e:
            logger.error(f"Failed to check version existence: {e}")
            return False

    def _compare_versions(self, current_version: str, latest_version: str) -> bool:
        """Compare two version strings."""
        try:
            return parse(latest_version) > parse(current_version)
        except TypeError:
            logger.warning(f"Failed to compare versions {current_version} and {latest_version}")
            return False

    def is_in_virtualenv(self) -> bool:
        """Check if running in a virtual environment."""
        return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.prefix != sys.base_prefix)
