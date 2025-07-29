#!/usr/bin/env python3
"""
Stacked bar plot example for Rekha documentation.
"""

import rekha as rk
from examples.utils import get_categorical_data


def stacked_bar_example(dark_mode=False):
    """Create a stacked bar plot showing component contributions."""
    df = get_categorical_data()

    # Aggregate by month (quarter) and component (product)
    sales_by_component = df.groupby(["quarter", "product"])["sales"].sum().reset_index()
    # Rename for clarity
    sales_by_component.columns = ["month", "component", "sales"]

    fig = rk.bar(
        data=sales_by_component,
        x="month",
        y="sales",
        color="component",
        barmode="stack",
        title="Monthly Sales Breakdown by Component",
        labels={"month": "Month", "sales": "Sales ($)", "component": "Component"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate stacked bar plot example")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating stacked bar plot example...")

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plot...")
        fig = stacked_bar_example(dark_mode=dark_mode)

        if args.output:
            os.makedirs(args.output, exist_ok=True)
            output_file = os.path.join(args.output, f"bar_stacked_{mode_name}.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    print(f"\nStacked bar plot example generated!")
