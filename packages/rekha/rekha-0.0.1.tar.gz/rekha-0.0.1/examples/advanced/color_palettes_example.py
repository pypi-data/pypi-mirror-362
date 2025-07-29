#!/usr/bin/env python3
"""
Color palette examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_palette_example(palette_name, dark_mode=False):
    """Create example plot for a specific palette."""
    # Generate sample data with 8 categories
    categories = ["A", "B", "C", "D", "E", "F", "G", "H"]
    values = [45, 38, 52, 41, 35, 48, 33, 44]

    # Create data with color grouping to show all palette colors
    df = pd.DataFrame(
        {
            "category": categories,
            "value": values,
            "group": categories,  # Each category gets its own color
        }
    )

    # Create bar chart with specified palette
    fig = rk.bar(
        df,
        x="category",
        y="value",
        color="group",  # This will use different colors from the palette
        title=f"{palette_name.title()} Color Palette",
        labels={"category": "", "value": "Value"},
        palette=palette_name,
        dark_mode=dark_mode,
    )

    return fig


def create_palette_comparison(dark_mode=False):
    """Create a comparison of all palettes."""
    # Sample data for comparison
    categories = ["A", "B", "C", "D", "E"]

    # Create a figure with subplots for each palette
    import matplotlib.pyplot as plt

    from rekha.theme import COLOR_PALETTES, set_rekha_theme

    # Apply theme
    set_rekha_theme(dark_mode)

    palettes = list(COLOR_PALETTES.keys())

    # Calculate grid size to fit all palettes
    n_palettes = len(palettes)
    n_cols = 4
    n_rows = (n_palettes + n_cols - 1) // n_cols  # Ceiling division

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten()

    for idx, palette_name in enumerate(palettes):
        if idx >= len(axes):
            break
        ax = axes[idx]
        values = np.random.randint(20, 80, len(categories))
        colors = COLOR_PALETTES[palette_name][: len(categories)]

        ax.bar(categories, values, color=colors)
        ax.set_title(palette_name.title(), fontsize=12, fontweight="bold")
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)

    # Hide unused subplots
    for idx in range(len(palettes), len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle("Rekha Color Palettes Comparison", fontsize=16, fontweight="bold")
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate color palette examples")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating color palette examples...")

    # Individual palette examples
    palettes = [
        "rekha",
        "pastel",
        "earth",
        "ocean",
        "warm",
        "cool",
        "monochrome",
        "vibrant",
        "ayu",
        "dracula",
        "monokai",
        "solarized",
        "nord",
        "gruvbox",
    ]

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plots...")

        # Individual palette plots
        for palette_name in palettes:
            fig = create_palette_example(palette_name, dark_mode)

            if args.output:
                os.makedirs(args.output, exist_ok=True)
                output_file = os.path.join(
                    args.output, f"palette_{palette_name}_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

        # Comparison plot
        # comparison_fig = create_palette_comparison(dark_mode)
        # if args.output:
        #     output_file = os.path.join(args.output, f"palette_comparison_{mode_name}.png")
        #     comparison_fig.savefig(output_file, dpi=150, bbox_inches='tight')
        #     print(f"✓ Saved: {output_file}")

    print(f"\nAll color palette examples generated!")
