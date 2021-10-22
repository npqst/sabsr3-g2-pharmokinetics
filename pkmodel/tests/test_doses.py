import unittest
from pkmodel.dose import (select_dose, unit_fn_dose,
                          pulse_series_dose, zero_dose)
import numpy as np


class DosesTest(unittest.TestCase):
    """
    Tests the dose functions in dose.
    """
    def test_select_dose(self):
        for key in ['normal', 'pulse', 'zero']:
            dose_fn = select_dose(key)
            self.assertTrue(callable(dose_fn))
        with self.assertRaises(Exception):
            select_dose('false_key')

    def test_unit_fn_dose(self):
        for i in range(10):
            x, t = np.random.uniform(0, 100, (2))
            self.assertEqual(x, unit_fn_dose(t, x))

    def test_zero_dose(self):
        for i in range(10):
            x, t = np.random.uniform(0, 100, (2))
            self.assertEqual(0., zero_dose(t, x))

    def test_pulse_series_dose(self):
        pulse_width = 0.5
        interval = 1.
        X1 = 2.
        X2 = 3.
        self.assertEqual(X1, pulse_series_dose(0.,
                                               X1,
                                               X2=X2,
                                               pulse_width=pulse_width,
                                               interval=interval))
        self.assertEqual(X2, pulse_series_dose(0.6,
                                               X1,
                                               X2=X2,
                                               pulse_width=pulse_width,
                                               interval=interval))
        self.assertEqual(X1, pulse_series_dose(1.6,
                                               X1,
                                               X2=X2,
                                               pulse_width=pulse_width,
                                               interval=interval))



