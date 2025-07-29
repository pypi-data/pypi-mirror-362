#!/usr/bin/env python3
"""
Line plot examples for Rekha documentation.

This script generates all the line plot examples shown in the user guide.
"""

import pandas as pd

import rekha as rk
from examples.utils import get_time_series_data


def basic_line(dark_mode=False):
    """Create a simple line plot showing a single time series."""
    df = get_time_series_data()

    fig = rk.line(
        data=df,
        x="date",
        y="users",
        title="Website Users Over Time",
        labels={"date": "Date", "users": "Daily Users"},
        dark_mode=dark_mode,
    )
    return fig


def multiple_lines(dark_mode=False):
    """Compare multiple metrics on the same plot."""
    df = get_time_series_data()

    # Reshape data for multiple lines
    metrics = ["users", "sessions"]
    data_long = pd.melt(
        df[["date"] + metrics],
        id_vars=["date"],
        value_vars=metrics,
        var_name="metric",
        value_name="value",
    )

    fig = rk.line(
        data=data_long,
        x="date",
        y="value",
        color="metric",
        title="Website Metrics Comparison",
        labels={"date": "Date", "value": "Count", "metric": "Metric"},
        dark_mode=dark_mode,
    )
    return fig


def line_with_markers(dark_mode=False):
    """Add markers to highlight individual data points."""
    df = get_time_series_data()

    # Use monthly data for cleaner marker display
    monthly_data = df.iloc[::30]  # Sample every 30 days

    fig = rk.line(
        data=monthly_data,
        x="date",
        y="users",
        title="Monthly User Trends",
        labels={"date": "Month", "users": "Users"},
        markers=True,
        line_width=3,
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate line plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating line plot examples...")

    plots = [
        ("basic", basic_line),
        ("multiple", multiple_lines),
        ("markers", line_with_markers),
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
                output_file = os.path.join(args.output, f"line_{name}_{mode_name}.png")
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll line plot examples generated!")
