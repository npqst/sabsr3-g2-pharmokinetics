import unittest
import pkmodel as pk


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        parameters = {
         'name':'test1',
         'injection_type': 'subcutaneous',
         'V_c': 1.0,
         'nr_compartments':1,
         'periph_1': (5.0, 3.0),
         'CL': 5.0,
         'X': 6.0,
         'dose_mode': 'normal'  
        }
        model = pk.models.Model(parameters)
        expected_model = {
         'injection_type': 'subcutaneous',
         'V_c': 1.0,
         'nr_compartments': 1,
         'periph_1': (5.0, 3.0),
         'CL': 5.0,
         'X': 6.0,
         'dose_mode': 'normal'  
        }
        self.assertEqual(model, expected_model)

        # if __name__ == '__main__':
            # unittest.main()

    def test_generate_model(self):
        parameters = {
         'name' : 'test1',
         'injection_type': 'subcutaneous',
         'V_c': 1.0,
         'nr_compartments':1,
         'periph_1': (5.0, 3.0),
         'CL': 5.0,
         'X': 6.0,
         'dose_mode': 'normal'  
        }
        model = pk.models.Model(parameters)
        test_array = [[(1,1),1, 1],  [(5.2,3.1), 2, 2.6]]
        test = model.generate_transition(test_array)
        expected_transition = [0, 4.65]
        
if __name__ == '__main__':
            unittest.main()

