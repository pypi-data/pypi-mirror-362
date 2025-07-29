"""Basic tests for Rekha plotting functionality."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import rekha as rk


class TestBasicPlots:
    """Test basic plotting functionality."""

    def setup_method(self):
        """Set up test data."""
        np.random.seed(42)
        self.df = pd.DataFrame(
            {
                "x": range(10),
                "y": np.random.randn(10),
                "category": ["A", "B"] * 5,
                "size": np.random.randint(20, 100, 10),
            }
        )

    def test_line_plot_creation(self):
        """Test line plot creation."""
        fig = rk.line(self.df, x="x", y="y")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)

    def test_scatter_plot_creation(self):
        """Test scatter plot creation."""
        fig = rk.scatter(self.df, x="x", y="y")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)

    def test_bar_plot_creation(self):
        """Test bar plot creation."""
        fig = rk.bar(self.df, x="category", y="y")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)

    def test_histogram_creation(self):
        """Test histogram creation."""
        fig = rk.histogram(self.df, x="y")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)

    def test_dark_mode(self):
        """Test dark mode functionality."""
        fig = rk.line(self.df, x="x", y="y", dark_mode=True)
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)

    def test_color_grouping(self):
        """Test color grouping in plots."""
        fig = rk.scatter(self.df, x="x", y="y", color="category")
        assert hasattr(fig, "ax")
        assert hasattr(fig, "fig")
        plt.close(fig.fig)


class TestTheme:
    """Test theme functionality."""

    def test_theme_application(self):
        """Test theme setting."""
        colors = rk.set_rekha_theme(dark_mode=False)
        assert "colors" in colors
        assert "accent" in colors
        assert "background" in colors

    def test_dark_theme_application(self):
        """Test dark theme setting."""
        colors = rk.set_rekha_theme(dark_mode=True)
        assert "colors" in colors
        assert "accent" in colors
        assert "background" in colors


class TestSubplots:
    """Test subplot functionality."""

    def test_subplots_creation(self):
        """Test subplots creation."""
        fig, axes = rk.subplots(2, 2)
        assert fig is not None
        assert axes is not None
        plt.close(fig)
