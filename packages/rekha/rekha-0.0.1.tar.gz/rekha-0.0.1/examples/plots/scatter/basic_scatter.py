#!/usr/bin/env python3
"""
Scatter plot examples for Rekha documentation.

This script generates all the scatter plot examples shown in the user guide.
"""

import rekha as rk
from examples.utils import get_iris, get_tips


def basic_scatter(dark_mode=False):
    """Simple relationship visualization."""
    df = get_iris()

    fig = rk.scatter(
        data=df,
        x="sepal_length",
        y="sepal_width",
        title="Iris Sepal Dimensions",
        labels={"sepal_length": "Sepal Length (cm)", "sepal_width": "Sepal Width (cm)"},
        dark_mode=dark_mode,
    )
    return fig


def colored_scatter(dark_mode=False):
    """Use color to distinguish categories."""
    df = get_iris()

    fig = rk.scatter(
        data=df,
        x="petal_length",
        y="petal_width",
        color="species",
        title="Iris Petal Dimensions by Species",
        labels={
            "petal_length": "Petal Length (cm)",
            "petal_width": "Petal Width (cm)",
            "species": "Species",
        },
        dark_mode=dark_mode,
    )
    return fig


def sized_scatter(dark_mode=False):
    """Combine color, size, and shape for complex visualizations."""
    df_tips = get_tips()

    fig = rk.scatter(
        data=df_tips,
        x="total_bill",
        y="tip",
        size="size",  # Party size
        color="time",  # Lunch vs Dinner
        title="Restaurant Tips Analysis",
        labels={
            "total_bill": "Total Bill ($)",
            "tip": "Tip ($)",
            "size": "Party Size",
            "time": "Meal Time",
        },
        alpha=0.7,
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate scatter plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating scatter plot examples...")

    plots = [
        ("basic", basic_scatter),
        ("colored", colored_scatter),
        ("sized", sized_scatter),
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
                    args.output, f"scatter_{name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll scatter plot examples generated!")
