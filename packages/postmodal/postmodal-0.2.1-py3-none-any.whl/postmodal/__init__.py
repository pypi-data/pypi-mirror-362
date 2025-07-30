"""Modal analysis package for structural dynamics."""

from .comparison import calculate_mac
from .comparison.matrix import (
    best_match,
    calculate_mac_matrix,
    calculate_mode_matching_matrix,
    match_modes,
)
from .complexity import (
    calculate_complexity_metrics,
    calculate_map,
    calculate_mpc,
    calculate_mpd,
)
from .manipulation import (
    align_phase,
    calculate_conversion_error,
    calculate_phase_distribution,
    complex_to_real,
    complex_to_real_batch,
    normalize_modeshape,
    normalize_modeshape_reference_dof,
    normalize_modeshape_unit_norm_max_amplitude,
    normalize_modeshape_unit_norm_vector_length,
    normalize_phase,
    optimize_conversion,
    unwrap_phase,
)
from .types import (
    ComplexityMetrics,
    ComplexityValue,
    Frequency,
    MACValue,
    ModalData,
    Modeshape,
)
from .validation import ModalValidator, validate_modal_data
from .visualization import (
    plot_mac_matrix,
    plot_modeshape_complexity,
    plot_modeshape_complexity_grid,
)

__all__ = [
    # Types
    "ModalData",
    "ComplexityMetrics",
    "Modeshape",
    "Frequency",
    "MACValue",
    "ComplexityValue",
    # Validation
    "ModalValidator",
    "validate_modal_data",
    # Complexity metrics
    "calculate_mpc",
    "calculate_map",
    "calculate_mpd",
    "calculate_complexity_metrics",
    # Comparison
    "calculate_mac",
    "calculate_mac_matrix",
    "calculate_mode_matching_matrix",
    "match_modes",
    "best_match",
    # Manipulation
    "normalize_modeshape",
    "normalize_modeshape_unit_norm_vector_length",
    "normalize_modeshape_unit_norm_max_amplitude",
    "normalize_modeshape_reference_dof",
    "align_phase",
    "unwrap_phase",
    "normalize_phase",
    "calculate_phase_distribution",
    "complex_to_real",
    "complex_to_real_batch",
    "calculate_conversion_error",
    "optimize_conversion",
    # Visualization
    "plot_mac_matrix",
    "plot_modeshape_complexity",
    "plot_modeshape_complexity_grid",
]
