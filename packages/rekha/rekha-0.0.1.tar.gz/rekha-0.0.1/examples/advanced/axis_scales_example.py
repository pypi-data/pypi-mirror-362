#!/usr/bin/env python3
"""
Axis scales and formatting examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_log_scale_example(dark_mode=False):
    """Create log scale demonstration plot."""
    # Generate exponential data
    np.random.seed(42)
    x = np.linspace(1, 5, 50)
    y = np.exp(x) + np.random.normal(0, np.exp(x) * 0.1, 50)

    df = pd.DataFrame({"x": x, "y": y})

    # Create plot with log scale
    fig = rk.scatter(
        df,
        x="x",
        y="y",
        title="Exponential Growth with Log Scale",
        labels={"x": "Time (years)", "y": "Population"},
        yscale="log",
        dark_mode=dark_mode,
    )

    return fig


def create_humanized_example(dark_mode=False):
    """Create humanized numbers demonstration plot."""
    # Tech company revenue data
    companies = ["Apple", "Microsoft", "Google", "Amazon", "Meta", "Tesla", "Netflix"]
    revenue = [
        383285000000,
        198270000000,
        282836000000,
        469822000000,
        116609000000,
        81462000000,
        31615000000,
    ]

    df = pd.DataFrame({"company": companies, "revenue": revenue})

    # Sort by revenue
    df = df.sort_values("revenue", ascending=True)

    # Create horizontal bar chart with humanized units
    fig = rk.bar(
        df,
        x="revenue",
        y="company",
        orientation="h",
        title="Tech Company Annual Revenue (2022)",
        labels={"company": "", "revenue": "Revenue"},
        humanize_units=True,
        humanize_format="intword",
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate axis scales examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating axis scales and formatting examples...")

    plots = [
        ("log_scale", create_log_scale_example),
        ("humanized", create_humanized_example),
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

    print(f"\nAll axis scales examples generated!")
