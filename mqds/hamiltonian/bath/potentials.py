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
