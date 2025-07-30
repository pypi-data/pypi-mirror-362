"""Complex to real modeshape conversion utilities."""

import numpy as np

from postmodal.manipulation.phase import align_phase


def complex_to_real(
    modeshape: np.ndarray,
    method: str = "phase",
    reference_dof: int | None = None,
) -> np.ndarray:
    """Convert a complex modeshape to a real-valued modeshape.

    This function converts a complex modeshape to a real-valued modeshape
    using one of several methods:
    - "phase": Use the real part of the phase-aligned modeshape
    - "magnitude": Use the magnitude with sign from real part
    - "projection": Project onto the real axis

    Parameters
    ----------
    modeshape : np.ndarray
        Complex modeshape array [n_dof]
    method : str, optional
        Conversion method, by default "phase"
    reference_dof : Optional[int], optional
        Index of the reference DOF for phase alignment, by default None

    Returns
    -------
    np.ndarray
        Real-valued modeshape [n_dof]

    Raises
    ------
    ValueError
        If method is not one of ["phase", "magnitude", "projection"]
    """
    if method not in ["phase", "magnitude", "projection"]:
        raise ValueError('method must be one of ["phase", "magnitude", "projection"]')

    if method == "phase":
        # Align phase and take real part
        aligned = align_phase(modeshape, reference_dof)
        return np.real(aligned)

    elif method == "magnitude":
        # Use magnitude with sign from real part
        magnitude = np.abs(modeshape)
        sign = np.sign(np.real(modeshape))
        return np.array(magnitude * sign)

    else:  # projection
        # Project onto real axis
        return np.real(modeshape)


def complex_to_real_batch(
    modeshapes: np.ndarray,
    method: str = "phase",
    reference_dof: int | None = None,
) -> np.ndarray:
    """Convert a batch of complex modeshapes to real-valued modeshapes.

    This function converts multiple complex modeshapes to real-valued modeshapes
    using the specified method.

    Parameters
    ----------
    modeshapes : np.ndarray
        Array of complex modeshapes [n_modes x n_dof]
    method : str, optional
        Conversion method, by default "phase"
    reference_dof : Optional[int], optional
        Index of the reference DOF for phase alignment, by default None

    Returns
    -------
    np.ndarray
        Array of real-valued modeshapes [n_modes x n_dof]

    See Also
    --------
    complex_to_real : Convert a single complex modeshape
    """
    # Explicitly cast the result to np.ndarray to satisfy the return type
    return np.array([complex_to_real(phi, method, reference_dof) for phi in modeshapes])


def calculate_conversion_error(
    complex_modeshape: np.ndarray,
    real_modeshape: np.ndarray,
) -> tuple[float, float]:
    """Calculate the error between complex and real modeshapes.

    This function computes two error metrics:
    1. Magnitude error: Relative difference in magnitudes
    2. Phase error: Average absolute phase difference

    Parameters
    ----------
    complex_modeshape : np.ndarray
        Original complex modeshape [n_dof]
    real_modeshape : np.ndarray
        Converted real modeshape [n_dof]

    Returns
    -------
    tuple[float, float]
        Tuple containing (magnitude_error, phase_error)
        - magnitude_error: Relative difference in magnitudes
        - phase_error: Average absolute phase difference in radians
    """
    # Calculate magnitude error
    complex_mag = np.abs(complex_modeshape)
    real_mag = np.abs(real_modeshape)
    magnitude_error = np.mean(np.abs(complex_mag - real_mag) / complex_mag)

    # Calculate phase error
    complex_phase = np.angle(complex_modeshape)
    real_phase = np.angle(real_modeshape)
    phase_error = np.mean(np.abs(complex_phase - real_phase))

    return magnitude_error, phase_error


def optimize_conversion(
    modeshape: np.ndarray,
    method: str = "phase",
    reference_dof: int | None = None,
) -> tuple[np.ndarray, float, float]:
    """Optimize the conversion of a complex modeshape to real.

    This function finds the optimal real-valued modeshape by minimizing
    the conversion error. It tries different reference DOFs and returns
    the one with the smallest error.

    Parameters
    ----------
    modeshape : np.ndarray
        Complex modeshape array [n_dof]
    method : str, optional
        Conversion method, by default "phase"
    reference_dof : Optional[int], optional
        Initial reference DOF to try, by default None

    Returns
    -------
    tuple[np.ndarray, float, float]
        Tuple containing (optimal_modeshape, magnitude_error, phase_error)
        - optimal_modeshape: Best real-valued modeshape
        - magnitude_error: Magnitude error for optimal conversion
        - phase_error: Phase error for optimal conversion
    """
    n_dof = len(modeshape)
    best_error = float("inf")
    # Initialize with a default value to ensure we never return None
    best_modeshape = complex_to_real(modeshape, method, reference_dof)
    best_mag_error = 0.0
    best_phase_error = 0.0

    # Try each DOF as reference
    for ref in range(n_dof):
        real_phi = complex_to_real(modeshape, method, ref)
        mag_error, phase_error = calculate_conversion_error(modeshape, real_phi)
        total_error = mag_error + phase_error

        if total_error < best_error:
            best_error = total_error
            best_modeshape = real_phi
            best_mag_error = mag_error
            best_phase_error = phase_error

    return best_modeshape, best_mag_error, best_phase_error
