import os
import tempfile
import unittest
import subprocess
from io import StringIO
from contextlib import redirect_stdout

from jbussdieker.cli.main import main


class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmpdir.cleanup()

    def test_generated_project_coverage_target_exits_zero(self):
        """Test that generated project's coverage make target exits with code 0."""
        project_name = "integration_test_project"

        # Create the project
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", project_name])

        # Change to project directory
        project_dir = os.path.join(self.tmpdir.name, project_name)
        os.chdir(project_dir)

        # Run coverage target - this should exit with code 0
        result = subprocess.run(
            ["make", "coverage"],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
        )

        # Verify exit code is 0
        self.assertEqual(
            result.returncode,
            0,
            f"Coverage target failed with exit code {result.returncode}. "
            f"stdout: {result.stdout}, stderr: {result.stderr}",
        )

        # Verify coverage output contains expected content
        self.assertIn("coverage run", result.stdout)
        self.assertIn("coverage report", result.stdout)

    def test_generated_project_lint_target_exits_zero(self):
        """Test that generated project's lint make target exits with code 0."""
        project_name = "integration_test_project_lint"

        # Create the project
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", project_name])

        # Change to project directory
        project_dir = os.path.join(self.tmpdir.name, project_name)
        os.chdir(project_dir)

        # Run lint target - this should exit with code 0
        result = subprocess.run(
            ["make", "lint"],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
        )

        # Verify exit code is 0
        self.assertEqual(
            result.returncode,
            0,
            f"Lint target failed with exit code {result.returncode}. "
            f"stdout: {result.stdout}, stderr: {result.stderr}",
        )

        # Verify lint output contains expected content
        self.assertIn("black --check", result.stdout)
        self.assertIn("mypy src/", result.stdout)

    def test_generated_project_format_target_exits_zero(self):
        """Test that generated project's format make target exits with code 0."""
        project_name = "integration_test_project_format"

        # Create the project
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", project_name])

        # Change to project directory
        project_dir = os.path.join(self.tmpdir.name, project_name)
        os.chdir(project_dir)

        # Run format target - this should exit with code 0
        result = subprocess.run(
            ["make", "format"],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
        )

        # Verify exit code is 0
        self.assertEqual(
            result.returncode,
            0,
            f"Format target failed with exit code {result.returncode}. "
            f"stdout: {result.stdout}, stderr: {result.stderr}",
        )

    def test_generated_project_build_target_exits_zero(self):
        """Test that generated project's build make target exits with code 0."""
        project_name = "integration_test_project_build"

        # Create the project
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", project_name])

        # Change to project directory
        project_dir = os.path.join(self.tmpdir.name, project_name)
        os.chdir(project_dir)

        # Run build target - this should exit with code 0
        result = subprocess.run(
            ["make", "build"],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
        )

        # Verify exit code is 0
        self.assertEqual(
            result.returncode,
            0,
            f"Build target failed with exit code {result.returncode}. "
            f"stdout: {result.stdout}, stderr: {result.stderr}",
        )

        # Verify build output contains expected content
        self.assertTrue(
            ".venv/bin/python -m build" in result.stdout or "build" in result.stdout,
            "Build command should appear in output",
        )

        # Verify that dist directory was created
        self.assertTrue(os.path.isdir("dist"), "dist directory should be created")

        # Verify that wheel and source distribution files exist
        dist_files = os.listdir("dist")
        self.assertTrue(
            any(f.endswith(".whl") for f in dist_files),
            "Should create wheel file",
        )
        self.assertTrue(
            any(f.endswith(".tar.gz") for f in dist_files),
            "Should create source distribution",
        )


if __name__ == "__main__":
    unittest.main()
