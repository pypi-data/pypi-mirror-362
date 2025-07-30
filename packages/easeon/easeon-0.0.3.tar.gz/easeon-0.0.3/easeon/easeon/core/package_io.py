"""File I/O operations for package lists."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

class PackageIO:
    """Handles reading and writing package lists to/from files."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the package I/O handler."""
        self.logger = logger or logging.getLogger(__name__)
    
    def load_from_file(self, file_path: Union[str, Path]) -> Dict[str, Optional[str]]:
        """
        Load packages from a requirements file or CSV.
        
        Args:
            file_path: Path to the requirements file or CSV
            
        Returns:
            Dictionary of package names to versions
        """
        file_path = Path(file_path)
        if not file_path.exists():
            self.logger.warning(f"File not found: {file_path}")
            return {}
            
        # Handle CSV files
        if file_path.suffix.lower() == '.csv':
            return self._load_from_csv(file_path)
            
        # Handle text requirements files
        return self._load_from_text(file_path)
        
    def _load_from_text(self, file_path: Path) -> Dict[str, Optional[str]]:
        """Load packages from a requirements.txt style file."""
        packages = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    # Handle -r requirements.txt
                    if line.startswith('-r '):
                        include_file = file_path.parent / line[2:].strip()
                        packages.update(self.load_from_file(include_file))
                        continue
                        
                    # Parse package name and version
                    if '==' in line:
                        name, version = line.split('==', 1)
                        packages[name.strip()] = version.strip()
                    else:
                        packages[line.strip()] = None
                        
        except Exception as e:
            self.logger.error(f"Error reading text file {file_path}: {e}")
            return {}
            
        return packages
        
    def _load_from_csv(self, file_path: Path) -> Dict[str, Optional[str]]:
        """Load packages from a CSV file with name,version columns."""
        import csv
        packages = {}
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                if 'name' not in reader.fieldnames:
                    self.logger.error(f"CSV file {file_path} is missing 'name' column")
                    return {}
                    
                for row in reader:
                    name = row.get('name', '').strip()
                    if not name:  # Skip empty names
                        continue
                        
                    version = row.get('version', '').strip()
                    packages[name] = version if version else None
                    
        except Exception as e:
            self.logger.error(f"Error reading CSV file {file_path}: {e}")
            return {}
            
        return packages
    
    def save_to_file(
        self, 
        packages: Dict[str, Optional[str]], 
        file_path: Union[str, Path],
        include_versions: bool = True
    ) -> bool:
        """
        Save packages to a requirements file.
        
        Args:
            packages: Dictionary of package names to versions
            file_path: Path to save the requirements file
            include_versions: Whether to include version specifiers
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for name, version in sorted(packages.items()):
                    if include_versions and version:
                        f.write(f"{name}=={version}\n")
                    else:
                        f.write(f"{name}\n")
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing to file {file_path}: {e}")
            return False
