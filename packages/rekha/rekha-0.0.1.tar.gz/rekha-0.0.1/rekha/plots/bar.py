"""
Bar plot implementation for Rekha.
"""

from typing import Optional

import numpy as np
import pandas as pd

from .base import BasePlot


class BarPlot(BasePlot):
    """Create a bar plot with consistent Rekha interface."""

    def __init__(
        self,
        data=None,
        x=None,
        y=None,
        color: Optional[str] = None,
        orientation: str = "v",
        text_auto: bool = False,
        barmode: str = "group",
        bar_edge: bool = False,
        bar_edge_color: Optional[str] = None,
        bar_edge_width: float = 1.0,
        bar_width: float = 0.8,
        **kwargs,
    ):
        """
        Create a bar plot.

        Parameters
        ----------
        orientation : str, default 'v'
            Bar orientation ('v' for vertical, 'h' for horizontal)
        text_auto : bool, default False
            Whether to automatically add value labels on bars
        barmode : str, default 'group'
            Bar mode ('group', 'stack', 'relative')
        bar_edge : bool, default False
            Whether to add edges around bars
        bar_edge_color : str, optional
            Color for bar edges (auto if None)
        bar_edge_width : float, default 1.0
            Width of bar edges
        bar_width : float, default 0.8
            Width of bars
        **kwargs
            Additional parameters passed to BasePlot
        """
        # Store bar-specific parameters
        self.orientation = orientation
        self.text_auto = text_auto
        self.barmode = barmode
        self.bar_edge = bar_edge
        self.bar_edge_color = bar_edge_color
        self.bar_edge_width = bar_edge_width
        self.bar_width = bar_width

        # Set default edge color based on theme
        if self.bar_edge_color is None:
            self.bar_edge_color = "black"  # Will be updated after theme is applied

        # Initialize base plot
        super().__init__(data=data, x=x, y=y, color=color, **kwargs)

        # Update edge color after theme is applied
        if self.bar_edge_color == "black":
            self.bar_edge_color = "black" if not self.dark_mode else "white"

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_plot(self):
        """Create the bar plot."""
        # Handle different bar modes
        if self.color and isinstance(self.data, pd.DataFrame):
            # Check if each x value has only one color value (1:1 mapping)
            # This would indicate we want single bars with different colors, not grouped bars
            x_color_mapping = self.data.groupby(self.x)[self.color].nunique()
            if (x_color_mapping == 1).all() and len(x_color_mapping) > 1:
                # Each x has exactly one color - use single bars with mapped colors
                self._create_single_series_bars_with_color_mapping()
            else:
                # Multiple series bar chart
                self._create_multi_series_bars()
        else:
            # Simple single-series bar plot
            self._create_single_series_bars()

    def _create_multi_series_bars(self):
        """Create multi-series bar chart."""
        # For horizontal bars, we need to swap x and y in the pivot
        if self.orientation == "h":
            pivot_index, pivot_values = self.y, self.x
        else:
            pivot_index, pivot_values = self.x, self.y

        try:
            # Try pivot first (faster, no aggregation)
            pivot_df = self.data.pivot(
                index=pivot_index, columns=self.color, values=pivot_values
            ).fillna(0)
        except ValueError:
            # If pivot fails due to duplicates, use pivot_table with sum aggregation
            pivot_df = self.data.pivot_table(
                values=pivot_values,
                index=pivot_index,
                columns=self.color,
                aggfunc="sum",
                fill_value=0,
            )

        if self.barmode == "stack":
            self._create_stacked_bars(pivot_df)
        elif self.barmode == "relative":
            self._create_relative_bars(pivot_df)
        else:  # barmode == 'group' (default)
            self._create_grouped_bars(pivot_df)

    def _create_stacked_bars(self, pivot_df):
        """Create stacked bar chart."""
        # Get consistent colors and order for categories
        categories, colors = self._get_consistent_colors_and_order(pivot_df.columns)

        # Reorder pivot_df columns to match the ordered categories
        pivot_df = pivot_df[categories]

        if self.orientation == "v":
            bottom = np.zeros(len(pivot_df))
            left = None
        else:
            left = np.zeros(len(pivot_df))
            bottom = None
        bars = []

        for i, col in enumerate(pivot_df.columns):
            edge_params = self._get_bar_edge_params()

            # Combine all kwargs, with plot_kwargs taking precedence
            bar_kwargs = {**edge_params, **self.plot_kwargs}
            if "zorder" not in bar_kwargs:
                bar_kwargs["zorder"] = 3

            if self.orientation == "v":
                bar = self.ax.bar(
                    pivot_df.index,
                    pivot_df[col],
                    bottom=bottom,
                    label=str(col),
                    color=colors[i],
                    width=self.bar_width,
                    **bar_kwargs,
                )
                if bottom is not None:
                    bottom += pivot_df[col]
            else:
                bar = self.ax.barh(
                    y=pivot_df.index,
                    width=pivot_df[col].values,
                    left=left,
                    label=str(col),
                    color=colors[i],
                    height=self.bar_width,
                    **bar_kwargs,
                )
                if left is not None:
                    left += pivot_df[col].values
            bars.append(bar)

        # Apply grayscale patterns for stacked bars
        if self.grayscale_friendly:
            self._apply_bw_bar_styles(bars)

        legend = self._add_legend_with_spacing()
        if legend and self.color:
            legend.set_title(self.color)

    def _create_relative_bars(self, pivot_df):
        """Create relative/percentage stacked bars."""
        # Get consistent colors and order for categories
        categories, colors = self._get_consistent_colors_and_order(pivot_df.columns)

        # Reorder pivot_df columns to match the ordered categories
        pivot_df = pivot_df[categories]

        pivot_df_pct = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

        if self.orientation == "v":
            bottom = np.zeros(len(pivot_df_pct))
            left = None
        else:
            left = np.zeros(len(pivot_df_pct))
            bottom = None
        bars = []

        for i, col in enumerate(pivot_df_pct.columns):
            edge_params = self._get_bar_edge_params()

            # Combine all kwargs, with plot_kwargs taking precedence
            bar_kwargs = {**edge_params, **self.plot_kwargs}
            if "zorder" not in bar_kwargs:
                bar_kwargs["zorder"] = 3

            if self.orientation == "v":
                bar = self.ax.bar(
                    pivot_df_pct.index,
                    pivot_df_pct[col],
                    bottom=bottom,
                    label=str(col),
                    color=colors[i],
                    width=self.bar_width,
                    **bar_kwargs,
                )
                if bottom is not None:
                    bottom += pivot_df_pct[col]
            else:
                bar = self.ax.barh(
                    y=pivot_df_pct.index,
                    width=pivot_df_pct[col].values,
                    left=left,
                    label=str(col),
                    color=colors[i],
                    height=self.bar_width,
                    **bar_kwargs,
                )
                if left is not None:
                    left += pivot_df_pct[col].values
            bars.append(bar)

        # Set y-axis to percentage for relative mode
        if self.orientation == "v":
            self.ax.set_ylim(0, 100)
            self.ax.set_ylabel(
                "Percentage (%)", fontsize=self.label_font_size, fontweight="bold"
            )
        else:
            self.ax.set_xlim(0, 100)
            self.ax.set_xlabel(
                "Percentage (%)", fontsize=self.label_font_size, fontweight="bold"
            )

        # Apply grayscale patterns
        if self.grayscale_friendly:
            self._apply_bw_bar_styles(bars)

        legend = self._add_legend_with_spacing()
        if legend and self.color:
            legend.set_title(self.color)

    def _create_grouped_bars(self, pivot_df):
        """Create grouped bar chart."""
        # Get consistent colors and order for categories
        categories, colors = self._get_consistent_colors_and_order(pivot_df.columns)

        # Reorder pivot_df columns to match the ordered categories
        pivot_df = pivot_df[categories]

        plot_kwargs = {
            "kind": "bar" if self.orientation == "v" else "barh",
            "ax": self.ax,
            "color": colors,
        }

        if self.orientation == "v":
            plot_kwargs["width"] = self.bar_width
        else:
            plot_kwargs["height"] = self.bar_width

        # Add edge parameters for grouped bars
        edge_params = self._get_bar_edge_params()
        plot_kwargs.update(edge_params)

        pivot_df.plot(**plot_kwargs)

        # Set zorder for all bar containers to appear above grid
        for container in self.ax.containers:
            for bar in container:
                bar.set_zorder(3)

        # Apply grayscale patterns for grouped bars
        if self.grayscale_friendly:
            bar_containers = []
            for i, container in enumerate(self.ax.containers):
                bar_containers.append(container)
            self._apply_bw_bar_styles(bar_containers)

        legend = self._add_legend_with_spacing()
        if legend and self.color:
            legend.set_title(self.color)

    def _create_single_series_bars_with_color_mapping(self):
        """Create single-series bar plot with different colors per bar based on color mapping."""
        # Get unique x values in order
        x_order = self.data[self.x].unique()

        # Create a mapping of x values to their color values
        x_to_color = self.data.set_index(self.x)[self.color].to_dict()

        # Get the color mapping for these categories
        unique_colors = self.data[self.color].unique()
        categories, colors = self._get_consistent_colors_and_order(unique_colors)
        color_map = dict(zip(categories, colors))

        # Prepare data
        x_data, y_data = self._prepare_data()

        edge_params = self._get_bar_edge_params()

        # Combine all kwargs, with plot_kwargs taking precedence
        bar_kwargs = {**edge_params, **self.plot_kwargs}
        if "zorder" not in bar_kwargs:
            bar_kwargs["zorder"] = 3

        # Create bars with appropriate colors
        bar_colors = [color_map[x_to_color[x]] for x in x_order]

        if self.orientation == "v":
            bars = self.ax.bar(
                x_data,
                y_data,
                color=bar_colors,
                width=self.bar_width,
                **bar_kwargs,
            )
        else:
            bars = self.ax.barh(
                y_data,
                x_data,
                color=bar_colors,
                height=self.bar_width,
                **bar_kwargs,
            )

        # Apply grayscale patterns if needed
        if self.grayscale_friendly:
            self._apply_bw_bar_styles(bars)

        # Add value labels if requested
        if self.text_auto:
            self._add_value_labels(bars)

    def _create_single_series_bars(self):
        """Create single-series bar plot."""
        x_data, y_data = self._prepare_data()

        edge_params = self._get_bar_edge_params()

        # Determine color for this series
        color = self._get_next_color()

        # Get kwargs with label
        bar_kwargs = self._get_plot_kwargs_with_label()
        bar_kwargs.update(edge_params)

        # Set default zorder if not provided by user
        if "zorder" not in bar_kwargs:
            bar_kwargs["zorder"] = 3

        if self.orientation == "v":
            bars = self.ax.bar(
                x_data,
                y_data,
                color=color,
                width=self.bar_width,
                **bar_kwargs,
            )
        else:
            bars = self.ax.barh(
                y_data,
                x_data,
                color=color,
                height=self.bar_width,
                **bar_kwargs,
            )

        # Apply grayscale patterns for single bar series
        if self.grayscale_friendly:
            self._apply_bw_bar_styles(bars)

        # Add value labels if requested (for simple bars only)
        if self.text_auto:
            self._add_value_labels(bars)

    def _get_bar_edge_params(self):
        """Get edge parameters for bar plots."""
        if self.bar_edge:
            return {"edgecolor": self.bar_edge_color, "linewidth": self.bar_edge_width}
        return {}

    def _apply_bw_bar_styles(self, bars):
        """Apply grayscale printing patterns to bar chart."""
        if not self.grayscale_friendly:
            return

        patterns = self._get_bw_patterns()
        if isinstance(bars, list):
            # Multiple bar series
            for i, bar_group in enumerate(bars):
                hatch = patterns["hatches"][i % len(patterns["hatches"])]
                for bar in bar_group:
                    bar.set_hatch(hatch)
                    bar.set_edgecolor("black" if not self.dark_mode else "white")
                    bar.set_linewidth(1.2)
        else:
            # Single bar series or individual bars
            hatch = patterns["hatches"][0]
            if hasattr(bars, "__iter__"):
                for bar in bars:
                    bar.set_hatch(hatch)
                    bar.set_edgecolor("black" if not self.dark_mode else "white")
                    bar.set_linewidth(1.2)
            else:
                bars.set_hatch(hatch)
                bars.set_edgecolor("black" if not self.dark_mode else "white")
                bars.set_linewidth(1.2)

    def _add_value_labels(self, bars):
        """Add value labels on bars."""
        for bar in bars:
            if self.orientation == "v":
                height = bar.get_height()
                self.ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )
            else:
                width = bar.get_width()
                self.ax.text(
                    width,
                    bar.get_y() + bar.get_height() / 2.0,
                    f"{width:.1f}",
                    ha="left",
                    va="center",
                    fontsize=9,
                )

    def _create_faceted_plot(self):
        """Create faceted bar plots."""
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


def bar(data=None, x=None, y=None, **kwargs):
    """
    Create a bar plot with Rekha styling.

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
    orientation : str, default 'v'
        Bar orientation ('v' for vertical, 'h' for horizontal)
    text_auto : bool, default False
        Whether to automatically add value labels on bars
    barmode : str, default 'group'
        Bar mode ('group', 'stack', 'relative')
    bar_edge : bool, default False
        Whether to add edges around bars
    bar_edge_color : str, optional
        Color for bar edges (auto if None)
    bar_edge_width : float, default 1.0
        Width of bar edges
    bar_width : float, default 0.8
        Width of bars
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
    BarPlot
        Bar plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> df = pd.DataFrame({'x': ['A','B','C'], 'y': [1,3,2]})
    >>> fig = rk.bar(df, x='x', y='y', title='My Bar Plot')
    >>> fig.show()
    """
    return BarPlot(data=data, x=x, y=y, **kwargs)
