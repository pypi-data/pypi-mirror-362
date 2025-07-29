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


if __name__ == "__main__":
    unittest.main()
