"""
AbstractSolution.py: Abstract class for solution of 1st Order Linear ODE
for pharmokinetic model
Authors: SABS R3 Group 2
20.10.2021
"""
from abc import ABC, abstractmethod


class AbstractSolution(ABC):
    @property
    @abstractmethod
    def get_solution(self):
        """Returns linear approximate solution of Model, computed with scipy ivp

        :raises NotImplementedError: Must be implemented by subclass
        """
        raise NotImplementedError("Abstract method")
