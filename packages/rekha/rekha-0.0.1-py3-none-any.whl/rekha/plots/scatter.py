"""
Scatter plot implementation for Rekha.
"""

from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .base import BasePlot


class ScatterPlot(BasePlot):
    """Create a scatter plot with consistent Rekha interface."""

    def __init__(
        self,
        data=None,
        x=None,
        y=None,
        color: Optional[str] = None,
        size: Union[str, List, np.ndarray, None] = None,
        shape: Optional[str] = None,
        trendline: Optional[str] = None,
        color_continuous_scale: Optional[str] = None,
        size_max: float = 200,
        point_size: float = 100,
        alpha: float = 0.7,
        **kwargs,
    ):
        """
        Create a scatter plot.

        Parameters
        ----------
        trendline : str, optional
            Type of trendline ('ols' for linear regression)
        color_continuous_scale : str, optional
            Colormap for numerical color mapping
        size_max : float, default 200
            Maximum point size for numerical sizing
        point_size : float, default 100
            Base point size
        alpha : float, default 0.7
            Point transparency
        **kwargs
            Additional parameters passed to BasePlot
        """
        # Store scatter-specific parameters
        self.trendline = trendline
        self.color_continuous_scale = color_continuous_scale
        self.size_max = size_max
        self.point_size = point_size

        # Initialize base plot
        super().__init__(
            data=data,
            x=x,
            y=y,
            color=color,
            size=size,
            shape=shape,
            alpha=alpha,
            **kwargs,
        )

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_plot(self):
        """Create the scatter plot."""
        x_data, y_data = self._prepare_data()

        # Determine if color/size are numerical or categorical
        color_is_numerical = False
        size_is_numerical = False

        if isinstance(self.data, pd.DataFrame):
            if self.color and self.color in self.data.columns:
                color_is_numerical = pd.api.types.is_numeric_dtype(
                    self.data[self.color]
                )
            if self.size and self.size in self.data.columns:
                size_is_numerical = pd.api.types.is_numeric_dtype(self.data[self.size])

        # Prepare size data
        size_data = self.point_size  # Default size
        if self.size:
            if isinstance(self.data, pd.DataFrame) and isinstance(self.size, str):
                if size_is_numerical:
                    # Numerical size: scale between point_size and size_max
                    size_values = self.data[self.size]
                    size_min, size_max = size_values.min(), size_values.max()
                    if size_max > size_min:
                        size_data = self.point_size + (size_values - size_min) / (
                            size_max - size_min
                        ) * (self.size_max - self.point_size)
                    else:
                        size_data = self.point_size
                else:
                    # Categorical size: different fixed sizes
                    size_data = self.data[self.size] * (self.point_size / 5)
            elif isinstance(self.size, (list, np.ndarray)):
                size_data = np.array(self.size) * (self.point_size / 5)

        # Prepare color data and colormap
        color_data = None
        cmap = None
        if (
            self.color
            and isinstance(self.data, pd.DataFrame)
            and self.color in self.data.columns
        ):
            if color_is_numerical:
                # Numerical color: use colormap
                color_data = self.data[self.color]
                if self.color_continuous_scale:
                    cmap = self.color_continuous_scale
                else:
                    cmap = "viridis" if not self.dark_mode else "plasma"

        # Prepare shape (marker) data
        shape_data = None
        if (
            self.shape
            and isinstance(self.data, pd.DataFrame)
            and self.shape in self.data.columns
        ):
            shape_categories = self.data[self.shape].unique()
            markers = self._get_markers()
            shape_mapping = {
                cat: markers[i % len(markers)] for i, cat in enumerate(shape_categories)
            }
            shape_data = self.data[self.shape].map(shape_mapping.get)  # type: ignore[arg-type]

        # Main plotting logic
        if (
            self.color
            and isinstance(self.data, pd.DataFrame)
            and not color_is_numerical
        ):
            # Categorical color: group by color and plot separately
            self._plot_categorical_color(x_data, y_data, size_data, shape_data)
        else:
            # Single group or numerical color
            self._plot_single_or_numerical(
                x_data,
                y_data,
                size_data,
                shape_data,
                color_data,
                cmap,
                color_is_numerical,
            )

    def _plot_categorical_color(self, x_data, y_data, size_data, shape_data):
        """Plot scatter with categorical color grouping."""
        # Get consistent colors and order for categories
        unique_categories = self.data[self.color].unique()
        categories, colors = self._get_consistent_colors_and_order(unique_categories)

        # Create a color mapping dict for easy lookup
        color_map = {cat: colors[i] for i, cat in enumerate(categories)}

        grouped_data = self.data.groupby(self.color, observed=True)

        # Iterate through categories in the ordered sequence
        for i, cat in enumerate(categories):
            if cat not in grouped_data.groups:
                continue
            group = grouped_data.get_group(cat)
            name = cat
            group_x, group_y = self._prepare_data(group, self.x, self.y)

            # Get size for this group
            if isinstance(size_data, pd.Series):
                group_size = size_data.loc[group.index]
            elif hasattr(size_data, "__iter__") and not isinstance(
                size_data, (str, int, float)
            ):
                group_size = (
                    size_data[group.index]
                    if hasattr(size_data, "__getitem__")
                    else size_data
                )
            else:
                group_size = size_data

            # Get shapes for this group
            group_marker = "o"  # default
            if shape_data is not None:
                group_shapes = shape_data[group.index].unique()
                if len(group_shapes) == 1:
                    group_marker = group_shapes[0]
                else:
                    # Mixed shapes in group - plot each shape separately
                    for shape_val in group_shapes:
                        shape_mask = shape_data[group.index] == shape_val
                        shape_indices = group.index[shape_mask]
                        if len(shape_indices) > 0:  # type: ignore[arg-type]
                            self._plot_scatter_group(
                                group_x[shape_mask],
                                group_y[shape_mask],
                                (
                                    group_size[shape_mask]  # type: ignore[index]
                                    if hasattr(group_size, "__getitem__")
                                    else group_size
                                ),
                                color_map[name],
                                shape_val,
                                f"{name} ({shape_val})",
                                i,
                            )
                    continue

            # Plot this color group
            # Get color from the mapping
            color = color_map[name]
            self._plot_scatter_group(
                group_x,
                group_y,
                group_size,
                color,
                group_marker,
                str(name),
                i,
            )

            # Add trendline if requested
            if self.trendline == "ols":
                self._add_trendline(group_x, group_y, i)

        self._add_legend_with_spacing()

    def _plot_single_or_numerical(
        self,
        x_data,
        y_data,
        size_data,
        shape_data,
        color_data,
        cmap,
        color_is_numerical,
    ):
        """Plot single group or numerical color scatter."""
        scatter_kwargs = self.plot_kwargs.copy()

        # Set size parameter if not provided by user
        if "s" not in scatter_kwargs:
            scatter_kwargs["s"] = size_data

        # Set default zorder if not provided by user
        if "zorder" not in scatter_kwargs:
            scatter_kwargs["zorder"] = 3

        if color_is_numerical and color_data is not None:
            # Numerical color with colormap
            scatter_kwargs.update({"c": color_data, "cmap": cmap, "alpha": self.alpha})
            scatter = self.ax.scatter(x_data, y_data, **scatter_kwargs)
            # Add colorbar for numerical color
            cbar = plt.colorbar(scatter, ax=self.ax)
            if self.labels and self.color in self.labels:
                cbar.set_label(
                    self.labels[self.color],
                    fontsize=self.label_font_size,
                    fontweight="bold",
                )
            else:
                cbar.set_label(
                    self.color or "", fontsize=self.label_font_size, fontweight="bold"
                )
        else:
            # Single color
            marker = "o"
            if shape_data is not None:
                # Multiple shapes: plot each separately
                unique_shapes = shape_data.unique()
                for shape_val in unique_shapes:
                    shape_mask = shape_data == shape_val
                    if np.any(shape_mask):
                        self._plot_scatter_group(
                            x_data[shape_mask],
                            y_data[shape_mask],
                            (
                                size_data[shape_mask]
                                if hasattr(size_data, "__getitem__")
                                else size_data
                            ),
                            self.colors["accent"],
                            shape_val,
                            f"Shape: {shape_val}",
                            0,
                        )
                if len(unique_shapes) > 1:
                    self._add_legend_with_spacing()
            else:
                # Single shape
                # Determine color for this series
                color = self._get_next_color()

                # Update scatter_kwargs with color and marker
                scatter_kwargs.update(
                    {
                        "color": color,
                        "alpha": self.alpha,
                        "marker": marker,
                    }
                )

                # Add label if provided
                label_kwargs = self._get_plot_kwargs_with_label()
                if "label" in label_kwargs:
                    scatter_kwargs["label"] = label_kwargs["label"]

                self.ax.scatter(x_data, y_data, **scatter_kwargs)

        # Add trendline if requested
        if self.trendline == "ols":
            self._add_trendline(x_data, y_data, 0)

    def _plot_scatter_group(
        self, x_data, y_data, size_data, color, marker, label, series_index
    ):
        """Plot a single scatter group with consistent styling."""
        scatter_kwargs = self.plot_kwargs.copy()

        # Remove label from kwargs if present, as we'll set it explicitly
        scatter_kwargs.pop("label", None)

        # Set size parameter if not provided by user
        if "s" not in scatter_kwargs:
            scatter_kwargs["s"] = size_data

        if self.grayscale_friendly:
            # Use distinctive markers and keep full colors for b/w printing compatibility
            patterns = self._get_bw_patterns()
            bw_marker = patterns["markers"][series_index % len(patterns["markers"])]
            scatter_kwargs.update(
                {
                    "c": color,
                    "edgecolors": "black" if not self.dark_mode else "white",
                    "linewidth": 1.5,
                    "marker": bw_marker,
                    "alpha": (self.alpha or 0.7) + 0.1,
                }
            )
        else:
            scatter_kwargs.update(
                {"color": color, "alpha": self.alpha or 1.0, "marker": marker}
            )

        self.ax.scatter(x_data, y_data, label=label, **scatter_kwargs)

    def _add_trendline(self, x_data, y_data, series_index):
        """Add trendline to scatter plot."""
        if len(x_data) < 2:
            return

        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)

        if self.grayscale_friendly:
            patterns = self._get_bw_patterns()
            self.ax.plot(
                x_data,
                p(x_data),
                linestyle=patterns["linestyles"][
                    series_index % len(patterns["linestyles"])
                ],
                color=self.colors["colors"][series_index % len(self.colors["colors"])],
                alpha=0.8,
                linewidth=2,
            )
        else:
            color = (
                self.colors["colors"][series_index % len(self.colors["colors"])]
                if series_index < len(self.colors["colors"])
                else self.colors["accent"]
            )
            self.ax.plot(x_data, p(x_data), "--", color=color, alpha=0.5)

    def _create_faceted_plot(self):
        """Create faceted scatter plots."""
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


def scatter(data=None, x=None, y=None, **kwargs):
    """
    Create a scatter plot with Rekha styling.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data to plot
    x, y : str, list, array, or None
        Column names or data for x and y axes
    color : str, optional
        Column name for color grouping or numerical coloring
    size : str, list, array, or None
        Column name or data for point sizing
    shape : str, optional
        Column name for shape/marker grouping
    facet_row : str, optional
        Column name for creating subplot rows
    facet_col : str, optional
        Column name for creating subplot columns
    base_plot : BasePlot, optional
        Existing Rekha plot to add to. Enables composition of multiple plot types.
    trendline : str, optional
        Type of trendline ('ols' for linear regression)
    color_continuous_scale : str, optional
        Colormap for numerical color mapping
    size_max : float, default 200
        Maximum point size for numerical sizing
    point_size : float, default 100
        Base point size
    alpha : float, default 0.7
        Point transparency
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
    ScatterPlot
        Scatter plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> df = pd.DataFrame({'x': [1,2,3], 'y': [1,4,2], 'cat': ['A','B','A']})
    >>> fig = rk.scatter(df, x='x', y='y', color='cat', title='My Scatter Plot')
    >>> fig.show()
    """
    return ScatterPlot(data=data, x=x, y=y, **kwargs)
