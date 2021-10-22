import unittest
import pkmodel as pk
import os


class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    """
    def generate_test_files(self):
        """ Run program to generate outputs from solution
        <-- its very difficult to self-contain solutions.py
        without creating an entire model module specifically for
        the tests. This is due to the solutions class calling
        a scipy.integrate object.

        :return: nill
        :output: plot + parameter file + solutions csv
        """

        protocol = pk.Protocol('pkmodel/tests/test_config_file.txt')
        model = protocol.generate_model()
        #solve model
        x = model.solve()
        #generate output from solved model
        x.output()

    def test_files_exist(self):

        self.generate_test_files()
        #test if plot exists in output directory (with correct naming)
        assert os.path.isfile('./Output/solutions_unittest_plot.png'), True
        #test if parameter file exists in output directory
        # <--(with correct naming)
        assert os.path.isfile('./Output/solutions_unittest_params.txt'), True
        #test if parameter file exists in output directory
        # <--(with correct naming)
        assert os.path.isfile('./Output/solutions_unittest_solution.csv'), True
