"""Module containing classes used to describe baths."""

from abc import ABC, abstractmethod

import numpy as np


class PotentialBase(ABC):
    """Abstract base class for potentials."""

    @abstractmethod
    def evaluate_potential(self, position: float) -> float:
        pass

    @abstractmethod
    def evaluate_gradient(self, position: float) -> float:
        pass


class PolynomialPotential(PotentialBase):
    """Polynomial potentials."""

    def __init__(self, coefficients: list[float] | np.ndarray) -> None:
        self.coefficients = np.asarray(coefficients, dtype=float)

    @staticmethod
    def _evaluate_polynomial(coefficients: np.ndarray, position: float) -> float:
        return np.sum([position**i * c for i, c in enumerate(coefficients)])

    @property
    def gradient_coefficients(self) -> np.ndarray:
        return np.array(
            [(i + 1) * coeff for i, coeff in enumerate(self.coefficients[1:])]
        )

    def evaluate_potential(self, position: float) -> float:
        return self._evaluate_polynomial(self.coefficients, position)

    def evaluate_gradient(self, position: float) -> float:
        return self._evaluate_polynomial(self.gradient_coefficients, position)


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


class Bath:
    """Class for a bosonic bath described by a collection of modes.""" ""

    def __init__(self, modes: list[BathMode]) -> None:
        """Initialize a bath from a collection of bath modes.

        Args:
            modes (list[BathMode]): A list of modes to include in the bath.
        """
        self.modes = modes
