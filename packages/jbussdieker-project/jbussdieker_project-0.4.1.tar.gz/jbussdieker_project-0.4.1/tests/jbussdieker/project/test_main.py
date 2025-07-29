import unittest

import jbussdieker.project


class TestService(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(jbussdieker.project))


if __name__ == "__main__":
    unittest.main()
