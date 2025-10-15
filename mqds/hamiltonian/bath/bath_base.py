from abc import ABC, abstractmethod


class BathBase(ABC):
    @abstractmethod
    def initialize(self, **kwargs) -> None:
        msg = "Initialization method not defined"
        raise NotImplementedError(msg)
