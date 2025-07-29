import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from camera_segment.cli import main


class TestCLI(unittest.TestCase):
    def test_version_output(self):
        buf = StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                main(["version"])
        output = buf.getvalue()
        self.assertIn("camera-segment: v", output)

    def test_no_arguments_prints_usage(self):
        fake_ep = MagicMock()
        fake_ep.name = "version"
        with patch("importlib.metadata.entry_points", return_value=[fake_ep]):
            buf = StringIO()
            with patch("sys.argv", ["camera-segment"]):
                with redirect_stdout(buf):
                    with self.assertRaises(SystemExit) as cm:
                        main(None)
            output = buf.getvalue()
        self.assertIn("Usage: camera-segment <command> [options]", output)
        self.assertIn("Available commands:", output)
        self.assertIn("version", output)
        self.assertEqual(cm.exception.code, 1)

    def test_unknown_command_prints_error(self):
        fake_ep = MagicMock()
        fake_ep.name = "version"
        with patch("importlib.metadata.entry_points", return_value=[fake_ep]):
            buf = StringIO()
            with redirect_stdout(buf):
                with self.assertRaises(SystemExit) as cm:
                    main(["notacommand"])
            output = buf.getvalue()
        self.assertIn("Unknown command: notacommand", output)
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
