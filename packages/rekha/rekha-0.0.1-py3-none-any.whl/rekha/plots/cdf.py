"""
Cumulative distribution function (CDF) plot implementation for Rekha.
"""

import numpy as np
import pandas as pd

from .base import BasePlot


class CDFPlot(BasePlot):
    """Create a cumulative distribution function plot with consistent Rekha interface."""

    def __init__(self, data=None, x=None, color=None, **kwargs):
        """
        Create a CDF plot.

        Parameters
        ----------
        **kwargs
            Additional parameters passed to BasePlot
        """
        # Initialize base plot
        super().__init__(data=data, x=x, y=None, color=color, **kwargs)

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_plot(self):
        """Create the CDF plot."""
        # Handle single or multiple series
        if self.color and isinstance(self.data, pd.DataFrame):
            # Get consistent colors and order for categories
            unique_categories = self.data[self.color].unique()
            categories, colors = self._get_consistent_colors_and_order(
                unique_categories
            )

            # Create a color mapping dict for easy lookup
            color_map = {cat: colors[i] for i, cat in enumerate(categories)}

            # Group by color column
            groups = self.data.groupby(self.color)
            patterns = self._get_bw_patterns()
            for i, (name, group) in enumerate(groups):
                x_data, _ = self._prepare_data(group, self.x, None)
                x_sorted = np.sort(x_data)  # type: ignore[arg-type]
                y_cdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)

                plot_kwargs = self.plot_kwargs.copy()
                # Get color from the mapping
                color = color_map[name]

                if self.grayscale_friendly:
                    # Keep color, add distinctive line style for b/w printing
                    plot_kwargs.update(
                        {
                            "color": color,
                            "linestyle": patterns["linestyles"][
                                i % len(patterns["linestyles"])
                            ],
                            "linewidth": 2.5,  # Slightly thicker for better b/w visibility
                        }
                    )
                else:
                    plot_kwargs.update(
                        {
                            "color": color,
                            "linewidth": 2,
                        }
                    )

                self.ax.plot(x_sorted, y_cdf, label=str(name), zorder=3, **plot_kwargs)
            self._add_legend_with_spacing()
        else:
            # Single series
            x_data, _ = self._prepare_data(self.data, self.x, None)
            x_sorted = np.sort(x_data)  # type: ignore[arg-type]
            y_cdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)

            # Determine color for this series
            color = self._get_next_color()

            plot_kwargs = self._get_plot_kwargs_with_label()
            if self.grayscale_friendly:
                patterns = self._get_bw_patterns()
                plot_kwargs.update(
                    {
                        "color": color,
                        "linestyle": patterns["linestyles"][
                            self._color_index % len(patterns["linestyles"])
                        ],
                        "linewidth": 2.5,
                    }
                )
            else:
                plot_kwargs.update({"color": color, "linewidth": 2})

            self.ax.plot(x_sorted, y_cdf, zorder=3, **plot_kwargs)

        # Set y-axis to 0-1 range
        self.ax.set_ylim(0, 1)

    def _create_faceted_plot(self):
        """Create faceted CDF plots."""
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

    def _apply_labels(self):
        """Apply axis labels for CDF plot."""
        if self.labels:
            x_label = self.labels.get(self.x, self.x) if isinstance(self.x, str) else ""
            self.ax.set_xlabel(
                x_label, fontsize=self.label_font_size, fontweight="bold"
            )
            self.ax.set_ylabel(
                "Cumulative Probability",
                fontsize=self.label_font_size,
                fontweight="bold",
            )
        else:
            if isinstance(self.x, str):
                self.ax.set_xlabel(
                    self.x, fontsize=self.label_font_size, fontweight="bold"
                )
            self.ax.set_ylabel(
                "Cumulative Probability",
                fontsize=self.label_font_size,
                fontweight="bold",
            )


def cdf(data=None, x=None, color=None, **kwargs):
    """
    Create a cumulative distribution function (CDF) plot with Rekha styling.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data to plot
    x : str, list, array, or None
        Column name or data for CDF
    color : str, optional
        Column name for color grouping
    facet_col : str, optional
        Column to use for creating subplots (facets)
    facet_row : str, optional
        Column to use for creating subplot rows
    title : str, optional
        Plot title
    labels : dict, optional
        Dictionary mapping column names to display labels
    dark_mode : bool, default False
        Whether to use dark theme
    figsize : tuple, default (10, 6)
        Figure size (width, height)
    grayscale_friendly : bool, default False
        Whether to use distinctive line styles for grayscale printing
    **kwargs
        Additional styling parameters

    Returns
    -------
    CDFPlot
        CDF plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     'values': np.random.normal(0, 1, 100),
    ...     'group': ['A'] * 50 + ['B'] * 50
    ... })
    >>> fig = rk.cdf(df, x='values', color='group', title='CDF Comparison')
    >>> fig.show()
    """
    return CDFPlot(data=data, x=x, color=color, **kwargs)
