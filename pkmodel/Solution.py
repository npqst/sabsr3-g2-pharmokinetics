""""
Solution.py: Class implementation for Solution of 1st Order ODE for
pharmokinetic model
Authors: SABS R3 Group 2
20.10.2021
"""

from pkmodel.AbstractSolution import AbstractSolution


class Solution(AbstractSolution):
    """Solution

    :param AbstractSolution: [description]
    :type AbstractSolution: [type]
    """
    def __init__(self, solution_vector) -> None:
        """Initialise instance of Solution class with a solution vector
        generated by Model.

        :param solution_vector: x * t matrix where x is number of compartments
        and t is length of time vector
        :type solution_vector: array of float
        """
        self.__solution_vector = solution_vector

    @property
    def get_solution(self):
        """Return solution vector

        :return: x * t matrix where x is number of compartments and t is
        length of time vector
        :rtype: array of float
        """
        return self.__solution_vector