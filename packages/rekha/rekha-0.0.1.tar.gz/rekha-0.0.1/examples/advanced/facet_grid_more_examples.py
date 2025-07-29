#!/usr/bin/env python3
"""
Additional facet grid examples for documentation.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_time_series_facet_example(dark_mode=False):
    """Create faceted time series plot."""
    # Generate sample time series data
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=30, freq="D")

    data_rows = []
    for product in ["Product A", "Product B", "Product C"]:
        for region in ["North", "South", "East", "West"]:
            base_sales = {"Product A": 100, "Product B": 80, "Product C": 120}[product]
            region_mult = {"North": 1.2, "South": 0.9, "East": 1.0, "West": 1.1}[region]

            sales = base_sales * region_mult + np.cumsum(np.random.randn(30) * 5)

            for i, date in enumerate(dates):
                data_rows.append(
                    {
                        "date": date,
                        "sales": sales[i],
                        "product_category": product,
                        "region": region,
                    }
                )

    df = pd.DataFrame(data_rows)

    # Create faceted time series
    fig = rk.line(
        df,
        x="date",
        y="sales",
        facet_col="product_category",
        facet_row="region",
        title="Sales Trends by Product and Region",
        figsize=(15, 12),
        dark_mode=dark_mode,
    )

    return fig


def create_distribution_comparison_example(dark_mode=False):
    """Create faceted histogram comparison."""
    # Generate experimental data
    np.random.seed(42)
    data_rows = []

    treatments = ["Control", "Treatment A", "Treatment B"]
    timepoints = ["Baseline", "Week 4", "Week 8"]

    for treatment in treatments:
        for timepoint in timepoints:
            # Different distributions for different conditions
            if treatment == "Control":
                base_mean = 100
            elif treatment == "Treatment A":
                base_mean = 105 if timepoint != "Baseline" else 100
            else:  # Treatment B
                base_mean = 110 if timepoint == "Week 8" else 100

            measurements = np.random.normal(base_mean, 15, 200)

            for measurement in measurements:
                data_rows.append(
                    {
                        "measurement": measurement,
                        "treatment": treatment,
                        "timepoint": timepoint,
                    }
                )

    df = pd.DataFrame(data_rows)

    # Create faceted histograms
    fig = rk.histogram(
        df,
        x="measurement",
        facet_col="treatment",
        facet_row="timepoint",
        nbins=30,
        alpha=0.7,
        title="Treatment Effects Over Time",
        figsize=(12, 8),
        dark_mode=dark_mode,
    )

    return fig


def create_ab_test_results_example(dark_mode=False):
    """Create faceted box plots for A/B test results."""
    # Generate A/B test data
    np.random.seed(42)
    data_rows = []

    variants = ["Control", "Variant A", "Variant B"]
    segments = ["New Users", "Returning Users", "Power Users"]
    devices = ["Mobile", "Desktop"]

    for variant in variants:
        for segment in segments:
            for device in devices:
                # Different conversion rates for different combinations
                base_rate = 0.10

                if variant == "Variant A":
                    base_rate *= 1.1
                elif variant == "Variant B":
                    base_rate *= 1.15

                if segment == "Power Users":
                    base_rate *= 1.5
                elif segment == "Returning Users":
                    base_rate *= 1.2

                if device == "Desktop":
                    base_rate *= 1.1

                # Generate conversion data
                n_users = 100
                conversions = np.random.binomial(1, base_rate, n_users)

                for conversion in conversions:
                    data_rows.append(
                        {
                            "variant": variant,
                            "conversion_rate": conversion,
                            "user_segment": segment,
                            "device_type": device,
                        }
                    )

    df = pd.DataFrame(data_rows)

    # Aggregate to get conversion rates
    agg_df = (
        df.groupby(["variant", "user_segment", "device_type"])
        .agg({"conversion_rate": "mean"})
        .reset_index()
    )

    # Create faceted box plot
    fig = rk.bar(
        agg_df,
        x="variant",
        y="conversion_rate",
        facet_col="user_segment",
        facet_row="device_type",
        title="A/B Test Results by Segment and Device",
        labels={"conversion_rate": "Conversion Rate", "variant": "Test Variant"},
        figsize=(12, 8),
        dark_mode=dark_mode,
    )

    return fig


def create_geographic_analysis_example(dark_mode=False):
    """Create faceted bar charts for geographic data."""
    # Generate geographic sales data
    np.random.seed(42)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    states = ["CA", "NY", "TX", "FL", "WA"]

    data_rows = []
    for state in states:
        # Different base sales for different states
        base_sales = {"CA": 1000, "NY": 900, "TX": 800, "FL": 700, "WA": 600}[state]

        for i, month in enumerate(months):
            # Seasonal variation
            seasonal_mult = 1 + 0.1 * np.sin(i * np.pi / 6)
            sales = base_sales * seasonal_mult * (1 + np.random.uniform(-0.1, 0.1))

            data_rows.append({"month": month, "sales": sales, "state": state})

    df = pd.DataFrame(data_rows)

    # Create faceted bar charts
    fig = rk.bar(
        df,
        x="month",
        y="sales",
        facet_col="state",
        title="Monthly Sales by State",
        labels={"sales": "Sales ($)", "month": "Month"},
        figsize=(15, 4),
        dark_mode=dark_mode,
    )

    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate additional facet grid examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating additional facet grid examples...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    examples = [
        ("facet_timeseries", create_time_series_facet_example),
        ("facet_distribution", create_distribution_comparison_example),
        ("facet_abtest", create_ab_test_results_example),
        ("facet_geographic", create_geographic_analysis_example),
    ]

    modes = []
    if args.mode in ["light", "both"]:
        modes.append(("light", False))
    if args.mode in ["dark", "both"]:
        modes.append(("dark", True))

    for mode_name, dark_mode in modes:
        print(f"\n📊 Generating {mode_name} mode plots...")
        for name, func in examples:
            try:
                fig = func(dark_mode=dark_mode)

                if args.output:
                    output_file = os.path.join(
                        args.output, f"advanced_{name}_{mode_name}.png"
                    )
                    fig.save(output_file, format="social")
                    print(f"✓ Saved: {output_file}")
                else:
                    fig.show()
            except Exception as e:
                print(f"✗ Error generating {name}: {e}")

    print("\nAdditional facet grid examples generated!")
