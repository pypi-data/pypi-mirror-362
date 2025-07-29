#!/usr/bin/env python3
"""
Grayscale mode examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_grayscale_bar(dark_mode=False):
    """Create a bar plot optimized for grayscale printing."""
    # Create sample data
    df = pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "product_a": [100, 120, 140, 110, 160],
            "product_b": [80, 90, 100, 120, 130],
            "product_c": [60, 70, 85, 95, 100],
        }
    )

    # Reshape for grouped bars
    df_long = pd.melt(df, id_vars=["month"], var_name="product", value_name="sales")
    df_long["product"] = (
        df_long["product"].str.replace("product_", "Product ").str.upper()
    )

    fig = rk.bar(
        df_long,
        x="month",
        y="sales",
        color="product",
        title="Monthly Sales by Product (grayscale Mode)",
        labels={"month": "Month", "sales": "Sales ($)", "product": "Product"},
        grayscale_friendly=True,
        dark_mode=dark_mode,
    )

    return fig


def create_grayscale_line(dark_mode=False):
    """Create a line plot with different line styles for grayscale."""
    # Generate time series data
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=50, freq="D")

    df = pd.DataFrame(
        {
            "date": np.tile(dates, 3),
            "value": np.concatenate(
                [
                    np.cumsum(np.random.randn(50)) + 100,
                    np.cumsum(np.random.randn(50)) + 110,
                    np.cumsum(np.random.randn(50)) + 95,
                ]
            ),
            "series": ["Series A"] * 50 + ["Series B"] * 50 + ["Series C"] * 50,
        }
    )

    fig = rk.line(
        df,
        x="date",
        y="value",
        color="series",
        title="Time Series Comparison (grayscale Mode)",
        labels={"date": "Date", "value": "Value", "series": "Series"},
        grayscale_friendly=True,
        markers=True,  # Add markers for additional distinction
        dark_mode=dark_mode,
    )

    return fig


def create_grayscale_scatter(dark_mode=False):
    """Create a scatter plot with different markers for grayscale."""
    # Generate sample data
    np.random.seed(42)
    n_points = 100

    df = pd.DataFrame(
        {
            "x": np.concatenate(
                [
                    np.random.normal(0, 1, n_points),
                    np.random.normal(2, 1, n_points),
                    np.random.normal(1, 1.5, n_points),
                ]
            ),
            "y": np.concatenate(
                [
                    np.random.normal(0, 1, n_points),
                    np.random.normal(1, 1.2, n_points),
                    np.random.normal(-1, 1, n_points),
                ]
            ),
            "group": ["Group A"] * n_points
            + ["Group B"] * n_points
            + ["Group C"] * n_points,
        }
    )

    fig = rk.scatter(
        df,
        x="x",
        y="y",
        color="group",
        title="Group Distribution (grayscale Mode)",
        labels={"x": "X Variable", "y": "Y Variable", "group": "Group"},
        grayscale_friendly=True,
        point_size=200,
        alpha=0.7,
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate grayscale mode examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating grayscale mode examples...")

    plots = [
        ("bw_bar", create_grayscale_bar),
        ("bw_line", create_grayscale_line),
        ("bw_scatter", create_grayscale_scatter),
    ]

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plots...")
        for name, func in plots:
            fig = func(dark_mode=dark_mode)

            if args.output:
                os.makedirs(args.output, exist_ok=True)
                output_file = os.path.join(
                    args.output, f"advanced_{name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll grayscale mode examples generated!")
