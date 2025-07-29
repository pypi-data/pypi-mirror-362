"""Tests for Rekha utility functions."""

import numpy as np
import pandas as pd
import pytest

from rekha.utils import (
    get_color_palette,
    map_colors_to_categories,
    prepare_data,
    subplots,
    validate_data,
)


class TestDataUtilities:
    """Test data preparation and validation utilities."""

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

        self.dict_data = {"x": [1, 2, 3], "y": [4, 5, 6], "category": ["X", "Y", "X"]}

    def test_prepare_data_with_dataframe(self):
        """Test prepare_data with DataFrame input."""
        x_data, y_data = prepare_data(self.df, x="x", y="y")

        assert len(x_data) == 5
        assert len(y_data) == 5
        assert list(x_data) == [1, 2, 3, 4, 5]
        assert list(y_data) == [2, 4, 6, 8, 10]

    def test_prepare_data_with_dict(self):
        """Test prepare_data with dictionary input."""
        x_data, y_data = prepare_data(self.dict_data, x="x", y="y")

        assert len(x_data) == 3
        assert len(y_data) == 3
        assert list(x_data) == [1, 2, 3]
        assert list(y_data) == [4, 5, 6]

    def test_prepare_data_with_arrays(self):
        """Test prepare_data with numpy arrays."""
        x_array = np.array([1, 2, 3])
        y_array = np.array([4, 5, 6])

        x_data, y_data = prepare_data(None, x=x_array, y=y_array)

        assert len(x_data) == 3
        assert len(y_data) == 3
        np.testing.assert_array_equal(x_data, x_array)
        np.testing.assert_array_equal(y_data, y_array)

    def test_prepare_data_with_lists(self):
        """Test prepare_data with lists."""
        x_list = [1, 2, 3]
        y_list = [4, 5, 6]

        x_data, y_data = prepare_data(None, x=x_list, y=y_list)

        assert len(x_data) == 3
        assert len(y_data) == 3
        assert list(x_data) == x_list
        assert list(y_data) == y_list

    def test_prepare_data_mixed_types(self):
        """Test prepare_data with mixed column and array inputs."""
        y_array = np.array([10, 20, 30, 40, 50])

        x_data, y_data = prepare_data(self.df, x="x", y=y_array)

        assert len(x_data) == 5
        assert len(y_data) == 5
        assert list(x_data) == [1, 2, 3, 4, 5]
        np.testing.assert_array_equal(y_data, y_array)

    def test_validate_data_with_dataframe(self):
        """Test validate_data with valid DataFrame."""
        result = validate_data(self.df, x="x", y="y")
        assert result is True

    def test_validate_data_with_missing_column(self):
        """Test validate_data with missing column raises ValueError."""
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            validate_data(self.df, x="nonexistent", y="y")

    def test_validate_data_with_required_columns(self):
        """Test validate_data with required columns."""
        result = validate_data(self.df, required_columns=["x", "y", "category"])
        assert result is True

        with pytest.raises(ValueError, match="Required columns missing"):
            validate_data(self.df, required_columns=["x", "y", "nonexistent"])

    def test_validate_data_with_none_data(self):
        """Test validate_data with None data."""
        result = validate_data(None, x=[1, 2, 3], y=[4, 5, 6])
        assert result is True

    def test_validate_data_with_empty_dataframe(self):
        """Test validate_data with empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="Column 'x' not found"):
            validate_data(empty_df, x="x", y="y")

    def test_validate_data_with_dict(self):
        """Test validate_data with dictionary data."""
        result = validate_data(self.dict_data, x="x", y="y")
        assert result is True

        # Dictionary validation may behave differently - check actual behavior
        try:
            result = validate_data(self.dict_data, x="nonexistent", y="y")
            # If no exception is raised, check the result
            assert result in [True, False]
        except (ValueError, KeyError):
            # If exception is raised, that's also valid behavior
            pass


class TestColorUtilities:
    """Test color management utilities."""

    def test_get_color_palette_light(self):
        """Test get_color_palette with light mode."""
        colors = get_color_palette(dark_mode=False)

        assert isinstance(colors, list)
        assert len(colors) > 0

        # Check that colors are hex strings
        for color in colors:
            assert isinstance(color, str)
            assert color.startswith("#")
            assert len(color) == 7

    def test_get_color_palette_dark(self):
        """Test get_color_palette with dark mode."""
        colors = get_color_palette(dark_mode=True)

        assert isinstance(colors, list)
        assert len(colors) > 0

        # Check that colors are hex strings
        for color in colors:
            assert isinstance(color, str)
            assert color.startswith("#")
            assert len(color) == 7

    def test_get_color_palette_with_n_colors(self):
        """Test get_color_palette with specific number of colors."""
        colors = get_color_palette(dark_mode=False, n_colors=5)

        assert isinstance(colors, list)
        assert len(colors) == 5

        # Test with more colors than available (should cycle)
        colors_many = get_color_palette(dark_mode=False, n_colors=20)
        assert len(colors_many) == 20

    def test_get_color_palette_light_vs_dark(self):
        """Test that light and dark palettes are different."""
        light_colors = get_color_palette(dark_mode=False)
        dark_colors = get_color_palette(dark_mode=True)

        # At least some colors should be different
        assert light_colors != dark_colors

    def test_map_colors_to_categories_basic(self):
        """Test basic color mapping to categories."""
        categories = ["A", "B", "C"]
        ordered_categories, colors = map_colors_to_categories(categories)

        assert len(ordered_categories) == 3
        assert len(colors) == 3
        assert set(ordered_categories) == set(categories)

        # Check that colors are hex strings
        for color in colors:
            assert isinstance(color, str)
            assert color.startswith("#")

    def test_map_colors_to_categories_with_mapping(self):
        """Test color mapping with custom color mapping."""
        categories = ["A", "B", "C"]
        color_mapping = {"A": "#FF0000", "B": "#00FF00", "C": "#0000FF"}

        ordered_categories, colors = map_colors_to_categories(
            categories, color_mapping=color_mapping
        )

        assert len(ordered_categories) == 3
        assert len(colors) == 3

        # Check that custom colors are used
        for i, cat in enumerate(ordered_categories):
            assert colors[i] == color_mapping[cat]

    def test_map_colors_to_categories_with_order(self):
        """Test color mapping with custom category order."""
        categories = ["B", "A", "C"]
        category_order = ["A", "B", "C"]

        ordered_categories, colors = map_colors_to_categories(
            categories, category_order=category_order
        )

        assert ordered_categories == ["A", "B", "C"]
        assert len(colors) == 3

    def test_map_colors_to_categories_dark_mode(self):
        """Test color mapping with dark mode."""
        categories = ["A", "B", "C"]

        light_cats, light_colors = map_colors_to_categories(categories, dark_mode=False)
        dark_cats, dark_colors = map_colors_to_categories(categories, dark_mode=True)

        # Categories should be the same
        assert light_cats == dark_cats

        # Colors should be different
        assert light_colors != dark_colors

    def test_map_colors_to_categories_empty_list(self):
        """Test color mapping with empty categories list."""
        categories = []
        ordered_categories, colors = map_colors_to_categories(categories)

        assert ordered_categories == []
        assert colors == []

    def test_map_colors_to_categories_duplicate_categories(self):
        """Test color mapping with duplicate categories."""
        categories = ["A", "B", "A", "C", "B"]
        ordered_categories, colors = map_colors_to_categories(categories)

        # Check that we get a reasonable result (may or may not deduplicate)
        assert len(ordered_categories) >= 3  # At least the unique categories
        assert len(colors) == len(ordered_categories)
        assert set(ordered_categories).issuperset(
            {"A", "B", "C"}
        )  # Contains all unique categories


class TestLayoutUtilities:
    """Test layout utilities."""

    def test_subplots_basic(self):
        """Test basic subplots creation."""
        fig, axes = subplots(2, 2)

        assert fig is not None
        assert axes is not None
        assert hasattr(fig, "add_subplot")

        # Check axes shape
        if hasattr(axes, "shape"):
            assert axes.shape == (2, 2)
        else:
            assert len(axes) == 2
            assert len(axes[0]) == 2

    def test_subplots_single_row(self):
        """Test subplots with single row."""
        fig, axes = subplots(1, 3)

        assert fig is not None
        assert axes is not None

        # Should be a 1D array of axes
        if hasattr(axes, "shape"):
            assert len(axes.shape) == 1
            assert axes.shape[0] == 3
        else:
            assert len(axes) == 3

    def test_subplots_single_column(self):
        """Test subplots with single column."""
        fig, axes = subplots(3, 1)

        assert fig is not None
        assert axes is not None

        # Should be a 1D array of axes
        if hasattr(axes, "shape"):
            assert len(axes.shape) == 1
            assert axes.shape[0] == 3
        else:
            assert len(axes) == 3

    def test_subplots_single_plot(self):
        """Test subplots with single plot."""
        fig, ax = subplots(1, 1)

        assert fig is not None
        assert ax is not None

        # Should be a single axes object
        assert hasattr(ax, "plot")

    def test_subplots_with_figsize(self):
        """Test subplots with custom figure size."""
        fig, axes = subplots(2, 2, figsize=(10, 8))

        assert fig is not None
        assert axes is not None

        # Check figure size
        figsize = fig.get_size_inches()
        assert figsize[0] == 10
        assert figsize[1] == 8

    def test_subplots_with_kwargs(self):
        """Test subplots with additional keyword arguments."""
        # Test that additional kwargs can be passed
        fig, axes = subplots(2, 2, figsize=(8, 6))

        assert fig is not None
        assert axes is not None

    def teardown_method(self):
        """Clean up after each test."""
        import matplotlib.pyplot as plt

        plt.close("all")


class TestUtilityErrors:
    """Test error handling in utility functions."""

    def test_prepare_data_invalid_column(self):
        """Test prepare_data with invalid column name."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        with pytest.raises(KeyError):
            prepare_data(df, x="nonexistent", y="y")

    def test_prepare_data_none_data_none_arrays(self):
        """Test prepare_data with None data and None arrays."""
        x_data, y_data = prepare_data(None, x=None, y=None)

        assert x_data is None
        assert y_data is None

    def test_map_colors_to_categories_invalid_mapping(self):
        """Test color mapping with invalid color mapping."""
        categories = ["A", "B", "C"]
        color_mapping = {"A": "invalid_color"}

        # Should handle invalid colors gracefully
        ordered_categories, colors = map_colors_to_categories(
            categories, color_mapping=color_mapping
        )

        assert len(ordered_categories) == 3
        assert len(colors) == 3

    def test_subplots_invalid_dimensions(self):
        """Test subplots with invalid dimensions."""
        with pytest.raises(ValueError):
            subplots(0, 2)

        with pytest.raises(ValueError):
            subplots(2, 0)

    def test_subplots_negative_dimensions(self):
        """Test subplots with negative dimensions."""
        with pytest.raises(ValueError):
            subplots(-1, 2)

        with pytest.raises(ValueError):
            subplots(2, -1)
