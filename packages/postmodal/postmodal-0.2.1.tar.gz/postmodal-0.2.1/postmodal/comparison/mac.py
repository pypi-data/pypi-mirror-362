"""Modal Assurance Criterion (MAC) calculation module."""

import numpy as np

from ..validation import ModalValidator


def calculate_mac(phi_1: np.ndarray, phi_2: np.ndarray) -> float:
    """Calculate the MAC value of two (complex) modeshape vectors.

    The Modal Assurance Criterion (MAC) is a measure of the correlation between
    two mode shapes. A MAC value close to 1 indicates strong correlation between
    the mode shapes, while a value close to 0 indicates weak correlation.

    $$
        MAC = \\frac{ |\\phi_1^H \\phi_2|^2 }{ (\\phi_1^H \\phi_1)(\\phi_2^H \\phi_2) }
    $$

    Where:
    - $\\phi_1, \\phi_2$: Complex mode shape vectors
    - $^H$: Hermitian transpose
    - $|...|$: Magnitude of complex number

    Parameters
    ----------
    phi_1 : np.ndarray
        First modeshape vector [n_dof]
    phi_2 : np.ndarray
        Second modeshape vector [n_dof]

    Returns
    -------
    float
        MAC value between 0 and 1

    Raises
    ------
    ValueError
        If modeshapes have different shapes
    """
    ModalValidator.validate_pair(phi_1, phi_2)

    numerator = np.abs(np.vdot(phi_1, phi_2)) ** 2
    denominator = np.vdot(phi_1, phi_1) * np.vdot(phi_2, phi_2)
    return float((numerator / denominator).real)
