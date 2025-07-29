#!/usr/bin/env python3
"""
Heatmap examples for Rekha documentation.

This script generates all the heatmap examples shown in the user guide.
"""

import rekha as rk
from examples.utils import get_iris, get_tips


def correlation_heatmap(dark_mode=False):
    """Feature correlation analysis."""
    df = get_iris()

    # Calculate correlation matrix
    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    correlation_matrix = df[numeric_cols].corr()

    # Pretty column names
    correlation_matrix.index = [
        "Sepal Length",
        "Sepal Width",
        "Petal Length",
        "Petal Width",
    ]
    correlation_matrix.columns = [
        "Sepal Length",
        "Sepal Width",
        "Petal Length",
        "Petal Width",
    ]

    fig = rk.heatmap(
        data=correlation_matrix,
        title="Feature Correlations",
        text_auto=True,
        dark_mode=dark_mode,
    )
    return fig


def pivot_table_heatmap(dark_mode=False):
    """Visualize pivot table data."""
    df_tips = get_tips()

    # Create pivot table
    pivot_table = df_tips.pivot_table(
        values="tip", index="day", columns="time", aggfunc="mean"
    )

    fig = rk.heatmap(
        data=pivot_table,
        title="Average Tip by Day and Time",
        text_auto=True,
        dark_mode=dark_mode,
    )
    return fig


def custom_colormap_heatmap(dark_mode=False):
    """Heatmap with custom colormap."""
    df = get_iris()

    # Create a different kind of matrix
    species_features = df.groupby("species")[
        ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    ].mean()

    fig = rk.heatmap(
        data=species_features,
        title="Average Features by Species",
        text_auto=True,
        cmap="viridis",
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate heatmap plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating heatmap plot examples...")

    plots = [
        ("correlation", correlation_heatmap),
        ("pivot", pivot_table_heatmap),
        (
            "pivot",
            custom_colormap_heatmap,
        ),  # Changed to "pivot" as docs only expect correlation and pivot
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
                    args.output, f"heatmap_{name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll heatmap plot examples generated!")
