#!/usr/bin/env python3
"""
Bar plot examples for Rekha documentation.

This script generates all the bar plot examples shown in the user guide.
"""

import rekha as rk
from examples.utils import get_categorical_data


def basic_bar(dark_mode=False):
    """Simple categorical comparison."""
    df = get_categorical_data()
    region_sales = df.groupby("region")["sales"].sum().reset_index()

    fig = rk.bar(
        data=region_sales,
        x="region",
        y="sales",
        title="Sales by Region",
        labels={"region": "Region", "sales": "Total Sales ($)"},
        dark_mode=dark_mode,
    )
    return fig


def grouped_bar(dark_mode=False):
    """Compare multiple categories side by side."""
    df = get_categorical_data()
    quarter_region = df.groupby(["region", "quarter"])["sales"].sum().reset_index()

    fig = rk.bar(
        data=quarter_region,
        x="region",
        y="sales",
        color="quarter",
        title="Quarterly Sales by Region",
        labels={"region": "Region", "sales": "Sales ($)", "quarter": "Quarter"},
        dark_mode=dark_mode,
    )
    return fig


def horizontal_bar(dark_mode=False):
    """Better for long category names."""
    df = get_categorical_data()
    product_sales = (
        df.groupby("product")["sales"].sum().reset_index().sort_values("sales")
    )

    fig = rk.bar(
        data=product_sales,
        x="sales",
        y="product",
        orientation="h",
        title="Sales by Product",
        labels={"sales": "Total Sales ($)", "product": "Product"},
        dark_mode=dark_mode,
    )
    return fig


def stacked_bar(dark_mode=False):
    """Show component contributions with stacked bars."""
    df = get_categorical_data()

    # Prepare data for stacking - aggregate by quarter and product
    stacked_data = df.groupby(["quarter", "product"])["sales"].sum().reset_index()

    fig = rk.bar(
        data=stacked_data,
        x="quarter",
        y="sales",
        color="product",
        barmode="stack",
        title="Quarterly Sales Breakdown by Product",
        labels={"quarter": "Quarter", "sales": "Sales ($)", "product": "Product"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate bar plot examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating bar plot examples...")

    plots = [
        ("basic", basic_bar),
        ("grouped", grouped_bar),
        ("horizontal", horizontal_bar),
        ("stacked", stacked_bar),
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
                output_file = os.path.join(args.output, f"bar_{name}_{mode_name}.png")
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll bar plot examples generated!")
