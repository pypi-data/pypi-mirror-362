import re
from easeon.core.package_validator import PackageValidator

class PackageName:
    """Class to validate package names according to PyPI rules."""
    
    def __init__(self, name: str):
        """Initialize with package name."""
        self.name = name
        self.valid = True
        self.error = ""
        self._validate()
    
    def _validate(self) -> None:
        """Validate the package name and set error message if invalid."""
        try:
            # Check for empty name
            if not self.name:
                self.valid = False
                self.error = "Package name cannot be empty"
                return
                
            # Normalize package name according to PyPI rules
            normalized_name = self.name.lower()
            # Only normalize characters that aren't part of version numbers
            if not any(op in self.name for op in ['==', '>=', '<=', '>', '<', '~=']):
                normalized_name = re.sub(r'[-_.]+', '-', normalized_name)
            
            # Check if name starts with a number
            if normalized_name[0].isdigit():
                self.valid = False
                self.error = f"Invalid package name: {self.name}. Package names cannot start with numbers"
                return
            
            # Check for valid characters
            if not all(c.isalnum() or c in '-._' for c in normalized_name):
                invalid_chars = ''.join(set(c for c in normalized_name if not (c.isalnum() or c in '-._')))
                self.valid = False
                self.error = f"Invalid character(s) in package name: {self.name}. Invalid characters: {invalid_chars}"
                return
            
            # Check for reserved names
            if normalized_name in PackageValidator.RESERVED_NAMES:
                self.valid = False
                self.error = f"Invalid package name: {self.name}. This is a reserved name"
                return
            
        except Exception as e:
            self.valid = False
            self.error = f"Invalid package name: {str(e)}"
    
    def is_valid(self) -> bool:
        """Return whether the package name is valid."""
        return self.valid
    
    def get_error(self) -> str:
        """Return the error message if any."""
        return self.error
