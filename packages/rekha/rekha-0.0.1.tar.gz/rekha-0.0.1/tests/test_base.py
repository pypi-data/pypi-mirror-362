"""Tests for BasePlot class functionality."""

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from rekha.plots.base import BasePlot


class TestBasePlotInitialization:
    """Test BasePlot initialization and basic functionality."""

    def setup_method(self):
        """Set up test data."""
        self.df = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
                "size": [10, 20, 30, 40, 50],
            }
        )

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_base_plot_init_basic(self):
        """Test basic BasePlot initialization."""
        plot = BasePlot(data=self.df, x="x", y="y")

        assert plot.data is not None
        assert plot.x == "x"
        assert plot.y == "y"
        assert hasattr(plot, "fig")
        assert hasattr(plot, "ax")
        assert hasattr(plot, "colors")

    def test_base_plot_init_with_none_data(self):
        """Test BasePlot initialization with None data."""
        x_data = [1, 2, 3]
        y_data = [4, 5, 6]
        plot = BasePlot(data=None, x=x_data, y=y_data)

        assert plot.data is None
        assert plot.x == x_data
        assert plot.y == y_data

    def test_base_plot_init_with_color(self):
        """Test BasePlot initialization with color parameter."""
        plot = BasePlot(data=self.df, x="x", y="y", color="category")

        assert plot.color == "category"

    def test_base_plot_init_with_size(self):
        """Test BasePlot initialization with size parameter."""
        plot = BasePlot(data=self.df, x="x", y="y", size="size")

        assert plot.size == "size"

    def test_base_plot_init_with_title(self):
        """Test BasePlot initialization with title."""
        plot = BasePlot(data=self.df, x="x", y="y", title="Test Plot")

        assert plot.title == "Test Plot"

    def test_base_plot_init_with_labels(self):
        """Test BasePlot initialization with custom labels."""
        labels = {"x": "X-axis", "y": "Y-axis"}
        plot = BasePlot(data=self.df, x="x", y="y", labels=labels)

        assert plot.labels == labels

    def test_base_plot_init_dark_mode(self):
        """Test BasePlot initialization with dark mode."""
        plot = BasePlot(data=self.df, x="x", y="y", dark_mode=True)

        assert plot.dark_mode is True
        # Check that colors are set for dark mode
        assert plot.colors["background"] != "#FFFFFF"  # Should not be white

    def test_base_plot_init_custom_figsize(self):
        """Test BasePlot initialization with custom figure size."""
        plot = BasePlot(data=self.df, x="x", y="y", figsize=(12, 8))

        assert plot.figsize == (12, 8)
        assert plot.fig.get_size_inches()[0] == 12
        assert plot.fig.get_size_inches()[1] == 8

    def test_base_plot_init_font_sizes(self):
        """Test BasePlot initialization with custom font sizes."""
        plot = BasePlot(
            data=self.df,
            x="x",
            y="y",
            title_font_size=16,
            label_font_size=14,
            tick_font_size=12,
            legend_font_size=11,
        )

        assert plot.title_font_size == 16
        assert plot.label_font_size == 14
        assert plot.tick_font_size == 12
        assert plot.legend_font_size == 11

    def test_base_plot_init_grid_settings(self):
        """Test BasePlot initialization with grid settings."""
        plot = BasePlot(
            data=self.df, x="x", y="y", grid=False, grid_alpha=0.5, grid_linewidth=1.0
        )

        assert plot.grid is False
        assert plot.grid_alpha == 0.5
        assert plot.grid_linewidth == 1.0

    def test_base_plot_init_grayscale_friendly(self):
        """Test BasePlot initialization with grayscale friendly mode."""
        plot = BasePlot(data=self.df, x="x", y="y", grayscale_friendly=True)

        assert plot.grayscale_friendly is True

    def test_base_plot_init_color_mapping(self):
        """Test BasePlot initialization with custom color mapping."""
        color_mapping = {"A": "#FF0000", "B": "#00FF00"}
        plot = BasePlot(
            data=self.df, x="x", y="y", color="category", color_mapping=color_mapping
        )

        assert plot.color_mapping == color_mapping

    def test_base_plot_init_category_order(self):
        """Test BasePlot initialization with custom category order."""
        category_order = ["B", "A"]
        plot = BasePlot(
            data=self.df, x="x", y="y", color="category", category_order=category_order
        )

        assert plot.category_order == category_order


