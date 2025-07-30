"""Modeshape normalization module."""

import warnings

import numpy as np

from ..validation import ModalValidator


def normalize_modeshape(modeshape: np.ndarray) -> np.ndarray:
    """Normalize a single modeshape or set of modeshapes (real part only).

    !!! warning "Deprecated since 1.0.0"
        Use `normalize_modeshape_unit_norm_vector_length()` instead, which supports both real and complex modeshapes.
        This function will be removed in a future version.

    This function normalizes only the real part of the modeshape(s) to unit norm.
    For a single modeshape, the 2-norm is used.
    For multiple modeshapes, each modeshape is normalized independently.

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof]

    Returns
    -------
    np.ndarray
        Normalized modeshape(s) with the same shape as input

    Raises
    ------
    ValueError
        If modeshape has incorrect dimensions
    """
    warnings.warn(
        "normalize_modeshape is deprecated and will be removed in a future version. "
        "Use normalize_modeshape_unit_norm_vector_length instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    ModalValidator.validate(modeshape)
    return normalize_modeshape_unit_norm_vector_length(modeshape.real)


def normalize_modeshape_unit_norm_vector_length(modeshape: np.ndarray) -> np.ndarray:
    """Normalize a single modeshape or set of modeshapes to unit norm (vector length).

    This normalization method scales each mode shape vector such that its Euclidean norm (vector length, 2-norm)
    becomes unity (length of 1). This is a mathematically simple and common method for general mode shape normalization,
    especially when focusing on the shape itself rather than physical scaling. Works for both real and complex mode shapes.


    For a mode shape $\\vec{\\Phi}_r$, the normalized mode shape $\\vec{\\Phi}_{r, normalized}$ is:

    $$
        \\vec{\\Phi}_{r, normalized} = \\frac{\\vec{\\Phi}_r}{||\\vec{\\Phi}_r||_2}
    $$

    Where $||\\vec{\\Phi}_r||_2$ is the Euclidean norm (2-norm) of the mode shape vector.

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.

    Returns
    -------
    np.ndarray
        Normalized modeshape(s) with the same shape as input.
        Each mode shape vector will have unit length (2-norm = 1).

    Raises
    ------
    ValueError
        If modeshape has incorrect dimensions
    """
    ModalValidator.validate(modeshape)

    if modeshape.ndim == 1:
        norm_val = np.linalg.norm(modeshape)
        return modeshape / norm_val if norm_val != 0 else modeshape

    # modeshape.ndim == 2
    norms = np.linalg.norm(modeshape, axis=1)
    return np.where(norms[:, np.newaxis] != 0, modeshape / norms[:, np.newaxis], modeshape)


def normalize_modeshape_unit_norm_max_amplitude(modeshape: np.ndarray) -> np.ndarray:
    """Normalize a single modeshape or set of modeshapes to unit norm (maximum amplitude).

    This normalization method scales each mode shape vector such that the component with the maximum absolute
    value is normalized to unity (magnitude of 1). This method emphasizes the largest displacement component and
    is useful when you want to scale mode shapes based on their peak amplitude. Works for both real and complex mode shapes.


    For a mode shape $\\vec{\\Phi}_r$, let $\\Phi_{max, r}$ be the component with the maximum absolute value in $\\vec{\\Phi}_r$.
    The normalized mode shape $\\vec{\\Phi}_{r, normalized}$ is:

    $$
        \\vec{\\Phi}_{r, normalized} = \\frac{\\vec{\\Phi}_r}{\\Phi_{max, r}}
    $$

    Note: In case of multiple components having the same maximum magnitude, the first encountered component with maximum magnitude is used as the reference.

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.

    Returns
    -------
    np.ndarray
        Normalized modeshape(s) with the same shape as input.
        Each mode shape will have maximum amplitude of 1.

    Raises
    ------
    ValueError
        If modeshape has incorrect dimensions
    """
    ModalValidator.validate(modeshape)

    if modeshape.ndim == 1:
        max_val = np.max(np.abs(modeshape))
        return modeshape / max_val if max_val != 0 else modeshape

    # modeshape.ndim == 2
    max_vals = np.max(np.abs(modeshape), axis=1)
    return np.where(max_vals[:, np.newaxis] != 0, modeshape / max_vals[:, np.newaxis], modeshape)


def normalize_modeshape_reference_dof(modeshape: np.ndarray, ref_dof_index: int) -> np.ndarray:
    """Normalize a single modeshape or set of modeshapes using a reference degree of freedom (DOF).

    This normalization method scales each mode shape vector such that the component at the specified
    reference DOF index is normalized to unity (value of 1). This is useful when you want to scale mode shapes
    relative to a specific point on the structure, often a sensor location in experimental modal analysis.
    Works for both real and complex mode shapes.


    For a mode shape $\\vec{\\Phi}_r$ and a chosen reference DOF index `k` (ref_dof_index),
    the normalized mode shape $\\vec{\\Phi}_{r, normalized}$ is:

    $$
        \\vec{\\Phi}_{r, normalized} = \\frac{\\vec{\\Phi}_r}{\\Phi_{kr}}
    $$

    Where $\\Phi_{kr}$ is the component of the mode shape vector at the reference DOF index `k`.

    Parameters
    ----------
    modeshape : np.ndarray
        Single modeshape [n_dof] or set of modeshapes [n_modes x n_dof].
        Can be real or complex-valued.
    ref_dof_index : int
        Index of the reference degree of freedom (0-indexed).
        Must be a valid index within the modeshape dimension (0 <= ref_dof_index < n_dof).

    Returns
    -------
    np.ndarray
        Normalized modeshape(s) with the same shape as input.
        Each mode shape will have value 1 at the reference DOF.

    Raises
    ------
    ValueError
        If modeshape has incorrect dimensions or ref_dof_index is invalid
    """
    ModalValidator.validate(modeshape)

    if not isinstance(ref_dof_index, int):
        raise TypeError("ref_dof_index must be an integer")

    if modeshape.ndim == 1:
        if not 0 <= ref_dof_index < modeshape.shape[0]:
            raise ValueError(
                f"ref_dof_index {ref_dof_index} is out of bounds for modeshape of length {modeshape.shape[0]}"
            )
        ref_val = modeshape[ref_dof_index]
        return modeshape / ref_val if ref_val != 0 else modeshape

    # modeshape.ndim == 2
    if not 0 <= ref_dof_index < modeshape.shape[1]:
        raise ValueError(f"ref_dof_index {ref_dof_index} is out of bounds for modeshape with {modeshape.shape[1]} DOFs")
    ref_vals = modeshape[:, ref_dof_index]
    return np.where(ref_vals[:, np.newaxis] != 0, modeshape / ref_vals[:, np.newaxis], modeshape)
