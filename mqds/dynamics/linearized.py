"""Linearized Dynamics."""

from typing import Callable

import numpy as np
from _mqds import linearized_dynamics

from mqds.hamiltonian.bath.bath_base import BathBase
from mqds.hamiltonian.interaction import InteractionBase
from mqds.hamiltonian.system import SystemBase

from .dynamics_base import DynamicsBase, DynamicsParameters


class LinearizedDynamics(DynamicsBase):
    """Run linearized phase space quantum dynamics"""

    def __init__(
        self,
        system: SystemBase,
        bath: BathBase,
        interation: InteractionBase,
        parameters: DynamicsParameters,
        system_callback: Callable,
    ) -> None:
        self.system_reporter = SystemReporter(func=system_callback)
        super().__init__(
            system=system, bath=bath, interation=interation, parameters=parameters
        )

    def evolve(self, **kwargs) -> None:
        linearized_dynamics(
            np.ones(3),
            np.ones(3),
            np.ones(2),
            np.ones(2),
            1e-3,
            10,
            2,
            10,
            np.ones((2, 2)),
            self.system_reporter,
        )


class SystemReporter:
    def __init__(self, func: Callable):
        self.func = func
        self.values = []

    def __call__(self, x_bath: np.ndarray, p_bath: np.ndarray):
        self.values.append(self.func(x_bath, p_bath))
