"""Modal comparison matrix operations."""

from collections.abc import Sequence
from typing import cast

import numpy as np
from numpy.typing import NDArray

from ..validation import ModalValidator


def calculate_mac_matrix(phi_1: np.ndarray, phi_2: np.ndarray) -> NDArray:
    """Calculate the MAC matrix between two sets of modeshapes.

    The Modal Assurance Criterion (MAC) matrix quantifies the correlation between
    all pairs of mode shapes from two sets. Each element (i,j) represents the MAC
    value between mode i from the first set and mode j from the second set.


    $$
        MAC_{ij} = \\frac{ |\\phi_{1i}^H \\phi_{2j}|^2 }{ (\\phi_{1i}^H \\phi_{1i})(\\phi_{2j}^H \\phi_{2j}) }
    $$

    Where:
    - $\\phi_{1i}$: i-th mode shape from first set
    - $\\phi_{2j}$: j-th mode shape from second set
    - $^H$: Hermitian transpose
    - $|...|$: Magnitude of complex number

    Parameters
    ----------
    phi_1 : np.ndarray
        First set of modeshapes [n_modes_1 x n_dof]
    phi_2 : np.ndarray
        Second set of modeshapes [n_modes_2 x n_dof]

    Returns
    -------
    NDArray
        MAC matrix [n_modes_1 x n_modes_2] with values between 0 and 1

    Raises
    ------
    ValueError
        If modeshapes have different shapes
    """
    ModalValidator.validate_pair(phi_1, phi_2)

    # discern between real and complex modes
    # numpy.vdot cannot be used here, since
    # "it should only be used for vectors."
    # https://numpy.org/doc/stable/reference/generated/numpy.vdot.html
    if np.iscomplexobj(phi_1) or np.iscomplexobj(phi_2):
        return cast(
            NDArray,
            np.square(
                np.abs(np.dot(phi_1, phi_2.conj().T))
                / (np.linalg.norm(phi_1, axis=1)[:, np.newaxis] * np.linalg.norm(phi_2, axis=1))
            ),
        )
    else:
        return cast(
            NDArray,
            np.square(
                np.abs(np.dot(phi_1, phi_2.T))
                / (np.linalg.norm(phi_1, axis=1)[:, np.newaxis] * np.linalg.norm(phi_2, axis=1))
            ),
        )


def calculate_mode_matching_matrix(
    frequencies_1: np.ndarray,
    modeshapes_1: np.ndarray,
    frequencies_2: np.ndarray,
    modeshapes_2: np.ndarray,
    modeshape_weight: float = 1.0,
) -> NDArray:
    """Calculate mode matching matrix considering frequency and MAC.

    Based on Simoen et al., 2014, "Dealing with uncertainty in model updating in damage assessment".
    The matching matrix combines frequency differences and MAC values to find corresponding modes
    between two sets. A lower value indicates a better match.


    $$
        M_{ij} = w(1 - MAC_{ij}) + |1 - f_{1i}/f_{2j}|
    $$

    Where:
    - $MAC_{ij}$: MAC value between modes i and j
    - $f_{1i}$: Frequency of mode i from first set
    - $f_{2j}$: Frequency of mode j from second set
    - $w$: Weight for modeshape contribution

    Parameters
    ----------
    frequencies_1 : np.ndarray
        Frequencies of first set [n_modes_1]
    modeshapes_1 : np.ndarray
        Modeshapes of first set [n_modes_1 x n_dof]
    frequencies_2 : np.ndarray
        Frequencies of second set [n_modes_2]
    modeshapes_2 : np.ndarray
        Modeshapes of second set [n_modes_2 x n_dof]
    modeshape_weight : float, optional
        Weight for modeshape contribution, by default 1.0

    Returns
    -------
    NDArray
        Matching matrix [n_modes_1 x n_modes_2] where lower values indicate better matches

    Raises
    ------
    ValueError
        If input arrays have incompatible shapes
    """
    mac_matrix = calculate_mac_matrix(modeshapes_1, modeshapes_2)
    freq_matrix = np.abs(1 - frequencies_1[:, np.newaxis] / frequencies_2[np.newaxis, :])

    return cast(NDArray, modeshape_weight * (1 - mac_matrix) + freq_matrix)


def match_modes(match_matrix: np.ndarray, threshold: float = 0.6) -> tuple[Sequence[int], Sequence[int]]:
    """Find best matching modes using matching matrix.

    This function finds pairs of modes that best match based on the matching matrix.
    It uses a greedy approach to find the best matches below the specified threshold.
    Each mode can only be matched once.

    Parameters
    ----------
    match_matrix : np.ndarray
        Matching matrix [n_modes_1 x n_modes_2] where lower values indicate better matches
    threshold : float, optional
        Threshold for acceptable matches, by default 0.6

    Returns
    -------
    Tuple[Sequence[int], Sequence[int]]
        Indices of matching modes from first and second set

    Raises
    ------
    ValueError
        If matrix contains non-positive values or is not 2D
    """
    if not np.all(match_matrix > 0.0):
        raise ValueError("All matrix values must be positive")
    if match_matrix.ndim != 2:
        raise ValueError("Matrix must be 2D")

    n_modes_1, n_modes_2 = match_matrix.shape
    n_modes_min = min(n_modes_1, n_modes_2)

    _match_matrix = match_matrix.copy()
    matching_modes_1 = []
    matching_modes_2 = []

    for _ in range(n_modes_min):
        match = best_match(_match_matrix, threshold)
        if match is None:
            break

        matching_modes_1.append(match[0])
        matching_modes_2.append(match[1])

        # Mark matched modes
        _match_matrix[match[0], :] = threshold + 1.0
        _match_matrix[:, match[1]] = threshold + 1.0

    return tuple(matching_modes_1), tuple(matching_modes_2)


def best_match(match_matrix: np.ndarray, threshold: float = 0.6) -> tuple[int, int] | None:
    """Find indices of best matching mode below threshold.

    This function finds the pair of modes with the lowest matching value that is
    still below the specified threshold. It is used internally by match_modes.

    Parameters
    ----------
    match_matrix : np.ndarray
        Matching matrix [n_modes_1 x n_modes_2] where lower values indicate better matches
    threshold : float, optional
        Threshold for acceptable matches, by default 0.6

    Returns
    -------
    Optional[Tuple[int, int]]
        Indices of best match, or None if no match below threshold

    Raises
    ------
    ValueError
        If matrix contains non-positive values or is not 2D
    """
    if not np.all(match_matrix > 0.0):
        raise ValueError("All matrix values must be positive")
    if match_matrix.ndim != 2:
        raise ValueError("Matrix must be 2D")

    if not np.any(match_matrix <= threshold):
        return None

    indices = np.unravel_index(np.argmin(match_matrix, axis=None), match_matrix.shape)
    return (int(indices[0]), int(indices[1]))
