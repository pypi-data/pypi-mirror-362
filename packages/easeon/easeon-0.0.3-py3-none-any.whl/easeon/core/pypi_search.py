import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PyPISearcher:
    """
    A class to search PyPI and TestPyPI for package versions and display results
    """
    
    def __init__(self, max_workers: int = 5, timeout: int = 10, use_testpypi: bool = False):
        """
        Initialize the PyPI searcher
        
        Args:
            max_workers: Maximum number of concurrent requests
            timeout: Request timeout in seconds
            use_testpypi: If True, search TestPyPI instead of PyPI
        """
        self.max_workers = max_workers
        self.timeout = timeout
        self.use_testpypi = use_testpypi
        self.results = []
        
        # Set base URLs
        if use_testpypi:
            self.base_url = 'https://test.pypi.org/pypi'
            self.index_name = 'TestPyPI'
        else:
            self.base_url = 'https://pypi.org/pypi'
            self.index_name = 'PyPI'
    
    def get_package_versions(self, package_name: str) -> Dict[str, Optional[List[str]]]:
        """
        Fetch available versions for a package from PyPI or TestPyPI
        
        Args:
            package_name: Name of the package to search
            
        Returns:
            Dictionary with package name and list of versions (or None if error)
        """
        try:
            url = f'{self.base_url}/{package_name}/json'
            with urllib.request.urlopen(url, timeout=self.timeout) as response:
                data = json.loads(response.read())
                versions = list(data['releases'].keys())
                # Sort versions in reverse order (newest first)
                versions.sort(reverse=True)
                return {
                    'name': package_name,
                    'versions': versions,
                    'latest': data['info']['version'],
                    'description': data['info']['summary'][:100] + '...' if len(data['info']['summary']) > 100 else data['info']['summary'],
                    'index': self.index_name
                }
        except Exception as e:
            return {
                'name': package_name,
                'versions': None,
                'error': str(e),
                'index': self.index_name
            }
    
    def search_packages(self, package_list: List[str]) -> List[Dict]:
        """
        Search multiple packages concurrently
        
        Args:
            package_list: List of package names to search
            
        Returns:
            List of dictionaries containing package information
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_package = {
                executor.submit(self.get_package_versions, package): package 
                for package in package_list
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_package):
                package = future_to_package[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'name': package,
                        'versions': None,
                        'error': f'Request failed: {str(e)}',
                        'index': self.index_name
                    })
        
        self.results = results
        return results
