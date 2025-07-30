"""Python environment detector for finding pytest."""

import subprocess
from typing import List, Optional
from pathlib import Path


class PythonEnvDetector:
    """Detects Python environment and finds pytest command."""

    def detect_pytest_command(self) -> Optional[List[str]]:
        """Detect the appropriate pytest command based on environment."""
        # Check for uv first (project preference)
        if self._check_command_exists(["uv", "--version"]):
            return ["uv", "run", "python", "-m", "pytest"]

        # Fallback to direct pytest if available
        if self._check_command_exists(["pytest", "--version"]):
            return ["pytest"]

        return None

    def _check_command_exists(self, command: List[str]) -> bool:
        """Check if a command exists and is executable."""
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def find_project_root(self) -> Path:
        """Find project root by looking for marker files."""
        current = Path.cwd()

        # Marker files in order of preference
        markers = ["uv.lock", "pyproject.toml", ".git", "setup.py"]

        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return current
            current = current.parent

        # If no marker found, return current directory
        return Path.cwd()
