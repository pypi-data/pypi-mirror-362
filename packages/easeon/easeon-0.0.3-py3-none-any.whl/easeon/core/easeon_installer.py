import logging
import sys
from pathlib import Path
from typing import List, Optional, Union

from easeon.core.file_handler import FileHandler
from easeon.core.package_list_manager import PackageListManager
from easeon.core.virtual_env_manager import VirtualEnvManager
from easeon.logging_helper import setup_logging
from easeon.paths import get_log_file_path

class EaseonInstaller:
    """
    A high-level interface for managing Python package installations with virtual environment support.
    
    This class provides methods to install packages from various sources while handling
    virtual environment creation, logging, and package management automatically.
    
    Features:
        - Automatic virtual environment creation and management
        - Support for multiple package sources (lists, files)
        - Configurable logging to files and/or console
        - Test PyPI support for development and testing
    
    Example:
        ```python
        # Basic usage
        installer = EaseonInstaller()
        installer.install_from_list(["requests", "numpy"])
        
        # With custom virtual environment
        installer = EaseonInstaller(env_name="myenv")
        
        # With custom logging
        installer = EaseonInstaller(log_destination="install.log")
        ```
    """
    
    def _ensure_self_installed(self, env_path: Union[str, Path]) -> None:
        """Ensure Easeon is installed in the target virtual environment.
        
        Args:
            env_path: Path to the virtual environment directory
        """
        import subprocess
        import sys
        
        env_path = Path(env_path).resolve()
        
        # Get the path to the virtual environment's Python
        if sys.platform == "win32":
            python_exec = env_path / "Scripts" / "python.exe"
        else:
            python_exec = env_path / "bin" / "python"
            
        # Check if Easeon is already installed in the virtual environment
        check_cmd = [str(python_exec), "-c", "import easeon; print(easeon.__version__)"]
        try:
            subprocess.run(check_cmd, check=True, capture_output=True, text=True)
            self.logger.info("Easeon is already installed in the virtual environment")
            return
        except subprocess.CalledProcessError:
            pass  # Easeon is not installed, proceed with installation
            
        # Get the path to the current project root (where setup.py is located)
        project_root = Path(__file__).parent.parent.parent
        setup_py = project_root / "setup.py"
        if not setup_py.exists():
            self.logger.warning("Could not find setup.py in project root")
            return
            
        # Install Easeon in development mode
        self.logger.info(f"Installing Easeon in development mode from {project_root}")
        pip_cmd = [str(python_exec), "-m", "pip", "install", "-e", str(project_root)]
        try:
            result = subprocess.run(pip_cmd, check=True, capture_output=True, text=True)
            self.logger.debug(f"Installation output: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"Installation warnings: {result.stderr}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to install Easeon in virtual environment: {e.stderr or e.stdout}"
            self.logger.error(error_msg)
            raise RuntimeError(f"Failed to install Easeon in the virtual environment: {error_msg}")

    def __init__(
        self,
        auto_create_venv: bool = True,
        env_name: Optional[str] = None,
        venv_location: Optional[Union[str, Path]] = None,
        use_test_pypi: bool = False,
        use_test_pypi_easeon: bool = False,
        log_destination: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Initialize the EaseonInstaller with the specified configuration.
        
        Args:
            auto_create_venv: If True, automatically creates a virtual environment
                if one is not already activated. Defaults to True.
            env_name: Name of the virtual environment to create or use.
                If None, uses the default '.venv' or the currently activated environment.
            use_test_pypi: If True, uses TestPyPI as the package index.
            use_test_pypi_easeon: If True, uses TestPyPI specifically for the easeon package.
            log_destination: Where to write log messages. Can be:
                - None: Logs only to home directory
                - Path/str: Path to a custom log file
                - "console": Logs to console and home directory
        
        Notes:
            - Logs are always written to the home directory at '~/easeon_install.log'
            - Virtual environments are created in the current working directory
            - All operations are logged with timestamps and error details
        """
        # Set up logging
        self.log_files = []
        
        # 1. Always log to the user's home directory
        home_log_file = Path.home() / 'easeon_install.log'
        self.log_files.append(str(home_log_file))
        
        # Set up logging to the home directory
        setup_logging(log_file=home_log_file, 
                     console=False,
                     log_level=logging.INFO)
        
        # 2. If a custom log destination is provided, add it as an additional log handler
        if log_destination and isinstance(log_destination, (str, Path)) and str(log_destination).lower() != 'console':
            custom_log_file = Path(log_destination)
            self.log_files.append(str(custom_log_file))
            
            # Add a new file handler for the custom log file
            file_handler = logging.FileHandler(
                str(custom_log_file),
                mode='a',
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)
            
            logging.info(f"Additional log file: {custom_log_file.resolve()}")
        
        # 3. If console logging is explicitly requested, add a console handler
        if log_destination and str(log_destination).lower() == 'console':
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            logging.getLogger().addHandler(console_handler)
            logging.info("Console logging enabled")
                    
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing EaseonInstaller")
        
        # Initialize components
        self.handler = FileHandler()
        self.manager = PackageListManager(
            use_test_pypi=use_test_pypi,
            use_test_pypi_easeon=use_test_pypi_easeon
        )
        
        self.auto_create_venv = auto_create_venv
        self.env_name = env_name or '.venv'
        self.venv_location = Path(venv_location) if venv_location else None
        self.use_test_pypi = use_test_pypi
        self.use_test_pypi_easeon = use_test_pypi_easeon

        # Set up virtual environment path
        if self.venv_location:
            self.virtual_env_manager = VirtualEnvManager(env_name=str(self.venv_location))
        else:
            self.virtual_env_manager = VirtualEnvManager(env_name=self.env_name)
        
        # Set up virtual environment only if explicitly requested
        if self.auto_create_venv and self.env_name:
            self.logger.info(f"Setting up virtual environment: {self.env_name}")
            self.virtual_env_manager.check_virtualenv(auto_create=True)
            venv_manager = VirtualEnvManager(env_name=self.env_name)
            venv_manager.check_virtualenv(auto_create=True)
            
            # Automatically install Easeon in the new virtual environment
            try:
                self._ensure_self_installed(Path(self.env_name))
            except Exception as e:
                self.logger.warning(f"Could not automatically install Easeon in virtual environment: {e}")
        else:
            self.logger.info("Using current Python environment (no virtual environment)")

    def _get_python_executable(self) -> str:
        """Get the Python executable path, preferring the virtual environment if available."""
        if hasattr(self, 'virtual_env_manager') and hasattr(self.virtual_env_manager, 'get_python_executable'):
            return self.virtual_env_manager.get_python_executable()
        return sys.executable

    def install_from_txt(self, path: str) -> None:
        """Install packages from a text file."""
        self.logger.info(f"Installing packages from text file: {path}")
        try:
            pkgs = self.handler.bulk_txt(path)
            self.manager.set_package_list(pkgs)
            python_executable = self._get_python_executable()
            self.manager.install(python_executable=python_executable)
            self.logger.info(f"Successfully installed packages from {path}")
        except Exception as e:
            self.logger.error(f"Failed to install packages from {path}: {e}", exc_info=True)
            raise

    def install_from_csv(self, path: str) -> None:
        """Install packages from a CSV file."""
        self.logger.info(f"Installing packages from CSV file: {path}")
        try:
            pkgs = self.handler.bulk_csv(path)
            self.manager.set_package_list(pkgs)
            python_executable = self._get_python_executable()
            self.manager.install(python_executable=python_executable)
            self.logger.info(f"Successfully installed packages from {path}")
        except Exception as e:
            self.logger.error(f"Failed to install packages from {path}: {e}", exc_info=True)
            raise

    def install_from_list(self, pkg_list: List[str]) -> None:
        """
        Install packages from a list of package specifications.
        
        Args:
            pkg_list: List of package specifications to install.
                Can include version specifiers (e.g., 'package==1.0.0' or 'package>=1.0.0').
                
        Example:
            ```python
            # Install specific versions
            installer.install_from_list(["requests==2.28.1", "numpy>=1.21.0"])
            
            # Install latest versions
            installer.install_from_list(["pandas", "matplotlib"])
            ```
            
        Raises:
            RuntimeError: If package installation fails
            
        Note:
            - All installations are logged to the configured log destinations
            - Virtual environment is automatically activated if configured
        """
        self.logger.info(f"Installing packages: {', '.join(pkg_list)}")
        try:
            self.manager.set_package_list(pkg_list)
            python_executable = self._get_python_executable()
            self.manager.install(python_executable=python_executable)
            self.logger.info("Successfully installed all packages")
        except Exception as e:
            self.logger.error(f"Failed to install packages: {e}", exc_info=True)
            raise
            
    def get_logs(self, lines: int = 50) -> str:
        """
        Retrieve logs from the home directory log file.
        
        Args:
            lines: Number of lines to retrieve (from the end of the file). 
                  If None, returns the entire log file.
                  
        Returns:
            str: The requested log content
            
        Raises:
            FileNotFoundError: If the log file doesn't exist
        """
        log_file = Path.home() / 'easeon_install.log'
        
        if not log_file.exists():
            return "No log file found at: " + str(log_file)
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                if lines is None:
                    return f.read()
                
                # Efficiently get last N lines
                from collections import deque
                return ''.join(deque(f, maxlen=lines))
                
        except Exception as e:
            self.logger.error(f"Error reading log file: {e}")
            raise
