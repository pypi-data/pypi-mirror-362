"""Functions for calculating modal complexity metrics."""

import numpy as np

from .types import ComplexityMetrics
from .validation import ModalValidator


def _calculate_mpc_old(mode: np.ndarray) -> float:
    """Calculate MPC using the original implementation."""
    mode_centered = mode - np.mean(mode)
    real_part = mode_centered.real
    imag_part = mode_centered.imag
    real_norm_sq = np.sum(real_part**2)
    imag_norm_sq = np.sum(imag_part**2)

    if imag_norm_sq < 1e-10:
        return 1.0

    real_imag_product = np.sum(real_part * imag_part)
    if abs(real_imag_product**2 - real_norm_sq * imag_norm_sq) < 1e-10:
        return 1.0

    epsilon_mpc = (imag_norm_sq - real_norm_sq) / (2 * real_imag_product)
    theta_mpc = np.arctan(abs(epsilon_mpc) + np.sign(epsilon_mpc) * np.sqrt(1 + epsilon_mpc**2))
    sin_sq = np.sin(theta_mpc) ** 2
    numerator_term = real_norm_sq + (1 / epsilon_mpc) * real_imag_product * (2 * (epsilon_mpc**2 + 1) * sin_sq - 1)

    if abs(real_norm_sq + imag_norm_sq) < 1e-10:
        return 0.0

    return float(numerator_term / (real_norm_sq + imag_norm_sq))


def _calculate_mpc_eigvals(mode: np.ndarray) -> float:
    """Calculate MPC using eigenvalue decomposition."""
    real_part = mode.real
    imag_part = mode.imag
    Sxx = np.sum(real_part**2)
    Syy = np.sum(imag_part**2)
    Sxy = np.sum(real_part * imag_part)
    A = np.array([[Sxx, Sxy], [Sxy, Syy]])
    eigvals = np.linalg.eigvals(A)
    lambda_1, lambda_2 = max(eigvals), min(eigvals)
    return float((lambda_1 - lambda_2) ** 2 / (lambda_1 + lambda_2) ** 2)


def _calculate_mpc_mac(mode: np.ndarray) -> float:
    """Calculate MPC using MAC formula."""
    real_part = mode.real
    imag_part = mode.imag
    Sxx = np.sum(real_part**2)
    Syy = np.sum(imag_part**2)
    Sxy = np.sum(real_part * imag_part)
    return float(((Sxx - Syy) ** 2 + 4 * Sxy**2) / ((Sxx + Syy) ** 2))


def calculate_mpc(modeshape: np.ndarray, method: str = "mac") -> np.ndarray:
    """Calculate Modal Phase Collinearity (MPC) for a modeshape or set of modeshapes.

    MPC quantifies the 'realness' of a mode shape by measuring the phase alignment
    of its components. A higher MPC value (≈ 1) indicates a more 'real' mode shape
    with phases close to 0° or 180°, suggesting proportionally damped or undamped behavior.
    A lower MPC value (≈ 0) suggests a more complex mode shape with scattered phases,
    indicating non-proportional damping or mode coupling.


    $$
        MPC(\\phi_j) = \\frac{||Re(\\tilde{\\phi}_j)||_2^2 + ||Im(\\tilde{\\phi}_j)||_2^2}
        {||Re(\\tilde{\\phi}_j)||_2^2 + \\epsilon_{MPC}^{-1} Re(\\tilde{\\phi}_j^T)Im(\\tilde{\\phi}_j)
        (2(\\epsilon_{MPC}^2 + 1)\\sin^2(\\theta_{MPC}) - 1)}
    $$


    Where:
    - $\\tilde{\\phi}_j$: Centered mode shape
    - $\\epsilon_{MPC}$: MPC epsilon parameter
    - $\\theta_{MPC}$: MPC angle parameter
    - $||...||_2^2$: Squared L2 norm

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.
    method : str, optional
        Method to use for MPC calculation:
        - "old": Original implementation using epsilon and theta parameters
        - "eigenvalue": Implementation using eigenvalue decomposition
        - "mac": Implementation using Modal Assurance Criterion formula (default)

    Returns
    -------
    np.ndarray
        MPC value(s).
        - Scalar if input is a single modeshape [].
        - 1D array [n_modes] if input is a set of modeshapes.

    Raises
    ------
    ValueError
        If the input `modeshape` is not a NumPy array or if method is invalid.
    NotImplementedError
        If the input `modeshape` has dimensions other than 1 or 2.
    """
    ModalValidator.validate(modeshape)

    if method not in ["old", "eigenvalue", "mac"]:
        raise ValueError('method must be one of "old", "eigenvalue", or "mac"')

    calculate_single_mpc = {
        "old": _calculate_mpc_old,
        "eigenvalue": _calculate_mpc_eigvals,
        "mac": _calculate_mpc_mac,
    }[method]

    if modeshape.ndim == 1:
        return np.array(calculate_single_mpc(modeshape))
    elif modeshape.ndim == 2:
        return np.array([calculate_single_mpc(mode) for mode in modeshape])
    else:
        raise NotImplementedError(f"modeshape has dimensions: {modeshape.ndim}, expecting 1 or 2.")


