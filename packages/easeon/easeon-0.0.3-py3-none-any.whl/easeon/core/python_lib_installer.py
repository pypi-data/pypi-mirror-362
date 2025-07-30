import os
import subprocess
import logging
import platform
from packaging import version
from typing import List, Optional, Dict, Tuple
from importlib.metadata import PackageNotFoundError

from easeon.core.utils import Utils
from easeon.core.file_handler import FileHandler
from easeon.core.package_manager import PackageManager
from easeon.core.virtual_env_manager import VirtualEnvManager
from easeon.core.package_list_manager import PackageListManager
from easeon.core.pypi_utils import PyPIUtils
from easeon.cli.cli_manager import CLIManager


class PythonLibInstaller:
    def __init__(self, env_name: str = None, auto_create_venv: bool = False, verbose: bool = False, use_test_pypi: bool = False, use_test_pypi_easeon: bool = False) -> None:
        self.logger = logging.getLogger(__name__)
        self.utils = Utils()
        self.file_handler = FileHandler()
        self.package_manager = PackageManager(verbose=verbose)
        self.virtual_env_manager = VirtualEnvManager(env_name)
        self.package_list_manager = PackageListManager()
        self.cli_manager = CLIManager(self)
        self.pypi_utils = PyPIUtils()
        self.use_test_pypi = use_test_pypi
        self.use_test_pypi_easeon = use_test_pypi_easeon
        
        self.utils.set_utf8_terminal_encoding()
        self.os_name: str = os.name
        self.platform_name: str = platform.system()
        self.verbose = verbose
        self.virtual_env_manager.check_virtualenv(auto_create_venv)

    def install(self) -> None:
        """Install packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to install.")
            self.logger.warning("Install called with empty package list.")
            return

    def get_list(self, packages: List[str]) -> None:
        """Set the package list."""
        self.package_list_manager.get_package_list(packages)

    def get_list_from_txt(self, file_path: str) -> None:
        """Load packages from a .txt file."""
        self.package_list_manager.load_from_file(file_path)

    def get_list_from_csv(self, file_path: str) -> None:
        """Load packages from a .csv file."""
        self.package_list_manager.load_from_file(file_path)

    def uninstall(self) -> None:
        """Uninstall packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to uninstall.")
            self.logger.warning("Uninstall called with empty package list.")
            return

        # Get the virtual environment path
        venv_path = self.virtual_env_manager.env_path
        if not os.path.exists(venv_path):
            print("❌ Error: No virtual environment found")
            print("Please create a virtual environment first or use auto_create_venv=True")
            return

        # Get the pip executable path in the virtual environment
        pip_path = os.path.join(self.virtual_env_manager.env_path, "Scripts", "pip.exe") if os.name == 'nt' else "pip"

        # Ensure virtual environment exists
        if not self.virtual_env_manager.is_in_virtualenv():
            self.logger.error("Not in a virtual environment")
            return

        try:
            for pkg in packages:
                print(f"🗑️ Uninstalling: {pkg}")
                self.logger.info(f"Uninstalling: {pkg}")
                
                if not self.utils.is_valid_package_name(pkg):
                    print(f"❌ Invalid name: {pkg}")
                    self.logger.warning(f"Invalid package name: {pkg}")
                    continue

                try:
                    subprocess.run([pip_path, "uninstall", "-y", pkg], check=True)
                    print(f"✅ Successfully uninstalled: {pkg}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to uninstall: {pkg}")
                    self.logger.error(f"Failed to uninstall {pkg}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Uninstallation failed: {str(e)}")

    def _is_package_already_installed(self, package_name: str) -> Tuple[bool, Optional[str]]:
        """Check if a package is already installed and return its version."""
        try:
            installed_version = version.parse(version.Version(package_name))
            return True, str(installed_version)
        except PackageNotFoundError:
            return False, None
        except Exception:
            return False, None

    def _run_pip_command(self, command: List[str], package_name: str) -> bool:
        """Run a pip command and handle errors."""
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Pip command failed for {package_name}: {str(e)}")
            return False


    def update(self) -> None:
        """Update packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to update.")
            self.logger.warning("Update called with empty package list.")
            return

        # Get the virtual environment path
        venv_path = self.virtual_env_manager.env_path
        if not os.path.exists(venv_path):
            print("❌ Error: No virtual environment found")
            print("Please create a virtual environment first or use auto_create_venv=True")
            return

        # Get the pip executable path in the virtual environment
        pip_path = os.path.join(venv_path, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
        
        # Get installed packages and their versions
        installed_packages = self._get_installed_packages()
        
        for pkg in packages:
            print(f"\n🔄 Checking for updates: {pkg}")
            self.logger.info(f"Checking for updates: {pkg}")
            
            if not self.utils.is_valid_package_name(pkg):
                print(f"❌ Invalid name: {pkg}")
                self.logger.warning(f"Invalid package name: {pkg}")
                continue

            # Skip if package is not installed
            if pkg not in installed_packages:
                print(f"⚠️ Package not installed: {pkg}")
                self.logger.warning(f"Package not installed: {pkg}")
                continue

            # Get current and latest versions
            current_version = installed_packages[pkg]
            latest_version = self.pypi_utils.get_latest_version(pkg, self.use_test_pypi)
            
            if latest_version:
                current = version.parse(current_version)
                latest = version.parse(latest_version)
                
                if current < latest:
                    print(f"🔍 Update available: {pkg} {current_version} -> {latest_version}")
                    try:
                        subprocess.run([pip_path, "install", "--upgrade", f"{pkg}=={latest_version}"], check=True)
                        print(f"✅ Updated: {pkg} to {latest_version}")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Failed to update: {pkg}")
                        self.logger.error(f"Failed to update {pkg}: {str(e)}")
                else:
                    print(f"✅ Already up to date: {pkg} ({current_version})")
            else:
                print(f"⚠️ No updates found: {pkg}")
                self.logger.info(f"No updates found for: {pkg}")

    def _get_installed_packages(self) -> Dict[str, str]:
        """Get a dictionary of installed packages and their versions."""
        try:
            import pkg_resources
            return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        except Exception as e:
            self.logger.error(f"Error getting installed packages: {str(e)}")
            return {}

    def uninstall(self) -> None:
        """Uninstall packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to uninstall.")
            self.logger.warning("Uninstall called with empty package list.")
            return

        # Get the virtual environment path
        venv_path = self.virtual_env_manager.env_path
        if not os.path.exists(venv_path):
            print("❌ Error: No virtual environment found")
            print("Please create a virtual environment first or use auto_create_venv=True")
            return

        # Get the pip executable path in the virtual environment
        pip_path = os.path.join(venv_path, 'Scripts' if os.name == 'nt' else 'bin', 'pip')
        
        # Get installed packages
        installed_packages = self._get_installed_packages()
        
        for pkg in packages:
            print(f"\n🗑 Uninstalling: {pkg}")
            self.logger.info(f"Uninstalling: {pkg}")
            
            if not self.utils.is_valid_package_name(pkg):
                print(f"❌ Invalid name: {pkg}")
                self.logger.warning(f"Invalid package name: {pkg}")
                continue

            # Skip if package is not installed
            if pkg not in installed_packages:
                print(f"⚠️ Package not installed: {pkg}")
                self.logger.warning(f"Package not installed: {pkg}")
                continue

            # Use the virtual environment's pip
            import subprocess
            try:
                subprocess.run([pip_path, "uninstall", "-y", pkg], check=True)
                print(f"✅ Successfully uninstalled: {pkg}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to uninstall: {pkg}")
                self.logger.error(f"Failed to uninstall {pkg}: {str(e)}")

    def uninstall(self) -> None:
        """Uninstall packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to uninstall.")
            self.logger.warning("Uninstall called with empty package list.")
            return

        for pkg in packages:
            print(f"\n📦 Uninstalling: {pkg}")
            self.logger.info(f"Uninstalling: {pkg}")
            if not self.package_manager.run_pip_command(["uninstall", "-y", pkg], pkg, uninstall=True):
                continue

    def update(self) -> None:
        """Update packages from the list."""
        packages = self.package_list_manager.get_package_list()
        if not packages:
            print("❗ No packages to update.")
            self.logger.warning("Update called with empty package list.")
            return

        for pkg in packages:
            print(f"\n📦 Updating: {pkg}")
            self.logger.info(f"Updating: {pkg}")
            if not self.package_manager.run_pip_command(["install", "--upgrade", pkg], pkg):
                continue

    def run_cli(self) -> None:
        """Run the command-line interface."""
        self.cli_manager.run()
