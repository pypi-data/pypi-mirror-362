import unittest
import subprocess
from unittest.mock import patch

from jbussdieker.project.git_utils import get_default_branch


class TestGitUtils(unittest.TestCase):
    def test_get_default_branch_with_config(self):
        """Test getting default branch from git config."""
        with patch("subprocess.run") as mock_run:
            mock_result = mock_run.return_value
            mock_result.returncode = 0
            mock_result.stdout = "master\n"

            result = get_default_branch()
            self.assertEqual(result, "master")

    def test_get_default_branch_fallback_to_master(self):
        """Test fallback to 'master' when git config fails."""
        with patch("subprocess.run") as mock_run:
            mock_result = mock_run.return_value
            mock_result.returncode = 1
            mock_result.stdout = ""

            result = get_default_branch()
            self.assertEqual(result, "master")

    def test_get_default_branch_git_not_found(self):
        """Test fallback to 'master' when git is not found."""
        with patch("subprocess.run", side_effect=FileNotFoundError("git not found")):
            result = get_default_branch()
            self.assertEqual(result, "master")

    def test_get_default_branch_called_process_error(self):
        """Test fallback to 'master' when subprocess raises CalledProcessError."""
        with patch(
            "subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")
        ):
            result = get_default_branch()
            self.assertEqual(result, "master")


if __name__ == "__main__":
    unittest.main()