def calculate_map(modeshape: np.ndarray) -> np.ndarray:
    """Calculate Modal Amplitude Proportionality (MAP) for a modeshape or set of modeshapes.

    MAP assesses the amplitude proportionality of a complex mode shape.
    A higher MAP value (≈ 1) indicates that the mode shape amplitudes are largely
    proportional to their real parts, suggesting a more 'real' amplitude distribution.
    A lower MAP value (< 1) indicates a deviation from real amplitude proportionality,
    suggesting a more complex amplitude distribution and significant imaginary components.


    $$
        MAP_r = \\frac{ \\sum_{j=1}^{n} |Re(\\Phi_{jr})| }{ \\sum_{j=1}^{n} |\\Phi_{jr}| }
    $$

    Where:
    - $\\Phi_{jr}$: j-th component of the r-th complex mode shape.
    - $Re(\\Phi_{jr})$: Real part of $\\Phi_{jr}$.
    - $n$: Number of DOFs.
    - $| ... |$: Magnitude (absolute value for scalar, modulus for complex).

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.

    Returns
    -------
    np.ndarray
        MAP value(s).
        - Scalar if input is a single modeshape [].
        - 1D array [n_modes] if input is a set of modeshapes.

    Raises
    ------
    ValueError
        If the input `modeshape` is not a NumPy array.
    NotImplementedError
        If the input `modeshape` has dimensions other than 1 or 2.
    """
    ModalValidator.validate(modeshape)

    if modeshape.ndim == 1:
        numerator = np.sum(np.abs(modeshape.real))
        denominator = np.sum(np.abs(modeshape))
        map_value = numerator / denominator if denominator != 0 else 0.0  # Handle potential division by zero
        return np.array(map_value)  # Return as 0D array for consistency

    elif modeshape.ndim == 2:
        map_values = []
        for mode in modeshape:
            numerator = np.sum(np.abs(mode.real))
            denominator = np.sum(np.abs(mode))
            map_value = numerator / denominator if denominator != 0 else 0.0  # Handle potential division by zero
            map_values.append(map_value)
        return np.array(map_values)

    else:
        raise NotImplementedError(f"modeshape has dimensions: {modeshape.ndim}, expecting 1 or 2.")


