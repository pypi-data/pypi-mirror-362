"""Utilities used in the package"""

import numpy as np


def set_rng(rng: np.random.Generator | None) -> np.random.Generator:
    """Sets the random number generator"""
    if rng is None:
        out = np.random.default_rng()
    else:
        out = rng
    return out
