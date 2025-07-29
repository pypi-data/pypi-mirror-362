"""
Heatmap plot implementation for Rekha.
"""

from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .base import BasePlot


class HeatmapPlot(BasePlot):
    """Create a heatmap with consistent Rekha interface."""

    def __init__(
        self,
        data=None,
        x: Optional[List[str]] = None,
        y: Optional[List[str]] = None,
        z: Optional[np.ndarray] = None,
        text_auto: bool = False,
        color_continuous_scale: Optional[str] = None,
        **kwargs,
    ):
        """
        Create a heatmap.

        Parameters
        ----------
        z : array, optional
            2D array of values (if not using DataFrame)
        text_auto : bool, default False
            Whether to show values in cells
        color_continuous_scale : str, optional
            Colormap name
        **kwargs
            Additional parameters passed to BasePlot
        """
        self.z = z
        self.text_auto = text_auto
        self.color_continuous_scale = color_continuous_scale

        # Initialize base plot
        super().__init__(data=data, x=x, y=y, **kwargs)

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_plot(self):
        """Create the heatmap."""
        # Prepare data
        if isinstance(self.data, pd.DataFrame):
            z_data = self.data.values
            x_labels = self.x or list(self.data.columns)
            y_labels = self.y or list(self.data.index)
        else:
            z_data = self.z if self.z is not None else self.data
            x_labels = self.x or list(range(z_data.shape[1]))
            y_labels = self.y or list(range(z_data.shape[0]))

        # Remove cmap from plot_kwargs to avoid conflict and get user preference
        plot_kwargs = self.plot_kwargs.copy()
        user_cmap = plot_kwargs.pop("cmap", None)

        # Choose colormap with priority: user-provided > color_continuous_scale > theme-based
        if user_cmap:
            cmap = user_cmap
        elif self.color_continuous_scale:
            cmap = self.color_continuous_scale
        elif self.grayscale_friendly:
            cmap = "gray"
        else:
            # Use theme-appropriate default colormap
            if self.dark_mode:
                cmap = "viridis"  # Good for dark themes
            else:
                cmap = "Greens"  # Good for light themes

        # Create heatmap
        im = self.ax.imshow(z_data, cmap=cmap, aspect="auto", **plot_kwargs)

        # Set ticks
        self.ax.set_xticks(np.arange(len(x_labels)))
        self.ax.set_yticks(np.arange(len(y_labels)))
        self.ax.set_xticklabels(x_labels)
        self.ax.set_yticklabels(y_labels)

        # Add grid lines for better readability
        if self.grid:
            # Create grid lines between cells
            self.ax.set_xticks(np.arange(len(x_labels) + 1) - 0.5, minor=True)
            self.ax.set_yticks(np.arange(len(y_labels) + 1) - 0.5, minor=True)
            self.ax.grid(
                which="minor",
                color=self.colors["text"],
                linestyle="-",
                linewidth=0.5,
                alpha=0.3,
                zorder=10,
            )
            # Remove major grid
            self.ax.grid(which="major", visible=False)

        # Add colorbar
        cbar = plt.colorbar(im, ax=self.ax)
        if self.labels and "color" in self.labels:
            cbar.set_label(self.labels["color"], rotation=270, labelpad=15)

        # Add text annotations if requested
        if self.text_auto:
            for i in range(len(y_labels)):
                for j in range(len(x_labels)):
                    # Choose text color based on background value for better contrast
                    if self.grayscale_friendly:
                        # For grayscale, use white text on dark cells, black on light
                        value_range = z_data.max() - z_data.min()
                        normalized_val = (
                            (z_data[i, j] - z_data.min()) / value_range
                            if value_range > 0
                            else 0.5
                        )
                        text_color = "white" if normalized_val > 0.5 else "black"
                    else:
                        text_color = "black" if not self.dark_mode else "white"

                    text = self.ax.text(
                        j,
                        i,
                        f"{z_data[i, j]:.2f}",
                        ha="center",
                        va="center",
                        color=text_color,
                        fontsize=8,
                        fontweight="bold" if self.grayscale_friendly else "normal",
                    )

    def _apply_labels(self):
        """Apply axis labels for heatmap."""
        if self.labels:
            self.ax.set_xlabel(
                self.labels.get("x", ""),
                fontsize=self.label_font_size,
                fontweight="bold",
            )
            self.ax.set_ylabel(
                self.labels.get("y", ""),
                fontsize=self.label_font_size,
                fontweight="bold",
            )

    def _create_faceted_plot(self):
        """Create faceted heatmap plots."""
        for i, row_val in enumerate(self.facet_row_values):
            for j, col_val in enumerate(self.facet_col_values):
                ax = self._get_wrapped_axes(i, j)

                # Get data for this facet
                facet_data = self._get_facet_data(row_val, col_val)

                if len(facet_data) == 0:
                    continue

                # Temporarily set the current axis and data
                original_ax = self.ax
                original_data = self.data
                self.ax = ax
                self.data = facet_data

                # Create the plot for this facet
                self._create_plot()

                # Restore original data and axis
                self.ax = original_ax
                self.data = original_data

        # Apply faceted finalization
        self._finalize_faceted_plot()
        self._show_legend_if_needed()


def heatmap(data=None, x=None, y=None, z=None, **kwargs):
    """
    Create a heatmap with Rekha styling.

    Parameters
    ----------
    data : DataFrame or array
        The data to plot
    x : list, optional
        Column labels
    y : list, optional
        Row labels
    z : array, optional
        2D array of values (if not using DataFrame)
    text_auto : bool, default False
        Whether to show values in cells
    color_continuous_scale : str, optional
        Colormap name
    facet_col : str, optional
        Column to use for creating subplots (facets)
    facet_row : str, optional
        Column to use for creating subplot rows
    title : str, optional
        Plot title
    labels : dict, optional
        Dictionary mapping axes to display labels
    dark_mode : bool, default False
        Whether to use dark theme
    figsize : tuple, default (10, 6)
        Figure size (width, height)
    grayscale_friendly : bool, default False
        Whether to use grayscale for grayscale printing
    **kwargs
        Additional styling parameters

    Returns
    -------
    HeatmapPlot
        Heatmap plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = np.random.rand(5, 5)
    >>> fig = rk.heatmap(data, title='Correlation Matrix')
    >>> fig.show()
    """
    return HeatmapPlot(data=data, x=x, y=y, z=z, **kwargs)
