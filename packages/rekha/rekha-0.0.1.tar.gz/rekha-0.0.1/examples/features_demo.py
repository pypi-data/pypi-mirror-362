#!/usr/bin/env python3
"""
Demo of new Rekha features: log scales, color palettes, and humanized units.
"""

import numpy as np
import pandas as pd

import rekha as rk


def demo_log_scale():
    """Demonstrate log scale functionality."""
    # Generate exponential data
    x = np.linspace(1, 5, 50)
    y = np.exp(x) + np.random.normal(0, 10, 50)

    df = pd.DataFrame({"x": x, "y": y})

    # Create plot with log scale
    fig = rk.scatter(
        df,
        x="x",
        y="y",
        title="Log Scale Example",
        yscale="log",  # Apply log scale to y-axis
        labels={"x": "Time", "y": "Growth (log scale)"},
    )

    return fig


def demo_color_palettes():
    """Demonstrate different color palettes."""
    # Generate sample data
    categories = ["A", "B", "C", "D", "E", "F", "G", "H"]
    values = np.random.randint(50, 200, len(categories))

    df = pd.DataFrame({"category": categories, "value": values})

    # Create plots with different palettes
    figs = {}

    for palette in ["rekha", "pastel", "earth", "ocean", "warm", "cool"]:
        fig = rk.bar(
            df,
            x="category",
            y="value",
            title=f"{palette.title()} Palette",
            palette=palette,  # Use different color palette
        )
        figs[palette] = fig

    return figs


def demo_humanized_units():
    """Demonstrate humanized unit formatting."""
    # Generate data with large numbers
    companies = ["Apple", "Microsoft", "Google", "Amazon", "Meta"]
    revenue = [383285000000, 198270000000, 282836000000, 469822000000, 116609000000]
    employees = [154000, 221000, 174014, 1525000, 77805]

    df = pd.DataFrame(
        {"company": companies, "revenue": revenue, "employees": employees}
    )

    # Create plot with humanized units
    fig = rk.bar(
        df,
        x="company",
        y="revenue",
        title="Tech Company Revenue (2022)",
        labels={"company": "Company", "revenue": "Annual Revenue"},
        humanize_units=True,  # Enable humanized formatting
        humanize_format="intword",  # Use "1M", "1B" format
    )

    return fig


def demo_combined_features():
    """Demonstrate combining multiple features."""
    # Generate exponential growth data
    years = list(range(2000, 2024))
    users = [1000 * (1.5 ** (year - 2000)) for year in years]

    df = pd.DataFrame({"year": years, "users": users})

    # Create plot with multiple features
    fig = rk.line(
        df,
        x="year",
        y="users",
        title="Platform User Growth (2000-2023)",
        labels={"year": "Year", "users": "Number of Users"},
        yscale="log",  # Log scale for exponential data
        humanize_units=True,  # Human-readable numbers
        palette="ocean",  # Ocean color palette
        dark_mode=True,  # Dark mode
        markers=True,  # Show data points
    )

    return fig


def demo_jupyter_support():
    """Demonstrate Jupyter notebook support."""
    # This will automatically display in Jupyter
    df = pd.DataFrame({"x": range(10), "y": [i**2 for i in range(10)]})

    # In Jupyter, this will display automatically without calling show()
    fig = rk.scatter(df, x="x", y="y", title="Auto-display in Jupyter")

    return fig


if __name__ == "__main__":
    print("Demonstrating new Rekha features...")

    # 1. Log scale
    print("\n1. Log scale example:")
    fig1 = demo_log_scale()
    fig1.show()

    # 2. Color palettes
    print("\n2. Color palette examples:")
    palette_figs = demo_color_palettes()
    for palette, fig in palette_figs.items():
        print(f"   - {palette} palette")
        # fig.show()  # Uncomment to see each

    # 3. Humanized units
    print("\n3. Humanized units example:")
    fig3 = demo_humanized_units()
    fig3.show()

    # 4. Combined features
    print("\n4. Combined features example:")
    fig4 = demo_combined_features()
    fig4.show()

    print("\nAll demos complete!")
