"""Package list management for Easeon."""

import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Union, Set

from .logger import setup_logger
from .package_operations import (
    is_valid_package_name,
    is_valid_version,
    parse_package_string,
    merge_package_lists,
    filter_packages,
    validate_package_name,
    normalize_package_name
)
from .package_io import PackageIO
from .package_installer import PackageInstaller

class PackageInstallationError(Exception):
    """Custom exception for package installation errors."""
    pass

class PackageListManager:
    """Manages a list of Python packages with version specifications.
    
    This class provides thread-safe operations for managing a list of packages,
    including adding, removing, and installing them.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None, 
                 use_test_pypi: bool = False, 
                 use_test_pypi_easeon: bool = False):
        """Initialize the PackageListManager.
        
        Args:
            logger: Optional logger instance. If not provided, a default one will be created.
            use_test_pypi: If True, uses TestPyPI as the package index.
            use_test_pypi_easeon: If True, uses TestPyPI specifically for the easeon package.
        """
        self._packages: Dict[str, Optional[str]] = {}
        self._package_count: int = 0
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self.logger = logger or setup_logger('package_list_manager')
        self._io = PackageIO(logger)
        self._installer = PackageInstaller(
            logger=logger,
            use_test_pypi=use_test_pypi,
            use_test_pypi_easeon=use_test_pypi_easeon
        )
        self.python_executable: Optional[str] = None

    # Core package management methods
    
    def add_package(self, package_name: str, version: Optional[str] = None, 
                   force: bool = False) -> bool:
        """Add or update a single package."""
        if not validate_package_name(package_name):
            self.logger.warning(f"Invalid package name: {package_name}")
            return False
            
        if version and not is_valid_version(version):
            self.logger.warning(f"Invalid version format: {version}")
            return False
            
        with self._lock:
            if package_name in self._packages and not force:
                self.logger.warning(f"Package {package_name} already exists")
                return False
                
            self._packages[package_name] = version
            self._package_count = len(self._packages)
            self.logger.info(f"Added package: {package_name}{f'=={version}' if version else ''}")
            return True

    def _extract_package_name(self, package_str: str) -> str:
        """Extract package name from a package string."""
        name, _ = parse_package_string(package_str)
        return name

    def add_packages(self, packages: List[str], force: bool = False) -> None:
        """Add or update multiple packages."""
        if not packages:
            return
            
        with self._lock:
            new_packages = self._packages.copy()
            
            for pkg in packages:
                try:
                    if not pkg or not isinstance(pkg, str):
                        continue
                        
                    pkg = pkg.strip()
                    if not pkg or pkg.startswith('#'):
                        continue
                        
                    name, version = parse_package_string(pkg)
                    if not validate_package_name(name):
                        self.logger.warning(f"Invalid package name: {name}")
                        continue
                        
                    if version and not is_valid_version(version):
                        self.logger.warning(f"Invalid version for {name}: {version}")
                        continue
                        
                    if name in new_packages and not force:
                        self.logger.warning(f"Skipping existing package: {name}")
                        continue
                        
                    new_packages[name] = version
                    
                except Exception as e:
                    self.logger.error(f"Error processing package '{pkg}': {e}", exc_info=True)
            
            self._packages = new_packages
            self._package_count = len(new_packages)
            self.logger.info(f"Processed {len(packages)} packages, {self._package_count} total")

    def remove_packages(self, packages: List[str]) -> int:
        """Remove packages from the list."""
        if not packages:
            return 0
            
        removed = 0
        with self._lock:
            for pkg in packages:
                name = pkg.split('==')[0].strip()
                if name in self._packages:
                    del self._packages[name]
                    removed += 1
                    
            self._package_count = len(self._packages)
            
        if removed:
            self.logger.info(f"Removed {removed} packages")
            
        return removed

    def clear(self) -> None:
        """Remove all packages from the list."""
        with self._lock:
            count = self._package_count
            self._packages.clear()
            self._package_count = 0
            
        if count:
            self.logger.info(f"Cleared {count} packages")
            
    # File I/O operations
    
    def load_from_file(self, file_path: Union[str, Path]) -> bool:
        """Load packages from a requirements file."""
        packages = self._io.load_from_file(file_path)
        if not packages:
            return False
            
        with self._lock:
            self._packages = packages
            self._package_count = len(packages)
            
        self.logger.info(f"Loaded {self._package_count} packages from {file_path}")
        return True
    
    def save_to_file(self, file_path: Union[str, Path], include_versions: bool = True) -> bool:
        """Save packages to a requirements file."""
        with self._lock:
            packages = self._packages.copy()
            
        success = self._io.save_to_file(packages, file_path, include_versions)
        if success:
            self.logger.info(f"Saved {self._package_count} packages to {file_path}")
            
        return success

    # Installation
    
    def install(self, 
               python_executable: Optional[Union[str, Path]] = None, 
               upgrade: bool = False,
               batch_size: int = 10,
               retry_attempts: int = 2,
               allow_prereleases: bool = False) -> Dict[str, bool]:
        """Install all packages in the list.
        
        Args:
            python_executable: Path to the Python executable to use for installation.
            upgrade: If True, upgrade packages to their latest versions.
            batch_size: Number of packages to install in each batch. If None, install all at once.
                     This can help avoid timeouts with large numbers of packages.
            retry_attempts: Number of retry attempts for failed installations.
            allow_prereleases: If True, allow installation of pre-release versions.
            
        Returns:
            Dict[str, bool]: A dictionary mapping package names to installation success status.
            
        Raises:
            RuntimeError: If there are no packages to install.
            ValueError: If batch_size is less than 1.
        """
        if batch_size is not None and batch_size < 1:
            raise ValueError("batch_size must be at least 1 or None")
            
        with self._lock:
            if not self._packages:
                self.logger.warning("No packages to install")
                return {}
                
            packages_to_install = self._packages.copy()
            
        # Set the Python executable for the installer
        self.python_executable = str(python_executable) if python_executable else None
        
        # Log installation context
        self.logger.info(
            f"Starting installation of {len(packages_to_install)} packages "
            f"with{'out' if not upgrade else ''} upgrade"
        )
        
        # Install packages in batches if batch_size is specified
        results = {}
        package_list = list(packages_to_install.items())
        total_packages = len(package_list)
        
        for i in range(0, total_packages, batch_size if batch_size else total_packages):
            batch = dict(package_list[i:i + batch_size] if batch_size else package_list)
            batch_num = (i // (batch_size or total_packages)) + 1
            total_batches = (total_packages + (batch_size - 1)) // (batch_size or total_packages)
            
            self.logger.info(
                f"Installing batch {batch_num}/{total_batches} "
                f"({len(batch)} packages)"
            )
            
            # Try installation with retries
            for attempt in range(retry_attempts + 1):
                try:
                    # Install the batch
                    success = self._installer.install(
                        packages=batch,
                        python_executable=python_executable,
                        upgrade=upgrade,
                        allow_prereleases=allow_prereleases
                    )
                    
                    # Record results
                    for pkg in batch:
                        results[pkg] = success
                    
                    if success:
                        self.logger.info(
                            f"Successfully installed batch {batch_num}/{total_batches}"
                        )
                        break  # Move to next batch on success
                    
                    if attempt < retry_attempts:
                        self.logger.warning(
                            f"Batch {batch_num} installation failed, "
                            f"retrying ({attempt + 1}/{retry_attempts})"
                        )
                    else:
                        self.logger.error(
                            f"Failed to install batch {batch_num} after "
                            f"{retry_attempts + 1} attempts"
                        )
                        
                except Exception as e:
                    self.logger.error(
                        f"Error installing batch {batch_num}: {str(e)}",
                        exc_info=True
                    )
                    
                    if attempt >= retry_attempts:
                        self.logger.error(
                            f"Giving up on batch {batch_num} after "
                            f"{retry_attempts + 1} attempts"
                        )
                        # Mark all packages in the failed batch as failed
                        for pkg in batch:
                            results[pkg] = False
        
        # Log installation summary
        success_count = sum(1 for success in results.values() if success)
        failed_count = len(results) - success_count
        
        self.logger.info(
            f"Installation complete. Success: {success_count}, "
            f"Failed: {failed_count}"
        )
        
        if failed_count > 0:
            failed_pkgs = [pkg for pkg, success in results.items() if not success]
            self.logger.warning(f"Failed to install packages: {', '.join(failed_pkgs)}")
        
        return results

    # Getters and info methods
    
    def get_package_list(self, include_versions: bool = True) -> List[str]:
        """Get the list of packages."""
        with self._lock:
            if include_versions:
                return [f"{k}=={v}" if v else k for k, v in self._packages.items()]
            return list(self._packages.keys())
    
    def get_package_count(self) -> int:
        """Get the number of packages in the list."""
        with self._lock:
            return self._package_count
    
    def has_package(self, package_name: str) -> bool:
        """Check if a package is in the list."""
        with self._lock:
            return package_name in self._packages
    
    def get_package_version(self, package_name: str) -> Optional[str]:
        """Get the version of a package if specified."""
        with self._lock:
            return self._packages.get(package_name)
    
    # Filtering
    
    def filter(self, include: Optional[List[str]] = None, 
              exclude: Optional[List[str]] = None) -> 'PackageListManager':
        """Return a new PackageListManager with filtered packages.
        
        Args:
            include: List of package names to include. If None, all packages are included.
            exclude: List of package names to exclude. These packages will be removed
                   from the result even if they are in the include list.
                   
        Returns:
            PackageListManager: A new instance containing only the filtered packages.
            
        Note:
            This method is thread-safe and creates a new PackageListManager instance
            with the same configuration as the current one.
        """
        # Create a new manager with the same configuration
        new_manager = PackageListManager(
            logger=self.logger,
            use_test_pypi=getattr(self._installer, 'use_test_pypi', False),
            use_test_pypi_easeon=getattr(self._installer, 'use_test_pypi_easeon', False),
            pypi_url=getattr(self._installer, 'pypi_url', 'https://pypi.org/simple'),
            test_pypi_url=getattr(self._installer, 'test_pypi_url', 'https://test.pypi.org/simple')
        )
        
        # Copy the Python executable path
        new_manager.python_executable = self.python_executable
        
        # Get the filtered packages in a thread-safe way
        with self._lock:
            filtered_packages = filter_packages(self._packages, include, exclude)
            
        # Update the new manager's packages
        with new_manager._lock:
            new_manager._packages = filtered_packages
            new_manager._package_count = len(filtered_packages)
            
        return new_manager
