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
            'periph_default': (1.0, 1.0),
            'periph_1': (1.0, 1.0),
            'CL': 1.0,
            'X': 1.0,
            'dose_mode': 'normal',
            'nr_compartments': 1,
            'run_mode': 'save',
            'time': 1
        }
        self.assertEqual(filled_params, true_params)

    def test_inputs_CLX(self):
        """
        Tests exceptions for bad inputs for CL, X and Time
        """
        from pkmodel import Protocol
        for i in 'CL', 'X':
            error_dict = {-1: f'{i} should be at least 0',
                          'test': f'{i} should be a float'}
            for j in -1, 'test':
                protocol = Protocol()
                protocol.params[i] = j
                with self.assertRaises(Exception) as context:
                    protocol.call_all_checks()
                    self.assertTrue(error_dict[j] in context.exception)

    def test_inputs_periph(self):
        from pkmodel import Protocol
        protocol = Protocol()
        error_dict = {
            "test": 'periph_1 should be a tuple',
            (-1.0, 0.0): 'values associated with the peripheral \
                compartment 1 should be float',
            ("test", "test2"): 'values associated with \
                the peripheral compartment 1 should be larger than 0'
        }
        for j in "test", (-1.0, 0.0), ("test", "test2"):
            protocol.params['periph_1'] = j
            with self.assertRaises(Exception) as context:
                protocol.call_all_checks()
                self.assertTrue(error_dict[j] in context.exception)

    def test_inputs_int(self):
        from pkmodel import Protocol
        for i in 'nr_compartments', 'time':
            error_dict = {
                -1: f'{i} should be at least 0',
                3.0: f'{i} should be a integer',
                "string": f'{i} should be a integer'
            }
            for j in -1, 3.0, "string":
                protocol = Protocol()
                protocol.params[i] = j
                with self.assertRaises(Exception) as context:
                    protocol.call_all_checks()
                    self.assertTrue(error_dict[j] in context.exception)
            if i == 'time':
                protocol = Protocol()
                protocol.params[i] = 6
                with self.assertRaises(Exception) as context:
                    protocol.call_all_checks()
                    self.assertTrue('Time should not exceed \
                        a value of 5 hours' in context.exception)

    def test_inputs_strings(self):
        from pkmodel import Protocol
        for i in 'name', 'injection_type':
            protocol = Protocol()
            protocol.params[i] = 3.0
            with self.assertRaises(Exception) as context:
                protocol.call_all_checks()
                self.assertTrue(f'{i} should be a string' in context.exception)

    def test_input_dict(self):
        from pkmodel import Protocol
        protocol = Protocol()
        with self.assertRaises(Exception) as context:
            protocol.params = "string"
            protocol.call_all_checks()
            self.assertTrue('data input should \
                be a dictionary' in context.exception)

    def test_generate_model(self):
        from pkmodel import Protocol
        for i in 'random', 'intravenous', 'subcutaneous':
            protocol = Protocol()
            protocol.params['injection_type'] = i
            with self.assertRaises(Exception) as context:
                protocol.generatemodel()
                if i == 'random':
                    self.assertTrue('model type should be \
                        either intravenous or\
                             subcutaneous' in context.exception)
                else:
                    self.assertFalse('model type should be \
                        either intravenous or \
                            subcutaneous' in context.exception)


if __name__ == '__main__':
    unittest.main()

