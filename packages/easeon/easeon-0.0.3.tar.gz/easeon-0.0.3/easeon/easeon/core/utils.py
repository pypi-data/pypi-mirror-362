from importlib.metadata import PackageNotFoundError
import os
import sys
import platform
import logging
import subprocess
import re
from typing import Optional, Tuple, Dict
from easeon.core.package_validator import PackageValidator

class Utils:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def set_utf8_terminal_encoding() -> None:
        """Set terminal encoding to UTF-8 for proper character display."""
        system = platform.system()
        if system == "Windows":
            subprocess.run("chcp 65001", shell=True)
        elif system in ["Linux", "Darwin"]:
            os.environ["LC_ALL"] = "en_US.UTF-8"
            os.environ["LANG"] = "en_US.UTF-8"
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
                sys.stderr.reconfigure(encoding="utf-8")

    @staticmethod
    def get_platform_info() -> Dict:
        """Get platform information.
        
        Returns:
            Dict containing platform information with keys:
            - system: Operating system name (e.g., 'Windows', 'Linux', 'Darwin')
            - os_name: Alias for system (for backward compatibility)
            - platform: Platform identifier including system, release and version
            - python_version: Python version string
            - node: Network name of the computer
            - release: OS release version
            - version: OS version
            - machine: Machine type (e.g., 'x86_64', 'AMD64')
            - processor: Processor name
        """
        import platform
        import socket
        system = platform.system()
        return {
            "system": system,
            "os_name": system,  # For backward compatibility
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "node": socket.gethostname(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    @staticmethod
    def is_valid_package_name(package_name: str) -> Tuple[bool, str]:
        """
        Validate package name and version format.
        
        Args:
            package_name: The package name to validate
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        # Check for empty package name
        if not package_name or package_name.strip() == "":
            return False, "Package name must not be empty."
        # Check for valid characters
        if any(c in package_name for c in ' @!'):
            invalid_chars = ''.join(set(c for c in package_name if c in ' @!'))
            return False, f"Invalid character(s) in package name: {package_name}. Invalid characters: {invalid_chars}"
        
        # If it's a version specification, validate version format
        if any(op in package_name for op in ['==', '>=', '<=', '>', '<', '~=']):
            try:
                # Extract version using regex
                match = re.match(r'^(.+?)(==|>=|<=|>|<|~=)(.+)$', package_name)
                if match:
                    name, op, version = match.groups()
                    name = name.strip()
                    version = version.strip()
                    from easeon.core.pypi_search import PyPISearcher
                    # Check for version existence on PyPI for '=='
                    if op == '==':
                        searcher = PyPISearcher()
                        info = searcher.get_package_versions(name)
                        if info.get('versions') and version in info['versions']:
                            return True, ""
                        else:
                            return False, f"Invalid version format: {version}."
                    else:
                        if version.endswith('.'):
                            return False, f"Invalid version format: {version}."
                    return True, ""
                
                return False, "Invalid requirement format"
            except Exception as e:
                return False, f"Invalid requirement format: {str(e)}"
        
        return True, ""

    @staticmethod
    def is_package_installed(package_name: str) -> bool:
        """
        Check if a package is installed in the current environment.
        
        Args:
            package_name: Name of the package to check
            
        Returns:
            True if package is installed, False otherwise
        """
        try:
            import pkg_resources
            return package_name in [pkg.key for pkg in pkg_resources.working_set]
        except ImportError:
            return False

    @staticmethod
    def is_package_installed_with_version(pkg_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validate package name and version, then check if it's installed.
        
        Args:
            pkg_str: Package name with optional version specifier
            
        Returns:
            Tuple[bool, Optional[str]]: (is_installed, version_if_installed)
        """
        validation = PackageValidator.validate_requirement(pkg_str)
        if not validation['valid']:
            return False, None
        
        package_name = validation['package_name']
        version_spec = validation['version_specifier']
        if '==' in pkg_str:
            name, required_ver = pkg_str.split('==')
        else:
            name, required_ver = pkg_str, None
        
        try:
            from importlib.metadata import version
            current_ver = version(name)
            if required_ver and current_ver != required_ver:
                return True, current_ver
            return True, None
        except (PackageNotFoundError, ModuleNotFoundError):
            return False, None
            
    @staticmethod
    def parse_version(version_str: str) -> Tuple[int, int, int]:
        """
        Parse a version string into a tuple of 3 integers.
        
        Args:
            version_str: Version string to parse (e.g., '1.2.3')
            
        Returns:
            Tuple of exactly 3 integers representing the version components (major, minor, patch)
            
        Raises:
            ValueError: If the version string is invalid
        """
        try:
            parts = list(map(int, version_str.split('.')))
            # Pad with zeros if needed to ensure exactly 3 parts
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts[:3])
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid version string: {version_str}")
            
    @staticmethod
    def is_windows() -> bool:
        """Check if the current platform is Windows."""
        return os.name == 'nt'
        
    @staticmethod
    def is_macos() -> bool:
        """Check if the current platform is macOS."""
        return platform.system() == 'Darwin'
        
    @staticmethod
    def is_linux() -> bool:
        """Check if the current platform is Linux."""
        return platform.system() == 'Linux'
        
    @staticmethod
    def get_home_dir() -> str:
        """
        Get the user's home directory.
        
        Returns:
            Path to the user's home directory
        """
        # Check both possible environment variables
        home = os.environ.get('HOME')
        if home:
            return home
            
        # On Windows, check USERPROFILE
        if os.name == 'nt':
            return os.environ.get('USERPROFILE', '')
            
        # Fallback to expanding ~
        return os.path.expanduser('~')
