"""Methods for the system."""

from enum import StrEnum, auto


class SystemBasis(StrEnum):
    """Bases for the discrete subsystem."""

    """Site basis"""
    SITE = auto()

    """Eigenstate basis"""
    EIGENSTATE = auto()


class SystemBase:
    def __init__(self, basis: SystemBasis = SystemBasis.SITE):
        self.basis = basis
