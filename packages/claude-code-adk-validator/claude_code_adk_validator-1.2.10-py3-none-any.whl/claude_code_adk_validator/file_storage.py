"""File storage for persisting test results - temporary test file."""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class FileStorage:
    """Handles storage and retrieval of test results."""

    def __init__(self, data_dir: str = ".claude/claude-code-adk-validator/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.test_results_file = self.data_dir / "test.json"

    def save_test_results(self, results: Dict[str, Any]) -> None:
        """Save test results to file."""
        with open(self.test_results_file, "w") as f:
            json.dump(results, f, indent=2)

    def load_test_results(self) -> Optional[Dict[str, Any]]:
        """Load test results from file."""
        if not self.test_results_file.exists():
            return None

        with open(self.test_results_file) as f:
            data: Dict[str, Any] = json.load(f)
            return data
