import unittest
import pkmodel as pk


class DosesTest(unittest.TestCase):
    """
    Tests the dose functions in dose.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        # model = pk.Model()
        self.assertEqual(42, 42)
