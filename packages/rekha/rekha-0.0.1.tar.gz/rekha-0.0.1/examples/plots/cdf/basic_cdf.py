#!/usr/bin/env python3
"""
CDF plot examples for Rekha documentation.

This script generates all the CDF examples shown in the user guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def basic_cdf(dark_mode=False):
    """Basic cumulative distribution function plot."""
    # Generate sample data
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)
    df = pd.DataFrame({"values": data})

    fig = rk.cdf(
        data=df,
        x="values",
        title="Cumulative Distribution Function",
        labels={"values": "Value", "y": "Cumulative Probability"},
        dark_mode=dark_mode,
    )
    return fig


def comparison_cdf(dark_mode=False):
    """Compare multiple distributions using CDFs."""
    # Generate different distributions
    np.random.seed(42)
    normal_dist = np.random.normal(100, 15, 1000)
    skewed_dist = np.random.lognormal(4.5, 0.5, 1000)
    uniform_dist = np.random.uniform(50, 150, 1000)

    df = pd.DataFrame(
        {
            "value": np.concatenate([normal_dist, skewed_dist, uniform_dist]),
            "distribution": ["Normal"] * 1000
            + ["Log-Normal"] * 1000
            + ["Uniform"] * 1000,
        }
    )

    fig = rk.cdf(
        data=df,
        x="value",
        color="distribution",
        title="Distribution Comparison using CDFs",
        labels={"value": "Value", "y": "Cumulative Probability"},
        dark_mode=dark_mode,
    )
    return fig


def percentile_analysis(dark_mode=False):
    """Use CDF for percentile analysis."""
    # Generate performance data
    np.random.seed(42)
    response_times = np.concatenate(
        [
            np.random.lognormal(3.0, 0.3, 800),  # Fast responses
            np.random.lognormal(4.0, 0.5, 150),  # Medium responses
            np.random.lognormal(5.0, 0.7, 50),  # Slow responses
        ]
    )

    df = pd.DataFrame({"response_time_ms": response_times})

    fig = rk.cdf(
        data=df,
        x="response_time_ms",
        title="Response Time Percentile Analysis",
        labels={"response_time_ms": "Response Time (ms)", "y": "Percentile"},
        dark_mode=dark_mode,
    )

    # Note: Additional customization would be done via matplotlib after getting the axes
    # For now, just return the basic CDF plot

    return fig


def grouped_cdf(dark_mode=False):
    """CDFs grouped by category."""
    # Generate data for different groups
    np.random.seed(42)

    data_rows = []
    for region in ["North", "South", "East", "West"]:
        # Different performance characteristics by region
        if region == "North":
            values = np.random.normal(100, 10, 500)
        elif region == "South":
            values = np.random.normal(110, 15, 500)
        elif region == "East":
            values = np.random.normal(95, 12, 500)
        else:  # West
            values = np.random.normal(105, 18, 500)

        for v in values:
            data_rows.append({"sales": v, "region": region})

    df = pd.DataFrame(data_rows)

    fig = rk.cdf(
        data=df,
        x="sales",
        color="region",
        title="Sales Distribution by Region",
        labels={"sales": "Sales ($k)", "y": "Cumulative Probability"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate CDF plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating CDF plot examples...")

    plots = [
        ("basic", basic_cdf),
        ("comparison", comparison_cdf),
        ("percentile", percentile_analysis),
        ("grouped", grouped_cdf),
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
                output_file = os.path.join(args.output, f"cdf_{name}_{mode_name}.png")
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll CDF plot examples generated!")
