import unittest
import pkmodel as pk
from pkmodel.AbstractModel import AbstractModel


class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    def test_create(self):
        """
        Tests Model creation.
        """
        parameters = [{'name': 'test1',
                      'injection_type': 'subcutaneous',
                       'V_c': 1.0,
                       'nr_compartments': 1,
                       'periph_1': (5.0, 3.0),
                       'CL': 5.0,
                       'X': 6.0,
                       'dose_mode': 'normal',
                       'time': 1
                       },
                      {'name': 'test1',
                      'injection_type': 'intravenous',
                       'V_c': 1.0,
                       'nr_compartments': 3,
                       'periph_1': (5.0, 3.0),
                       'periph_2': (1.0, 4.7),
                       'periph_3': (6.0, 2.4),
                       'CL': 0,
                       'X': 1.6,
                       'dose_mode': 'normal',
                       'time': 1
                       }]
        expected_model = [{'name': 'test1',
                          'injection_type': 'subcutaneous',
                           'V_c': 1.0,
                           'nr_compartments': 1,
                           'periph_1': (5.0, 3.0),
                           'CL': 5.0,
                           'X': 6.0,
                           'dose_mode': 'normal',
                           'time': 1
                           },
                          {'name': 'test1',
                          'injection_type': 'intravenous',
                           'V_c': 1.0,
                           'nr_compartments': 3,
                           'periph_1': (5.0, 3.0),
                           'periph_2': (1.0, 4.7),
                           'periph_3': (6.0, 2.4),
                           'CL': 0,
                           'X': 1.6,
                           'dose_mode': 'normal',
                           'time': 1
                           }]
        for i in range(0, 1):
            model = pk.models.Model(parameters[i])
            self.assertEqual(model.parameters, expected_model[i])

    def test_generate_model(self):
        """
        Tests generate_model for 3 cases
        """
        parameters = {'name': 'test1',
                      'injection_type': 'subcutaneous',
                      'V_c': 1.0,
                      'nr_compartments': 1,
                      'periph_1': (5.0, 3.0),
                      'CL': 5.0,
                      'X': 6.0,
                      'dose_mode': 'normal',
                      'time': 1
                      }
        model = pk.models.Model(parameters)
        test_array = [[(1, 1), 1, 1], [(0, 0), 0, 0], [(5.2, 3.1), 2, 2.6]]
        expected_transition = [0, 0, 4.65]
        for i in range(0, 1):
            test = model.generate_transition(*test_array[i])
            self.assertEqual(test, expected_transition[i])

    def test_abstractmodel(self):
        AbstractModel.__abstractmethods__ = set()
        model = AbstractModel()
        with self.assertRaises(NotImplementedError):
            model.solve()
        # class Dummy(AbstractModel):
            # self.assertTrue(AbstractModel, NotImplementedError)

    # def test_abstractmodel(self):
        # with self.assertRaises(TypeError):
            # TestModel()


# class TestModel(AbstractModel):
    # def ___init___(self):
        # pass


if __name__ == '__main__':
    unittest.main()
