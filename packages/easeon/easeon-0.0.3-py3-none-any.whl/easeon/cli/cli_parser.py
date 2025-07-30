import argparse
import logging
from pathlib import Path
from typing import List, Optional, Set, Tuple, TypeVar, Union

# Type variable for generic return types
T = TypeVar('T')

class CLIParser:
    """Handles command line argument parsing and validation for Easeon."""
    
    def __init__(self) -> None:
        """Initialize the CLI Parser with argument definitions."""
        self.parser = self._create_parser()
        self.logger = logging.getLogger(__name__)
        
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="Easeon - A simple Python package manager",
            epilog="Example: easeon -i requirements.txt --venv --verbose"
        )
        
        # Create mutually exclusive group for commands
        command_group = parser.add_mutually_exclusive_group(required=True)
        
        # Add command line arguments
        command_group.add_argument(
            "-i", "--install",
            type=str,
            metavar="FILE",
            help="Install packages from a requirements file (TXT or CSV)"
        )
        
        command_group.add_argument(
            "-u", "--uninstall",
            type=str,
            metavar="FILE",
            help="Uninstall packages from a requirements file (TXT or CSV)"
        )
        
        command_group.add_argument(
            "-up", "--update",
            type=str,
            metavar="FILE",
            help="Update packages from a requirements file (TXT or CSV)"
        )
        
        # Optional arguments
        optional_group = parser.add_argument_group("optional arguments")
        
        optional_group.add_argument(
            "--test-pypi",
            action="store_true",
            help="Use TestPyPI instead of PyPI for package installation/updates"
        )
        
        optional_group.add_argument(
            "--venv",
            nargs='?',
            const=".venv",  # Default value if --venv is used without argument
            metavar="PATH",
            help="Create/use a virtual environment in the specified directory (default: .venv)"
        )
        
        optional_group.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Enable verbose output with debug information"
        )
        
        return parser
        
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command line arguments.
        
        Args:
            args: List of command line arguments. If None, uses sys.argv[1:]
            
        Returns:
            Namespace containing parsed arguments
        """
        try:
            return self.parser.parse_args(args)
        except argparse.ArgumentError as e:
            self.logger.error("Argument parsing error: %s", str(e))
            self.parser.print_help()
            raise
        
    def validate_args(self, args: argparse.Namespace) -> bool:
        """Validate command line arguments.
        
        Args:
            args: Parsed command line arguments
            
        Returns:
            bool: True if arguments are valid, False otherwise
        """
        # Check file arguments
        file_args = [
            (args.install, "install"),
            (args.uninstall, "uninstall"),
            (args.update, "update")
        ]
        
        valid_extensions = {'.txt', '.csv'}
        
        for file_path, arg_name in file_args:
            if not file_path:
                continue
                
            # Check file extension
            if not any(file_path.lower().endswith(ext) for ext in valid_extensions):
                print(f"❌ Error: Invalid file extension for --{arg_name}. "
                      f"Supported formats: {', '.join(valid_extensions)}")
                return False
                
            # Check if file exists
            if not Path(file_path).is_file():
                print(f"❌ Error: File not found: {file_path}")
                return False
                
        return True
