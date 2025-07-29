import unittest

import jbussdieker.commit


class TestService(unittest.TestCase):
    def test_version(self):
        self.assertIn("__version__", dir(jbussdieker.commit))


if __name__ == "__main__":
    unittest.main()
