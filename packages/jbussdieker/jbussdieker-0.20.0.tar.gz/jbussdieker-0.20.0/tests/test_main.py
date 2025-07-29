import unittest
import subprocess
import sys
import jbussdieker.__main__


class TestMain(unittest.TestCase):
    def test_main_module_runs(self):
        result = subprocess.run(
            [sys.executable, "-m", "jbussdieker", "version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "jbussdieker: v" in result.stdout
