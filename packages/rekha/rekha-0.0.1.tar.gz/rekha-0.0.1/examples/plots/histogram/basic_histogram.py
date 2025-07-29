#!/usr/bin/env python3
"""
Histogram examples for Rekha documentation.

This script generates all the histogram examples shown in the user guide.
"""

import numpy as np
import pandas as pd

import rekha as rk
from examples.utils import get_distribution_data, get_iris


def basic_histogram(dark_mode=False):
    """Simple distribution visualization."""
    # Generate normal distribution
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)
    df = pd.DataFrame({"values": data})

    fig = rk.histogram(
        data=df,
        x="values",
        title="Normal Distribution",
        labels={"values": "Value"},
        nbins=30,
        dark_mode=dark_mode,
    )
    return fig


def comparison(dark_mode=False):
    """Compare distributions using side-by-side facets."""
    # Create multiple distributions for comparison
    normal = get_distribution_data("normal")
    skewed = get_distribution_data("skewed")

    df = pd.DataFrame({"normal": normal, "skewed_right": skewed})

    # Reshape to long format
    data_long = pd.melt(
        df[["normal", "skewed_right"]], var_name="distribution", value_name="value"
    )

    fig = rk.histogram(
        data=data_long,
        x="value",
        facet_col="distribution",
        title="Distribution Comparison",
        labels={"value": "Value", "distribution": "Type"},
        nbins=25,
        dark_mode=dark_mode,
    )
    return fig


def grouped_histogram(dark_mode=False):
    """Compare distributions across groups."""
    df_iris = get_iris()

    fig = rk.histogram(
        data=df_iris,
        x="petal_length",
        color="species",
        title="Petal Length by Species",
        labels={"petal_length": "Petal Length (cm)", "species": "Species"},
        alpha=0.8,
        nbins=20,
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate histogram plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating histogram plot examples...")

    plots = [
        ("basic", basic_histogram),
        ("comparison", comparison),
        ("grouped", grouped_histogram),
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
                    args.output, f"histogram_{name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll histogram plot examples generated!")
