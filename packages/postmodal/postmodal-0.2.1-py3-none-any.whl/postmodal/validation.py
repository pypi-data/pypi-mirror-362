"""Validation utilities for modal analysis data."""

import numpy as np


class ModalValidator:
    """Validator for modeshape data."""

    @staticmethod
    def validate(modeshape: np.ndarray) -> None:
        """Validate a modeshape array.

        Parameters
        ----------
        modeshape : np.ndarray
            The modeshape array to validate

        Raises
        ------
        TypeError
            If modeshape is not a numpy array
        ValueError
            If modeshape has incorrect dimensions
        """
        if not isinstance(modeshape, np.ndarray):
            raise TypeError("Modeshape must be a numpy array")
        if modeshape.ndim not in [1, 2]:
            raise ValueError("Modeshape must be 1D or 2D array")
        if modeshape.size == 0:
            raise ValueError("Modeshape array cannot be empty")

    @staticmethod
    def validate_pair(phi_1: np.ndarray, phi_2: np.ndarray) -> None:
        """Validate a pair of modeshapes for comparison.

        Parameters
        ----------
        phi_1 : np.ndarray
            First modeshape
        phi_2 : np.ndarray
            Second modeshape

        Raises
        ------
        ValueError
            If modeshapes have different shapes
        """
        # Validate individual modeshapes first
        ModalValidator.validate(phi_1)
        ModalValidator.validate(phi_2)
        if phi_1.shape != phi_2.shape:
            raise ValueError("Modeshapes must have the same shape")

    @staticmethod
    def validate_frequency(frequency: np.ndarray) -> None:
        """Validate frequency data.

        Parameters
        ----------
        frequency : np.ndarray
            Array of frequencies to validate

        Raises
        ------
        TypeError
            If frequency is not a numpy array
        ValueError
            If frequency is not 1D or contains non-positive values
        """
        if not isinstance(frequency, np.ndarray):
            raise TypeError("Frequency must be a numpy array")
        if frequency.ndim != 1:
            raise ValueError("Frequency must be 1D array")
        if np.any(frequency <= 0):
            raise ValueError("All frequencies must be positive")


def validate_modal_data(frequencies: np.ndarray, modeshapes: np.ndarray) -> None:
    """Validate modal data (frequencies and modeshapes).

    Parameters
    ----------
    frequencies : np.ndarray
        Array of natural frequencies [n_modes]
    modeshapes : np.ndarray
        Array of mode shapes [n_modes x n_dof]

    Raises
    ------
    ValueError
        If data dimensions are incompatible
    """
    ModalValidator.validate(modeshapes)
    ModalValidator.validate_frequency(frequencies)

    if frequencies.shape[0] != modeshapes.shape[0]:
        raise ValueError("Number of frequencies must match number of modes")
