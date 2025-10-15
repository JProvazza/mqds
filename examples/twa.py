"""Example demonstrating the Truncated Wigner Approximation."""

import numpy as np

from mqds.dynamics import DynamicsParameters, LinearizedDynamics
from mqds.hamiltonian import bath, interaction, system


def my_function(
    input_array1: np.ndarray, input_array2: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    return input_array1, input_array2


dp = DynamicsParameters(temperature=300.0, runtime=10.0)
system = system.SystemBase()
interaction = interaction.InteractionBase()
bath = bath.PhaseSpaceBath(modes=[], distribution=bath.Distributions.WIGNER)
ld = LinearizedDynamics(
    system=system,
    bath=bath,
    interation=interaction,
    parameters=dp,
    system_callback=my_function,
)
ld.evolve()
print(ld.system_reporter.values)
