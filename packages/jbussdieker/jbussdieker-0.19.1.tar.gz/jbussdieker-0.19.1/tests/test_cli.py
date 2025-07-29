import os
import tempfile
import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from jbussdieker.cli.main import main


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmpdir.name, "config.json")
        os.environ["JBUSSDIEKER_CONFIG"] = self.config_path

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("JBUSSDIEKER_CONFIG", None)

    def test_version_output(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["version"])
        output = buf.getvalue()
        self.assertIn("jbussdieker: v", output)

    def test_no_arguments(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main([])
        output = buf.getvalue()
        self.assertIn("usage: ", output)

    def test_config(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config"])
        output = buf.getvalue()
        self.assertIn("Current config", output)

    def test_config_set_log_format(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config", "--set", 'log_format="FOOLEVEL: %(message)s"'])
        output = buf.getvalue()
        self.assertIn("Set log_format", output)
        buf2 = StringIO()
        with redirect_stdout(buf2):
            main(["version"])
        output2 = buf2.getvalue()
        self.assertIn("FOOLEVEL:", output2)
        self.assertIn("jbussdieker: v", output2)

    def test_config_set_log_level(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config", "--set", 'log_format="%(levelname)s: %(message)s"'])
            main(["config", "--set", "log_level=DEBUG"])
        output = buf.getvalue()
        self.assertIn("Set log_level", output)
        self.assertIn("Set log_format", output)
        buf2 = StringIO()
        with redirect_stdout(buf2):
            main(["version"])
        output2 = buf2.getvalue()
        self.assertIn("DEBUG", output2)
        self.assertIn("jbussdieker: v", output2)

    def test_config_set_private(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config", "--set", "private=true"])
        output = buf.getvalue()
        self.assertIn("Set private", output)

    def test_config_set_custom(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config", "--set", "mycustomkey=42"])
        output = buf.getvalue()
        self.assertIn("Set custom setting", output)

    def test_config_set_invalid(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["config", "--set", "foo"])
        output = buf.getvalue()
        self.assertIn("Invalid format", output)

    def test_verbose_sets_debug_logging(self):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["--verbose", "version"])
        output = buf.getvalue()
        self.assertIn("Parsed args:", output)
        self.assertIn("jbussdieker: v", output)

    @patch("jbussdieker.cli.main.get_eps")
    def test_entry_point_registers_success(self, mock_get_eps):
        # Mock entry point with a register function
        mock_register = MagicMock()
        mock_ep = MagicMock()
        mock_ep.load.return_value = mock_register
        mock_get_eps.return_value = [mock_ep]
        buf = StringIO()
        with redirect_stdout(buf):
            main(["version"])
        mock_ep.load.assert_called_once()
        mock_register.assert_called_once()

    @patch("jbussdieker.cli.main.get_eps")
    def test_entry_point_load_fails(self, mock_get_eps):
        # Mock entry point that raises an exception on load
        mock_ep = MagicMock()
        mock_ep.name = "fail_ep"
        mock_ep.load.side_effect = Exception("load error")
        mock_get_eps.return_value = [mock_ep]
        buf = StringIO()
        with redirect_stdout(buf):
            main(["version"])
        mock_ep.load.assert_called_once()


class TestCLICreate(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmpdir.cleanup()

    def test_create_project_directory(self):
        buf = StringIO()
        project_name = "mytestproject"
        with redirect_stdout(buf):
            main(["project", project_name])
        output = buf.getvalue()
        self.assertIn("Created new project", output)
        self.assertTrue(os.path.isdir(project_name))
        self.assertTrue(os.path.isfile(os.path.join(project_name, ".gitignore")))
        self.assertTrue(
            os.path.isdir(os.path.join(project_name, ".github", "workflows"))
        )
        self.assertTrue(
            os.path.isfile(os.path.join(project_name, ".github", "workflows", "ci.yml"))
        )
        self.assertTrue(
            os.path.isfile(
                os.path.join(project_name, ".github", "workflows", "publish.yml")
            )
        )
        self.assertTrue(os.path.isfile(os.path.join(project_name, "Makefile")))
        self.assertTrue(os.path.isfile(os.path.join(project_name, "pyproject.toml")))
        self.assertTrue(os.path.isfile(os.path.join(project_name, "README.md")))
        self.assertTrue(os.path.isfile(os.path.join(project_name, "LICENSE")))
        self.assertTrue(os.path.isdir(os.path.join(project_name, "src", project_name)))
        self.assertTrue(
            os.path.isfile(
                os.path.join(project_name, "src", project_name, "__init__.py")
            )
        )
        self.assertTrue(os.path.isdir(os.path.join(project_name, "tests")))
        self.assertTrue(
            os.path.isfile(os.path.join(project_name, "tests", "__init__.py"))
        )

    def test_create_existing_directory_fails(self):
        os.makedirs("existing_project")
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", "existing_project"])
        output = buf.getvalue()
        self.assertIn("already exists", output)

    def test_generated_pyproject_toml_content(self):
        project_name = "content_test_project"

        # Create the project
        buf = StringIO()
        with redirect_stdout(buf):
            main(["project", project_name])

        # Read and verify pyproject.toml content
        with open(os.path.join(project_name, "pyproject.toml")) as f:
            content = f.read()

        # This would have failed with the Config object bug
        self.assertIn('description = "Generated by jbussdieker."', content)
        self.assertIn('name = "content_test_project"', content)
        self.assertIn('version = "0.0.0"', content)


class TestCLICommit(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.tmpdir.name, "config.json")
        os.environ["JBUSSDIEKER_CONFIG"] = self.config_path

    def tearDown(self):
        self.tmpdir.cleanup()
        os.environ.pop("JBUSSDIEKER_CONFIG", None)

    @patch("jbussdieker.commit.cli.run_commit")
    def test_commit_command_success(self, mock_run_commit):
        buf = StringIO()
        with redirect_stdout(buf):
            main(["commit"])
        mock_run_commit.assert_called()

    @patch("jbussdieker.commit.cli.run_commit", side_effect=Exception("fail"))
    def test_commit_command_error(self, mock_run_commit):
        buf = StringIO()
        with redirect_stdout(buf):
            result = main(["commit"])
        self.assertEqual(result, 1)
        mock_run_commit.assert_called()


if __name__ == "__main__":
    unittest.main()
