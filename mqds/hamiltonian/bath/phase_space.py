"""Module containing classes used to describe baths."""

from enum import StrEnum, auto

import numpy as np

from .bath_base import BathBase
from .potentials import PotentialBase


class Distributions(StrEnum):
    """Different types of phase space distributions."""

    """Wigner Distribution."""
    WIGNER = auto()

    """Boltzmann Distribution."""
    BOLTZMANN = auto()


class BathMode:
    """A single mode in the bosonic environment."""

    def __init__(self, potential: PotentialBase, *, mass_au: float = 1.0) -> None:
        """Initialize a bath mode with a potential object and a mass. Assumes atomic units for both.

        Args:
            potential (PotentialBase): An instance of the potential energy object.
            mass_au (float): Mass of the mode in atomic units, defaults to 1.0.
        """
        self.potential = potential
        self.mass_au = mass_au

    def energy(self, *, position_au: float, momentum_au: float) -> float:
        """Return the total energy of a bath mode.

        Args:
            position_au:
            momentum_au:

        Returns:

        """
        return self.kinetic_energy(momentum_au=momentum_au) + self.potential_energy(
            position_au=position_au
        )

    def kinetic_energy(self, *, momentum_au: float) -> float:
        """Evaluate the kinetic energy. Assumes momentum is in atomic_units.

        Args:
            momentum_au (float): Momentum at which to evaluate the kinetic energy.

        Returns:
            float: The kinetic energy evaluated at momentum_au.
        """
        return momentum_au**2 / (2.0 * self.mass_au)

    def potential_energy(self, *, position_au: float) -> float:
        """Evaluate the potential energy at a given position. Assumes atomic units.

        Args:
            position_au (float): Position at which to evaluate the potential energy.

        Returns:
            float: The potential energy evaluated at position_au.
        """
        return self.potential.evaluate_potential(position=position_au)

    def force(self, *, position_au: float) -> float:
        """Evaluate the force on a bath mode at a given position. Assumes atomic units.

        Args:
            position_au (float): Position at which to evaluate the force.

        Returns:
            float: The force evaluated at position_au.
        """
        return -self.potential.evaluate_gradient(position=position_au)


class PhaseSpaceBath(BathBase):
    """Class for a bosonic bath described by a collection of modes.""" ""

    def __init__(self, modes: list[BathMode], distribution: Distributions) -> None:
        """Initialize a bath from a collection of bath modes.

        Args:
            modes (list[BathMode]): A list of modes to include in the bath.
        """
        self.modes = modes
        self.distribution = distribution
        self._positions = None
        self._momenta = None

    @classmethod
    def from_spectral_density(cls):
        msg = "Still have to decide on format for spectral density files."
        raise NotImplementedError(msg)

    @property
    def n_modes(self) -> int:
        """Number of modes in the phase space bath.

        Returns:
            int: Length of the modes list.
        """
        return len(self.modes)

    @property
    def initial_positions(self) -> int:
        return self._positions

    @property
    def initial_momenta(self) -> int:
        return self._momenta

    def initialize(
        self, temperature: float, n_traj: int, *, x_loc: float = 0.0, p_loc: float = 0.0
    ) -> None:
        sigma_x = 1.0 if self.distribution == Distributions.WIGNER else 2.0
        sigma_p = 1.0 if self.distribution == Distributions.WIGNER else 2.0
        self._positions = np.random.normal(
            loc=x_loc, scale=sigma_x, size=(n_traj, self.n_modes)
        )
        self._momenta = np.random.normal(
            loc=p_loc, scale=sigma_p, size=(n_traj, self.n_modes)
        )
