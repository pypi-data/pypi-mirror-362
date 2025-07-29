"""
Line plot implementation for Rekha.
"""

from typing import Optional

import pandas as pd

from .base import BasePlot


class LinePlot(BasePlot):
    """Create a line plot with consistent Rekha interface."""

    def __init__(
        self,
        data=None,
        x=None,
        y=None,
        color: Optional[str] = None,
        line_width: float = 2.0,
        line_style: str = "-",
        markers: bool = False,
        marker_size: float = 6.0,
        **kwargs,
    ):
        """
        Create a line plot.

        Parameters
        ----------
        line_width : float, default 2.0
            Width of the lines
        line_style : str, default '-'
            Line style ('-', '--', '-.', ':')
        markers : bool, default False
            Whether to show markers at data points
        marker_size : float, default 6.0
            Size of markers if enabled
        **kwargs
            Additional parameters passed to BasePlot
        """
        # Store line-specific parameters
        self.line_width = line_width
        self.line_style = line_style
        self.markers = markers
        self.marker_size = marker_size

        # Initialize base plot
        super().__init__(data=data, x=x, y=y, color=color, **kwargs)

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_plot(self):
        """Create the line plot."""
        # Handle single or multiple series
        if (
            self.color
            and isinstance(self.data, pd.DataFrame)
            and self.color in self.data.columns
        ):
            # Get consistent colors and order for categories
            unique_categories = self.data[self.color].unique()
            categories, colors = self._get_consistent_colors_and_order(
                unique_categories
            )

            # Create a color mapping dict for easy lookup
            color_map = {cat: colors[i] for i, cat in enumerate(categories)}

            # Group by color column
            grouped_data = self.data.groupby(self.color)
            patterns = self._get_bw_patterns()

            # Iterate through categories in the ordered sequence
            for i, cat in enumerate(categories):
                if cat not in grouped_data.groups:
                    continue
                group = grouped_data.get_group(cat)
                name = cat
                x_data, y_data = self._prepare_data(group, self.x, self.y)

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
                            "linewidth": self.line_width
                            * 1.25,  # Slightly thicker for better b/w visibility
                        }
                    )
                else:
                    plot_kwargs.update(
                        {
                            "color": color,
                            "linewidth": self.line_width,
                            "linestyle": self.line_style,
                        }
                    )

                if self.markers:
                    markers = self._get_markers()
                    plot_kwargs["marker"] = markers[i % len(markers)]
                    plot_kwargs["markersize"] = self.marker_size

                self.ax.plot(x_data, y_data, label=str(name), zorder=3, **plot_kwargs)

            self._add_legend_with_spacing()
        else:
            # Single series
            x_data, y_data = self._prepare_data()
            plot_kwargs = self.plot_kwargs.copy()

            # Determine color for this series
            color = self._get_next_color()

            if self.grayscale_friendly:
                patterns = self._get_bw_patterns()
                plot_kwargs.update(
                    {
                        "color": color,
                        "linestyle": patterns["linestyles"][
                            self._color_index % len(patterns["linestyles"])
                        ],
                        "linewidth": self.line_width * 1.25,
                    }
                )
            else:
                plot_kwargs.update(
                    {
                        "color": color,
                        "linewidth": self.line_width,
                        "linestyle": self.line_style,
                    }
                )

            if self.markers:
                markers = self._get_markers()
                plot_kwargs["marker"] = markers[self._color_index % len(markers)]
                plot_kwargs["markersize"] = self.marker_size

            # Get kwargs with label
            final_kwargs = self._get_plot_kwargs_with_label()
            final_kwargs.update(plot_kwargs)  # Merge existing settings

            self.ax.plot(x_data, y_data, zorder=3, **final_kwargs)

    def _create_faceted_plot(self):
        """Create faceted line plots."""
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


def line(data=None, x=None, y=None, **kwargs):
    """
    Create a line plot with Rekha styling.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data to plot
    x, y : str, list, array, or None
        Column names or data for x and y axes
    color : str, optional
        Column name for color grouping
    facet_row : str, optional
        Column name for creating subplot rows
    facet_col : str, optional
        Column name for creating subplot columns
    line_width : float, default 2.0
        Width of the lines
    line_style : str, default '-'
        Line style ('-', '--', '-.', ':')
    markers : bool, default False
        Whether to show markers at data points
    marker_size : float, default 6.0
        Size of markers if enabled
    title : str, optional
        Plot title
    labels : dict, optional
        Dictionary mapping column names to display labels
    dark_mode : bool, default False
        Whether to use dark theme
    figsize : tuple, default (10, 6)
        Figure size (width, height)
    grayscale_friendly : bool, default False
        Whether to add patterns for grayscale printing
    **kwargs
        Additional styling parameters

    Returns
    -------
    LinePlot
        Line plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> df = pd.DataFrame({'x': [1,2,3], 'y': [1,4,2]})
    >>> fig = rk.line(df, x='x', y='y', title='My Line Plot')
    >>> fig.show()
    """
    return LinePlot(data=data, x=x, y=y, **kwargs)
