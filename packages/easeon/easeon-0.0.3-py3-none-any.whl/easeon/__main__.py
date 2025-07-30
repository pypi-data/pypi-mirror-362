"""Main entry point for the Easeon CLI."""

import logging
import sys
from typing import List, Optional

from easeon.core.easeon_installer import EaseonInstaller
from easeon.logging_helper import setup_logging


def main(args: Optional[List[str]] = None) -> None:
    """Run the Easeon CLI.
    
    Args:
        args: Command line arguments. If None, uses sys.argv[1:]
    """
    # Set up logging with default settings
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        from easeon.cli.cli_manager import CLIManager
        
        # Initialize the installer with default settings
        installer = EaseonInstaller()
        
        # Initialize and run the CLI
        cli_manager = CLIManager(installer)
        cli_manager.run(args)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        logger.critical("An unexpected error occurred: %s", str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
