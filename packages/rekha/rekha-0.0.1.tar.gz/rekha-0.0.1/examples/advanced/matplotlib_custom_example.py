#!/usr/bin/env python3
"""
Matplotlib customization examples for documentation.
"""

import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Rectangle

import rekha as rk


def create_matplotlib_custom_example(dark_mode=False):
    """Create a plot with matplotlib customizations."""
    # Generate sample data
    np.random.seed(42)
    n_points = 100

    df = pd.DataFrame(
        {
            "x": np.linspace(0, 10, n_points),
            "y": 2 * np.sin(np.linspace(0, 10, n_points))
            + np.random.normal(0, 0.2, n_points),
            "category": np.random.choice(["A", "B"], n_points),
        }
    )

    # Create base plot with Rekha
    fig = rk.scatter(
        df,
        x="x",
        y="y",
        color="category",
        title="Customized Plot with Matplotlib",
        labels={"x": "X Variable", "y": "Y Variable"},
        figsize=(10, 6),
        dark_mode=dark_mode,
    )

    # Access matplotlib axes
    ax = fig.get_axes()[0]

    # Add annotations
    important_point = df.loc[df["y"].idxmax()]
    ax.annotate(
        "Peak Value",
        xy=(important_point["x"], important_point["y"]),
        xytext=(important_point["x"] - 2, important_point["y"] + 1),
        fontsize=12,
        arrowprops=dict(
            arrowstyle="->", color="red" if not dark_mode else "#FF6B6B", lw=2
        ),
    )

    # Add reference lines
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5, label="Zero line")
    ax.axvline(x=5, color="gray", linestyle=":", alpha=0.5, label="Midpoint")

    # Add shaded region
    ax.axvspan(
        3,
        7,
        alpha=0.1,
        color="blue" if not dark_mode else "lightblue",
        label="Region of Interest",
    )

    # Add custom shapes - highlight a region with interesting data
    # Find a region with high density of points
    y_center = df[(df["x"] > 2) & (df["x"] < 3)]["y"].mean()
    rect = Rectangle(
        (2, y_center - 0.5),
        1,
        1,
        linewidth=2,
        edgecolor="green" if not dark_mode else "#2ECC71",
        facecolor="green" if not dark_mode else "#2ECC71",
        alpha=0.2,
    )
    ax.add_patch(rect)

    # Add a circle to highlight another point
    circle = Circle(
        (7.5, 0.5), 0.3, color="orange" if not dark_mode else "#FFA500", alpha=0.5
    )
    ax.add_patch(circle)

    # Add text box
    textstr = f'n = {len(df)}\nMean Y = {df["y"].mean():.2f}'
    props = dict(
        boxstyle="round",
        facecolor="wheat" if not dark_mode else "#34495E",
        alpha=0.8 if not dark_mode else 0.5,
    )
    ax.text(
        0.02,
        0.98,
        textstr,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=props,
    )

    # Update legend to include new elements
    ax.legend(loc="lower right")

    # Customize grid
    ax.grid(True, alpha=0.3, linestyle=":", linewidth=1)

    return fig


def create_dual_axis_example(dark_mode=False):
    """Create a plot with dual y-axes."""
    # Generate sample data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    temperature = [5, 8, 15, 20, 25, 28]
    rainfall = [120, 100, 80, 60, 40, 30]

    df_temp = pd.DataFrame({"month": months, "temperature": temperature})

    # Create primary plot
    fig = rk.line(
        df_temp,
        x="month",
        y="temperature",
        title="Temperature and Rainfall Trends",
        labels={"month": "Month", "temperature": "Temperature (°C)"},
        color=None,  # Single series
        figsize=(10, 6),
        dark_mode=dark_mode,
    )

    ax1 = fig.get_axes()[0]

    # Customize primary axis
    line1 = ax1.get_lines()[0]
    line1.set_color("tab:red")
    line1.set_linewidth(3)
    line1.set_marker("o")
    line1.set_markersize(8)
    ax1.set_ylabel("Temperature (°C)", color="tab:red", fontsize=12, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    # Create secondary y-axis
    ax2 = ax1.twinx()
    line2 = ax2.plot(
        months, rainfall, "b-s", linewidth=3, markersize=8, label="Rainfall", alpha=0.8
    )
    ax2.set_ylabel("Rainfall (mm)", color="tab:blue", fontsize=12, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    # Add legends
    ax1.legend([line1], ["Temperature"], loc="upper left")
    ax2.legend(loc="upper right")

    # Add grid for both axes
    ax1.grid(True, alpha=0.3, axis="x")
    ax2.grid(True, alpha=0.2, axis="y", linestyle=":")

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate matplotlib customization examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating matplotlib customization examples...")

    plots = [
        ("matplotlib_custom", create_matplotlib_custom_example),
        ("matplotlib_dual_axis", create_dual_axis_example),
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

    print(f"\nAll matplotlib customization examples generated!")
