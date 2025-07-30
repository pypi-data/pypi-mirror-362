"""Custom types and data classes for modal analysis."""

from dataclasses import dataclass, field
from typing import NewType

import numpy as np

# Custom types for better type safety
Modeshape = NewType("Modeshape", np.ndarray)
Frequency = NewType("Frequency", np.ndarray)
MACValue = NewType("MACValue", float)
ComplexityValue = NewType("ComplexityValue", float)


@dataclass
class ModalData:
    """Container for modal analysis data.

    Attributes
    ----------
    frequencies : np.ndarray
        Array of natural frequencies [n_modes]. Must be positive real values.
    modeshapes : np.ndarray
        Array of mode shapes [n_modes x n_dof]
    damping : np.ndarray, optional
        Array of damping ratios [n_modes], defaults to zeros.
        Must be real-valued positive numbers in range [0, 1].
    """

    frequencies: np.ndarray
    modeshapes: np.ndarray
    damping: np.ndarray | None = field(default_factory=lambda: np.array([]))

    def _validate_frequencies(self) -> None:
        """Validate frequency data."""
        if not isinstance(self.frequencies, np.ndarray):
            raise TypeError("frequencies must be a numpy array")
        if not np.isreal(self.frequencies).all():
            raise ValueError("frequencies must be real-valued")
        if np.any(self.frequencies <= 0):
            raise ValueError("frequencies must be positive")

    def _validate_modeshapes(self) -> None:
        """Validate modeshape data."""
        if not isinstance(self.modeshapes, np.ndarray):
            raise TypeError("modeshapes must be a numpy array")
        if self.modeshapes.ndim not in [1, 2]:
            raise ValueError("modeshapes must be 1D or 2D array")
        if self.frequencies.shape[0] != self.modeshapes.shape[0]:
            raise ValueError("Number of frequencies must match number of modes")

    def _validate_damping(self) -> None:
        """Validate damping data."""
        if self.damping is None or len(self.damping) == 0:
            self.damping = np.zeros_like(self.frequencies)
            return

        if not isinstance(self.damping, np.ndarray):
            raise TypeError("damping must be a numpy array")
        if not np.isreal(self.damping).all():
            raise ValueError("damping must be real-valued")
        if self.damping.shape != self.frequencies.shape:
            raise ValueError("damping must have same shape as frequencies")
        if np.any(self.damping < 0):
            raise ValueError("damping ratios must be non-negative")
        if np.any(self.damping > 1):
            raise ValueError("damping ratios must be less than or equal to 1")

    def __post_init__(self) -> None:
        """Validate the data after initialization."""
        self._validate_frequencies()
        self._validate_modeshapes()
        self._validate_damping()


@dataclass
class ComplexityMetrics:
    """Container for modal complexity metrics.

    Attributes
    ----------
    mpc : np.ndarray
        Modal Phase Collinearity values [n_modes]
    map : np.ndarray
        Modal Amplitude Proportionality values [n_modes]
    mpd : np.ndarray
        Mean Phase Deviation values [n_modes] in degrees
    """

    mpc: np.ndarray
    map: np.ndarray
    mpd: np.ndarray

    def __post_init__(self) -> None:
        """Validate the metrics after initialization."""
        shapes = [
            self.mpc.shape,
            self.map.shape,
            self.mpd.shape,
        ]
        if not all(s == shapes[0] for s in shapes):
            raise ValueError("All metrics must have the same shape")
