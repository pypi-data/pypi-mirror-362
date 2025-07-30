"""
easeon - Python Package Management Utility

This module provides the main entry point for the Easeon package manager.
It uses modular components from the core package for better organization.

Author: Kiran Soorya R.S
License: MIT
"""

import logging
import sys
from easeon.core import EaseonInstaller
from easeon.cli import CLIParser

# Get logger for this module
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Parse arguments using the CLI parser
        parser = CLIParser()
        args = parser.parse_args()
        
        # Create installer instance with flags
        installer = EaseonInstaller(
            use_test_pypi=args.test_pypi,
            use_test_pypi_easeon=args.test_pypi_easeon,
            auto_create_venv=True
        )
        
        # Install TestPyPI version of easeon if requested
        if args.test_pypi_easeon:
            # Check if we have a virtual environment
            if not installer.virtual_env_manager.is_in_virtualenv():
                print("❌ Error: TestPyPI installation requires a virtual environment")
                print("Please create a virtual environment first or use auto_create_venv=True")
                sys.exit(1)
            
            # Install TestPyPI version of easeon in the created virtual environment
            import subprocess
            print("📦 Installing TestPyPI version of easeon...")
            subprocess.run(["pip", "install", "-i", "https://test.pypi.org/simple/", "easeon"], check=True)
            print("✅ TestPyPI version of easeon installed")
        
        installer.run_cli()
