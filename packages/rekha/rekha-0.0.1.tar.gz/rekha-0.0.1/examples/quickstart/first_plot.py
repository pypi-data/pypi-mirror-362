#!/usr/bin/env python3
"""
First plot example from the quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_first_plot(dark_mode=False):
    """Create the first plot shown in quickstart."""
    # Create compelling sample data - stock market performance
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]

    data = []
    for stock in stocks:
        base_price = np.random.uniform(100, 200)
        trend = np.random.uniform(0.1, 0.5)
        volatility = np.random.uniform(5, 15)
        prices = base_price + np.cumsum(np.random.randn(100) * volatility + trend)

        for date, price in zip(dates, prices):
            data.append({"date": date, "stock": stock, "price": price})

    df = pd.DataFrame(data)

    # One line creates a professional visualization
    fig = rk.line(
        df,
        x="date",
        y="price",
        color="stock",
        title="Tech Stock Performance - Q1 2023",
        labels={"price": "Stock Price ($)", "date": "Date"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Generate first plot example")
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating first plot example...")

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plot...")
        fig = create_first_plot(dark_mode=dark_mode)

        if args.output:
            os.makedirs(args.output, exist_ok=True)
            output_file = os.path.join(
                args.output, f"quickstart_first_plot_{mode_name}.png"
            )
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    # Also save a special dark mode version for the dark mode demo
    if args.output and args.mode in ["dark", "both"]:
        output_file = os.path.join(args.output, "quickstart_dark_mode.png")
        fig = create_first_plot(dark_mode=True)
        fig.save(output_file, format="social")
        print(f"✓ Saved: {output_file} (dark mode demo)")

    print(f"\nFirst plot example generated!")
