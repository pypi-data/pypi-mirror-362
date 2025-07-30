"""Tests for Python environment detector."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from claude_code_adk_validator.python_env_detector import PythonEnvDetector


def test_detect_uv_environment():
    """Test that detector finds uv and pytest in uv environment."""
    detector = PythonEnvDetector()

    # Mock subprocess.run to simulate uv being available
    with patch("subprocess.run") as mock_run:
        # First call checks for uv
        mock_run.return_value = Mock(returncode=0, stdout="uv 0.5.14\n")

        result = detector.detect_pytest_command()

        assert result == ["uv", "run", "python", "-m", "pytest"]
        mock_run.assert_called_with(
            ["uv", "--version"], capture_output=True, text=True, check=False
        )


def test_fallback_to_pytest_when_no_uv():
    """Test that detector falls back to pytest when uv not available."""
    detector = PythonEnvDetector()

    with patch("subprocess.run") as mock_run:
        # First call - uv not found, second call - pytest found
        mock_run.side_effect = [
            Mock(returncode=1),  # uv --version fails
            Mock(returncode=0, stdout="pytest 8.4.1\n"),  # pytest --version succeeds
        ]

        result = detector.detect_pytest_command()

        assert result == ["pytest"]
        assert mock_run.call_count == 2


def test_returns_none_when_no_pytest_available():
    """Test that detector returns None when no pytest found."""
    detector = PythonEnvDetector()

    with patch("subprocess.run") as mock_run:
        # All commands fail
        mock_run.return_value = Mock(returncode=1)

        result = detector.detect_pytest_command()

        assert result is None


def test_find_project_root_with_uv_lock():
    """Test that detector finds project root by uv.lock."""
    detector = PythonEnvDetector()

    # Create a temporary directory structure

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create uv.lock in temp dir
        (temp_path / "uv.lock").touch()

        # Create a subdirectory
        sub_dir = temp_path / "src" / "submodule"
        sub_dir.mkdir(parents=True)

        # Mock cwd to be in the subdirectory
        with patch("pathlib.Path.cwd", return_value=sub_dir):
            root = detector.find_project_root()

            assert root == temp_path
