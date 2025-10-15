from enum import StrEnum, auto

import numpy as np

LIGHT = 2.99792458e10  # In cm/s
PLANCK = 6.626068e-34
AVOGADRO = 6.0221415e23
HBAR = PLANCK / 2.0 / np.pi
AU_TIME_TO_SECONDS = 2.418884326505e-17
AU_TO_ANGSTROM = 0.52917725
AMU_TO_ELECTRON_REST_MASS = 1822.4032318265


class Units(StrEnum):
    """Enum for units."""

    """Wavenumbers."""
    WAVENUMBERS = auto()

    """Hartrees."""
    HARTREES = auto()

    """Atomic units of angular frequency."""
    AU_ANG_FREQ = auto()

    """Atomic units of time."""
    AU_TIME = auto()

    """Femtoseconds."""
    FEMTOSECONDS = auto()


_conversion_factor = {
    ("fs", "au_time"): 1.0e-15 / AU_TIME_TO_SECONDS,
    ("wvnbr", "au_ang_freq"): LIGHT / (1.0 / AU_TIME_TO_SECONDS) * 2.0 * np.pi,
    ("wvnbr", "hz_ang"): LIGHT * 2.0 * np.pi,
    ("s", "fs"): 1.0e15,
    ("bohr", "angstrom"): 0.529177249,
    ("amu", "au_mass"): AMU_TO_ELECTRON_REST_MASS,
}
