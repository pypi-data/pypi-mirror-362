"""MAC matrix visualization module."""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.projections.polar import PolarAxes
from matplotlib.ticker import FixedFormatter, FixedLocator


def _calculateGridLayout(nPlots: int) -> tuple[int, int]:
    """Calculate the best number of rows and columns for a given number of plots.

    This function determines the optimal grid layout (number of rows and columns)
    to display a specified number of plots. It uses a heuristic approach to find
    a layout that is as close to a square as possible.

    Parameters
    ----------
    nPlots : int
        The number of plots to arrange in a grid.

    Returns
    -------
    tuple[int, int]
        A tuple containing:
        - n_row : int
            The number of rows in the grid.
        - n_col : int
            The number of columns in the grid.
    """
    # hack:
    if nPlots == 4:
        return 4, 1
    # hack:
    if nPlots == 20:
        return 5, 4
    sqrN = np.sqrt(nPlots)
    nWide = np.ceil(sqrN)
    nHigh = np.floor(sqrN)
    if (nWide * nHigh) < nPlots:
        nWide = nWide + 1
        if (nWide * nHigh) <= sqrN:
            nHigh = nHigh + 1
    return int(nWide), int(nHigh)


def plot_mac_matrix(
    mac_matrix: np.ndarray,
    x_tick_labels: list[str],
    y_tick_labels: list[str],
    text_color_variable: bool = True,
    invert_scale: bool = False,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot the MAC matrix.

    Parameters
    ----------
    mac_matrix : np.ndarray
        MAC matrix [n_modes_1 x n_modes_2]
    x_tick_labels : list[str]
        Labels for x-axis ticks (columns of the MAC matrix)
    y_tick_labels : list[str]
        Labels for y-axis ticks (rows of the MAC matrix)
    text_color_variable : bool, optional
        Whether to vary text color based on MAC value, by default True
    invert_scale : bool, optional
        Whether to invert the colormap scale, by default False
    ax : Optional[Axes], optional
        Matplotlib axes to plot on, by default None

    Returns
    -------
    tuple[Figure, Axes]
        The figure and axes objects

    Raises
    ------
    ValueError
        If dimensions of inputs are incompatible
    """
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = cast(Figure, ax.figure)

    # Validate dimensions
    if len(x_tick_labels) != mac_matrix.shape[1]:
        raise ValueError("Number of x_tick_labels must match number of columns in mac_matrix")
    if len(y_tick_labels) != mac_matrix.shape[0]:
        raise ValueError("Number of y_tick_labels must match number of rows in mac_matrix")

    # Set up colormap
    cmap = "Greys_r" if invert_scale else "Greys"
    norm = Normalize(vmin=0, vmax=1)

    # Plot matrix
    _ = ax.matshow(mac_matrix, norm=norm, cmap=cmap)

    # Configure grid
    ax.grid(False, which="major")
    ax.xaxis.set_minor_locator(FixedLocator([x + 0.5 for x in range(mac_matrix.shape[1] - 1)]))
    ax.yaxis.set_minor_locator(FixedLocator([x + 0.5 for x in range(mac_matrix.shape[0] - 1)]))

    # Configure ticks and labels
    ax.xaxis.set_major_locator(FixedLocator(range(mac_matrix.shape[1])))
    ax.set_xticklabels(x_tick_labels, rotation=90)
    ax.yaxis.set_major_locator(FixedLocator(range(mac_matrix.shape[0])))
    ax.yaxis.set_major_formatter(FixedFormatter(y_tick_labels))

    # Add grid lines
    ax.grid(True, which="minor", color="0.7", linestyle="-", linewidth=1.5)

    # Configure labels
    ax.xaxis.set_label_position("top")
    # ax.set(xlabel="Numerical modes", ylabel="OMA modes")

    # Add text annotations
    def _get_text_color(value: float) -> str:
        """Return text color based on MAC value.

        Parameters
        ----------
        value : float
            The MAC value to determine text color for

        Returns
        -------
        str
            The text color as a string
        """
        if invert_scale:
            return "0.8" if value < 0.4 else "0.2"
        else:
            return "0.8" if value > 0.6 else "0.2"

    for irow in range(mac_matrix.shape[0]):
        for jcol in range(mac_matrix.shape[1]):
            ax.text(
                jcol + 0.0,
                irow + 0.0,
                f"{mac_matrix[irow, jcol]:.2f}",
                color=("C0" if not text_color_variable else _get_text_color(mac_matrix[irow, jcol])),
                size=10,
                fontweight="bold",
                va="center",
                ha="center",
            )

    return fig, ax


def plot_modeshape_complexity(
    modeshape: np.ndarray,
    ax: PolarAxes | None = None,
) -> tuple[Figure, PolarAxes]:
    """Plot the complexity of a modeshape using a polar Argand diagram.

    Parameters
    ----------
    modeshape : np.ndarray
        Complex modeshape vector
    ax : Optional[PolarAxes], optional
        Matplotlib polar axes to plot on, by default None

    Returns
    -------
    tuple[Figure, PolarAxes]
        The figure and axes containing the complexity plot

    Raises
    ------
    ValueError
        If the provided axes is not a polar projection
    """
    if ax is None:
        fig = plt.figure()
        ax = cast(PolarAxes, fig.add_subplot(111, projection="polar"))
    else:
        fig = cast(Figure, ax.get_figure())
        if ax.name != "polar":
            raise ValueError("Axes must be polar projection")

    # Calculate magnitude and phase
    magnitude = np.abs(modeshape)
    phase = np.angle(modeshape, deg=True)

    # Plot the complex mode shape points
    ax.scatter(np.radians(phase), magnitude, marker="o")

    # Add lines from origin to each point
    for i in range(len(modeshape)):
        ax.plot([0, np.radians(phase[i])], [0, magnitude[i]], "k--", alpha=0.3)

    # Add grid
    ax.grid(True)

    # Set the position of the radial tick labels to 90 degrees
    ax.set_rlabel_position(90)

    return fig, ax


def plot_modeshape_complexity_grid(
    frequencies: np.ndarray,
    modeshapes: np.ndarray,
    figsize: tuple[float, float] | None = None,
    n_row: int | None = None,
    n_col: int | None = None,
    hspace: float = 0.4,
    wspace: float = 0.4,
) -> tuple[Figure, np.ndarray]:
    """Plot multiple modeshape complexity plots in a grid layout.

    Parameters
    ----------
    frequencies : np.ndarray
        Array of frequencies for each mode
    modeshapes : np.ndarray
        Array of complex modeshapes
    figsize : Optional[tuple[float, float]], optional
        Figure size, by default None
    n_row : Optional[int], optional
        Number of rows in grid, by default None
    n_col : Optional[int], optional
        Number of columns in grid, by default None
    hspace : float, optional
        Horizontal spacing between plots, by default 0.4
    wspace : float, optional
        Vertical spacing between plots, by default 0.4

    Returns
    -------
    tuple[Figure, np.ndarray]
        The figure and array of axes containing the complexity plots
    """
    n_modes = len(frequencies)

    if n_row is None or n_col is None:
        n_row, n_col = _calculateGridLayout(n_modes)

    if figsize is None:
        figsize = (4 * n_col, 4 * n_row)

    fig, axs = plt.subplots(
        figsize=figsize,
        nrows=n_row,
        ncols=n_col,
        gridspec_kw={"hspace": hspace, "wspace": wspace},
        sharex=False,
        sharey=False,
        subplot_kw={"projection": "polar"},
    )

    for i in range(n_modes):
        ax = cast(PolarAxes, axs.flatten()[i])
        _, _ = plot_modeshape_complexity(modeshapes[i], ax=ax)
        ax.set_title(f"{frequencies[i]:.2f} Hz")

    return fig, axs
