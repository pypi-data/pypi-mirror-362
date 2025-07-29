"""
Rekha plotting functions - Beautiful matplotlib visualizations.
"""

# Import layout utilities
from ..utils.layout import subplots
from .bar import BarPlot, bar
from .base import BasePlot
from .box import BoxPlot, box
from .cdf import CDFPlot, cdf
from .heatmap import HeatmapPlot, heatmap
from .histogram import HistogramPlot, histogram
from .line import LinePlot, line
from .scatter import ScatterPlot, scatter

__all__ = [
    # Base class
    "BasePlot",
    # Main plot functions (consistent interface)
    "line",
    "scatter",
    "bar",
    "histogram",
    "heatmap",
    "box",
    "cdf",
    # Plot classes (for advanced usage)
    "LinePlot",
    "ScatterPlot",
    "BarPlot",
    "HistogramPlot",
    "HeatmapPlot",
    "BoxPlot",
    "CDFPlot",
    # Layout functions
    "subplots",
]
