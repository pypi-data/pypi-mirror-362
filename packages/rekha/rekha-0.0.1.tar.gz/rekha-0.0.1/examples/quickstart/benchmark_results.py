#!/usr/bin/env python3
"""
Benchmark results visualization from quickstart guide.
"""

import pandas as pd

import rekha as rk


def create_benchmark_plot(dark_mode=False):
    """Create grouped bar chart for benchmark results."""
    # Create benchmark data
    benchmark_data = pd.DataFrame(
        {
            "task": [
                "Language\nModeling",
                "Question\nAnswering",
                "Text\nSummarization",
                "Code\nGeneration",
                "Translation",
                "Sentiment\nAnalysis",
            ],
            "rekha_score": [94.2, 91.8, 89.5, 92.1, 88.7, 95.3],
            "baseline_score": [87.5, 84.2, 81.9, 85.6, 82.1, 89.7],
        }
    )

    # Reshape for grouped bars
    benchmark_long = pd.melt(
        benchmark_data,
        id_vars=["task"],
        value_vars=["rekha_score", "baseline_score"],
        var_name="method",
        value_name="score",
    )
    benchmark_long["method"] = (
        benchmark_long["method"].str.replace("_score", "").str.title()
    )

    # Create grouped bar chart for benchmark results
    fig = rk.bar(
        benchmark_long,
        x="task",
        y="score",
        color="method",
        title="AI Benchmark Results: Rekha vs Baseline",
        labels={"task": "Benchmark Task", "score": "Performance Score (%)"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate benchmark_results plot examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating benchmark_results plot examples...")

    plots = [
        ("create_benchmark_plot", create_benchmark_plot),
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
                # Generate quickstart benchmark plot
                output_file = os.path.join(
                    args.output, f"quickstart_benchmark_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll benchmark_results plot examples generated!")
