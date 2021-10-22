"""
AbstractProtocol.py: Abstract class for 1st Order Linear ODE for pharmokinetic
model
"""
from abc import ABC, abstractmethod

from pkmodel.AbstractModel import AbstractModel


class AbstractProtocol(ABC):
    @abstractmethod
    def generate_model(self) -> AbstractModel:
        """Generates 1st Order linear ODE pharmokinetic model from input
        arguments that define model protocol.

        :raises NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("Abstract method")
