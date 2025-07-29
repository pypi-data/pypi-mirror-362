#!/usr/bin/env python3
"""
Tests for advanced features in Rekha.
"""

import numpy as np
import pandas as pd
import pytest

import rekha as rk


class TestFaceting:
    """Test faceting/grid layout functionality."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        self.sample_data = []

        for category in ["A", "B", "C"]:
            for region in ["North", "South"]:
                for i in range(20):
                    self.sample_data.append(
                        {
                            "x": np.random.randn(),
                            "y": np.random.randn(),
                            "category": category,
                            "region": region,
                            "value": np.random.uniform(10, 100),
                        }
                    )

        self.df = pd.DataFrame(self.sample_data)

    def test_facet_col_basic(self):
        """Test basic column faceting."""
        fig = rk.scatter(self.df, x="x", y="y", facet_col="category")

        # Should create subplots for each category
        assert fig.fig is not None
        assert hasattr(fig, "facet_col_values")
        assert len(fig.facet_col_values) == 3  # A, B, C
        assert set(fig.facet_col_values) == {"A", "B", "C"}

    def test_facet_row_basic(self):
        """Test basic row faceting."""
        fig = rk.scatter(self.df, x="x", y="y", facet_row="region")

        # Should create subplots for each region
        assert fig.fig is not None
        assert hasattr(fig, "facet_row_values")
        assert len(fig.facet_row_values) == 2  # North, South
        assert set(fig.facet_row_values) == {"North", "South"}

    def test_facet_grid_both(self):
        """Test grid faceting with both rows and columns."""
        fig = rk.scatter(
            self.df, x="x", y="y", facet_col="category", facet_row="region"
        )

        # Should create 2x3 grid (2 regions x 3 categories)
        assert fig.fig is not None
        assert len(fig.facet_row_values) == 2
        assert len(fig.facet_col_values) == 3
        assert fig.is_faceted is True

    def test_facet_bar_plot(self):
        """Test faceting with bar plots."""
        fig = rk.bar(self.df, x="category", y="value", facet_col="region")

        assert fig.fig is not None
        assert len(fig.facet_col_values) == 2

    def test_facet_line_plot(self):
        """Test faceting with line plots."""
        # Create time series data
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        data = []
        for region in ["North", "South"]:
            for i, date in enumerate(dates):
                data.append(
                    {"date": date, "value": i + np.random.randn(), "region": region}
                )

        df = pd.DataFrame(data)

        fig = rk.line(df, x="date", y="value", facet_col="region")

        assert fig.fig is not None
        assert len(fig.facet_col_values) == 2

    def test_facet_with_dark_mode(self):
        """Test faceting with dark mode."""
        fig = rk.scatter(self.df, x="x", y="y", facet_col="category", dark_mode=True)

        assert fig.fig is not None
        assert fig.dark_mode is True

    def test_facet_invalid_column(self):
        """Test faceting with invalid column name."""
        with pytest.raises(KeyError):
            rk.scatter(self.df, x="x", y="y", facet_col="invalid_column")

    def test_facet_empty_data(self):
        """Test faceting with empty dataframe."""
        empty_df = pd.DataFrame({"x": [], "y": [], "category": []})

        # Empty data should raise an error or handle gracefully
        with pytest.raises((ValueError, IndexError)):
            rk.scatter(empty_df, x="x", y="y", facet_col="category")


class TestMarginalPlots:
    """Test marginal plot functionality."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        self.x_data = np.random.randn(100)
        self.df = pd.DataFrame({"x": self.x_data})

    def test_marginal_box(self):
        """Test histogram with box marginal plot."""
        fig = rk.histogram(self.df, x="x", marginal="box")

        assert fig.fig is not None
        assert fig.marginal == "box"
        assert hasattr(fig, "ax_marginal")

    def test_marginal_violin(self):
        """Test histogram with violin marginal plot."""
        fig = rk.histogram(self.df, x="x", marginal="violin")

        assert fig.fig is not None
        assert fig.marginal == "violin"
        assert hasattr(fig, "ax_marginal")

    def test_marginal_none(self):
        """Test histogram without marginal plot."""
        fig = rk.histogram(self.df, x="x", marginal=None)

        assert fig.fig is not None
        assert fig.marginal is None
        assert not hasattr(fig, "ax_marginal")

    def test_marginal_with_dark_mode(self):
        """Test marginal plots with dark mode."""
        fig = rk.histogram(self.df, x="x", marginal="box", dark_mode=True)

        assert fig.fig is not None
        assert fig.dark_mode is True
        assert fig.marginal == "box"

    def test_marginal_invalid_type(self):
        """Test invalid marginal type."""
        # Create histogram with invalid marginal type should raise an error
        with pytest.raises((ValueError, AttributeError)):
            rk.histogram(self.df, x="x", marginal="invalid_type")


