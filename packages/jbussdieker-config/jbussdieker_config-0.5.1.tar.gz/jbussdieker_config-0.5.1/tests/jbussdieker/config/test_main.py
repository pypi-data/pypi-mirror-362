import unittest

import jbussdieker.config


class TestService(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(jbussdieker.config))


if __name__ == "__main__":
    unittest.main()
