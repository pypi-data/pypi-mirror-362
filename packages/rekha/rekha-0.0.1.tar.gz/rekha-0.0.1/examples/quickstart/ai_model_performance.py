#!/usr/bin/env python3
"""
AI Model Performance visualization from quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_model_performance_plot(dark_mode=False):
    """Multi-dimensional scatter plot showing model performance."""
    # Create realistic AI model performance data
    np.random.seed(42)
    model_data = pd.DataFrame(
        {
            "model_size": [7, 13, 30, 65, 175, 540] * 3,
            "throughput": [950, 680, 420, 280, 150, 85]
            + [720, 510, 320, 210, 120, 65]
            + [580, 410, 260, 170, 95, 50],
            "framework": ["Rekha"] * 6 + ["PyTorch"] * 6 + ["TensorFlow"] * 6,
            "memory_gb": [8, 15, 32, 68, 145, 380]
            + [12, 22, 45, 89, 195, 520]
            + [15, 28, 52, 98, 215, 580],
        }
    )

    # Multi-dimensional scatter plot showing model performance
    fig = rk.scatter(
        model_data,
        x="model_size",
        y="throughput",
        color="framework",
        size="memory_gb",
        title="AI Model Performance: Throughput vs Model Size",
        labels={
            "model_size": "Model Size (B Parameters)",
            "throughput": "Throughput (tokens/sec)",
            "memory_gb": "Memory Usage (GB)",
        },
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate AI model performance scatter plot"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating AI model performance scatter plot...")

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    # Generate plots based on mode
    if args.mode in ["light", "both"]:
        fig = create_model_performance_plot(dark_mode=False)
        if args.output:
            output_file = os.path.join(args.output, "quickstart_scatter_light.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    if args.mode in ["dark", "both"]:
        fig = create_model_performance_plot(dark_mode=True)
        if args.output:
            output_file = os.path.join(args.output, "quickstart_scatter_dark.png")
            fig.save(output_file, format="social")
            print(f"✓ Saved: {output_file}")
        else:
            fig.show()

    print("\nAI model performance plot generated!")
