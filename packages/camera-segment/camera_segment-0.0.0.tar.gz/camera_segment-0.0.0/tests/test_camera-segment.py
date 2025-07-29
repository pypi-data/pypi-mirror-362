import unittest

import camera-segment


class TestPackage(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(camera-segment))


if __name__ == "__main__":
    unittest.main()
