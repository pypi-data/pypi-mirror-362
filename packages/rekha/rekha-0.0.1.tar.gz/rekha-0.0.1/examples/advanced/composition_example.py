#!/usr/bin/env python3
"""
Plot composition examples for Rekha.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_bar_line_composition(dark_mode=False):
    """Create a composed bar and line plot."""
    # Generate sample data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]

    df = pd.DataFrame(
        {
            "month": months,
            "actual_sales": [100, 120, 115, 130, 125, 140, 145, 160],
            "forecast": [105, 118, 120, 128, 130, 135, 142, 155],
            "target": [110, 125, 125, 135, 135, 145, 150, 165],
        }
    )

    # Create base bar plot
    bar_plot = rk.bar(
        df,
        x="month",
        y="actual_sales",
        title="Sales Performance vs Forecast and Target",
        labels={"month": "Month", "actual_sales": "Sales ($k)"},
        dark_mode=dark_mode,
    )

    # Add line plot for forecast on top
    line_plot = rk.line(
        df, x="month", y="forecast", base_plot=bar_plot, markers=True, label="Forecast"
    )

    # Add another line for target
    target_plot = rk.line(
        df,
        x="month",
        y="target",
        base_plot=line_plot,
        line_style="--",
        markers=True,
        label="Target",
    )

    # Update legend to show all elements
    ax = target_plot.ax
    ax.legend()

    return target_plot


def create_scatter_line_composition(dark_mode=False):
    """Create a composed scatter and trend line plot."""
    # Generate correlated data
    np.random.seed(42)
    n_points = 100

    x = np.random.uniform(0, 10, n_points)
    y = 2.5 * x + 10 + np.random.normal(0, 3, n_points)

    df = pd.DataFrame({"x": x, "y": y})

    # Create base scatter plot
    scatter_plot = rk.scatter(
        df,
        x="x",
        y="y",
        title="Data Points with Trend Line",
        labels={"x": "X Variable", "y": "Y Variable"},
        alpha=0.6,
        dark_mode=dark_mode,
    )

    # Calculate trend line
    z = np.polyfit(x, y, 1)
    trend_x = np.array([x.min(), x.max()])
    trend_y = z[0] * trend_x + z[1]

    trend_df = pd.DataFrame({"x": trend_x, "y": trend_y})

    # Add trend line
    line_plot = rk.line(
        trend_df,
        x="x",
        y="y",
        base_plot=scatter_plot,
        color="red",
        line_width=3,
        label=f"Trend: y={z[0]:.2f}x+{z[1]:.2f}",
    )

    # Add legend
    line_plot.ax.legend()

    return line_plot


def create_multi_series_composition(dark_mode=False):
    """Create a composition with multiple data series."""
    # Generate time series data
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=50, freq="D")

    # Different metrics with different scales
    df = pd.DataFrame(
        {
            "date": dates,
            "revenue": 1000 + np.cumsum(np.random.randn(50) * 20),
            "users": 500 + np.cumsum(np.random.randn(50) * 10),
            "conversion_rate": 0.1 + np.random.randn(50) * 0.02,
        }
    )

    # Sample every 10 days for bar chart and format dates
    df_bars = df[::10].copy()
    df_bars["date_str"] = df_bars["date"].dt.strftime("%b %d")  # type: ignore[attr-defined]

    # Create base plot with revenue (bar chart)
    bar_plot = rk.bar(
        df_bars,
        x="date_str",
        y="revenue",
        title="Business Metrics Over Time",
        labels={"date_str": "Date", "revenue": "Revenue ($)"},
        alpha=0.7,
        bar_width=0.2,  # Narrower bars for better composition
        dark_mode=dark_mode,
    )

    # For line plot, we need to map dates to bar positions
    # Create numeric x positions for the full dataset
    bar_dates = df_bars["date"].values  # type: ignore[attr-defined]
    df["x_pos"] = np.interp(
        df["date"].astype(np.int64),
        bar_dates.astype(np.int64),
        np.arange(len(bar_dates)),
    )

    # Add user count as line
    line_plot = rk.line(
        df,
        x="x_pos",
        y="users",
        base_plot=bar_plot,
        color="green",
        line_width=3,
        label="Active Users",
    )

    # Since conversion rate is on a different scale, we'd need dual axis
    # For now, let's add it as scatter points scaled up
    df["conversion_scaled"] = df["conversion_rate"] * 5000  # Scale to match revenue

    scatter_plot = rk.scatter(
        df[::3],
        x="x_pos",
        y="conversion_scaled",  # Sample every 3 days
        base_plot=line_plot,
        point_size=50,
        alpha=0.8,
        label="Conversion Rate (scaled)",
    )

    # Update legend
    scatter_plot.ax.legend()

    return scatter_plot


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate plot composition examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating plot composition examples...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    examples = [
        ("composition_bar_line", create_bar_line_composition),
        ("composition_scatter_trend", create_scatter_line_composition),
        ("composition_multi_series", create_multi_series_composition),
    ]

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plots...")
        for name, func in examples:
            try:
                fig = func(dark_mode=dark_mode)

                if args.output:
                    output_file = os.path.join(
                        args.output, f"advanced_{name}_{mode_name}.png"
                    )
                    fig.save(output_file, format="social")
                    print(f"✓ Saved: {output_file}")
                else:
                    fig.show()
            except Exception as e:
                print(f"✗ Error generating {name}: {e}")
                import traceback

                traceback.print_exc()

    print("\nPlot composition examples generated!")
