import unittest

import %%PROJECT_NAME%%


class TestPackage(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(%%PROJECT_NAME%%))


if __name__ == "__main__":
    unittest.main()
