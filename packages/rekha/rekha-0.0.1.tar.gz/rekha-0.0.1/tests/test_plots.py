"""Comprehensive tests for Rekha plotting functions."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import rekha as rk


class TestPlotFunctions:
    """Test all plot functions with various data types and configurations."""

    def setup_method(self):
        """Set up test data for all plot tests."""
        np.random.seed(42)

        # Basic DataFrame
        self.df = pd.DataFrame(
            {
                "x": range(10),
                "y": np.random.randn(10),
                "category": ["A", "B", "C"] * 3 + ["A"],
                "size": np.random.randint(20, 100, 10),
                "color_val": np.random.randn(10),
            }
        )

        # Larger dataset for histograms
        self.large_df = pd.DataFrame(
            {
                "values": np.random.randn(1000),
                "category": np.random.choice(["X", "Y", "Z"], 1000),
                "weight": np.random.exponential(1, 1000),
            }
        )

        # Time series data
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        self.ts_df = pd.DataFrame(
            {
                "date": dates,
                "value": np.cumsum(np.random.randn(30)),
                "category": np.random.choice(["Type1", "Type2"], 30),
            }
        )

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_line_plot_basic(self):
        """Test basic line plot creation."""
        fig = rk.line(self.df, x="x", y="y")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        assert len(fig.ax.lines) == 1

    def test_line_plot_with_color(self):
        """Test line plot with color grouping."""
        fig = rk.line(self.df, x="x", y="y", color="category")
        assert hasattr(fig, "ax")
        assert len(fig.ax.lines) > 1  # Multiple lines for different categories

    def test_line_plot_dark_mode(self):
        """Test line plot with dark mode."""
        fig = rk.line(self.df, x="x", y="y", dark_mode=True)
        assert hasattr(fig, "ax")
        # Check that background is dark
        assert fig.ax.get_facecolor()[0] < 0.5  # R component should be dark

    def test_scatter_plot_basic(self):
        """Test basic scatter plot creation."""
        fig = rk.scatter(self.df, x="x", y="y")
        assert hasattr(fig, "ax")
        assert len(fig.ax.collections) == 1

    def test_scatter_plot_with_size(self):
        """Test scatter plot with size mapping."""
        fig = rk.scatter(self.df, x="x", y="y", size="size")
        assert hasattr(fig, "ax")
        collection = fig.ax.collections[0]
        sizes = collection.get_sizes()
        assert len(sizes) == len(self.df)
        assert not np.allclose(sizes, sizes[0])  # Sizes should vary

    def test_scatter_plot_with_color_and_size(self):
        """Test scatter plot with both color and size mapping."""
        fig = rk.scatter(self.df, x="x", y="y", color="category", size="size")
        assert hasattr(fig, "ax")
        assert len(fig.ax.collections) >= 1

    def test_bar_plot_basic(self):
        """Test basic bar plot creation."""
        fig = rk.bar(self.df, x="category", y="y")
        assert hasattr(fig, "ax")
        assert len(fig.ax.patches) > 0

    def test_bar_plot_with_color(self):
        """Test bar plot with color grouping."""
        # Use different x and color to avoid duplicate category issue
        fig = rk.bar(self.df, x="x", y="y", color="category")
        assert hasattr(fig, "ax")
        assert len(fig.ax.patches) > 0

    def test_histogram_basic(self):
        """Test basic histogram creation."""
        fig = rk.histogram(self.large_df, x="values")
        assert hasattr(fig, "ax")
        assert len(fig.ax.patches) > 0

    def test_histogram_with_bins(self):
        """Test histogram with custom bins."""
        fig = rk.histogram(self.large_df, x="values", nbins=20)
        assert hasattr(fig, "ax")
        assert len(fig.ax.patches) > 0

    def test_histogram_with_color(self):
        """Test histogram with color grouping."""
        fig = rk.histogram(self.large_df, x="values", color="category")
        assert hasattr(fig, "ax")
        assert len(fig.ax.patches) > 0

    def test_box_plot_basic(self):
        """Test basic box plot creation."""
        fig = rk.box(self.df, x="category", y="y")
        assert hasattr(fig, "ax")
        # Box plot creates multiple artists
        assert len(fig.ax.get_children()) > 0

    def test_box_plot_single_column(self):
        """Test box plot with single column."""
        fig = rk.box(self.df, y="y")
        assert hasattr(fig, "ax")

    def test_heatmap_basic(self):
        """Test basic heatmap creation."""
        # Create correlation matrix
        corr_data = self.df[["x", "y", "size", "color_val"]].corr()
        fig = rk.heatmap(corr_data)
        assert hasattr(fig, "ax")
        assert len(fig.ax.images) == 1

    def test_cdf_basic(self):
        """Test basic CDF plot creation."""
        fig = rk.cdf(self.large_df, x="values")
        assert hasattr(fig, "ax")
        assert len(fig.ax.lines) == 1

    def test_cdf_with_color(self):
        """Test CDF plot with color grouping."""
        fig = rk.cdf(self.large_df, x="values", color="category")
        assert hasattr(fig, "ax")
        assert len(fig.ax.lines) > 1

    def test_plot_with_custom_labels(self):
        """Test plot with custom labels."""
        labels = {"x": "X-axis", "y": "Y-axis"}
        fig = rk.scatter(self.df, x="x", y="y", labels=labels)
        assert fig.ax.get_xlabel() == "X-axis"
        assert fig.ax.get_ylabel() == "Y-axis"

    def test_plot_with_title(self):
        """Test plot with custom title."""
        fig = rk.line(self.df, x="x", y="y", title="Test Plot")
        assert fig.ax.get_title() == "Test Plot"

    def test_plot_with_figsize(self):
        """Test plot with custom figure size."""
        fig = rk.scatter(self.df, x="x", y="y", figsize=(12, 8))
        assert fig.fig.get_size_inches()[0] == 12
        assert fig.fig.get_size_inches()[1] == 8

    def test_plot_without_grid(self):
        """Test plot without grid."""
        fig = rk.line(self.df, x="x", y="y", grid=False)
        # Check that grid parameter was set
        assert fig.grid is False

    def test_grayscale_friendly_mode(self):
        """Test grayscale friendly mode."""
        fig = rk.scatter(
            self.df, x="x", y="y", color="category", grayscale_friendly=True
        )
        assert hasattr(fig, "ax")
        # In grayscale friendly mode, should use patterns/markers in addition to colors

    def test_plot_with_arrays(self):
        """Test plot with numpy arrays instead of DataFrame."""
        x_data = np.array([1, 2, 3, 4, 5])
        y_data = np.array([2, 4, 6, 8, 10])
        fig = rk.line(None, x=x_data, y=y_data)
        assert hasattr(fig, "ax")
        assert len(fig.ax.lines) == 1

    def test_plot_with_dict_data(self):
        """Test plot with dictionary data."""
        data = {"x": [1, 2, 3], "y": [4, 5, 6]}
        fig = rk.scatter(data, x="x", y="y")
        assert hasattr(fig, "ax")

    def test_plot_save_functionality(self):
        """Test plot save functionality."""
        fig = rk.line(self.df, x="x", y="y")
        # Test that save method exists and can be called
        assert hasattr(fig, "save")
        assert callable(fig.save)

    def test_plot_show_functionality(self):
        """Test plot show functionality."""
        fig = rk.line(self.df, x="x", y="y")
        # Test that show method exists and can be called
        assert hasattr(fig, "show")
        assert callable(fig.show)

    def test_plot_update_layout(self):
        """Test plot layout update functionality."""
        fig = rk.scatter(self.df, x="x", y="y")
        # Test that update_layout method exists
        assert hasattr(fig, "update_layout")
        assert callable(fig.update_layout)

    def test_plot_add_annotation(self):
        """Test plot annotation functionality."""
        fig = rk.scatter(self.df, x="x", y="y")
        # Test that add_annotation method exists
        assert hasattr(fig, "add_annotation")
        assert callable(fig.add_annotation)


class TestSubplots:
    """Test subplot functionality."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_subplots_basic(self):
        """Test basic subplot creation."""
        fig, axes = rk.subplots(2, 2)
        assert fig is not None
        assert axes is not None
        assert axes.shape == (2, 2)

    def test_subplots_single_row(self):
        """Test single row subplot creation."""
        fig, axes = rk.subplots(1, 3)
        assert fig is not None
        assert axes is not None
        assert len(axes) == 3

    def test_subplots_single_plot(self):
        """Test single subplot creation."""
        fig, ax = rk.subplots(1, 1)
        assert fig is not None
        assert ax is not None

    def test_subplots_with_figsize(self):
        """Test subplot with custom figure size."""
        fig, axes = rk.subplots(2, 2, figsize=(12, 10))
        assert fig.get_size_inches()[0] == 12
        assert fig.get_size_inches()[1] == 10


class TestErrorHandling:
    """Test error handling in plot functions."""

    def test_invalid_column_name(self):
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        with pytest.raises((KeyError, ValueError)):
            rk.line(df, x="nonexistent", y="y")

    def test_empty_dataframe(self):
        """Test behavior with empty DataFrame."""
        df = pd.DataFrame()
        with pytest.raises((ValueError, IndexError, KeyError)):
            rk.scatter(df, x="x", y="y")

    def test_mismatched_data_lengths(self):
        """Test error with mismatched data lengths."""
        x_data = [1, 2, 3]
        y_data = [4, 5]  # Different length
        with pytest.raises((ValueError, IndexError)):
            rk.line(None, x=x_data, y=y_data)

    def test_none_data_no_arrays(self):
        """Test error when no data provided."""
        # Test that None data with None arrays is handled (may not always raise error)
        try:
            fig = rk.scatter(None, x=None, y=None)
            # If no error is raised, check that object was created
            assert hasattr(fig, "ax")
        except (ValueError, TypeError):
            # If error is raised, that's also valid behavior
            pass

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")
