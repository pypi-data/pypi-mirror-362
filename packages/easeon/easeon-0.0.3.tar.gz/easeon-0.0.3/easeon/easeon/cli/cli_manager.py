"""Command Line Interface Manager for Easeon."""

import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Any, Union, Dict, Tuple

from ..core.easeon_installer import EaseonInstaller
from ..core.virtual_env_manager import VirtualEnvManager
from .cli_parser import CLIParser


class CLIManager:
    """Manages the command line interface for Easeon.
    
    This class handles the main CLI workflow including argument parsing,
    command execution, and error handling.
    """
    
    def __init__(self, installer: EaseonInstaller) -> None:
        """Initialize the CLI Manager.
        
        Args:
            installer: An instance of EaseonInstaller to handle package operations
        """
        self.installer = installer
        self.logger = logging.getLogger(__name__)
        self.parser = CLIParser()
        self._instance_id = id(self)  # Unique identifier for this instance

    def _resolve_file_path(self, file_path: Union[str, Path], check_exists: bool = True) -> Path:
        """Resolve and validate a file path.
        
        Args:
            file_path: The file path to resolve (can be relative or absolute)
            check_exists: If True, verifies the file exists and is accessible
            
        Returns:
            Path: Resolved absolute path
            
        Raises:
            ValueError: If the path is invalid, doesn't exist (if check_exists=True),
                      or is outside the allowed directories
        """
        if not file_path:
            raise ValueError("File path cannot be empty")
            
        try:
            # Convert to Path if it's a string
            path = Path(file_path) if isinstance(file_path, str) else file_path
            
            # Resolve to absolute path
            try:
                abs_path = path.resolve(strict=False)
            except RuntimeError as e:  # Handle too long paths on Windows
                error_msg = f"Path resolution error: {e}"
                self.logger.error(error_msg)
                raise ValueError(error_msg) from e
                
            # Check if path is within allowed directories (security check)
            try:
                abs_path.relative_to(Path.cwd())
            except ValueError as e:
                # Path is outside the current working directory
                error_msg = f"File path must be within the project directory: {abs_path}"
                self.logger.warning(error_msg)
                raise ValueError(error_msg) from e
                
            # Verify file exists and is accessible if required
            if check_exists:
                if not abs_path.exists():
                    error_msg = f"File not found: {abs_path}"
                    self.logger.error(error_msg)
                    raise FileNotFoundError(error_msg)
                if not os.access(abs_path, os.R_OK):
                    error_msg = f"No read permission for file: {abs_path}"
                    self.logger.error(error_msg)
                    raise PermissionError(error_msg)
                    
            return abs_path
            
        except (TypeError, ValueError, OSError) as e:
            error_msg = f"Invalid file path '{file_path}': {e}"
            self.logger.error(error_msg, exc_info=True)
            raise ValueError(error_msg) from e
            
    def _handle_file_operation(self, file_path: Union[str, Path], operation: str) -> bool:
        """Handle common file operations with proper error handling.
        
        Args:
            file_path: Path to the file to operate on
            operation: Operation to perform ('install', 'uninstall', 'update')
            
        Returns:
            bool: True if operation was successful, False otherwise
        """
        try:
            # Resolve and validate the file path
            file = self._resolve_file_path(file_path)
            
            # Log the operation
            self.logger.info("%s packages from file: %s", operation.capitalize(), file)
            
            # Call the appropriate method based on file extension
            if file.suffix == ".txt":
                handler_method = getattr(self.installer, f"{operation}_from_txt")
            elif file.suffix == ".csv":
                handler_method = getattr(self.installer, f"{operation}_from_csv")
            else:
                error_msg = f"Unsupported file type: {file.suffix}"
                self.logger.error(error_msg)
                print(f"❌ {error_msg}")
                return False
                
            # Execute the operation
            result = handler_method(str(file))
            if result:
                print(f"✅ Packages {operation}ed successfully!")
            return result
            
        except Exception as e:
            error_msg = f"Error during {operation} operation: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            print(f"❌ {error_msg}")
            return False

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the command-line interface.
        
        Args:
            args: Command line arguments. If None, uses sys.argv[1:]
            
        Returns:
            int: Exit code (0 for success, non-zero for errors)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not self.parser.validate_args(parsed_args):
                print("❌ Invalid arguments. Use --help for usage.")
                return 1
                
        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            print(f"❌ {error_msg}")
            return 1

        # Set up logging level based on verbosity
        if parsed_args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            self.logger.debug("Debug logging enabled")

        self.logger.info("Running in CLI mode with arguments: %s", parsed_args)
        self.logger.debug("Instance ID: %s", self._instance_id)

        # Handle virtual environment if requested
        if parsed_args.venv is not None:
            try:
                env_path = Path(parsed_args.venv).resolve()
                self.logger.info("Setting up virtual environment at: %s", str(env_path))
                
                # Ensure parent directory exists
                env_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Create the virtual environment first
                venv_manager = VirtualEnvManager(env_name=str(env_path))
                self.logger.info(f"Creating virtual environment at: {env_path}")
                venv_manager.check_virtualenv(auto_create=True)
                if not os.path.exists(env_path):
                    raise RuntimeError("Failed to create virtual environment")
                self.logger.info("Virtual environment created successfully")
                
                # Get the Python executable from the virtual environment
                python_executable = venv_manager.get_python_executable()
                
                # Create the installer with the virtual environment path
                self.installer = EaseonInstaller(
                    auto_create_venv=False,  # We've already created the venv
                    env_name=str(env_path),  # Pass the full path as env_name
                    use_test_pypi=parsed_args.test_pypi,
                    log_destination="console" if parsed_args.verbose else None
                )
                
                # Set the Python executable for the package manager
                self.installer.manager.python_executable = python_executable
                
                # Get activation commands
                if sys.platform == 'win32':
                    activate_script = env_path / 'Scripts' / 'activate'
                    activate_cmd = f'"{activate_script}"'
                    relative_activate = f'.\\{env_path.relative_to(Path.cwd())}\\Scripts\\activate'
                else:
                    activate_script = env_path / 'bin' / 'activate'
                    activate_cmd = f'source "{activate_script}"'
                    relative_activate = f'source {env_path.relative_to(Path.cwd())}/bin/activate'
                
                print(f"✅ Virtual environment is ready at: {env_path}")
                print("\nTo activate this virtual environment, run one of these commands:")
                print(f"\n    {activate_cmd}")
                print(f"\n    {relative_activate}")
                
            except Exception as e:
                error_msg = f"Failed to set up virtual environment: {e}"
                self.logger.error(error_msg, exc_info=True)
                print(f"❌ {error_msg}")
                return 1

        def load_file(file_path: str) -> bool:
            """Load packages from file.
            
            Args:
                file_path: Path to the file containing packages
                
            Returns:
                bool: True if packages were loaded successfully, False otherwise
            """
            try:
                file = self._resolve_file_path(file_path)
                if file.suffix == ".txt":
                    packages = self.installer.handler.bulk_txt(str(file))
                elif file.suffix == ".csv":
                    packages = self.installer.handler.bulk_csv(str(file))
                else:
                    print(f"❌ Unsupported file type: {file.suffix}")
                    self.logger.error("Unsupported file type: %s", file.suffix)
                    return False
                
                if packages:
                    self.installer.manager.set_package_list(packages)
                    self.logger.info("Loaded %d packages from %s", len(packages), file_path)
                    return True
                    
                self.logger.warning("No packages found in file: %s", file_path)
                return False
                
            except Exception as e:
                error_msg = f"Error loading file {file_path}: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                print(f"❌ {error_msg}")
                return False

        # Set test PyPI flag if needed
        self.installer.manager.use_test_pypi = parsed_args.test_pypi
        
        # Handle operations
        exit_code = 0
        try:
            if parsed_args.install:
                if not self._handle_file_operation(parsed_args.install, 'install'):
                    exit_code = 1
                    
            elif parsed_args.uninstall:
                if not self._handle_file_operation(parsed_args.uninstall, 'uninstall'):
                    exit_code = 1
                    
            elif parsed_args.update:
                # The _handle_file_operation will handle the update operation
                if not self._handle_file_operation(parsed_args.update, 'update'):
                    exit_code = 1
                    
        except Exception as e:
            error_msg = f"Operation failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            print(f"❌ {error_msg}")
            return 1
            
        return 0
