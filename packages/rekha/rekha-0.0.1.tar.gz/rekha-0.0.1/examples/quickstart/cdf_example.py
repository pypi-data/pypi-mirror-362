#!/usr/bin/env python3
"""
CDF example for quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_cdf_plot(dark_mode=False):
    """Create CDF plot comparing response times."""
    # Generate sample data
    np.random.seed(42)

    # Simulate response times for different server types
    standard_server = np.random.lognormal(3.5, 0.5, 500)  # Mean ~33ms
    optimized_server = np.random.lognormal(3.0, 0.3, 500)  # Mean ~20ms
    premium_server = np.random.lognormal(2.5, 0.2, 500)  # Mean ~12ms

    # Create DataFrame
    df = pd.DataFrame(
        {
            "response_time": np.concatenate(
                [standard_server, optimized_server, premium_server]
            ),
            "server_type": ["Standard"] * 500 + ["Optimized"] * 500 + ["Premium"] * 500,
        }
    )

    # Create CDF plot
    fig = rk.cdf(
        df,
        x="response_time",
        color="server_type",
        title="Response Time Distribution by Server Type",
        labels={"response_time": "Response Time (ms)", "y": "Cumulative Probability"},
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate CDF example plot")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating CDF example plot...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    # Generate plots based on mode
    if args.mode in ["light", "both"]:
        fig = create_cdf_plot(dark_mode=False)
        if args.output:
            output_file = os.path.join(args.output, "quickstart_cdf_light.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    if args.mode in ["dark", "both"]:
        fig = create_cdf_plot(dark_mode=True)
        if args.output:
            output_file = os.path.join(args.output, "quickstart_cdf_dark.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    print("\nCDF example plot generated!")
