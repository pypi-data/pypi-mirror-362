import unittest

import jbussdieker.cli


class TestJbussdieker(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(jbussdieker.cli))


if __name__ == "__main__":
    unittest.main()