class TestStatisticalFeatures:
    """Test statistical plotting features."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        n_points = 50
        self.df = pd.DataFrame(
            {
                "x": np.linspace(0, 10, n_points),
                "y": 2 * np.linspace(0, 10, n_points) + np.random.randn(n_points) * 2,
                "category": np.random.choice(["A", "B"], n_points),
                "error": np.random.uniform(0.5, 2.0, n_points),
            }
        )

    def test_error_bars_available(self):
        """Test that error bar functionality exists."""
        # Check if scatter plot supports error bars
        fig = rk.scatter(self.df, x="x", y="y")

        # Should be able to add error bars manually via matplotlib
        assert fig.ax is not None

        # Test manual error bar addition
        fig.ax.errorbar(
            self.df["x"], self.df["y"], yerr=self.df["error"], fmt="none", alpha=0.5
        )

        assert fig.fig is not None

    def test_trend_line_composition(self):
        """Test adding trend lines via composition."""
        # Create base scatter plot
        scatter_fig = rk.scatter(self.df, x="x", y="y")

        # Calculate trend line
        z = np.polyfit(self.df["x"], self.df["y"], 1)
        trend_x = np.array([self.df["x"].min(), self.df["x"].max()])
        trend_y = z[0] * trend_x + z[1]

        trend_df = pd.DataFrame({"x": trend_x, "y": trend_y})

        # Add trend line using composition
        line_fig = rk.line(trend_df, x="x", y="y", base_plot=scatter_fig)

        assert line_fig.fig is not None
        assert line_fig.ax is scatter_fig.ax  # Should share same axes

    def test_confidence_intervals_manual(self):
        """Test manual confidence interval implementation."""
        fig = rk.scatter(self.df, x="x", y="y")

        # Calculate confidence intervals manually
        z = np.polyfit(self.df["x"], self.df["y"], 1)
        trend_line = z[0] * self.df["x"] + z[1]
        residuals = self.df["y"] - trend_line
        std_err = np.std(residuals)

        # Add confidence bands
        fig.ax.fill_between(
            self.df["x"],
            trend_line - 1.96 * std_err,
            trend_line + 1.96 * std_err,
            alpha=0.2,
        )

        assert fig.fig is not None


class TestAxisCustomization:
    """Test axis customization features."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        self.df = pd.DataFrame(
            {
                "x": np.linspace(1, 5, 50),
                "y": np.exp(np.linspace(1, 5, 50)) + np.random.randn(50) * 100,
                "large_values": np.random.uniform(1e6, 1e9, 50),
            }
        )

    def test_log_scale(self):
        """Test logarithmic scale functionality."""
        fig = rk.scatter(self.df, x="x", y="y", yscale="log")

        assert fig.fig is not None
        # Check if log scale was applied
        assert fig.ax.get_yscale() == "log"

    def test_humanized_units(self):
        """Test humanized number formatting."""
        # Test if humanize functionality exists
        fig = rk.bar(self.df.head(10), x="x", y="large_values")

        # Check if we can access and modify tick formatting
        assert fig.ax is not None

        # Manually apply humanization to test the capability
        from matplotlib.ticker import FuncFormatter

        def humanize_func(x, pos):
            """Simple humanization function."""
            if x >= 1e9:
                return f"{x/1e9:.1f}B"
            elif x >= 1e6:
                return f"{x/1e6:.1f}M"
            elif x >= 1e3:
                return f"{x/1e3:.1f}K"
            return str(int(x))

        fig.ax.yaxis.set_major_formatter(FuncFormatter(humanize_func))
        assert fig.fig is not None

    def test_custom_axis_labels(self):
        """Test custom axis labeling."""
        fig = rk.scatter(
            self.df, x="x", y="y", labels={"x": "Custom X Label", "y": "Custom Y Label"}
        )

        assert fig.ax.get_xlabel() == "Custom X Label"
        assert fig.ax.get_ylabel() == "Custom Y Label"

    def test_axis_limits(self):
        """Test setting axis limits."""
        fig = rk.scatter(self.df, x="x", y="y")

        # Set custom limits
        fig.ax.set_xlim(0, 6)
        fig.ax.set_ylim(0, 1000)

        xlim = fig.ax.get_xlim()
        ylim = fig.ax.get_ylim()

        assert xlim[0] == 0
        assert xlim[1] == 6
        assert ylim[0] == 0
        assert ylim[1] == 1000