def calculate_mpd(modeshape: np.ndarray, weights: str = "magnitude") -> np.ndarray:
    """Calculate Mean Phase Deviation (MPD) for a modeshape or set of modeshapes.

    MPD quantifies the phase scatter within a mode shape by measuring the weighted average
    of phase deviations from the mean phase angle. The mean phase is determined by solving
    a total least squares problem using SVD to find the best straight line fit through
    the mode shape in the complex plane.


    $$
        MP(\\phi_j) = \\arctan\\left(\\frac{-V_{12}}{V_{22}}\\right)

        MPD(\\phi_j) = \\frac{\\sum_{o=1}^{n_y} w_o \\arccos\\left|\\frac{Re(\\phi_{jo})V_{22} - Im(\\phi_{jo})V_{12}}{\\sqrt{V_{12}^2 + V_{22}^2}|\\phi_{jo}|}\\right|}{\\sum_{o=1}^{n_y} w_o}
    $$

    Where:
    - $MP(\\phi_j)$: Mean phase angle determined by SVD
    - $V_{12}, V_{22}$: Elements of the V matrix from SVD of [Re(φj) Im(φj)]
    - $w_o$: Weighting factors (either |φjo| or 1 for equal weights)
    - $\\phi_{jo}$: Complex mode shape components
    - $n_y$: Number of DOFs

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.
    weights : str, optional
        Weighting scheme for phase deviations:
        - "magnitude": weights are the magnitude of each mode shape component (default)
        - "equal": equal weights for all components

    Returns
    -------
    np.ndarray
        MPD value(s) in degrees.
        - Scalar if input is a single modeshape [].
        - 1D array [n_modes] if input is a set of modeshapes.

    Raises
    ------
    TypeError
        If the input `modeshape` is not a NumPy array.
    NotImplementedError
        If the input `modeshape` has dimensions other than 1 or 2.
    ValueError
        If `weights` is not one of "magnitude" or "equal".
    """
    if not isinstance(modeshape, np.ndarray):
        raise TypeError("Input modeshape must be a NumPy array.")

    if weights not in ["magnitude", "equal"]:
        raise ValueError('weights must be either "magnitude" or "equal"')

    def calculate_single_mpd(mode: np.ndarray) -> float:
        # Form matrix with real and imaginary parts
        A = np.column_stack((mode.real, mode.imag))

        # Compute SVD
        U, S, Vh = np.linalg.svd(A)
        V = Vh.T  # Convert to V matrix

        # Extract V12 and V22
        V12, V22 = V[0, 1], V[1, 1]

        # Calculate weights based on chosen scheme
        if weights == "magnitude":
            weights_array = np.abs(mode).astype(np.float64)
        else:  # equal weights
            weights_array = np.ones(len(mode), dtype=np.float64)

        # Calculate denominator term
        denom_term = np.sqrt(V12**2 + V22**2)

        # Calculate phase deviations for each component
        phase_deviations = np.zeros(len(mode), dtype=np.float64)
        for i, (phi, w) in enumerate(zip(mode, weights_array, strict=False)):
            if w == 0:  # Skip zero components
                continue

            # Calculate numerator term
            num_term = (phi.real * V22 - phi.imag * V12) / (denom_term * w)

            # Ensure argument is in [-1, 1] for arccos
            num_term = np.clip(num_term, -1.0, 1.0)

            # Calculate phase deviation
            phase_deviations[i] = np.arccos(np.abs(num_term))

        # Calculate weighted average
        if np.sum(weights_array) == 0:
            return 0.0

        mpd_radians = float(np.sum(weights_array * phase_deviations) / np.sum(weights_array))
        return float(np.degrees(mpd_radians))

    if modeshape.ndim == 1:
        return np.array(calculate_single_mpd(modeshape))
    elif modeshape.ndim == 2:
        return np.array([calculate_single_mpd(mode) for mode in modeshape])
    else:
        raise NotImplementedError(f"modeshape has dimensions: {modeshape.ndim}, expecting 1 or 2.")


def calculate_complexity_metrics(modeshape: np.ndarray) -> ComplexityMetrics:
    """Calculate all complexity metrics for a modeshape or set of modeshapes.

    This function computes all available complexity metrics:
    - Modal Phase Collinearity (MPC)
    - Modal Amplitude Proportionality (MAP)
    - Mean Phase Deviation (MPD)

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.

    Returns
    -------
    ComplexityMetrics
        Container with all computed complexity metrics.
        Each metric has shape [] for single modeshape or [n_modes] for multiple modeshapes.

    Raises
    ------
    ValueError
        If modeshape has incorrect dimensions
    """
    ModalValidator.validate(modeshape)

    # Calculate all metrics
    mpc_values = calculate_mpc(modeshape)
    map_values = calculate_map(modeshape)
    mpd_values = calculate_mpd(modeshape)

    # Return as ComplexityMetrics container
    return ComplexityMetrics(
        mpc=mpc_values,
        map=map_values,
        mpd=mpd_values,
    )
