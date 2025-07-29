#!/usr/bin/env python3
"""
Box plot examples for Rekha documentation.

This script generates all the box plot examples shown in the user guide.
"""

import rekha as rk
from examples.utils import get_iris


def basic_box(dark_mode=False):
    """Single variable distribution summary."""
    df = get_iris()

    fig = rk.box(
        data=df,
        y="sepal_length",
        title="Sepal Length Distribution",
        dark_mode=dark_mode,
    )
    return fig


def grouped_box(dark_mode=False):
    """Compare distributions across categories."""
    df = get_iris()

    fig = rk.box(
        data=df,
        x="species",
        y="petal_length",
        title="Petal Length by Species",
        labels={"species": "Species", "petal_length": "Petal Length (cm)"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate box plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating box plot examples...")

    plots = [
        ("basic", basic_box),
        ("grouped", grouped_box),
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
                output_file = os.path.join(args.output, f"box_{name}_{mode_name}.png")
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll box plot examples generated!")
