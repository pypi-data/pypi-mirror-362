#!/usr/bin/env python3
"""
Generate additional quickstart plots that are referenced in docs but not directly generated.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_bar_plot(dark_mode=False):
    """Create a bar plot for quickstart."""
    # Sample data
    data = pd.DataFrame(
        {"category": ["A", "B", "C", "D", "E"], "value": [23, 45, 56, 78, 32]}
    )

    fig = rk.bar(
        data=data,
        x="category",
        y="value",
        title="Sample Bar Chart",
        dark_mode=dark_mode,
    )
    return fig


def create_histogram_plot(dark_mode=False):
    """Create a histogram for quickstart."""
    # Generate random data
    np.random.seed(42)
    data = pd.DataFrame({"values": np.random.normal(100, 20, 1000)})

    fig = rk.histogram(
        data=data,
        x="values",
        title="Distribution Example",
        nbins=30,
        dark_mode=dark_mode,
    )
    return fig


def create_line_styles_plot(dark_mode=False):
    """Create a line plot with different styles for quickstart."""
    # Generate data
    x = np.linspace(0, 10, 100)
    data = pd.DataFrame(
        {
            "x": np.tile(x, 3),
            "y": np.concatenate([np.sin(x), np.cos(x), np.sin(x) * np.cos(x)]),
            "style": ["Sine"] * 100 + ["Cosine"] * 100 + ["Product"] * 100,
        }
    )

    fig = rk.line(
        data=data,
        x="x",
        y="y",
        color="style",
        title="Line Styles Example",
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate additional quickstart plots")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating additional quickstart plots...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    # Generate plots based on mode
    plots = [
        ("bar", create_bar_plot),
        ("histogram", create_histogram_plot),
        ("line_styles", create_line_styles_plot),
    ]

    for plot_name, plot_func in plots:
        if args.mode in ["light", "both"]:
            fig = plot_func(dark_mode=False)
            if args.output:
                output_file = os.path.join(
                    args.output, f"quickstart_{plot_name}_light.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

        if args.mode in ["dark", "both"]:
            fig = plot_func(dark_mode=True)
            if args.output:
                output_file = os.path.join(
                    args.output, f"quickstart_{plot_name}_dark.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print("\nAdditional quickstart plots generated!")