class TestPlotComposition:
    """Test plot composition workflows."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        self.df = pd.DataFrame(
            {
                "x": np.linspace(0, 10, 20),
                "y1": np.linspace(0, 10, 20) + np.random.randn(20),
                "y2": np.linspace(0, 10, 20) * 0.5 + np.random.randn(20),
                "category": ["A", "B"] * 10,
            }
        )

    def test_bar_line_composition(self):
        """Test composing bar and line plots."""
        # Create base bar plot
        bar_fig = rk.bar(self.df, x="x", y="y1")

        # Add line plot on same axes
        line_fig = rk.line(self.df, x="x", y="y2", base_plot=bar_fig)

        assert line_fig.fig is not None
        assert line_fig.ax is bar_fig.ax
        assert line_fig.fig is bar_fig.fig

    def test_scatter_line_composition(self):
        """Test composing scatter and line plots."""
        # Create base scatter plot
        scatter_fig = rk.scatter(self.df, x="x", y="y1")

        # Add line plot
        line_fig = rk.line(self.df, x="x", y="y2", base_plot=scatter_fig)

        assert line_fig.ax is scatter_fig.ax

    def test_multiple_composition(self):
        """Test multiple plot composition."""
        # Create base plot
        base_fig = rk.scatter(self.df, x="x", y="y1")

        # Add first overlay
        overlay1 = rk.line(self.df, x="x", y="y2", base_plot=base_fig)

        # Add second overlay
        overlay2 = rk.bar(
            self.df.iloc[::3],  # Subset for bars
            x="x",
            y="y1",
            base_plot=overlay1,
            alpha=0.5,
        )

        # All should share the same axes
        assert overlay2.ax is overlay1.ax
        assert overlay1.ax is base_fig.ax

    def test_composition_with_different_data(self):
        """Test composition with different datasets."""
        # Create different datasets
        df1 = pd.DataFrame({"x": [1, 2, 3, 4], "y": [10, 20, 15, 25]})

        df2 = pd.DataFrame({"x": [1.5, 2.5, 3.5, 4.5], "y": [12, 18, 22, 28]})

        # Create base plot
        base_fig = rk.bar(df1, x="x", y="y")

        # Add overlay with different data
        overlay = rk.scatter(df2, x="x", y="y", base_plot=base_fig)

        assert overlay.ax is base_fig.ax


class TestAdvancedColorFeatures:
    """Test advanced color functionality."""

    def setup_method(self):
        """Set up test data for each test."""
        np.random.seed(42)
        self.df = pd.DataFrame(
            {
                "x": np.random.randn(50),
                "y": np.random.randn(50),
                "category": np.random.choice(["A", "B", "C", "D"], 50),
                "value": np.random.uniform(0, 100, 50),
            }
        )

    def test_custom_color_mapping(self):
        """Test custom color mapping functionality."""
        custom_colors = {"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"}

        fig = rk.scatter(
            self.df, x="x", y="y", color="category", color_mapping=custom_colors
        )

        assert fig.fig is not None
        assert hasattr(fig, "color_mapping")
        if hasattr(fig, "color_mapping"):
            assert fig.color_mapping == custom_colors

    def test_alpha_transparency(self):
        """Test alpha/transparency functionality."""
        fig = rk.scatter(self.df, x="x", y="y", alpha=0.5)

        assert fig.fig is not None
        assert hasattr(fig, "alpha")
        assert fig.alpha == 0.5

    def test_color_by_continuous_variable(self):
        """Test coloring by continuous variable."""
        fig = rk.scatter(self.df, x="x", y="y", color="value")  # Continuous variable

        assert fig.fig is not None
        # Should handle continuous color mapping

    def test_palette_with_color_override(self):
        """Test palette combined with color mapping override."""
        custom_colors = {"A": "#FF0000"}  # Override just one category

        fig = rk.scatter(
            self.df,
            x="x",
            y="y",
            color="category",
            palette="cool",
            color_mapping=custom_colors,
        )

        assert fig.fig is not None

    def test_grayscale_friendly_with_patterns(self):
        """Test grayscale-friendly mode with patterns."""
        # Create aggregated data properly
        grouped_data = self.df.groupby("category")["value"].mean().reset_index()

        fig = rk.bar(grouped_data, x="category", y="value", grayscale_friendly=True)

        assert fig.fig is not None
        assert fig.grayscale_friendly is True


if __name__ == "__main__":
    pytest.main([__file__])
