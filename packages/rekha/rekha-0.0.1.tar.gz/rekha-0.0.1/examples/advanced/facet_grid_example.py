#!/usr/bin/env python3
"""
Facet grid examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_facet_grid_example(dark_mode=False):
    """Create a facet grid example with scatter plots."""
    # Generate sample data
    np.random.seed(42)
    data_rows = []

    for category in ["A", "B", "C"]:
        for region in ["North", "South"]:
            n_points = 50
            base_x = np.random.randn(n_points)
            base_y = np.random.randn(n_points)

            # Add some differences between categories and regions
            if category == "A":
                x = base_x + 0.5
                y = base_y + 0.3
            elif category == "B":
                x = base_x - 0.5
                y = base_y + 0.1
            else:  # C
                x = base_x
                y = base_y - 0.4

            if region == "North":
                y = y + 0.2

            for i in range(n_points):
                data_rows.append(
                    {"x": x[i], "y": y[i], "category": category, "region": region}
                )

    df = pd.DataFrame(data_rows)

    # Create faceted scatter plot using native support
    fig = rk.scatter(
        df,
        x="x",
        y="y",
        facet_col="category",
        facet_row="region",
        title="Data Distribution by Category and Region",
        figsize=(12, 8),
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate facet grid example")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating facet grid example...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    # Generate plots based on mode
    if args.mode in ["light", "both"]:
        fig = create_facet_grid_example(dark_mode=False)
        if args.output:
            output_file = os.path.join(args.output, "advanced_facet_grid_light.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    if args.mode in ["dark", "both"]:
        fig = create_facet_grid_example(dark_mode=True)
        if args.output:
            output_file = os.path.join(args.output, "advanced_facet_grid_dark.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    print("\nFacet grid example generated!")
