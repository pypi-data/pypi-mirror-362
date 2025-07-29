"""
Layout utilities for Rekha plotting library.
"""

from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ..theme import set_rekha_theme


def subplots(
    rows: int = 1,
    cols: int = 1,
    dark_mode: bool = False,
    figsize: Optional[Tuple[float, float]] = None,
    **kwargs,
) -> Tuple[Figure, Union[Axes, np.ndarray]]:
    """
    Create subplots with Rekha theme.

    Parameters
    ----------
    rows : int, default 1
        Number of rows of subplots
    cols : int, default 1
        Number of columns of subplots
    dark_mode : bool, default False
        Whether to use dark theme
    figsize : tuple, optional
        Figure size (width, height). If None, auto-calculated
    **kwargs
        Additional arguments passed to plt.subplots

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object
    axes : matplotlib.axes.Axes or numpy.ndarray
        The axes object(s)

    Examples
    --------
    >>> import rekha as rk
    >>> fig, axes = rk.subplots(2, 2, figsize=(12, 8))
    >>> # Use axes[0, 0], axes[0, 1], etc. for individual plots
    """
    set_rekha_theme(dark_mode)

    if not figsize:
        figsize = (10 * cols, 6 * rows)

    return plt.subplots(rows, cols, figsize=figsize, **kwargs)
