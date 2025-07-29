import unittest
import logging
import sys

from jbussdieker.logging import setup_logging


class TestLogging(unittest.TestCase):
    def test_setup_logging(self):
        logger = logging.getLogger()
        dummy_handler = logging.StreamHandler()
        logger.addHandler(dummy_handler)
        self.assertIn(dummy_handler, logger.handlers)
        test_level = logging.WARNING
        test_format = "%(levelname)s: TEST: %(message)s"
        setup_logging(level=test_level, format=test_format)
        self.assertEqual(logger.level, test_level)
        self.assertNotIn(dummy_handler, logger.handlers)
        self.assertEqual(len(logger.handlers), 1)
        handler = logger.handlers[0]
        self.assertIsInstance(handler, logging.StreamHandler)
        self.assertIs(handler.stream, sys.stdout)
        self.assertEqual(handler.formatter._fmt, test_format)


if __name__ == "__main__":
    unittest.main()
