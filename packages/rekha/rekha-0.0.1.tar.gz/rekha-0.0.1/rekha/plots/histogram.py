"""
Histogram plot implementation for Rekha.
"""

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from .base import BasePlot


class HistogramPlot(BasePlot):
    """Create a histogram with consistent Rekha interface."""

    def __init__(
        self,
        data=None,
        x=None,
        y=None,
        nbins: Optional[int] = None,
        marginal: Optional[str] = None,
        alpha: float = 0.7,
        **kwargs,
    ):
        """
        Create a histogram.

        Parameters
        ----------
        nbins : int, optional
            Number of bins (auto if None)
        marginal : str, optional
            Type of marginal plot ('box', 'violin')
        alpha : float, default 0.7
            Histogram transparency
        **kwargs
            Additional parameters passed to BasePlot
        """
        self.nbins = nbins
        self.marginal = marginal
        self.alpha = alpha

        # Validate marginal type
        if self.marginal is not None and self.marginal not in ["box", "violin"]:
            raise ValueError(
                f"Invalid marginal type '{self.marginal}'. Supported types: 'box', 'violin'"
            )

        # Initialize base plot
        super().__init__(data=data, x=x, y=y, **kwargs)

        # Create the plot
        if self.is_faceted:
            self._create_faceted_plot()
        else:
            self._create_plot()
            self._finalize_plot()
            self._show_legend_if_needed()

    def _create_figure(self):
        """Create matplotlib figure and axes with optional marginal."""
        if self.marginal:
            # Create subplots for marginal plot
            self.fig = plt.figure(figsize=self.figsize)
            gs = self.fig.add_gridspec(2, 1, height_ratios=[1, 4], hspace=0.05)
            self.ax_marginal = self.fig.add_subplot(gs[0])
            self.ax = self.fig.add_subplot(gs[1])

            # Hide x-axis for marginal plot
            self.ax_marginal.set_xticks([])
            self.ax_marginal.spines["bottom"].set_visible(False)
        else:
            self.fig, self.ax = plt.subplots(figsize=self.figsize)

        self.ax.tick_params(axis="both", which="major", labelsize=self.tick_font_size)

    def _create_plot(self):
        """Create the histogram."""
        # Handle grouped histograms
        if (
            self.color
            and isinstance(self.data, pd.DataFrame)
            and self.color in self.data.columns
        ):
            self._create_grouped_histograms()
        else:
            self._create_single_histogram()

    def _create_single_histogram(self):
        """Create a single histogram."""
        x_data, _ = self._prepare_data()

        # Create histogram
        hist_kwargs = self.plot_kwargs.copy()

        # Determine color for this series
        color = self._get_next_color()

        if self.grayscale_friendly:
            # For grayscale printing, add edge and hatch pattern
            patterns = self._get_bw_patterns()
            hist_kwargs.update(
                {
                    "color": color,
                    "alpha": self.alpha + 0.1,
                    "edgecolor": "black" if not self.dark_mode else "white",
                    "linewidth": 1.2,
                    "hatch": patterns["hatches"][
                        self._color_index % len(patterns["hatches"])
                    ],
                }
            )
        else:
            hist_kwargs.update(
                {
                    "color": color,
                    "alpha": self.alpha,
                    "edgecolor": "white",
                }
            )

        # Get kwargs with label
        hist_kwargs.update(self._get_plot_kwargs_with_label())

        # Handle bins parameter - use nbins if provided, otherwise check kwargs
        if "bins" not in hist_kwargs:
            hist_kwargs["bins"] = self.nbins or "auto"

        # Set default zorder if not provided
        if "zorder" not in hist_kwargs:
            hist_kwargs["zorder"] = 3

        n, bins, patches = self.ax.hist(x_data, **hist_kwargs)  # type: ignore[arg-type]

        # Add legend spacing if there's a label
        if "label" in hist_kwargs:
            self._add_legend_with_spacing()

        # Add marginal plot if requested
        self._add_marginal_plot()

    def _create_grouped_histograms(self):
        """Create grouped histograms with different colors."""
        x_data, _ = self._prepare_data()

        # Get consistent colors and order for categories
        unique_categories = self.data[self.color].unique()
        categories, colors = self._get_consistent_colors_and_order(unique_categories)

        # Create a color mapping dict for easy lookup
        color_map = {str(cat): colors[i] for i, cat in enumerate(categories)}

        # Group data by color column
        groups = self.data.groupby(self.color, observed=True)

        # Collect all data to determine common bins
        all_data = []
        group_data = []
        group_names = []

        for name, group in groups:
            group_x, _ = self._prepare_data(group, self.x, None)
            all_data.extend(group_x)  # type: ignore[arg-type]
            group_data.append(group_x)
            group_names.append(str(name))

        # Determine common bins for all groups
        bins = self.nbins or "auto"
        if bins == "auto":
            bins = min(30, max(10, int(len(all_data) ** 0.5)))

        # Plot each group
        for i, (data, name) in enumerate(zip(group_data, group_names)):
            # Get color from the mapping
            color = color_map[name]

            hist_kwargs = self.plot_kwargs.copy()

            if self.grayscale_friendly:
                patterns = self._get_bw_patterns()
                hist_kwargs.update(
                    {
                        "color": color,
                        "alpha": self.alpha + 0.1,
                        "edgecolor": "black" if not self.dark_mode else "white",
                        "linewidth": 1.2,
                        "hatch": patterns["hatches"][i % len(patterns["hatches"])],
                        "label": name,
                    }
                )
            else:
                hist_kwargs.update(
                    {
                        "color": color,
                        "alpha": self.alpha,
                        "edgecolor": "white",
                        "label": name,
                    }
                )

            # Set bins and zorder if not already in kwargs
            if "bins" not in hist_kwargs:
                hist_kwargs["bins"] = bins
            if "zorder" not in hist_kwargs:
                hist_kwargs["zorder"] = 3

            # Create histogram for this group
            n, bins_used, patches = self.ax.hist(data, **hist_kwargs)

        # Add legend with spacing
        self._add_legend_with_spacing()

        # Add marginal plot if requested
        self._add_marginal_plot()

    def _add_marginal_plot(self):
        """Add marginal plot if requested."""
        if not self.marginal or not hasattr(self, "ax_marginal"):
            return

        x_data, _ = self._prepare_data()

        if self.marginal == "box":
            self.ax_marginal.boxplot(
                x_data,  # type: ignore[arg-type]
                vert=False,
                widths=0.7,
                patch_artist=True,
                boxprops=dict(facecolor=self.colors["accent"], alpha=0.7),
                medianprops=dict(color=self.colors["text"]),
            )
            self.ax_marginal.set_ylim(0.5, 1.5)
            self.ax_marginal.set_xlim(self.ax.get_xlim())
        elif self.marginal == "violin":
            parts = self.ax_marginal.violinplot(x_data, vert=False, widths=0.7)  # type: ignore[arg-type]
            for pc in parts["bodies"]:  # type: ignore[attr-defined]
                pc.set_facecolor(self.colors["accent"])
                pc.set_alpha(0.7)
            self.ax_marginal.set_xlim(self.ax.get_xlim())

    def _create_faceted_plot(self):
        """Create faceted histogram plots."""
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


def histogram(data=None, x=None, **kwargs):
    """
    Create a histogram with Rekha styling.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data to plot
    x : str, list, array, or None
        Column name or data for histogram
    nbins : int, optional
        Number of bins (auto if None)
    marginal : str, optional
        Type of marginal plot ('box', 'violin')
    alpha : float, default 0.7
        Histogram transparency
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
    HistogramPlot
        Histogram plot object with matplotlib figure and axes

    Examples
    --------
    >>> import rekha as rk
    >>> import pandas as pd
    >>> df = pd.DataFrame({'values': [1,2,2,3,3,3,4,4,5]})
    >>> fig = rk.histogram(df, x='values', title='Distribution')
    >>> fig.show()
    """
    return HistogramPlot(data=data, x=x, **kwargs)
