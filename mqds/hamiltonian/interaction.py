"""Methods for the system."""

import numpy as np


class InteractionBase:
    def value(self, **kwargs) -> np.ndarray:
        msg = "Not Implemented, will return the system-bath coupling at each order."
        raise NotImplementedError(msg)
