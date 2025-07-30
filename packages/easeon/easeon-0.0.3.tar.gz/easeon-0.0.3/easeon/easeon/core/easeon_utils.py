from easeon.core.file_handler import FileHandler
from easeon.core.package_list_manager import PackageListManager
from typing import List

def install_packages_from_txt(path: str) -> None:
    handler = FileHandler()
    manager = PackageListManager()
    pkgs = handler.bulk_txt(path)
    manager.set_package_list(pkgs)
    manager.install()

def install_packages_from_csv(path: str) -> None:
    handler = FileHandler()
    manager = PackageListManager()
    pkgs = handler.bulk_csv(path)
    manager.set_package_list(pkgs)
    manager.install()

def install_packages_from_list(pkg_list: List[str]) -> None:
    manager = PackageListManager()
    manager.set_package_list(pkg_list)
    manager.install()

def search_pypi(package_name: str, testpypi: bool = False) -> dict:
    """Search for a package on PyPI or TestPyPI and return info dict."""
    from easeon.core.pypi_search import PyPISearcher
    searcher = PyPISearcher(use_testpypi=testpypi)
    return searcher.get_package_versions(package_name)
