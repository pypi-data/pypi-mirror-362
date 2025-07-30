import re
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.requirements import Requirement, InvalidRequirement
from packaging.version import parse, InvalidVersion
from typing import Tuple, Optional, Dict, Any

class PackageValidator:
    """Optimized package name and version validation using packaging library."""
    
    PACKAGE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$')
    VERSION_PATTERN = re.compile(r'^\d+(\.\d+)*([a-zA-Z0-9]+)?$')
    RESERVED_NAMES = frozenset({
        'pip', 'setuptools', 'wheel', 'distutils', 'pkg_resources',
        'sys', 'os', 'io', 'json', 'http', 'urllib', 'email',
        'test', 'tests', 'doc', 'docs', 'example', 'examples',
        'aux', 'con', 'prn', 'nul',
        'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9',
        'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9'
    })

    @classmethod
    def parse_requirement(cls, requirement_string: str) -> Optional[Tuple[str, str]]:
        try:
            req = Requirement(requirement_string)
            return req.name, str(req.specifier) if req.specifier else ""
        except InvalidRequirement:
            return None

    @classmethod
    def is_valid_package_name(cls, package_name: str) -> Tuple[bool, str]:
        try:
            if not package_name:
                return False, "Requirement string must be a non-empty string"
            if any(op in package_name for op in ['==', '>=', '<=', '>', '<', '~=']):
                return cls._validate_version_specification(package_name)
            if '-' in package_name:
                return False, f"Invalid package name: {package_name}. Package name must contain only letters, numbers, and special characters (_-.)"
            if not package_name:
                return False, "Package name cannot be empty"
            if package_name[0].isdigit():
                return False, f"Invalid package name: {package_name}"
            if not all(c.isalnum() or c in '._-' for c in package_name):
                return False, f"Invalid package name: {package_name}"
            if package_name.lower() in cls.RESERVED_NAMES:
                return False, f"Invalid package name: {package_name}"
            return True, ""
        except Exception as e:
            return False, f"Invalid requirement format: {e}."

    @classmethod
    def is_valid_version_specifier(cls, version_spec: str) -> bool:
        if not version_spec:
            return True
        try:
            if '==' in version_spec:
                version = version_spec.split('==')[1]
                try:
                    parsed_version = parse(version)
                    if not all(isinstance(x, int) for x in parsed_version.release):
                        return False
                except InvalidVersion:
                    return False
            else:
                SpecifierSet(version_spec)
            return True
        except InvalidSpecifier:
            return False

    @classmethod
    def validate_requirement(cls, requirement_string: str) -> Dict[str, Any]:
        result = {
            'valid': False,
            'package_name': None,
            'version_specifier': None,
            'normalized_name': None,
            'errors': []
        }
        if not requirement_string or not isinstance(requirement_string, str):
            result['errors'].append("Requirement string must be a non-empty string")
            return result
        parsed = cls.parse_requirement(requirement_string)
        if not parsed:
            result['errors'].append("Invalid requirement format")
            return result
        package_name, version_spec = parsed
        result['package_name'] = package_name
        result['version_specifier'] = version_spec
        result['normalized_name'] = package_name.lower() if package_name else None
        if not cls.is_valid_package_name(package_name)[0]:
            result['errors'].append(f"Invalid package name: {package_name}. Package name must be a string containing only letters, numbers, and special characters (_-.)")
            return result
        if version_spec:
            if not cls.is_valid_version_specifier(version_spec):
                result['errors'].append(f"Invalid version format: {version_spec}. Version must be in the format 'major.minor.patch'")
        result['valid'] = len(result['errors']) == 0
        return result
