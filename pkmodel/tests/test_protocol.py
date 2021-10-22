import unittest


class ProtocolTest(unittest.TestCase):
    """
    Tests the :class:`Protocol` class.
    """
    def test_read_config_file(self):
        """
        Test read_config_file function.
        """
        from pkmodel import Protocol
        # Will initialise Protocol with default parameters
        # but will not interfere with the test
        protocol = Protocol()
        test_dict = protocol.read_config('pkmodel/tests/testarray1.txt')
        true_dict = {
            'name': 'model_test_1',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'nr_compartments': 1,
            'periph_1': (5.0, 3.0),
            'CL': 5.0,
            'X': 6.0,
        }
        self.assertEqual(test_dict, true_dict)
        test_dict_repeat = protocol.read_config('pkmodel/tests/testarray2.txt')
        true_dict_repeat = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
        }
        self.assertEqual(test_dict_repeat, true_dict_repeat)

    def test_fill_parameters(self):
        """
        Test fill_parameters function.
        """
        from pkmodel import Protocol
        protocol = Protocol('pkmodel/tests/testarray2.txt')
        filled_params = protocol.params
        true_params = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
        }
        self.assertEqual(filled_params, true_params)

if __name__ == '__main__':
    unittest.main()

