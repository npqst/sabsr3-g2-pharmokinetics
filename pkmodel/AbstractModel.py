"""
AbstractModel.py: Abstract class for 1st Order Linear ODE for pharmokinetic
model
Authors: SABS R3 Group 2
20.10.2021
"""
from abc import ABC, abstractmethod

from .AbstractSolution import AbstractSolution


class AbstractModel(ABC):
    @abstractmethod
    def solve(self) -> AbstractSolution:
        """ Abstract class for 1st Order Linear ODE for pharmokinetic model

        :raises NotImplementedError: [description]
        """
        raise NotImplementedError("Abstract method")

