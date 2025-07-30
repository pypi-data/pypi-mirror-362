import subprocess
import sys
import logging
from typing import List

class PackageManager:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)

    def run_pip_command(self, args: List[str], pkg: str, uninstall: bool = False) -> bool:
        """Execute pip commands with error handling."""
        result = subprocess.run([sys.executable, "-m", "pip"] + args, capture_output=True, text=True)
        if result.returncode != 0:
            stderr = result.stderr.lower()
            self.logger.error(f"pip error with {pkg}: {stderr}")
            if "could not find a version" in stderr:
                print(f"❌ Version not found ➤ {pkg}")
            elif "no matching distribution" in stderr:
                print(f"❌ No match ➤ {pkg}")
            elif "temporary failure" in stderr or "connectionerror" in stderr:
                print("🌐 Network issue. Check your internet.")
            elif "permission denied" in stderr:
                print("🔐 Permission denied. Try as admin.")
            elif uninstall and "not installed" in stderr:
                print(f"⚠️ Not installed ➤ {pkg}")
            else:
                print(f"⚠️ pip error with {pkg}:\n{result.stderr}")
            return False
        
        if self.verbose:
            print(result.stdout.strip())
        print(f"✅ {'Uninstalled' if uninstall else 'Installed'}: {pkg}")
        self.logger.info(f"{'Uninstalled' if uninstall else 'Installed'}: {pkg}")
        return True
