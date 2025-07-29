"""
Box plot implementation for Rekha.
"""

import pandas as pd

from .base import BasePlot


class BoxPlot(BasePlot):
    """Create a box plot with consistent Rekha interface."""

    def __init__(self, data=None, x=None, y=None, color=None, **kwargs):
        """
        Create a box plot.

        Parameters
        ----------
        **kwargs
            Additional parameters passed to BasePlot
        """
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
        """Create the box plot."""
        if isinstance(self.data, pd.DataFrame):
            if self.x and not self.color:
                # Group by x
                groups = self.data.groupby(self.x, observed=True)[self.y].apply(list)

                # Get consistent colors and order for x categories
                categories, colors = self._get_consistent_colors_and_order(groups.index)

                # Reorder groups to match the ordered categories
                groups = groups[categories]
                positions = range(len(groups))

                bp = self.ax.boxplot(
                    groups.values,
                    positions=positions,
                    patch_artist=True,
                    **self.plot_kwargs,
                )

                # Color the boxes with consistent colors
                for i, box in enumerate(bp["boxes"]):
                    # Get color from the consistent mapping
                    color = colors[i]
                    box.set_facecolor(color)
                    box.set_alpha(0.7)

                    # Apply grayscale patterns
                    if self.grayscale_friendly:
                        patterns = self._get_bw_patterns()
                        box.set_hatch(patterns["hatches"][i % len(patterns["hatches"])])
                        box.set_edgecolor("black" if not self.dark_mode else "white")
                        box.set_linewidth(1.5)

                # Style whiskers, caps, medians, and fliers
                self._style_boxplot_elements(bp)

                self.ax.set_xticks(positions)
                self.ax.set_xticklabels(groups.index)

            elif self.color:
                # Group by color for side-by-side boxes
                # Get consistent colors and order for categories
                unique_categories = self.data[self.color].unique()
                categories, colors = self._get_consistent_colors_and_order(
                    unique_categories
                )

                # Create a color mapping dict for easy lookup
                color_map = {cat: colors[i] for i, cat in enumerate(categories)}

                color_groups = self.data.groupby(self.color, observed=True)
                n_colors = len(color_groups)
                width = 0.8 / n_colors

                for i, (color_name, color_data) in enumerate(color_groups):
                    if self.x:
                        x_groups = color_data.groupby(self.x, observed=True)[
                            self.y
                        ].apply(list)
                        positions = [j + i * width for j in range(len(x_groups))]
                    else:
                        x_groups = pd.Series([color_data[self.y].values])
                        positions = [i * width]

                    bp = self.ax.boxplot(
                        x_groups.values,
                        positions=positions,
                        widths=width * 0.8,
                        patch_artist=True,
                        label=str(color_name),
                        **self.plot_kwargs,
                    )

                    # Color the boxes
                    for box in bp["boxes"]:
                        box.set_facecolor(color_map[color_name])
                        box.set_alpha(0.7)

                        # Apply grayscale patterns
                        if self.grayscale_friendly:
                            patterns = self._get_bw_patterns()
                            box.set_hatch(
                                patterns["hatches"][i % len(patterns["hatches"])]
                            )
                            box.set_edgecolor(
                                "black" if not self.dark_mode else "white"
                            )
                            box.set_linewidth(1.5)

                    # Style whiskers, caps, medians, and fliers
                    self._style_boxplot_elements(bp)

                if self.x:
                    self.ax.set_xticks(
                        [j + width * (n_colors - 1) / 2 for j in range(len(x_groups))]  # type: ignore[possibly-unbound]
                    )
                    self.ax.set_xticklabels(x_groups.index)  # type: ignore[possibly-unbound]

                self._add_legend_with_spacing()
            else:
                # Single box plot
                bp = self.ax.boxplot(
                    [self.data[self.y].values], patch_artist=True, **self.plot_kwargs
                )

                # Determine color for this series
                color = self._get_next_color()

                bp["boxes"][0].set_facecolor(color)
                bp["boxes"][0].set_alpha(0.7)

                # Apply grayscale patterns
                if self.grayscale_friendly:
                    patterns = self._get_bw_patterns()
                    bp["boxes"][0].set_hatch(patterns["hatches"][0])
                    bp["boxes"][0].set_edgecolor(
                        "black" if not self.dark_mode else "white"
                    )
                    bp["boxes"][0].set_linewidth(1.5)

                # Style whiskers, caps, medians, and fliers
                self._style_boxplot_elements(bp)

    def _style_boxplot_elements(self, bp):
        """Style boxplot whiskers, caps, medians, and fliers for proper theme visibility."""
        # Set color based on theme
        element_color = self.colors["text"]

        # Style whiskers (vertical lines extending from boxes)
        for whisker in bp["whiskers"]:
            whisker.set_color(element_color)
            whisker.set_linewidth(1.5)

        # Style caps (horizontal lines at end of whiskers)
        for cap in bp["caps"]:
            cap.set_color(element_color)
            cap.set_linewidth(1.5)

        # Style medians (horizontal lines in middle of boxes)
        for median in bp["medians"]:
            median.set_color(element_color)
            median.set_linewidth(2)

        # Style fliers (outlier points)
        for flier in bp["fliers"]:
            flier.set_markerfacecolor(element_color)
            flier.set_markeredgecolor(element_color)
            flier.set_markersize(4)

    def _create_faceted_plot(self):
        """Create faceted box plots."""
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


def box(data=None, x=None, y=None, color=None, **kwargs):
    """
    Create a box plot with Rekha styling.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data to plot
    x : str, optional
        Column name for grouping variable
    y : str, list, array, or None
        Column name or data for box plot values
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
        Whether to add patterns for grayscale printing
    **kwargs
        Additional styling parameters

    Returns
    -------
    BoxPlot
        Box plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     'category': ['A', 'B', 'A', 'B', 'A', 'B'],
    ...     'values': [1, 2, 3, 4, 5, 6]
    ... })
    >>> fig = rk.box(df, x='category', y='values', title='Box Plot')
    >>> fig.show()
    """
    return BoxPlot(data=data, x=x, y=y, color=color, **kwargs)
