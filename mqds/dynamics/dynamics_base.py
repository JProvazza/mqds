from abc import ABC, abstractmethod
from dataclasses import dataclass

from mqds.hamiltonian.bath.bath_base import BathBase
from mqds.hamiltonian.interaction import InteractionBase
from mqds.hamiltonian.system import SystemBase


@dataclass
class DynamicsParameters:
    """Parameters that are necessary for running dynamics simulations."""

    runtime: float
    temperature: float


class DynamicsBase(ABC):
    def __init__(
        self,
        system: SystemBase,
        bath: BathBase,
        interation: InteractionBase,
        parameters: DynamicsParameters,
    ) -> None:
        self.system = system
        self.bath = bath
        self.interaction = interation
        self.parameters = parameters

    @abstractmethod
    def evolve(self, **kwargs) -> None:
        pass
