"""Package installation functionality for Easeon."""

import logging
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Dict, Any

from packaging.version import Version, InvalidVersion

class PackageInstaller:
    """Handles package installation operations."""
    
    def __init__(self, 
                 logger: Optional[logging.Logger] = None, 
                 use_test_pypi: bool = False, 
                 use_test_pypi_easeon: bool = False,
                 pypi_url: str = "https://pypi.org/simple",
                 test_pypi_url: str = "https://test.pypi.org/simple"):
        """Initialize the package installer.
        
        Args:
            logger: Optional logger instance. If not provided, a default one will be created.
            use_test_pypi: If True, uses TestPyPI as the package index.
            use_test_pypi_easeon: If True, uses TestPyPI specifically for the easeon package.
            pypi_url: Base URL for the main PyPI repository.
            test_pypi_url: Base URL for the TestPyPI repository.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.use_test_pypi = use_test_pypi
        self.use_test_pypi_easeon = use_test_pypi_easeon
        self.pypi_url = pypi_url.rstrip('/')
        self.test_pypi_url = test_pypi_url.rstrip('/')
    
    def install(
        self,
        packages: Dict[str, Optional[str]],
        python_executable: Optional[Union[str, Path]] = None,
        upgrade: bool = False,
        allow_prereleases: bool = False
    ) -> bool:
        """
        Install packages using pip with optional TestPyPI configuration.
        
        Args:
            packages: Dictionary of package names to versions. If version is None,
                    the latest version will be installed.
            python_executable: Path to Python executable to use for installation.
            upgrade: If True, upgrade the packages to the newest available version.
            allow_prereleases: If True, allow installation of pre-release and development
                            versions. Be cautious with this in production environments.
            
        Returns:
            bool: True if installation was successful, False otherwise.
            
        Raises:
            ValueError: If any package name or version is invalid.
            subprocess.SubprocessError: If the pip install command fails.
        """
        if not packages:
            self.logger.warning("No packages to install")
            return True
            
        # Validate package names and versions
        self._validate_package_names_and_versions(packages)
        
        # Determine pip command
        python_cmd = self._get_python_cmd(python_executable)
        if not python_cmd:
            return False
            
        # Build package list with versions and handle TestPyPI configuration
        package_specs = []
        for name, version in packages.items():
            if version:
                # Validate version format if provided
                if not self._is_valid_version(version):
                    raise ValueError(f"Invalid version format for package {name}: {version}")
                package_spec = f"{name}=={version}"
            else:
                package_spec = name
                
            # Add pre-release flag if allowed
            if allow_prereleases and not version:
                package_spec = f"{package_spec} --pre"
                
            package_specs.append(package_spec)
        
        # Prepare base pip install command with additional safety options
        cmd = [
            str(python_cmd),
            "-m",
            "pip",
            "install",
            "--no-cache-dir",  # Don't use pip cache to avoid issues with corrupted downloads
            "--no-warn-script-location",  # Avoid warning about PATH issues
            *(["--upgrade"] if upgrade else []),
            *(["--pre"] if allow_prereleases else []),
        ]
        
        # Add user warning about pre-releases if enabled
        if allow_prereleases:
            self.logger.warning("Pre-release versions are allowed. This may install unstable packages.")
            
        # Log the installation context
        self.logger.info(
            f"Installing {len(packages)} package(s) "
            f"with{'out' if not upgrade else ''} upgrade "
            f"using Python at: {python_cmd}"
        )
        
        # Add package index configuration
        if self.use_test_pypi:
            cmd.extend(["--index-url", f"{self.test_pypi_url}/"])
            cmd.extend(["--extra-index-url", f"{self.pypi_url}/"])
        
        # Add package specs to the command
        cmd.extend(package_specs)
        
        # Special handling for easeon package with TestPyPI
        if self.use_test_pypi_easeon and any(pkg.startswith('easeon') for pkg in package_specs):
            self.logger.info("Using TestPyPI for easeon package installation")
            # For easeon package, we need to specify the exact index
            easeon_cmd = cmd.copy()
            easeon_pkgs = [pkg for pkg in package_specs if pkg.startswith('easeon')]
            easeon_cmd[-len(package_specs):] = easeon_pkgs
            
            # Use TestPyPI for easeon packages
            easeon_cmd.extend(["--index-url", f"{self.test_pypi_url}/"])
            easeon_cmd.extend(["--extra-index-url", f"{self.pypi_url}/"])
            
            # Run the command for easeon package
            if not self._run_install_command(easeon_cmd, "easeon"):
                return False
            
            # Remove easeon packages from the main command
            cmd[-len(package_specs):] = [pkg for pkg in package_specs if not pkg.startswith('easeon')]
            if not cmd[-len([pkg for pkg in package_specs if not pkg.startswith('easeon')]):]:
                # If only easeon packages were requested, we're done
                return True
        
        # Run the command for all other packages
        return self._run_install_command(cmd, "packages")
        
    def _run_install_command(self, cmd: List[str], package_type: str) -> bool:
        """Helper method to run the pip install command with proper error handling.
        
        Args:
            cmd: The command to run as a list of strings
            package_type: Type of packages being installed (for logging purposes)
            
        Returns:
            bool: True if the command was successful, False otherwise
            
        Raises:
            subprocess.SubprocessError: If there's an error executing the command
            PermissionError: If there are permission issues
            FileNotFoundError: If the command or Python interpreter is not found
        """
        import shutil
        import sys
        
        # Check if the command exists
        executable = cmd[0] if cmd else None
        if executable and not shutil.which(executable):
            error_msg = f"Command not found: {executable}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        self.logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            # Run the command with a timeout to prevent hanging
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
                encoding='utf-8',
                errors='replace'  # Handle encoding errors gracefully
            )
            
            # Log the output
            if result.stdout:
                self.logger.debug(f"Command output:\n{result.stdout}")
                
            if result.stderr:
                # Check for common warnings in stderr
                stderr_lower = result.stderr.lower()
                if 'warning' in stderr_lower or 'deprecation' in stderr_lower:
                    self.logger.warning(f"Command warnings:\n{result.stderr}")
                else:
                    self.logger.info(f"Command info:\n{result.stderr}")
                    
            return True
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out after 5 minutes: {' '.join(cmd)}"
            self.logger.error(error_msg)
            return False
            
        except subprocess.CalledProcessError as e:
            # Handle specific error cases
            if 'permission denied' in str(e).lower():
                error_msg = f"Permission denied when running command: {e}"
                self.logger.error(error_msg)
                raise PermissionError(error_msg) from e
                
            elif 'no such file or directory' in str(e).lower():
                error_msg = f"File or directory not found: {e}"
                self.logger.error(error_msg)
                raise FileNotFoundError(error_msg) from e
                
            # For other errors, log the details
            error_msg = f"Command failed with return code {e.returncode}: {e}"
            self.logger.error(error_msg)
            
            if e.stdout:
                self.logger.debug(f"Command stdout:\n{e.stdout}")
                
            if e.stderr:
                self.logger.error(f"Command stderr:\n{e.stderr}")
                
                # Check for common error patterns
                if 'could not find a version' in e.stderr.lower():
                    self.logger.error("Package version not found. Please check the package name and version.")
                elif 'no matching distribution found' in e.stderr.lower():
                    self.logger.error("No matching distribution found. The package may not exist or may not be available for your platform/Python version.")
                    
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error executing command: {e}"
            self.logger.error(error_msg, exc_info=True)
            raise
    
    def _validate_package_names_and_versions(self, packages: Dict[str, Optional[str]]) -> None:
        """Validate package names and versions.
        
        Args:
            packages: Dictionary of package names to versions
            
        Raises:
            ValueError: If any package name is invalid or empty
        """
        if not packages:
            return
            
        for name, version in packages.items():
            if not name or not isinstance(name, str) or not name.strip():
                raise ValueError("Package name cannot be empty")
                
            # Basic validation for package name (PEP 508)
            if not re.match(r'^([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9._-]*[A-Za-z0-9])$', name):
                raise ValueError(f"Invalid package name: {name}")
                
            # Check for common typos in package names
            if '_' in name and '-' not in name:
                self.logger.warning(
                    f"Package name '{name}' contains underscores. "
                    f"Did you mean '{name.replace('_', '-')}'?"
                )
    
    def _is_valid_version(self, version: str) -> bool:
        """Check if a version string is valid according to PEP 440.
        
        Args:
            version: Version string to validate
            
        Returns:
            bool: True if the version string is valid, False otherwise
        """
        if not version:
            return False
            
        # Basic version pattern matching (simplified from PEP 440)
        version_pattern = re.compile(
            r'^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*'  # Release segment
            r'((a|b|rc)(0|[1-9][0-9]*))?'  # Pre-release segment
            r'(\.post(0|[1-9][0-9]*))?'  # Post-release segment
            r'(\.dev(0|[1-9][0-9]*))?$'  # Development release segment
        )
        
        return bool(version_pattern.match(version))
    
    def _get_python_cmd(self, python_executable: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """Get the Python executable path."""
        if python_executable:
            python_executable = Path(python_executable).resolve()
            if not python_executable.exists():
                self.logger.error(f"Python executable not found: {python_executable}")
                return None
            return python_executable
            
        # Default to sys.executable if available
        import sys
        return Path(sys.executable) if sys.executable else None
        
    def install_packages(self, packages: List[str]) -> bool:
        """Install multiple packages.
        
        Args:
            packages: List of package names to install
            
        Returns:
            bool: True if all packages were installed successfully, False otherwise
        """
        if not packages:
            self.logger.warning("No packages to install")
            return True
            
        python_cmd = self._get_python_cmd()
        if not python_cmd:
            return False
            
        cmd = [str(python_cmd), "-m", "pip", "install"]
        
        # Add TestPyPI index if configured
        if self.use_test_pypi:
            cmd.extend(["--index-url", "https://test.pypi.org/simple/"])
            cmd.extend(["--extra-index-url", "https://pypi.org/simple"])
            
        # Add all packages to the command
        cmd.extend(packages)
        
        # Run the command
        return self._run_install_command(cmd, "installation")
        
    def uninstall_packages(
        self, 
        packages: List[str], 
        python_executable: Optional[Union[str, Path]] = None,
        batch_size: int = 10,
        ignore_missing: bool = False
    ) -> Dict[str, bool]:
        """Uninstall multiple packages with detailed error reporting.
        
        Args:
            packages: List of package names to uninstall
            python_executable: Optional path to Python executable to use for uninstallation
            batch_size: Number of packages to uninstall in each batch. If None, uninstall all at once.
                     This can help avoid timeouts with large numbers of packages.
            ignore_missing: If True, don't treat missing packages as errors.
            
        Returns:
            Dict[str, bool]: A dictionary mapping package names to uninstallation success status.
            
        Raises:
            ValueError: If packages list is empty or batch_size is invalid.
        """
        if not packages:
            self.logger.warning("No packages to uninstall")
            return {}
            
        if batch_size is not None and batch_size < 1:
            raise ValueError("batch_size must be at least 1 or None")
            
        python_cmd = self._get_python_cmd(python_executable)
        if not python_cmd:
            return {pkg: False for pkg in packages}
            
        # Remove duplicates while preserving order
        unique_packages = list(dict.fromkeys(packages))
        total_packages = len(unique_packages)
        results = {}
        
        self.logger.info(f"Starting uninstallation of {total_packages} packages")
        
        # Process packages in batches
        for i in range(0, total_packages, batch_size if batch_size else total_packages):
            batch = unique_packages[i:i + (batch_size or total_packages)]
            batch_num = (i // (batch_size or total_packages)) + 1
            total_batches = (total_packages + (batch_size - 1)) // (batch_size or total_packages)
            
            self.logger.info(
                f"Uninstalling batch {batch_num}/{total_batches} "
                f"({len(batch)} packages): {', '.join(batch)}"
            )
            
            # Check which packages are actually installed
            installed_pkgs = []
            for pkg in batch:
                if self.get_installed_version(pkg) is not None:
                    installed_pkgs.append(pkg)
                    results[pkg] = True  # Assume success initially
                else:
                    msg = f"Package not installed: {pkg}"
                    if ignore_missing:
                        self.logger.warning(msg)
                        results[pkg] = True
                    else:
                        self.logger.error(msg)
                        results[pkg] = False
            
            if not installed_pkgs:
                continue
                
            # Build the uninstall command for this batch
            cmd = [
                str(python_cmd),
                "-m",
                "pip",
                "uninstall",
                "-y",  # Auto-confirm uninstallation
                "--no-python-version-warning",
                *installed_pkgs
            ]
            
            # Run the uninstall command
            success = self._run_install_command(cmd, "uninstallation")
            
            # Verify uninstallation and update results
            for pkg in installed_pkgs:
                if self.get_installed_version(pkg) is None:
                    results[pkg] = True
                    self.logger.debug(f"Successfully uninstalled: {pkg}")
                else:
                    results[pkg] = False
                    self.logger.error(f"Failed to uninstall: {pkg}")
        
        # Log summary
        success_count = sum(1 for success in results.values() if success)
        failed_count = len(results) - success_count
        
        self.logger.info(
            f"Uninstallation complete. Success: {success_count}, "
            f"Failed: {failed_count}"
        )
        
        if failed_count > 0:
            failed_pkgs = [pkg for pkg, success in results.items() if not success]
            self.logger.warning(f"Failed to uninstall packages: {', '.join(failed_pkgs)}")
        
        return results
        
    def get_installed_version(self, package: str) -> Optional[str]:
        """Get the installed version of a package.
        
        Args:
            package: Name of the package
            
        Returns:
            Optional[str]: Version string if package is installed, None otherwise
        """
        python_cmd = self._get_python_cmd()
        if not python_cmd:
            return None
            
        cmd = [str(python_cmd), "-m", "pip", "freeze"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return None
            
        # Parse the output to find the package
        for line in result.stdout.splitlines():
            if line.startswith(f"{package}=="):
                return line.split("==", 1)[1].strip()
                
        return None
