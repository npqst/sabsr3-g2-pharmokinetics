"""
AbstractModel.py: Abstract class for 1st Order Linear ODE for pharmokinetic
model
"""
from abc import ABC, abstractmethod

from .AbstractSolution import AbstractSolution


class AbstractModel(ABC):
    @abstractmethod
    def solve(self) -> AbstractSolution:
        """ Abstract class for 1st Order Linear ODE for pharmokinetic model

        :raises NotImplementedError:  Must be implemented by subclasses.
        """
        raise NotImplementedError("Abstract method")

