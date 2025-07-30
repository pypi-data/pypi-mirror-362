import csv
import tempfile
from typing import List
import logging

class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def bulk_txt(self, path: str) -> List[str]:
        """Read package list from a text file."""
        try:
            with open(path, 'r', encoding="utf-8") as f:
                return [
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.strip().startswith('#')
                ]
        except FileNotFoundError:
            print(f"❌ File not found: {path}")
            self.logger.error(f"Text file not found: {path}")
            return []

    def bulk_csv(self, path: str) -> List[str]:
        """Read package list from a CSV file."""
        try:
            with open(path, 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                return [
                    row[0].strip() for row in reader
                    if row and not row[0].strip().startswith('#')
                ]
        except FileNotFoundError:
            print(f"❌ File not found: {path}")
            self.logger.error(f"CSV file not found: {path}")
            return []

    def write_temp_package_list(self, packages: List[str]) -> str:
        """Write package list to a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt", encoding="utf-8") as f:
            f.write("\n".join(packages))
            return f.name
