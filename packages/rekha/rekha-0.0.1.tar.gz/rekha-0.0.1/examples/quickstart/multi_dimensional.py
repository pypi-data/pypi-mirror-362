#!/usr/bin/env python3
"""
Multi-dimensional analysis from quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_multidimensional_plot(dark_mode=False):
    """Advanced scatter plot with multiple encodings."""
    # Create complex real-world data
    np.random.seed(42)
    n_models = 50
    model_analysis = pd.DataFrame(
        {
            "parameters_b": np.random.uniform(1, 200, n_models),
            "accuracy": np.random.uniform(75, 98, n_models),
            "inference_speed": np.random.uniform(10, 1000, n_models),
            "memory_gb": np.random.uniform(4, 500, n_models),
            "architecture": np.random.choice(
                ["Transformer", "CNN", "RNN", "Hybrid"], n_models
            ),
            "efficiency_score": np.random.uniform(60, 95, n_models),
        }
    )

    # Advanced scatter plot with multiple encodings
    fig = rk.scatter(
        model_analysis,
        x="parameters_b",
        y="accuracy",
        color="efficiency_score",
        size="memory_gb",
        shape="architecture",
        title="Multi-Dimensional Model Analysis",
        labels={
            "parameters_b": "Model Parameters (B)",
            "accuracy": "Accuracy (%)",
            "efficiency_score": "Efficiency Score",
            "memory_gb": "Memory Usage (GB)",
        },
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate multi_dimensional plot examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating multi_dimensional plot examples...")

    plots = [
        ("create_multidimensional_plot", create_multidimensional_plot),
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
                # Generate quickstart multidim plot
                output_file = os.path.join(
                    args.output, f"quickstart_multidim_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print(f"\nAll multi_dimensional plot examples generated!")
