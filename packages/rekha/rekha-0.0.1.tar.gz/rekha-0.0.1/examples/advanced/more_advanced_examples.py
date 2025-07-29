#!/usr/bin/env python3
"""
More advanced examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_sorted_bar_example(dark_mode=False):
    """Create bar plot with sorted categories."""
    # Create sample data
    df = pd.DataFrame(
        {
            "product": [
                "Product A",
                "Product B",
                "Product C",
                "Product D",
                "Product E",
            ],
            "sales": [150, 320, 280, 90, 410],
        }
    )

    # Sort by sales value
    df_sorted = df.sort_values("sales", ascending=False)

    fig = rk.bar(
        df_sorted,
        x="product",
        y="sales",
        title="Product Sales (Sorted by Value)",
        labels={"product": "Product", "sales": "Sales ($)"},
        dark_mode=dark_mode,
    )

    return fig


def create_custom_color_order_example(dark_mode=False):
    """Create plot with custom category ordering."""
    # Create sample data with logical ordering
    np.random.seed(42)
    sizes = ["XS", "S", "M", "L", "XL", "XXL"]
    sales = [45, 78, 120, 95, 62, 30]

    df = pd.DataFrame(
        {
            "size": sizes * 3,  # Repeat for multiple data points
            "sales": sales * 3 + np.random.normal(0, 10, len(sizes) * 3),
        }
    )

    # Create categorical with proper order
    df["size"] = pd.Categorical(df["size"], categories=sizes, ordered=True)

    fig = rk.box(
        df,
        x="size",
        y="sales",
        title="Sales Distribution by Size",
        labels={"size": "Size", "sales": "Sales ($)"},
        dark_mode=dark_mode,
    )

    return fig


def create_reference_lines_example(dark_mode=False):
    """Create plot with reference lines and annotations."""
    # Generate time series data
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=90, freq="D")
    values = 100 + np.cumsum(np.random.randn(90)) * 2

    df = pd.DataFrame({"date": dates, "value": values})

    # Create line plot
    fig = rk.line(
        df,
        x="date",
        y="value",
        title="Time Series with Reference Elements",
        labels={"date": "Date", "value": "Value"},
        dark_mode=dark_mode,
    )

    # Add customizations
    ax = fig.get_axes()[0]

    # Add horizontal reference line
    mean_val = values.mean()
    ax.axhline(
        y=mean_val,
        color="red",
        linestyle="--",
        alpha=0.7,
        label=f"Mean: {mean_val:.1f}",
    )

    # Add vertical reference line
    important_date = dates[45]
    ax.axvline(
        x=important_date, color="green", linestyle=":", alpha=0.7, label="Event Date"
    )

    # Add shaded region
    ax.axhspan(
        values.min(),
        np.percentile(values, 25),
        alpha=0.1,
        color="red",
        label="Bottom Quartile",
    )

    # Update legend
    ax.legend()

    return fig


def create_grouped_colored_bar_example(dark_mode=False):
    """Create grouped bar plot with consistent colors."""
    # Create sample data
    categories = ["Q1", "Q2", "Q3", "Q4"]

    df = pd.DataFrame(
        {
            "quarter": categories * 3,
            "revenue": [100, 120, 140, 160, 90, 110, 130, 150, 80, 100, 120, 140],
            "product": ["Product A"] * 4 + ["Product B"] * 4 + ["Product C"] * 4,
        }
    )

    # Define custom colors
    color_scheme = {
        "Product A": "#FF6B6B",
        "Product B": "#4ECDC4",
        "Product C": "#45B7D1",
    }

    fig = rk.bar(
        df,
        x="quarter",
        y="revenue",
        color="product",
        title="Quarterly Revenue by Product",
        labels={"quarter": "Quarter", "revenue": "Revenue ($k)", "product": "Product"},
        color_mapping=color_scheme,
        dark_mode=dark_mode,
    )

    return fig


def create_annotated_scatter_example(dark_mode=False):
    """Create scatter plot with annotations."""
    # Generate sample data
    np.random.seed(42)
    n_points = 50

    df = pd.DataFrame(
        {
            "efficiency": np.random.uniform(0.6, 0.95, n_points),
            "cost": np.random.uniform(50, 150, n_points),
        }
    )

    # Add categories based on efficiency/cost ratio
    df["category"] = pd.cut(
        df["efficiency"] / df["cost"] * 100,
        bins=3,
        labels=["Low ROI", "Medium ROI", "High ROI"],
    )

    fig = rk.scatter(
        df,
        x="cost",
        y="efficiency",
        color="category",
        title="Cost vs Efficiency Analysis",
        labels={"cost": "Cost ($)", "efficiency": "Efficiency Score"},
        alpha=0.7,
        dark_mode=dark_mode,
    )

    # Add annotations
    ax = fig.get_axes()[0]

    # Highlight best and worst points
    best_idx = (df["efficiency"] / df["cost"]).idxmax()
    worst_idx = (df["efficiency"] / df["cost"]).idxmin()

    ax.annotate(
        "Best ROI",
        xy=(df.loc[best_idx, "cost"], df.loc[best_idx, "efficiency"]),
        xytext=(df.loc[best_idx, "cost"] + 10, df.loc[best_idx, "efficiency"] + 0.05),
        arrowprops=dict(arrowstyle="->", color="green", lw=2),
    )

    ax.annotate(
        "Worst ROI",
        xy=(df.loc[worst_idx, "cost"], df.loc[worst_idx, "efficiency"]),
        xytext=(df.loc[worst_idx, "cost"] + 10, df.loc[worst_idx, "efficiency"] - 0.05),
        arrowprops=dict(arrowstyle="->", color="red", lw=2),
    )

    return fig


def create_combined_plot_types_example(dark_mode=False):
    """Create plot combining multiple visualization types."""
    # Generate sample data
    np.random.seed(42)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    df = pd.DataFrame(
        {
            "month": months,
            "actual": [100, 120, 115, 130, 125, 140],
            "forecast": [105, 118, 120, 128, 130, 135],
            "target": [110, 125, 125, 135, 135, 145],
        }
    )

    # Create bar plot for actual values
    fig = rk.bar(
        df,
        x="month",
        y="actual",
        title="Sales Performance vs Forecast and Target",
        labels={"month": "Month", "actual": "Sales ($k)"},
        dark_mode=dark_mode,
    )

    # Add line plots for forecast and target
    ax = fig.get_axes()[0]

    # Add forecast line
    ax.plot(
        df["month"],
        df["forecast"],
        "o-",
        color="orange",
        linewidth=2,
        markersize=8,
        label="Forecast",
    )

    # Add target line
    ax.plot(
        df["month"],
        df["target"],
        "s--",
        color="red",
        linewidth=2,
        markersize=6,
        alpha=0.7,
        label="Target",
    )

    # Update legend
    ax.legend()

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate more advanced examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating more advanced examples...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    examples = [
        # ("sorted_bar", create_sorted_bar_example),  # Not documented yet
        ("custom_order", create_custom_color_order_example),
        ("reference_lines", create_reference_lines_example),
        ("grouped_colors", create_grouped_colored_bar_example),
        ("annotated_scatter", create_annotated_scatter_example),
        ("combined_types", create_combined_plot_types_example),
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

    print("\nMore advanced examples generated!")
