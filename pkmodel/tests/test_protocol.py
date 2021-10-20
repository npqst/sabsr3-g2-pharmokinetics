import unittest
# import pkmodel as pk


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    def test_fill_parameters(self):
        """
        Tests Protocol creation.
        """
        value = 4
        assert value, 4

