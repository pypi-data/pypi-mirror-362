"""Integration tests for Rekha components working together."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import rekha as rk


@pytest.mark.integration
class TestPlotIntegration:
    """Test integration between different plot types and features."""

    def setup_method(self):
        """Set up test data."""
        np.random.seed(42)

        # Dataset with multiple data types
        self.df = pd.DataFrame(
            {
                "x": range(20),
                "y": np.random.randn(20),
                "category": np.random.choice(["A", "B", "C"], 20),
                "size": np.random.randint(10, 100, 20),
                "continuous": np.random.randn(20) * 10,
                "boolean": np.random.choice([True, False], 20),
            }
        )

        # Time series data
        dates = pd.date_range("2023-01-01", periods=50, freq="D")
        self.ts_df = pd.DataFrame(
            {
                "date": dates,
                "value": np.cumsum(np.random.randn(50)) + 100,
                "category": np.random.choice(["Type1", "Type2", "Type3"], 50),
            }
        )

        # Large dataset for performance testing
        self.large_df = pd.DataFrame(
            {
                "x": np.random.randn(1000),
                "y": np.random.randn(1000),
                "category": np.random.choice(["A", "B", "C", "D"], 1000),
                "size": np.random.randint(5, 50, 1000),
            }
        )

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_theme_consistency_across_plots(self):
        """Test that theme is consistent across different plot types."""
        # Set dark theme
        rk.set_rekha_theme(dark_mode=True)

        # Create different plot types with explicit dark_mode
        line_plot = rk.line(self.df, x="x", y="y", dark_mode=True)
        scatter_plot = rk.scatter(self.df, x="x", y="y", dark_mode=True)
        bar_plot = rk.bar(self.df, x="x", y="y", dark_mode=True)

        # All plots should be created successfully
        assert hasattr(line_plot, "ax")
        assert hasattr(scatter_plot, "ax")
        assert hasattr(bar_plot, "ax")

        # Check that dark mode was applied
        assert line_plot.dark_mode is True
        assert scatter_plot.dark_mode is True
        assert bar_plot.dark_mode is True

    def test_color_mapping_consistency(self):
        """Test that color mapping is consistent across plots."""
        # Set custom color mapping
        color_mapping = {"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"}

        # Create different plots with same color mapping
        scatter_plot = rk.scatter(
            self.df, x="x", y="y", color="category", color_mapping=color_mapping
        )
        line_plot = rk.line(
            self.df, x="x", y="y", color="category", color_mapping=color_mapping
        )

        # Both should use the same color mapping
        assert scatter_plot.color_mapping == line_plot.color_mapping == color_mapping

    def test_category_order_consistency(self):
        """Test that category order is consistent across plots."""
        category_order = ["C", "A", "B"]

        # Create different plots with same category order
        scatter_plot = rk.scatter(
            self.df, x="x", y="y", color="category", category_order=category_order
        )
        bar_plot = rk.bar(
            self.df, x="x", y="y", color="category", category_order=category_order
        )

        # Both should use the same category order
        assert scatter_plot.category_order == bar_plot.category_order == category_order

    def test_subplot_integration(self):
        """Test creating subplots with different plot types."""
        fig, axes = rk.subplots(2, 2, figsize=(12, 10))

        # Create different plot types in subplots
        # Note: This tests the subplot creation, individual plots would need to be created separately
        assert fig is not None
        assert axes is not None
        assert axes.shape == (2, 2)

        # Test that we can access individual axes
        ax1 = axes[0, 0]
        ax2 = axes[0, 1]
        ax3 = axes[1, 0]
        ax4 = axes[1, 1]

        assert ax1 is not None
        assert ax2 is not None
        assert ax3 is not None
        assert ax4 is not None

    def test_plot_with_all_features(self):
        """Test plot with all available features enabled."""
        plot = rk.scatter(
            self.df,
            x="x",
            y="y",
            color="category",
            size="size",
            title="Complete Feature Test",
            labels={"x": "X-axis", "y": "Y-axis"},
            dark_mode=True,
            figsize=(10, 8),
            grid=True,
            color_mapping={"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"},
            category_order=["A", "B", "C"],
        )

        # Verify all features are applied
        assert plot.title == "Complete Feature Test"
        assert plot.labels == {"x": "X-axis", "y": "Y-axis"}
        assert plot.dark_mode is True
        assert plot.figsize == (10, 8)
        assert plot.grid is True
        assert plot.color_mapping == {"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"}
        assert plot.category_order == ["A", "B", "C"]

        # Check that plot was created successfully
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_time_series_integration(self):
        """Test integration with time series data."""
        # Test line plot with time series
        plot = rk.line(self.ts_df, x="date", y="value", color="category")

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

        # Should handle datetime x-axis
        assert len(plot.ax.lines) > 0

    def test_large_dataset_performance(self):
        """Test performance with large datasets."""
        # Create plot with large dataset
        plot = rk.scatter(self.large_df, x="x", y="y", color="category", size="size")

        # Should create plot without errors
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")
        assert len(plot.ax.collections) > 0

    def test_multiple_plots_memory_management(self):
        """Test memory management with multiple plots."""
        plots = []

        # Create multiple plots
        for i in range(10):
            plot = rk.scatter(self.df, x="x", y="y", title=f"Plot {i}")
            plots.append(plot)

        # All plots should be created successfully
        assert len(plots) == 10

        for i, plot in enumerate(plots):
            assert hasattr(plot, "ax")
            assert hasattr(plot, "fig")
            assert plot.title == f"Plot {i}"

    def test_plot_customization_chain(self):
        """Test chaining plot customization methods."""
        plot = rk.scatter(self.df, x="x", y="y", color="category")

        # Test that customization methods can be chained
        assert hasattr(plot, "update_layout")
        assert hasattr(plot, "add_annotation")

        # Test method chaining works
        plot.update_layout(title="Updated Title")
        plot.add_annotation("Test annotation", x=5, y=0)

        # Plot should still be functional
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")


@pytest.mark.integration
class TestDataTypeIntegration:
    """Test integration with different data types."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_numpy_array_integration(self):
        """Test integration with numpy arrays."""
        x_data = np.array([1, 2, 3, 4, 5])
        y_data = np.array([2, 4, 6, 8, 10])

        plot = rk.line(None, x=x_data, y=y_data)

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")
        assert len(plot.ax.lines) == 1

    def test_list_integration(self):
        """Test integration with Python lists."""
        x_data = [1, 2, 3, 4, 5]
        y_data = [2, 4, 6, 8, 10]

        plot = rk.scatter(None, x=x_data, y=y_data)

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")
        assert len(plot.ax.collections) == 1

    def test_dict_integration(self):
        """Test integration with dictionary data."""
        data = {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 6, 8, 10],
            "category": ["A", "B", "A", "B", "A"],
        }

        plot = rk.bar(data, x="x", y="y")  # Use x instead of category

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")
        assert len(plot.ax.patches) > 0

    def test_mixed_data_types(self):
        """Test integration with mixed data types."""
        df = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
            }
        )

        # Mix DataFrame columns with arrays - use column name for size
        plot = rk.scatter(df, x="x", y="y", color="category", size="y")

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_categorical_data_integration(self):
        """Test integration with categorical data."""
        df = pd.DataFrame(
            {
                "x": pd.Categorical(["A", "B", "C", "A", "B"]),
                "y": [1, 2, 3, 4, 5],
                "category": pd.Categorical(["X", "Y", "X", "Y", "X"]),
            }
        )

        plot = rk.bar(df, x="x", y="y", color="category")

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_datetime_integration(self):
        """Test integration with datetime data."""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        df = pd.DataFrame(
            {
                "date": dates,
                "value": np.random.randn(10),
                "category": np.random.choice(["A", "B"], 10),
            }
        )

        plot = rk.line(df, x="date", y="value", color="category")

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")


