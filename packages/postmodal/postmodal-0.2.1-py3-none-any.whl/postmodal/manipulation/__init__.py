"""Modeshape manipulation utilities.

This module provides functions for manipulating modeshapes, including
normalization, phase alignment, and complex-to-real conversion.

!!! note
    The `normalize_modeshape()` function is deprecated and will be removed in a future version.
    Use `normalize_modeshape_unit_norm_vector_length()` instead.
"""

from .conversion import (
    calculate_conversion_error,
    complex_to_real,
    complex_to_real_batch,
    optimize_conversion,
)
from .normalize import (
    normalize_modeshape,  # deprecated
    normalize_modeshape_reference_dof,
    normalize_modeshape_unit_norm_max_amplitude,
    normalize_modeshape_unit_norm_vector_length,
)
from .phase import (
    align_phase,
    calculate_phase_distribution,
    normalize_phase,
    unwrap_phase,
)

__all__ = [
    # Normalization
    "normalize_modeshape",  # deprecated
    "normalize_modeshape_unit_norm_vector_length",
    "normalize_modeshape_unit_norm_max_amplitude",
    "normalize_modeshape_reference_dof",
    # Phase manipulation
    "align_phase",
    "unwrap_phase",
    "normalize_phase",
    "calculate_phase_distribution",
    # Complex to real conversion
    "complex_to_real",
    "complex_to_real_batch",
    "calculate_conversion_error",
    "optimize_conversion",
]
