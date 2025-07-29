"""
Base plot class with common functionality for all Rekha plots.
"""

from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..theme import set_rekha_theme


class BasePlot:
    """
    Base class for all Rekha plots providing common functionality and consistent interface.

    This class implements all shared functionality across different plot types including:

    * Theme management (light/dark modes)
    * Color palette handling
    * Font size and styling options
    * Grid and layout configuration
    * Grayscale printing support
    * Data preparation and validation
    * Export functionality with format optimization

    All plot types in Rekha inherit from this class to ensure a uniform API
    and consistent styling options across the entire library.

    Attributes
    ----------
    fig : matplotlib.figure.Figure
        The matplotlib figure object
    ax : matplotlib.axes.Axes
        The matplotlib axes object
    colors : dict
        Color palette and theme configuration
    data : DataFrame, dict, or None
        The input data for plotting

    Examples
    --------
    This class is not meant to be used directly. Instead, use the specific
    plot functions like `line()`, `scatter()`, `bar()`, etc.

    >>> import rekha as rk
    >>> import pandas as pd
    >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    >>> fig = rk.line(df, x='x', y='y')  # Uses LinePlot(BasePlot)
    >>> fig.show()
    """

    def __init__(
        self,
        data: Union[pd.DataFrame, Dict, None] = None,
        x: Union[str, List, np.ndarray, None] = None,
        y: Union[str, List, np.ndarray, None] = None,
        color: Optional[str] = None,
        size: Union[str, List, np.ndarray, None] = None,
        shape: Optional[str] = None,
        facet_row: Optional[str] = None,
        facet_col: Optional[str] = None,
        base_plot: Optional["BasePlot"] = None,
        title: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        dark_mode: bool = False,
        figsize: Tuple[float, float] = (10, 6),
        title_font_size: float = 16,
        label_font_size: float = 14,
        tick_font_size: float = 12,
        legend_font_size: float = 12,
        legend_loc: str = "best",
        grid: bool = True,
        grid_alpha: float = 0.6,
        grid_linewidth: float = 0.5,
        grayscale_friendly: bool = False,
        color_mapping: Optional[Dict[str, str]] = None,
        category_order: Optional[List[str]] = None,
        # Faceting parameters
        share_x: bool = True,
        share_y: bool = True,
        subplot_titles: bool = True,
        col_wrap: Optional[int] = None,
        row_wrap: Optional[int] = None,
        subplot_spacing: float = 0.3,
        margin_spacing: float = 0.1,
        # Theme and styling parameters
        palette: str = "rekha",
        # Axis scale parameters
        xscale: Optional[str] = None,
        yscale: Optional[str] = None,
        # Humanized formatting parameters
        humanize_units: bool = False,
        humanize_format: str = "intword",
        # Tick rotation
        rotate_xticks: Union[bool, float] = False,
        # Common matplotlib parameters
        alpha: Optional[float] = None,
        label: Optional[str] = None,
        edgecolor: Optional[str] = None,
        linewidth: Optional[float] = None,
        zorder: Optional[float] = None,
        **kwargs,
    ):
        """
        Initialize base plot with common parameters.

        This constructor sets up all the common functionality that every Rekha plot
        needs, including theme configuration, data handling, and styling options.

        Parameters
        ----------
        data : pd.DataFrame, dict, or None
            The data to plot. Can be:

            * pandas DataFrame with named columns
            * Dictionary with array-like values
            * None if x/y are provided directly as arrays

        x : str, list, array, or None
            X-axis data specification:

            * str: Column name in `data`
            * array-like: Direct data values
            * None: Use index or default values

        y : str, list, array, or None
            Y-axis data specification (same format as `x`)

        color : str, optional
            Column name in `data` for color grouping. Creates different colors
            for each unique value in this column.

        size : str, list, array, or None
            Column name or data for point/marker sizing (scatter plots)

        shape : str, optional
            Column name in `data` for marker shape grouping (scatter plots)

        facet_row : str, optional
            Column name in `data` for creating subplot rows. Each unique value
            in this column creates a separate row of subplots.

        facet_col : str, optional
            Column name in `data` for creating subplot columns. Each unique value
            in this column creates a separate column of subplots.

        base_plot : BasePlot, optional
            Existing Rekha plot to add to. If provided, this plot will be added
            to the existing plot's axes instead of creating a new figure. This
            enables composition of multiple plot types while staying within the
            Rekha API.

        title : str, optional
            Plot title text

        labels : dict, optional
            Custom axis labels. Maps column names to display labels.
            Example: ``{'x_col': 'X Axis Label', 'y_col': 'Y Axis Label'}``

        dark_mode : bool, default False
            Whether to use dark theme. When True:

            * Uses dark background colors
            * Switches to light text and grid colors
            * Adjusts color palette for dark backgrounds

        figsize : tuple, default (10, 6)
            Figure size as (width, height) in inches

        title_font_size : float, default 16
            Font size for the plot title

        label_font_size : float, default 14
            Font size for axis labels

        tick_font_size : float, default 12
            Font size for axis tick labels

        legend_font_size : float, default 12
            Font size for legend text
        legend_loc : str, default 'best'
            Legend location ('best', 'upper right', 'upper left', 'lower left',
            'lower right', 'right', 'center left', 'center right', 'lower center',
            'upper center', 'center')

        grid : bool, default True
            Whether to show grid lines

        grid_alpha : float, default 0.6
            Transparency of grid lines (0=invisible, 1=opaque)

        grid_linewidth : float, default 0.5
            Width of grid lines in points

        grayscale_friendly : bool, default False
            Whether to optimize for grayscale printing:

            * Uses patterns/hatching for differentiation
            * Increases contrast and line weights
            * Uses distinctive markers and line styles

        color_mapping : dict, optional
            Custom mapping of category values to colors.
            Example: ``{'Category A': 'red', 'Category B': 'blue'}``

        category_order : list, optional
            Custom ordering for categorical data. Affects legend order
            and color assignment.

        share_x : bool, default True
            Whether to share x-axis across facets. When True, all subplots
            will have the same x-axis range for easier comparison.

        share_y : bool, default True
            Whether to share y-axis across facets. When True, all subplots
            will have the same y-axis range for easier comparison.

        subplot_titles : bool, default True
            Whether to automatically generate titles for each subplot based
            on the faceting variables and their values.

        col_wrap : int, optional
            Maximum number of columns before wrapping to a new row. Useful
            when faceting by a variable with many categories.

        row_wrap : int, optional
            Maximum number of rows before wrapping to a new column. Useful
            when faceting by a variable with many categories.

        subplot_spacing : float, default 0.3
            Spacing between subplots as a fraction of subplot size.
            Higher values create more space between plots.

        margin_spacing : float, default 0.1
            Margin spacing around the entire figure as a fraction of figure size.
            Controls space for overall title and axis labels.

        palette : str, default 'rekha'
            Color palette to use. Options include 'rekha' (default), 'pastel',
            'bright', 'muted', 'colorblind', etc.

        xscale : str, optional
            X-axis scale type. Options: 'linear', 'log', 'symlog', 'logit'.
            If None, uses matplotlib's default (usually 'linear').

        yscale : str, optional
            Y-axis scale type. Options: 'linear', 'log', 'symlog', 'logit'.
            If None, uses matplotlib's default (usually 'linear').

        humanize_units : bool, default False
            Whether to format axis tick labels in human-readable form.
            For example, 1000000 becomes '1M', 1500 becomes '1.5K'.

        humanize_format : str, default 'intword'
            Format style for humanized numbers:

            * 'intword': Convert to words (1M, 2.5K)
            * 'intcomma': Add commas (1,000,000)
            * 'scientific': Scientific notation (1.0e6)
            * 'fractional': Convert to fractions where applicable

        rotate_xticks : bool or float, default False
            Whether to rotate x-axis tick labels:

            * False: No rotation (default)
            * True: Rotate 45 degrees
            * float: Rotate by specified degrees (e.g., 30, 45, 90)

        alpha : float, optional
            Transparency level for plot elements (0=transparent, 1=opaque).
            Applies to bars, areas, markers, etc. depending on plot type.

        label : str, optional
            Label for this data series in the legend. If provided, a legend
            will be automatically shown.

        edgecolor : str, optional
            Color for edges of plot elements (bars, markers, etc.).
            Can be a color name, hex code, or RGB tuple.

        linewidth : float, optional
            Width of lines or edges in points. Applies to different elements
            depending on plot type (e.g., bar edges, line plots, marker edges).

        zorder : float, optional
            Drawing order for plot elements. Higher values are drawn on top.
            Useful for layering multiple plots.

        **kwargs
            Additional keyword arguments passed to the specific plot type.
            These are plot-specific and passed through to matplotlib functions.

        Notes
        -----
        This class handles the common initialization for all Rekha plots.
        Specific plot types add their own parameters and override methods
        as needed while maintaining this consistent base interface.

        The color system automatically handles:

        * Categorical color mapping with consistent palettes
        * Dark/light theme switching
        * Grayscale printing optimization
        * Custom color overrides via `color_mapping`
        """
        # Store all parameters
        self.data = data
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.shape = shape
        self.facet_row = facet_row
        self.facet_col = facet_col
        self.base_plot = base_plot
        self.title = title
        self.labels = labels or {}
        self.dark_mode = dark_mode
        self.palette = palette
        self.figsize = figsize
        self.title_font_size = title_font_size
        self.label_font_size = label_font_size
        self.tick_font_size = tick_font_size
        self.legend_font_size = legend_font_size
        self.legend_loc = legend_loc
        self.grid = grid
        self.grid_alpha = grid_alpha
        self.grid_linewidth = grid_linewidth
        self.grayscale_friendly = grayscale_friendly
        self.color_mapping = color_mapping or {}
        self.category_order = category_order

        # Faceting parameters
        self.share_x = share_x
        self.share_y = share_y
        self.subplot_titles = subplot_titles
        self.col_wrap = col_wrap
        self.row_wrap = row_wrap
        self.subplot_spacing = subplot_spacing
        self.margin_spacing = margin_spacing

        # Store the scale and formatting parameters
        self.xscale = xscale
        self.yscale = yscale
        self.humanize_units = humanize_units
        self.humanize_format = humanize_format
        self.rotate_xticks = rotate_xticks

        # Store common matplotlib parameters
        self.alpha = alpha
        self.label = label
        self.edgecolor = edgecolor
        self.linewidth = linewidth
        self.zorder = zorder

        # Build plot_kwargs from explicit matplotlib parameters
        self.plot_kwargs = {}
        if alpha is not None:
            self.plot_kwargs["alpha"] = alpha
        if label is not None:
            self.plot_kwargs["label"] = label
        if edgecolor is not None:
            self.plot_kwargs["edgecolor"] = edgecolor
        if linewidth is not None:
            self.plot_kwargs["linewidth"] = linewidth
        if zorder is not None:
            self.plot_kwargs["zorder"] = zorder

        # Add any remaining kwargs
        self.plot_kwargs.update(kwargs)

        # Check if we need faceting
        self.is_faceted = (facet_row is not None) or (facet_col is not None)

        # Check if we're composing on an existing plot
        self.is_composite = base_plot is not None

        # Initialize matplotlib objects
        self.fig = None
        self.ax = None
        self.axes = None  # For faceted plots
        self.colors = None
        self._color_index = 0  # Track which color to use next

        # If composing, inherit from base plot
        if self.is_composite:
            if base_plot.is_faceted:
                raise ValueError("Cannot compose on faceted plots")
            self.fig = base_plot.fig
            self.ax = base_plot.ax
            self.colors = base_plot.colors
            self.dark_mode = base_plot.dark_mode
            self.grayscale_friendly = base_plot.grayscale_friendly
            # Inherit and increment color index
            self._color_index = getattr(base_plot, "_color_index", 0) + 1
            # Don't create a new figure
        else:
            # Apply theme and create figure
            self._apply_theme()
            if self.is_faceted:
                self._create_faceted_figure()
            else:
                self._create_figure()

    def _apply_theme(self):
        """Apply the Rekha theme."""
        self.colors = set_rekha_theme(self.dark_mode, self.palette)

    def _create_figure(self):
        """Create matplotlib figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.tick_params(axis="both", which="major", labelsize=self.tick_font_size)

    def _create_faceted_figure(self):
        """Create matplotlib figure and axes for faceted plots."""
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Faceting requires data to be a pandas DataFrame")

        # Get unique values for faceting
        row_values = []
        col_values = []

        if self.facet_row:
            row_values = sorted(self.data[self.facet_row].unique())
        else:
            row_values = [None]  # Single row

        if self.facet_col:
            col_values = sorted(self.data[self.facet_col].unique())
        else:
            col_values = [None]  # Single column

        # Apply wrapping
        if self.col_wrap and len(col_values) > self.col_wrap:
            # Reshape columns into multiple rows
            total_subplots = len(row_values) * len(col_values)
            n_cols = self.col_wrap
            n_rows = (total_subplots + n_cols - 1) // n_cols  # Ceiling division
            wrapped_layout = True
        elif self.row_wrap and len(row_values) > self.row_wrap:
            # Reshape rows into multiple columns
            total_subplots = len(row_values) * len(col_values)
            n_rows = self.row_wrap
            n_cols = (total_subplots + n_rows - 1) // n_rows  # Ceiling division
            wrapped_layout = True
        else:
            n_rows = len(row_values)
            n_cols = len(col_values)
            wrapped_layout = False

        # Store original facet grid dimensions for mapping
        self.original_n_rows = len(row_values)
        self.original_n_cols = len(col_values)

        # Calculate figure size with spacing
        base_width = self.figsize[0]
        base_height = self.figsize[1]

        # Adjust for margins and spacing
        subplot_width = base_width / max(1, n_cols) * (1 - self.margin_spacing)
        subplot_height = base_height / max(1, n_rows) * (1 - self.margin_spacing)

        fig_width = (
            subplot_width * n_cols * (1 + self.subplot_spacing)
            + base_width * self.margin_spacing
        )
        fig_height = (
            subplot_height * n_rows * (1 + self.subplot_spacing)
            + base_height * self.margin_spacing
        )

        # Create subplots with sharing
        sharex = "all" if self.share_x else False
        sharey = "all" if self.share_y else False

        self.fig, self.axes = plt.subplots(
            n_rows,
            n_cols,
            figsize=(fig_width, fig_height),
            squeeze=False,
            sharex=sharex,
            sharey=sharey,
        )

        # Store facet information
        self.facet_row_values = row_values
        self.facet_col_values = col_values
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.wrapped_layout = wrapped_layout

        # Configure spacing
        self.fig.subplots_adjust(
            hspace=self.subplot_spacing,
            wspace=self.subplot_spacing,
            left=self.margin_spacing,
            right=1 - self.margin_spacing / 2,
            top=1 - self.margin_spacing,
            bottom=self.margin_spacing,
        )

        # Configure each subplot
        for i in range(n_rows):
            for j in range(n_cols):
                ax = self.axes[i, j]
                ax.tick_params(
                    axis="both", which="major", labelsize=self.tick_font_size
                )

        # Set up the first axes as the default (for compatibility)
        self.ax = self.axes[0, 0]

    def _prepare_data(self, data_override=None, x_override=None, y_override=None):
        """
        Extract x and y data from various input formats.

        Returns
        -------
        tuple
            (x_data, y_data) arrays
        """
        data_to_use = data_override if data_override is not None else self.data
        x_to_use = x_override if x_override is not None else self.x
        y_to_use = y_override if y_override is not None else self.y

        if isinstance(data_to_use, pd.DataFrame):
            x_data = data_to_use[x_to_use] if isinstance(x_to_use, str) else x_to_use
            y_data = data_to_use[y_to_use] if isinstance(y_to_use, str) else y_to_use
        elif isinstance(data_to_use, dict):
            x_data = (
                data_to_use.get(x_to_use, x_to_use)
                if isinstance(x_to_use, str)
                else x_to_use
            )
            y_data = (
                data_to_use.get(y_to_use, y_to_use)
                if isinstance(y_to_use, str)
                else y_to_use
            )
        else:
            x_data = x_to_use
            y_data = y_to_use

        return x_data, y_data

    def _get_consistent_colors_and_order(self, categories):
        """Get consistent colors and ordering for categories."""
        if hasattr(categories, "tolist"):
            categories = categories.tolist()
        elif not isinstance(categories, list):
            categories = list(categories)

        # Apply custom ordering if specified
        if self.category_order:
            ordered_categories = []
            for cat in self.category_order:
                if cat in categories:
                    ordered_categories.append(cat)
            for cat in categories:
                if cat not in ordered_categories:
                    ordered_categories.append(cat)
            categories = ordered_categories
        else:
            categories = sorted(categories)

        # Assign colors
        colors = []
        for i, cat in enumerate(categories):
            if str(cat) in self.color_mapping:
                colors.append(self.color_mapping[str(cat)])
            else:
                colors.append(self.colors["colors"][i % len(self.colors["colors"])])

        return categories, colors

    def _get_bw_patterns(self):
        """Get patterns for grayscale printing compatibility."""
        if not self.grayscale_friendly:
            return {}

        return {
            "hatches": ["", "///", "...", "xxx", "\\\\\\", "||", "--", "++", "**"],
            "linestyles": [
                "-",
                "--",
                "-.",
                ":",
                (0, (3, 1, 1, 1)),
                (0, (5, 2)),
                (0, (1, 1)),
                (0, (3, 5, 1, 5)),
            ],
            "markers": ["o", "s", "^", "D", "v", ">", "<", "p", "*", "h"],
        }

    def _get_markers(self):
        """Get marker patterns for shape mapping."""
        return ["o", "s", "^", "D", "v", ">", "<", "p", "*", "h"]

    def _setup_grid(self):
        """Setup grid with proper z-order to appear behind plot elements."""
        if self.grid:
            self.ax.grid(
                True, alpha=self.grid_alpha, linewidth=self.grid_linewidth, zorder=-10
            )
            # Force grid to render below all plot elements
            self.ax.set_axisbelow(True)
        else:
            self.ax.grid(False)

    def _apply_labels(self):
        """Apply axis labels based on configuration."""
        if self.labels:
            xlabel = self.labels.get(self.x, self.x) if isinstance(self.x, str) else ""
            ylabel = self.labels.get(self.y, self.y) if isinstance(self.y, str) else ""
        else:
            xlabel = self.x if isinstance(self.x, str) else ""
            ylabel = self.y if isinstance(self.y, str) else ""

        if xlabel:
            self.ax.set_xlabel(xlabel, fontsize=self.label_font_size, fontweight="bold")
        if ylabel:
            self.ax.set_ylabel(ylabel, fontsize=self.label_font_size, fontweight="bold")

    def _apply_title(self):
        """Apply title if specified."""
        if self.title:
            self.ax.set_title(
                self.title, fontsize=self.title_font_size, fontweight="500", pad=20
            )

    def _apply_scales(self):
        """Apply axis scales if specified."""
        if self.xscale:
            self.ax.set_xscale(self.xscale)
        if self.yscale:
            self.ax.set_yscale(self.yscale)

    def _apply_humanized_formatting(self):
        """Apply humanized number formatting to axes."""
        if not self.humanize_units:
            return

        import humanize
        import matplotlib.ticker as ticker

        def humanize_formatter(x, pos):
            """Format numbers in human-readable form."""
            if self.humanize_format == "intword":
                return humanize.intword(x)
            elif self.humanize_format == "intcomma":
                return humanize.intcomma(x)
            elif self.humanize_format == "scientific":
                return humanize.scientific(x)
            elif self.humanize_format == "fractional":
                return humanize.fractional(x)
            else:
                return str(x)

        # Apply to y-axis by default (most common for bar charts, etc.)
        self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(humanize_formatter))

        # For horizontal bar charts, apply to x-axis instead
        if hasattr(self, "orientation") and self.orientation == "h":
            self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(humanize_formatter))
            self.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

    def _adjust_tick_density(self, ax=None):
        """Dynamically adjust tick density based on plot size and label width."""
        if ax is None:
            ax = self.ax

        # Get current x-tick labels
        labels = ax.get_xticklabels()
        if not labels:
            return

        # Get plot width in inches and convert to approximate pixels
        fig_width_inch = ax.get_figure().get_figwidth()
        axes_bbox = ax.get_position()
        ax_width_inch = fig_width_inch * axes_bbox.width
        ax_width_pixels = ax_width_inch * 72  # 72 DPI assumption

        # Estimate average label width (in pixels)
        # Use a conservative estimate based on font size
        avg_char_width = self.tick_font_size * 0.6  # Approximate pixels per character
        max_label_length = max(len(str(label.get_text())) for label in labels)
        estimated_label_width = max_label_length * avg_char_width

        # Add padding between labels
        label_padding = 20  # pixels
        total_label_width = estimated_label_width + label_padding

        # Calculate ideal number of ticks
        ideal_num_ticks = int(ax_width_pixels / total_label_width)
        ideal_num_ticks = max(2, min(ideal_num_ticks, 10))  # Between 2 and 10 ticks

        # Apply the calculated number of ticks
        current_ticks = ax.get_xticks()
        if len(current_ticks) > ideal_num_ticks:
            # Reduce number of ticks
            step = max(1, len(current_ticks) // ideal_num_ticks)
            new_ticks = current_ticks[::step]
            ax.set_xticks(new_ticks)

        # For dates, use matplotlib's auto date formatter with max ticks
        if any(
            isinstance(label.get_text(), str) and "-" in label.get_text()
            for label in labels
        ):
            from matplotlib.dates import AutoDateFormatter, AutoDateLocator

            locator = AutoDateLocator(maxticks=ideal_num_ticks)
            formatter = AutoDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

        # Only rotate labels if explicitly requested or if severe overlap is likely
        # Don't auto-rotate by default - let the user decide
        if self.rotate_xticks:
            labels = ax.get_xticklabels()
            rotation = (
                self.rotate_xticks
                if isinstance(self.rotate_xticks, (int, float))
                else 45
            )
            for label in labels:
                label.set_rotation(rotation)
                label.set_ha("right" if rotation > 0 else "center")

    def _finalize_plot(self):
        """Apply common finalization steps."""
        if not self.is_composite:
            self._apply_labels()
            self._apply_title()
            self._setup_grid()
            self._apply_scales()
            self._apply_humanized_formatting()
            self._adjust_tick_density()

    def update_layout(self, **kwargs):
        """
        Update plot layout - matplotlib style.

        Parameters
        ----------
        title : str, optional
            Plot title
        xlabel : str, optional
            X-axis label
        ylabel : str, optional
            Y-axis label
        xlim : tuple, optional
            X-axis limits
        ylim : tuple, optional
            Y-axis limits
        xscale : str, optional
            X-axis scale ('linear', 'log', 'symlog', 'logit')
        yscale : str, optional
            Y-axis scale ('linear', 'log', 'symlog', 'logit')
        """
        if "title" in kwargs:
            self.ax.set_title(
                kwargs["title"], fontsize=self.title_font_size, fontweight="500", pad=20
            )
        if "xlabel" in kwargs:
            self.ax.set_xlabel(
                kwargs["xlabel"], fontsize=self.label_font_size, fontweight="bold"
            )
        if "ylabel" in kwargs:
            self.ax.set_ylabel(
                kwargs["ylabel"], fontsize=self.label_font_size, fontweight="bold"
            )
        if "xlim" in kwargs:
            self.ax.set_xlim(kwargs["xlim"])
        if "ylim" in kwargs:
            self.ax.set_ylim(kwargs["ylim"])
        if "xscale" in kwargs:
            self.ax.set_xscale(kwargs["xscale"])
        if "yscale" in kwargs:
            self.ax.set_yscale(kwargs["yscale"])
        return self

    def add_annotation(self, text: str, x: float, y: float, **kwargs):
        """Add annotation to the plot."""
        self.ax.annotate(text, xy=(x, y), **kwargs)
        return self

    def show(self):
        """
        Display the plot in the current output (Jupyter notebook, script, etc.).

        This method automatically handles layout optimization and displays
        the plot using matplotlib's show() function. In Jupyter notebooks,
        the plot will appear inline. In scripts, it will open in a new window.

        Notes
        -----
        This method calls ``plt.tight_layout()`` before showing to ensure
        proper spacing of plot elements.

        Examples
        --------
        >>> import rekha as rk
        >>> import pandas as pd
        >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        >>> fig = rk.line(df, x='x', y='y', title='Sample Plot')
        >>> fig.show()  # Display the plot
        """
        plt.tight_layout()
        plt.show()

    def get_axes(self):
        """
        Get all axes from the figure.

        Returns
        -------
        list of matplotlib.axes.Axes
            Always returns a list of axes objects for consistent API:
            - Single plots: list with one axes object
            - Faceted plots: flat list of all axes

        Examples
        --------
        >>> fig = rk.scatter(df, x='x', y='y')
        >>> ax = fig.get_axes()[0]  # Get the single axes
        >>> ax.set_title("Custom Title")

        >>> fig = rk.scatter(df, x='x', y='y', facet_col='category')
        >>> axes = fig.get_axes()  # List of all axes
        >>> for ax in axes:
        ...     ax.grid(True)
        """
        if self.is_faceted:
            # Return flat list of all axes for easy iteration
            return self.axes.flatten()
        else:
            return [self.ax]

    def _repr_html_(self):
        """
        IPython/Jupyter notebook representation.

        This method enables automatic display of plots in Jupyter notebooks
        without needing to call show().
        """
        # Import here to avoid dependency issues
        try:
            from IPython.display import display

            plt.tight_layout()
            display(self.fig)
            return ""
        except ImportError:
            # Fall back to standard representation if not in IPython
            return repr(self)

    def save(
        self,
        filename: str,
        format: str = "auto",
        transparent: Optional[bool] = None,
        **kwargs,
    ):
        """
        Save the plot to file with optimized settings for different use cases.

        This method provides intelligent export options optimized for different
        contexts. It automatically adjusts resolution, format, and other settings
        based on the intended use case.

        Parameters
        ----------
        filename : str
            Output filename. Extension will be auto-added if not provided
            when using format presets.

        format : str, default 'auto'
            Export format preset with optimized settings:

            * **'web'**: SVG with transparent background, perfect for websites
              and documentation. Vector format scales perfectly.
            * **'paper'**: PDF with white background and high quality,
              ideal for academic papers and publications.
            * **'social'**: High-resolution PNG (300 DPI) with transparent background
              by default, for social media, presentations, and online sharing.
            * **'presentation'**: PNG optimized for slides with good balance
              of file size and quality.
            * **'auto'**: Automatically detect format from file extension:

              - ``.svg`` → 'web' format
              - ``.pdf`` → 'paper' format
              - ``.png``, ``.jpg``, ``.jpeg`` → 'social' format

        transparent : bool, optional
            Whether to use transparent background. If None (default), uses:
            - True for PNG formats (social, presentation)
            - True for SVG format (web)
            - False for PDF format (paper)
            - Can be overridden by setting explicitly

        **kwargs
            Additional parameters passed to matplotlib's ``savefig()``.
            These override the format preset defaults.

        Examples
        --------
        >>> import rekha as rk
        >>> fig = rk.scatter(df, x='x', y='y')
        >>>
        >>> # Save for web (SVG with transparency)
        >>> fig.save('plot.svg', format='web')
        >>>
        >>> # Save for academic paper (high-quality PDF)
        >>> fig.save('figure1.pdf', format='paper')
        >>>
        >>> # Save for social media (high-res PNG with transparency)
        >>> fig.save('chart.png', format='social')
        >>>
        >>> # Save with solid background
        >>> fig.save('chart.png', format='social', transparent=False)
        >>>
        >>> # Auto-detect from extension
        >>> fig.save('plot.png')  # Uses 'social' format with transparency
        >>>
        >>> # Custom settings with white background
        >>> fig.save('plot.png', format='social', dpi=450, transparent=False)

        Notes
        -----
        The method automatically calls ``plt.tight_layout()`` before saving
        to ensure optimal spacing. Each format preset is optimized for its
        intended use case:

        * **Web**: Vector format, small file size, scales perfectly
        * **Paper**: High quality, white background, publication-ready
        * **Social**: High resolution, transparent by default for versatility
        * **Presentation**: Balanced quality and file size for slides

        PNG files are saved with transparent backgrounds by default to provide
        maximum flexibility. Use ``transparent=False`` to get a solid background
        matching the theme (white for light mode, dark for dark mode).
        """
        plt.tight_layout()

        # Auto-detect format from extension if not specified
        if format == "auto":
            ext = filename.lower().split(".")[-1]
            if ext == "svg":
                format = "web"
            elif ext == "pdf":
                format = "paper"
            elif ext in ["png", "jpg", "jpeg"]:
                format = "social"
            else:
                format = "web"

        # Set format-specific parameters
        save_kwargs = {}

        if format == "web":
            # SVGs default to transparent
            use_transparent = transparent if transparent is not None else True
            save_kwargs.update(
                {
                    "format": "svg",
                    "transparent": use_transparent,
                    "bbox_inches": "tight",
                    "pad_inches": 0.1,
                }
            )
            # Only set facecolor if not transparent
            if not use_transparent:
                save_kwargs["facecolor"] = self.colors["background"]
            if not filename.endswith(".svg"):
                filename += ".svg"
        elif format == "paper":
            # PDFs default to solid background
            use_transparent = transparent if transparent is not None else False
            save_kwargs.update(
                {
                    "format": "pdf",
                    "transparent": use_transparent,
                    "bbox_inches": "tight",
                    "pad_inches": 0.1,
                }
            )
            # Only set facecolor if not transparent
            if not use_transparent:
                save_kwargs["facecolor"] = (
                    "white" if not self.dark_mode else self.colors["background"]
                )
            if not filename.endswith(".pdf"):
                filename += ".pdf"
        elif format == "social":
            # Default to transparent for PNGs unless explicitly set
            use_transparent = transparent if transparent is not None else True
            save_kwargs.update(
                {
                    "format": "png",
                    "dpi": 300,
                    "transparent": use_transparent,
                    "bbox_inches": "tight",
                    "pad_inches": 0.1,
                }
            )
            # Only set facecolor if not transparent
            if not use_transparent:
                save_kwargs["facecolor"] = self.colors["background"]
            if not filename.endswith(".png"):
                filename += ".png"
        elif format == "presentation":
            # Default to transparent for PNGs unless explicitly set
            use_transparent = transparent if transparent is not None else True
            save_kwargs.update(
                {
                    "format": "png",
                    "dpi": 150,
                    "transparent": use_transparent,
                    "bbox_inches": "tight",
                    "pad_inches": 0.1,
                }
            )
            # Only set facecolor if not transparent
            if not use_transparent:
                save_kwargs["facecolor"] = self.colors["background"]
            if not filename.endswith(".png"):
                filename += ".png"

        # Override with any user-provided kwargs
        save_kwargs.update(kwargs)

        plt.savefig(filename, **save_kwargs)

    def save_all_formats(self, base_name: str, **kwargs):
        """Save plot in all common formats for different use cases."""
        self.save(f"{base_name}_web.svg", format="web", **kwargs)
        self.save(f"{base_name}_paper.pdf", format="paper", **kwargs)
        self.save(f"{base_name}_social.png", format="social", **kwargs)

    def _get_facet_data(self, row_val, col_val):
        """Get subset of data for specific facet."""
        mask = pd.Series([True] * len(self.data), index=self.data.index)  # type: ignore[arg-type]

        if self.facet_row and row_val is not None:
            mask = mask & (self.data[self.facet_row] == row_val)

        if self.facet_col and col_val is not None:
            mask = mask & (self.data[self.facet_col] == col_val)

        return self.data[mask]

    def _get_wrapped_axes(self, facet_row_idx, facet_col_idx):
        """Get the axes for a facet, handling wrapping if needed."""
        if not self.wrapped_layout:
            return self.axes[facet_row_idx, facet_col_idx]

        # Calculate the linear position in the original grid
        linear_pos = facet_row_idx * self.original_n_cols + facet_col_idx

        # Map to wrapped grid coordinates
        wrapped_row = linear_pos // self.n_cols
        wrapped_col = linear_pos % self.n_cols

        return self.axes[wrapped_row, wrapped_col]

    def _finalize_faceted_plot(self):
        """Apply labels and titles for faceted plots."""
        # Set subplot titles if enabled
        if self.subplot_titles:
            for i, row_val in enumerate(self.facet_row_values):
                for j, col_val in enumerate(self.facet_col_values):
                    ax = self._get_wrapped_axes(i, j)

                    # Create subplot title
                    title_parts = []
                    if self.facet_col and col_val is not None:
                        col_label = self.labels.get(self.facet_col, self.facet_col)
                        title_parts.append(f"{col_label}: {col_val}")
                    if self.facet_row and row_val is not None:
                        row_label = self.labels.get(self.facet_row, self.facet_row)
                        title_parts.append(f"{row_label}: {row_val}")

                    if title_parts:
                        ax.set_title(
                            ", ".join(title_parts), fontsize=self.legend_font_size
                        )

        # Apply grid to all subplots
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                ax = self.axes[i, j]
                if self.grid:
                    ax.grid(
                        True,
                        alpha=self.grid_alpha,
                        linewidth=self.grid_linewidth,
                        zorder=-10,
                    )
                    # Force grid to render below all plot elements
                    ax.set_axisbelow(True)
                else:
                    ax.grid(False)

        # Set axis labels only on edge subplots
        xlabel = self.labels.get(self.x, self.x) if isinstance(self.x, str) else "X"
        ylabel = self.labels.get(self.y, self.y) if isinstance(self.y, str) else "Y"

        # Bottom row gets x-labels
        for j in range(self.n_cols):
            ax = self.axes[self.n_rows - 1, j]
            ax.set_xlabel(xlabel, fontsize=self.label_font_size, fontweight="bold")

        # Left column gets y-labels
        for i in range(self.n_rows):
            ax = self.axes[i, 0]
            ax.set_ylabel(ylabel, fontsize=self.label_font_size, fontweight="bold")

        # Set overall title
        if self.title:
            self.fig.suptitle(
                self.title, fontsize=self.title_font_size, fontweight="500", y=0.98
            )

        # Adjust tick density for all subplots
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                ax = self.axes[i, j]
                if ax.has_data():  # Only adjust for axes with data
                    self._adjust_tick_density(ax)

        # Adjust layout
        self.fig.tight_layout()
        if self.title:
            self.fig.subplots_adjust(top=0.92)

    def _get_next_color(self):
        """Get the next color in the sequence for composition."""
        if self.is_composite:
            return self.colors["colors"][self._color_index % len(self.colors["colors"])]
        else:
            return self.colors["accent"]

    def _get_color_for_series(self, series_index=0):
        """Get color for a specific series, accounting for composition."""
        if self.is_composite:
            # When composing, all series in this plot use the same color
            return self.colors["colors"][self._color_index % len(self.colors["colors"])]
        else:
            # When not composing, each series gets a different color
            return self.colors["colors"][series_index % len(self.colors["colors"])]

    def _get_plot_kwargs_with_label(self, label=None):
        """Get plot kwargs with optional label for legend."""
        kwargs = self.plot_kwargs.copy()
        if label:
            kwargs["label"] = label
        elif "label" in self.plot_kwargs:
            kwargs["label"] = self.plot_kwargs["label"]
        return kwargs

    def _show_legend_if_needed(self):
        """Show legend automatically if there are labeled elements."""
        if self.is_faceted:
            # For faceted plots, check each subplot
            for ax in self.get_axes():
                if ax.get_legend_handles_labels()[0]:  # Has legend handles
                    ax.legend(fontsize=self.legend_font_size, loc=self.legend_loc)
        else:
            # For single plots, check the main axis
            if self.ax.get_legend_handles_labels()[0]:  # Has legend handles
                self._add_legend_with_spacing()

    def _add_legend_with_spacing(self):
        """Add legend with intelligent positioning and y-axis adjustment."""
        # First, add the legend to see where matplotlib places it
        legend = self.ax.legend(
            fontsize=self.legend_font_size, loc=self.legend_loc, framealpha=0.9
        )

        # Check if we need to extend y-axis based on legend position
        # This handles both explicit upper locations and 'best' when it chooses upper
        if legend:
            # Get the legend's bounding box in axes coordinates
            bbox = legend.get_window_extent()
            bbox_axes = bbox.transformed(self.ax.transAxes.inverted())

            # Check if legend is in the upper portion of the plot (y > 0.6)
            if bbox_axes.y1 > 0.6:
                # Get current axis limits
                ylim = self.ax.get_ylim()
                y_range = ylim[1] - ylim[0]

                # For stacked bars or when legend has many items, need more space
                # Calculate extension based on legend height
                legend_height_ratio = bbox_axes.height
                y_extension = y_range * max(0.15, legend_height_ratio * 0.5)

                new_ylim = (ylim[0], ylim[1] + y_extension)
                self.ax.set_ylim(new_ylim)

        return legend

    def show_legend(self):
        """Manually show the legend with appropriate styling."""
        self._show_legend_if_needed()
        return self