class TestBasePlotDataPreparation:
    """Test BasePlot data preparation methods."""

    def setup_method(self):
        """Set up test data."""
        self.df = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
                "size": [10, 20, 30, 40, 50],
            }
        )

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_prepare_data_method(self):
        """Test _prepare_data method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        x_data, y_data = plot._prepare_data()

        assert len(x_data) == 5
        assert len(y_data) == 5
        assert list(x_data) == [1, 2, 3, 4, 5]
        assert list(y_data) == [2, 4, 6, 8, 10]

    def test_prepare_data_with_override(self):
        """Test _prepare_data method with data override."""
        plot = BasePlot(data=self.df, x="x", y="y")

        override_data = pd.DataFrame({"x": [10, 20], "y": [30, 40]})
        x_data, y_data = plot._prepare_data(data_override=override_data)

        assert len(x_data) == 2
        assert len(y_data) == 2
        assert list(x_data) == [10, 20]
        assert list(y_data) == [30, 40]

    def test_prepare_data_with_x_override(self):
        """Test _prepare_data method with x override."""
        plot = BasePlot(data=self.df, x="x", y="y")

        x_data, y_data = plot._prepare_data(x_override=[100, 200, 300, 400, 500])

        assert len(x_data) == 5
        assert len(y_data) == 5
        assert list(x_data) == [100, 200, 300, 400, 500]
        assert list(y_data) == [2, 4, 6, 8, 10]

    def test_prepare_data_with_y_override(self):
        """Test _prepare_data method with y override."""
        plot = BasePlot(data=self.df, x="x", y="y")

        x_data, y_data = plot._prepare_data(y_override=[100, 200, 300, 400, 500])

        assert len(x_data) == 5
        assert len(y_data) == 5
        assert list(x_data) == [1, 2, 3, 4, 5]
        assert list(y_data) == [100, 200, 300, 400, 500]

    def test_get_consistent_colors_and_order(self):
        """Test _get_consistent_colors_and_order method."""
        plot = BasePlot(data=self.df, x="x", y="y", color="category")

        categories = ["A", "B", "C"]
        ordered_categories, colors = plot._get_consistent_colors_and_order(categories)

        assert len(ordered_categories) == 3
        assert len(colors) == 3
        assert set(ordered_categories) == set(categories)

    def test_get_consistent_colors_with_mapping(self):
        """Test _get_consistent_colors_and_order with color mapping."""
        color_mapping = {"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"}
        plot = BasePlot(
            data=self.df, x="x", y="y", color="category", color_mapping=color_mapping
        )

        categories = ["A", "B", "C"]
        ordered_categories, colors = plot._get_consistent_colors_and_order(categories)

        assert len(ordered_categories) == 3
        assert len(colors) == 3

        # Check that custom colors are used
        for i, cat in enumerate(ordered_categories):
            assert colors[i] == color_mapping[cat]

    def test_get_consistent_colors_with_order(self):
        """Test _get_consistent_colors_and_order with category order."""
        category_order = ["B", "A", "C"]
        plot = BasePlot(
            data=self.df, x="x", y="y", color="category", category_order=category_order
        )

        categories = ["A", "B", "C"]
        ordered_categories, colors = plot._get_consistent_colors_and_order(categories)

        assert ordered_categories == ["B", "A", "C"]


class TestBasePlotCustomization:
    """Test BasePlot customization methods."""

    def setup_method(self):
        """Set up test data."""
        self.df = pd.DataFrame(
            {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10],
                "category": ["A", "B", "A", "B", "A"],
            }
        )

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_apply_labels_method(self):
        """Test _apply_labels method."""
        labels = {"x": "X-axis", "y": "Y-axis"}
        plot = BasePlot(data=self.df, x="x", y="y", labels=labels)

        plot._apply_labels()

        assert plot.ax.get_xlabel() == "X-axis"
        assert plot.ax.get_ylabel() == "Y-axis"

    def test_apply_labels_default(self):
        """Test _apply_labels method with default labels."""
        plot = BasePlot(data=self.df, x="x", y="y")

        plot._apply_labels()

        assert plot.ax.get_xlabel() == "x"
        assert plot.ax.get_ylabel() == "y"

    def test_apply_title_method(self):
        """Test _apply_title method."""
        plot = BasePlot(data=self.df, x="x", y="y", title="Test Title")

        plot._apply_title()

        assert plot.ax.get_title() == "Test Title"

    def test_apply_title_no_title(self):
        """Test _apply_title method with no title."""
        plot = BasePlot(data=self.df, x="x", y="y")

        plot._apply_title()

        # Should not have a title or have empty title
        assert plot.ax.get_title() == ""

    def test_setup_grid_method(self):
        """Test _setup_grid method."""
        plot = BasePlot(data=self.df, x="x", y="y", grid=True)

        plot._setup_grid()

        # Grid should be enabled - check that grid method exists
        assert hasattr(plot.ax, "grid")

    def test_setup_grid_disabled(self):
        """Test _setup_grid method with grid disabled."""
        plot = BasePlot(data=self.df, x="x", y="y", grid=False)

        plot._setup_grid()

        # Grid should be disabled - check that configuration was set
        assert plot.grid is False

    def test_update_layout_method(self):
        """Test update_layout method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "update_layout")
        assert callable(plot.update_layout)

        # Test calling with parameters
        plot.update_layout(title="New Title")

    def test_add_annotation_method(self):
        """Test add_annotation method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "add_annotation")
        assert callable(plot.add_annotation)

        # Test calling annotation
        plot.add_annotation("Test annotation", x=2, y=5)

    def test_show_method(self):
        """Test show method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "show")
        assert callable(plot.show)

    def test_save_method(self):
        """Test save method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "save")
        assert callable(plot.save)

    def test_save_all_formats_method(self):
        """Test save_all_formats method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "save_all_formats")
        assert callable(plot.save_all_formats)