@pytest.mark.integration
class TestErrorHandlingIntegration:
    """Test error handling across integrated components."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_invalid_data_error_consistency(self):
        """Test that invalid data errors are consistent across plot types."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        # Test that all plot types handle invalid columns consistently
        plot_functions = [rk.line, rk.scatter, rk.bar]

        for plot_func in plot_functions:
            with pytest.raises((KeyError, ValueError)):
                plot_func(df, x="nonexistent", y="y")

    def test_empty_data_error_consistency(self):
        """Test that empty data errors are consistent across plot types."""
        df = pd.DataFrame()

        # Test that all plot types handle empty data consistently
        plot_functions = [rk.line, rk.scatter, rk.bar]

        for plot_func in plot_functions:
            with pytest.raises((ValueError, IndexError, KeyError)):
                plot_func(df, x="x", y="y")

    def test_mismatched_data_lengths(self):
        """Test error handling with mismatched data lengths."""
        x_data = [1, 2, 3]
        y_data = [4, 5]  # Different length

        plot_functions = [rk.line, rk.scatter]

        for plot_func in plot_functions:
            with pytest.raises((ValueError, IndexError)):
                plot_func(None, x=x_data, y=y_data)

    def test_theme_error_recovery(self):
        """Test that plots can recover from theme errors."""
        # Even if theme setting fails, plots should still work
        try:
            rk.set_rekha_theme(dark_mode=True)
        except Exception:
            pass  # Ignore theme errors

        # Plots should still work
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        plot = rk.scatter(df, x="x", y="y")

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_color_mapping_error_recovery(self):
        """Test that plots handle partial color mappings correctly."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "category": ["A", "B", "C"]})

        # Partial color mapping - only specify color for A, others should use default colors
        partial_color_mapping = {"A": "#FF0000"}  # Red for A

        plot = rk.scatter(
            df, x="x", y="y", color="category", color_mapping=partial_color_mapping
        )

        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

        # Plot should still be created
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")


@pytest.mark.integration
class TestPerformanceIntegration:
    """Test performance aspects of integrated components."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_large_dataset_with_all_features(self):
        """Test performance with large dataset and all features."""
        # Create large dataset
        n = 5000
        df = pd.DataFrame(
            {
                "x": np.random.randn(n),
                "y": np.random.randn(n),
                "category": np.random.choice(["A", "B", "C", "D"], n),
                "size": np.random.randint(1, 100, n),
                "continuous": np.random.randn(n) * 10,
            }
        )

        # Create plot with all features
        plot = rk.scatter(
            df,
            x="x",
            y="y",
            color="category",
            size="size",
            title="Performance Test",
            dark_mode=True,
            grid=True,
        )

        # Should create plot without errors
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_multiple_categories_performance(self):
        """Test performance with many categories."""
        # Create dataset with many categories
        n = 1000
        n_categories = 20
        categories = [f"Category_{i}" for i in range(n_categories)]

        df = pd.DataFrame(
            {
                "x": np.random.randn(n),
                "y": np.random.randn(n),
                "category": np.random.choice(categories, n),
            }
        )

        plot = rk.scatter(df, x="x", y="y", color="category")

        # Should handle many categories without errors
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")

    def test_plot_creation_speed(self):
        """Test that plot creation is reasonably fast."""
        df = pd.DataFrame(
            {
                "x": np.random.randn(1000),
                "y": np.random.randn(1000),
                "category": np.random.choice(["A", "B", "C"], 1000),
            }
        )

        import time

        # Time plot creation
        start_time = time.time()
        plot = rk.scatter(df, x="x", y="y", color="category")
        end_time = time.time()

        # Should create plot reasonably quickly (less than 5 seconds)
        assert (end_time - start_time) < 5.0
        assert hasattr(plot, "ax")
        assert hasattr(plot, "fig")
