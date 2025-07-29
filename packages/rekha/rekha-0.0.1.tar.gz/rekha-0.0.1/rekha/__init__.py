"""
Rekha - Beautiful matplotlib visualizations with a Plotly Express-like interface

This library provides a simple, intuitive API for creating beautiful plots
while maintaining the full power and customization of matplotlib.
"""

from .plots import BasePlot, bar, box, cdf, heatmap, histogram, line, scatter, subplots
from .theme import REKHA_COLORS, REKHA_DARK_COLORS, set_rekha_theme

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.1.0"

__author__ = "Vajra Team"
__email__ = "team@project-vajra.org"

__all__ = [
    "line",
    "scatter",
    "bar",
    "histogram",
    "heatmap",
    "box",
    "cdf",
    "subplots",
    "BasePlot",
    "set_rekha_theme",
    "REKHA_COLORS",
    "REKHA_DARK_COLORS",
]
