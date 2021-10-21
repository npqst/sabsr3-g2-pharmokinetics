import unittest
import pkmodel as pk


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    # def test_create(self):
    #     """
    #     Tests Protocol creation.
    #     """
    #     # model = pk.Protocol()
    #     self.assertEqual(43, 43)

    #     new_dict={}

    def test_generate_model(self):
        # from pkmodel.protocol import Protocol
        protocol = pk.Protocol('pkmodel/tests/testarray1.txt')
        with self.assertRaises(Exception) as context:
            protocol.generate_model()
        self.assertTrue('model type should be either'
                        ' intravenous or subcutaneous' in context.exception)