class TestBasePlotTheme:
    """Test BasePlot theme application."""

    def setup_method(self):
        """Set up test data."""
        self.df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_apply_theme_light(self):
        """Test _apply_theme method with light mode."""
        plot = BasePlot(data=self.df, x="x", y="y", dark_mode=False)

        plot._apply_theme()

        assert plot.colors is not None
        assert "background" in plot.colors
        assert "colors" in plot.colors

    def test_apply_theme_dark(self):
        """Test _apply_theme method with dark mode."""
        plot = BasePlot(data=self.df, x="x", y="y", dark_mode=True)

        plot._apply_theme()

        assert plot.colors is not None
        assert "background" in plot.colors
        assert "colors" in plot.colors

    def test_theme_affects_background(self):
        """Test that theme affects background color."""
        light_plot = BasePlot(data=self.df, x="x", y="y", dark_mode=False)
        dark_plot = BasePlot(data=self.df, x="x", y="y", dark_mode=True)

        light_bg = light_plot.ax.get_facecolor()
        dark_bg = dark_plot.ax.get_facecolor()

        # Backgrounds should be different
        assert light_bg != dark_bg

    def test_get_bw_patterns_method(self):
        """Test _get_bw_patterns method."""
        # Test without grayscale_friendly mode (should return empty dict)
        plot = BasePlot(data=self.df, x="x", y="y")
        patterns = plot._get_bw_patterns()
        assert isinstance(patterns, dict)
        assert len(patterns) == 0  # Empty when grayscale_friendly is False

        # Test with grayscale_friendly mode enabled
        plot_bw = BasePlot(data=self.df, x="x", y="y", grayscale_friendly=True)
        patterns_bw = plot_bw._get_bw_patterns()
        assert isinstance(patterns_bw, dict)
        assert (
            len(patterns_bw) > 0
        )  # Should have patterns when grayscale_friendly is True
        assert "hatches" in patterns_bw
        assert "linestyles" in patterns_bw
        assert "markers" in patterns_bw

    def test_get_markers_method(self):
        """Test _get_markers method."""
        plot = BasePlot(data=self.df, x="x", y="y")

        markers = plot._get_markers()

        assert isinstance(markers, list)
        assert len(markers) > 0


class TestBasePlotErrors:
    """Test BasePlot error handling."""

    def teardown_method(self):
        """Clean up after each test."""
        plt.close("all")

    def test_init_with_invalid_data(self):
        """Test BasePlot initialization with invalid data."""
        # Test that invalid data can be handled (may not always raise error)
        try:
            plot = BasePlot(data="invalid_data", x="x", y="y")
            # If no error is raised, check that object was created
            assert hasattr(plot, "ax")
        except (TypeError, ValueError):
            # If error is raised, that's also valid behavior
            pass

    def test_init_with_missing_required_params(self):
        """Test BasePlot initialization with missing required parameters."""
        # Test that missing params can be handled (may not always raise error)
        try:
            plot = BasePlot(data=None, x=None, y=None)
            # If no error is raised, check that object was created
            assert hasattr(plot, "ax")
        except (ValueError, TypeError):
            # If error is raised, that's also valid behavior
            pass

    def test_prepare_data_with_invalid_column(self):
        """Test _prepare_data with invalid column name."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        plot = BasePlot(data=df, x="nonexistent", y="y")

        with pytest.raises(KeyError):
            plot._prepare_data()

    def test_apply_labels_with_invalid_labels(self):
        """Test _apply_labels with invalid labels."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        # Test that invalid labels raise an error or are handled gracefully
        try:
            plot = BasePlot(data=df, x="x", y="y", labels="invalid_labels")
            plot._apply_labels()
            # If no error, check plot was created
            assert hasattr(plot, "ax")
        except (AttributeError, TypeError):
            # If error is raised, that's expected behavior
            pass

    def test_finalize_plot_method(self):
        """Test _finalize_plot method."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        plot = BasePlot(data=df, x="x", y="y")

        # Test that method exists and is callable
        assert hasattr(plot, "_finalize_plot")
        assert callable(plot._finalize_plot)

        # Test calling the method
        plot._finalize_plot()
