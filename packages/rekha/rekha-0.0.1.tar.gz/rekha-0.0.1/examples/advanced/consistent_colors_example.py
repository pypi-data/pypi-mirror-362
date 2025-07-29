#!/usr/bin/env python3
"""
Consistent colors and ordering examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_consistent_colors_example(
    plot_type="bar", example_type="problem", dark_mode=False
):
    """Create plots demonstrating color and ordering consistency issues and solutions."""
    # Define natural fruit colors that users would expect
    natural_colors = {
        "Orange": "#FF8C00",  # Orange color for orange fruit
        "Strawberry": "#DC143C",  # Red color for strawberry
        "Watermelon": "#228B22",  # Green color for watermelon
    }

    # Use the same random seed for reproducibility
    np.random.seed(42)

    # Sales data: Watermelon sells most, then Orange, then Strawberry
    # This creates a non-intuitive order when sorted alphabetically
    sales_data = {
        "Orange": [85, 90, 95, 100],  # Medium sales
        "Strawberry": [60, 65, 70, 75],  # Lowest sales
        "Watermelon": [120, 125, 130, 135],  # Highest sales (counter-intuitive!)
    }

    # Different scenarios to demonstrate the problems and solutions
    if example_type == "problem":
        # PROBLEM: Mixed order + default colors (fruits don't get their natural colors)
        fruit_order = [
            "Watermelon",
            "Orange",
            "Strawberry",
        ]  # Wrong order (not by sales)
        color_mapping = None  # No explicit mapping - gets default colors
        title = "Problem: Mixed Order + Default Colors"

    elif example_type == "color_fixed":
        # SOLUTION 1: Same mixed order but with correct fruit colors
        fruit_order = ["Watermelon", "Orange", "Strawberry"]  # Still wrong order
        color_mapping = natural_colors  # Now fruits get their natural colors
        title = "Solution 1: Natural Colors (Order Still Mixed)"

    else:  # example_type == 'both_fixed'
        # SOLUTION 2: Correct order (by sales) + correct colors
        fruit_order = [
            "Watermelon",
            "Orange",
            "Strawberry",
        ]  # Correct order by sales (highest to lowest)
        color_mapping = natural_colors  # Natural colors
        title = "Solution 2: Correct Order + Natural Colors"

    if plot_type == "bar":
        # Generate data in the specified fruit order
        df_data = []
        for fruit in fruit_order:
            for i, quarter in enumerate(["Q1", "Q2", "Q3", "Q4"]):
                df_data.append(
                    {"quarter": quarter, "fruit": fruit, "sales": sales_data[fruit][i]}
                )

        df = pd.DataFrame(df_data)

        # For the "both fixed" case, also specify category order
        if example_type == "both_fixed":
            category_order = [
                "Watermelon",
                "Orange",
                "Strawberry",
            ]  # Highest to lowest sales
        else:
            category_order = None

        fig = rk.bar(
            df,
            x="quarter",
            y="sales",
            color="fruit",
            title=title,
            labels={
                "quarter": "Quarter",
                "sales": "Sales (thousands)",
                "fruit": "Fruit",
            },
            color_mapping=color_mapping,
            category_order=category_order,
            dark_mode=dark_mode,
        )

    elif plot_type == "line":
        # Line chart showing trends over time
        dates = pd.date_range("2023-01-01", periods=25, freq="D")

        # Generate trend data for each fruit (matching sales hierarchy)
        trend_data = {
            "Orange": np.cumsum(np.random.randn(25) * 1.5) + 92,  # Medium trend
            "Strawberry": np.cumsum(np.random.randn(25) * 1) + 67,  # Lowest trend
            "Watermelon": np.cumsum(np.random.randn(25) * 2) + 125,  # Highest trend
        }

        df_data = []
        for fruit in fruit_order:
            for i, date in enumerate(dates):
                df_data.append(
                    {"date": date, "fruit": fruit, "sales": trend_data[fruit][i]}
                )

        df = pd.DataFrame(df_data)

        # For the "both fixed" case, also specify category order
        if example_type == "both_fixed":
            category_order = [
                "Watermelon",
                "Orange",
                "Strawberry",
            ]  # Highest to lowest sales
        else:
            category_order = None

        fig = rk.line(
            df,
            x="date",
            y="sales",
            color="fruit",
            title=title,
            labels={"date": "Date", "sales": "Daily Sales", "fruit": "Fruit"},
            color_mapping=color_mapping,
            category_order=category_order,
            markers=True,
            dark_mode=dark_mode,
        )

    elif plot_type == "scatter":
        # Scatter plot showing price vs popularity
        n_points = 40  # More points for better visibility

        scatter_data = {
            "Orange": {
                "price": np.random.normal(3.5, 0.5, n_points),  # Medium price
                "popularity": np.random.normal(75, 10, n_points),  # Medium popularity
            },
            "Strawberry": {
                "price": np.random.normal(5.0, 0.8, n_points),  # Higher price
                "popularity": np.random.normal(60, 12, n_points),  # Lower popularity
            },
            "Watermelon": {
                "price": np.random.normal(2.5, 0.4, n_points),  # Lower price
                "popularity": np.random.normal(
                    85, 8, n_points
                ),  # High popularity (counter-intuitive!)
            },
        }

        df_data = []
        for fruit in fruit_order:
            for i in range(n_points):
                df_data.append(
                    {
                        "fruit": fruit,
                        "price": scatter_data[fruit]["price"][i],
                        "popularity": scatter_data[fruit]["popularity"][i],
                    }
                )

        df = pd.DataFrame(df_data)

        # For the "both fixed" case, also specify category order
        if example_type == "both_fixed":
            category_order = [
                "Watermelon",
                "Orange",
                "Strawberry",
            ]  # Highest to lowest sales
        else:
            category_order = None

        fig = rk.scatter(
            df,
            x="price",
            y="popularity",
            color="fruit",
            title=title,
            labels={
                "price": "Price per lb ($)",
                "popularity": "Popularity Score",
                "fruit": "Fruit",
            },
            color_mapping=color_mapping,
            category_order=category_order,
            point_size=120,
            alpha=0.7,
            dark_mode=dark_mode,
        )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate consistent colors examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating fruit sales color consistency examples...")

    # Generate three scenarios for each plot type:
    # 1. Problem: Wrong order + default colors
    # 2. Color Fixed: Wrong order + natural colors
    # 3. Both Fixed: Correct order + natural colors
    plots = [
        (
            "colors_bar_problem",
            lambda dm: create_consistent_colors_example("bar", "problem", dm),
        ),
        (
            "colors_bar_color_fixed",
            lambda dm: create_consistent_colors_example("bar", "color_fixed", dm),
        ),
        (
            "colors_bar_both_fixed",
            lambda dm: create_consistent_colors_example("bar", "both_fixed", dm),
        ),
        (
            "colors_line_problem",
            lambda dm: create_consistent_colors_example("line", "problem", dm),
        ),
        (
            "colors_line_color_fixed",
            lambda dm: create_consistent_colors_example("line", "color_fixed", dm),
        ),
        (
            "colors_line_both_fixed",
            lambda dm: create_consistent_colors_example("line", "both_fixed", dm),
        ),
        (
            "colors_scatter_problem",
            lambda dm: create_consistent_colors_example("scatter", "problem", dm),
        ),
        (
            "colors_scatter_color_fixed",
            lambda dm: create_consistent_colors_example("scatter", "color_fixed", dm),
        ),
        (
            "colors_scatter_both_fixed",
            lambda dm: create_consistent_colors_example("scatter", "both_fixed", dm),
        ),
    ]

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plots...")
        for name, func in plots:
            fig = func(dark_mode)

            if args.output:
                os.makedirs(args.output, exist_ok=True)
                output_file = os.path.join(
                    args.output, f"advanced_{name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll fruit sales color consistency examples generated!")
