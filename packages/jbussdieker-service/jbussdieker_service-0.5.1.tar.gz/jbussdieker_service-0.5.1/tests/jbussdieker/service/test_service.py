import unittest

import jbussdieker.service


class TestService(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(jbussdieker.service))


if __name__ == "__main__":
    unittest.main()
