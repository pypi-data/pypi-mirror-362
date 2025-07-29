#!/usr/bin/env python3
"""
Training metrics dashboard from quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_training_metrics_plot(dark_mode=False):
    """Visualize training loss curves."""
    # Create realistic training data
    np.random.seed(42)
    epochs = list(range(1, 101))
    training_data = pd.DataFrame(
        {
            "epoch": epochs * 3,
            "loss": (
                [
                    4.5 * np.exp(-0.08 * i) + 0.1 + np.random.normal(0, 0.02)
                    for i in epochs
                ]
                + [
                    4.2 * np.exp(-0.06 * i) + 0.15 + np.random.normal(0, 0.03)
                    for i in epochs
                ]
                + [
                    3.8 * np.exp(-0.05 * i) + 0.2 + np.random.normal(0, 0.04)
                    for i in epochs
                ]
            ),
            "model": ["GPT-4"] * 100 + ["LLaMA-2"] * 100 + ["PaLM"] * 100,
        }
    )

    # Visualize training loss curves
    fig = rk.line(
        training_data,
        x="epoch",
        y="loss",
        color="model",
        title="Training Loss Convergence Comparison",
        labels={"epoch": "Training Epoch", "loss": "Loss"},
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate training_metrics plot examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating training_metrics plot examples...")

    plots = [
        ("create_training_metrics_plot", create_training_metrics_plot),
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
                    args.output, f"quickstart_training_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print("\nAll training_metrics plot examples generated!")
