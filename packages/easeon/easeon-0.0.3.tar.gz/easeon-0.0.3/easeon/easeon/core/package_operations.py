"""Package operations and validation utilities."""

import re
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Union, Set
from packaging.version import Version, InvalidVersion

logger = logging.getLogger(__name__)


def is_valid_package_name(package_name: str) -> bool:
    """Check if a package name is valid.
    
    Args:
        package_name: The package name to validate
        
    Returns:
        bool: True if the package name is valid, False otherwise
    """
    if not package_name or not isinstance(package_name, str):
        return False
        
    # Check package name format (simplified for demonstration)
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', package_name))


def is_valid_version(version: str) -> bool:
    """Check if a version string is valid.
    
    Args:
        version: The version string to validate
        
    Returns:
        bool: True if the version is valid, False otherwise
    """
    if not version or not isinstance(version, str):
        return False
        
    try:
        Version(version)
        return True
    except InvalidVersion:
        return False


def parse_package_string(pkg_str: str) -> Tuple[str, Optional[str]]:
    """Parse a package string into name and version.
    
    Args:
        pkg_str: Package string (e.g., 'numpy==1.23.0' or 'pandas')
        
    Returns:
        Tuple of (package_name, version)
    """
    if not pkg_str or not isinstance(pkg_str, str):
        return "", None
        
    pkg_str = pkg_str.strip()
    if '==' in pkg_str:
        parts = pkg_str.split('==', 1)
        return parts[0].strip(), parts[1].strip() if len(parts) > 1 else None
    return pkg_str.strip(), None


def merge_package_lists(
    existing: Dict[str, Optional[str]], 
    new: Dict[str, Optional[str]], 
    force: bool = False
) -> Dict[str, Optional[str]]:
    """Merge two package dictionaries with version conflict resolution.
    
    Args:
        existing: Existing packages {name: version}
        new: New packages to add/update {name: version}
        force: If True, overwrite existing versions
        
    Returns:
        Merged package dictionary
    """
    result = existing.copy()
    
    for name, version in new.items():
        if name not in result:
            # New package
            result[name] = version
        elif force and version is not None:
            # Force update version
            result[name] = version
        elif version is not None and result.get(name) is None:
            # Add version to existing package
            result[name] = version
            
    return result


def filter_packages(
    packages: Dict[str, Optional[str]],
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None
) -> Dict[str, Optional[str]]:
    """Filter packages based on include/exclude patterns.
    
    Args:
        packages: Dictionary of package names to versions
        include: List of package patterns to include (if None, include all)
        exclude: List of package patterns to exclude
        
    Returns:
        Filtered package dictionary
    """
    if not include and not exclude:
        return packages.copy()
        
    result = {}
    for name, version in packages.items():
        # Check if included
        if include and not any(re.match(pattern, name) for pattern in include):
            continue
            
        # Check if excluded
        if exclude and any(re.match(pattern, name) for pattern in exclude):
            continue
            
        result[name] = version
        
    return result


def validate_package_name(name: str) -> bool:
    """Validate a package name.
    
    Args:
        name: Package name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', name))


def normalize_package_name(name: str) -> str:
    """Normalize a package name.
    
    Args:
        name: Package name to normalize
        
    Returns:
        Normalized package name
    """
    if not name:
        return ''
    return name.lower().replace('_', '-')
