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
            'periph_1': (1.0, 1.0),
            'CL': 1.0,
            'X': 1.0,
            'dose_mode': 'normal',
            'nr_compartments': 1,
            'save_mode': 'save',
            'time': 1.0         
        }
        self.assertEqual(filled_params, true_params)

    def test_inputs_CLXTime(self):
        """
        Tests exceptions for bad inputs for CL, X and Time 
        """
        from pkmodel import Protocol
        protocol = Protocol()
        test_dictionary = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'periph_1': (1.0, 1.0),
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
        }
        for i in 'CL', 'X', 'Time':
            error_dict = {-1: f'{i} should be at least 0', 'test': f'{i} should be a float'}
            for j in -1, 'test':
                test_dictionaryCLXTime = test_dictionary.copy()
                test_dictionaryCLXTime[i] = j
                with self.assertRaises(Exception) as context:
                    protocol.fill_parameters(test_dictionaryCLXTime)
                    self.assertTrue(error_dict[j] in context.exception)

    def test_inputs_periph(self):
        from pkmodel import Protocol
        protocol = Protocol()
        test_dictionary = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'periph_1': (2.0, 3.0),
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
        }
        error_dict = {
            "test": 'periph_1 should be a tuple', 
            (-1.0, 0.0): 'values associated with the peripheral compartment 1 should be float',
            ("test", "test2"): 'values associated with the peripheral compartment 1 should be larger than 0'
            }
        for j in "test", (-1.0, 0.0), ("test", "test2"):
            test_dictionaryPeriph = test_dictionary.copy()
            test_dictionaryPeriph['periph_1'] = j
            with self.assertRaises(Exception) as context:
                protocol.fill_parameters(test_dictionaryPeriph)
                self.assertTrue(error_dict[j] in context.exception)

    def test_inputs_nr_compartments(self):
        from pkmodel import Protocol
        protocol = Protocol()
        test_dictionary = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'periph_1': (2.0, 3.0),
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 3,          # nr of peripheral compartments
        }
        error_dict = {
            -1: 'nr_compartments should be at least 0', 
            3.0: 'nr_compartments should be a integer',
            "string": 'nr_compartments should be a integer'
            }
        for j in -1, 3.0, "string":
            test_dictionaryCmpt = test_dictionary.copy()
            test_dictionaryCmpt['nr_compartments'] = j
            with self.assertRaises(Exception) as context:
                protocol.fill_parameters(test_dictionaryCmpt)
                self.assertTrue(error_dict[j] in context.exception)
    
    def test_inputs_strings(self):
        from pkmodel import Protocol
        protocol = Protocol()
        test_dictionary = {
            'name': 'model_test_2',
            'injection_type': 'intravenous',
            'V_c': 2.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'periph_1': (2.0, 3.0),
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 3,          # nr of peripheral compartments
        }
        for i in 'name', 'injection_type':
            test_dictionaryCmpt = test_dictionary.copy()
            test_dictionaryCmpt['nr_compartments'] = 3.0
            with self.assertRaises(Exception) as context:
                protocol.fill_parameters(test_dictionaryCmpt)
                self.assertTrue(f'{i} should be a string' in context.exception)

    def test_input_dict(self):
        from pkmodel import Protocol
        protocol = Protocol()
        with self.assertRaises(Exception) as context:
                protocol.fill_parameters("string")
                self.assertTrue('data input should \
                    be a dictionary' in context.exception)





if __name__ == '__main__':
    unittest.main()

