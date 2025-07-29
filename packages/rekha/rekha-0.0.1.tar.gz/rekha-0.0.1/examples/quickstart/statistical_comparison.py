#!/usr/bin/env python3
"""
Statistical comparison box plots from quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_statistical_comparison(dark_mode=False):
    """Box plot comparing model performance across datasets."""
    # Create statistical comparison data
    np.random.seed(42)
    comparison_data = []
    for dataset in ["GLUE", "SuperGLUE", "HellaSwag", "MMLU", "HumanEval"]:
        for model in ["Rekha-7B", "GPT-3.5", "Claude-2", "PaLM-62B"]:
            # Generate realistic scores with different distributions
            if "Rekha" in model:
                scores = np.random.normal(92, 3, 20)
            elif "GPT" in model:
                scores = np.random.normal(87, 4, 20)
            elif "Claude" in model:
                scores = np.random.normal(89, 3.5, 20)
            else:  # PaLM
                scores = np.random.normal(85, 5, 20)

            for score in scores:
                comparison_data.append(
                    {
                        "dataset": dataset,
                        "model": model,
                        "score": max(60, min(100, score)),  # Clamp to realistic range
                    }
                )

    comparison_df = pd.DataFrame(comparison_data)

    # Box plot comparing model performance across datasets
    fig = rk.box(
        comparison_df,
        x="dataset",
        y="score",
        title="Model Performance Across Evaluation Datasets",
        labels={"dataset": "Evaluation Dataset", "score": "Performance Score (%)"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate statistical_comparison plot examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating statistical_comparison plot examples...")

    plots = [
        ("create_statistical_comparison", create_statistical_comparison),
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
                # Remove '_plot' suffix from function names for cleaner filenames
                clean_name = name.replace("_plot", "")
                output_file = os.path.join(
                    args.output, f"quickstart_boxplot_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print("\nAll statistical_comparison plot examples generated!")
