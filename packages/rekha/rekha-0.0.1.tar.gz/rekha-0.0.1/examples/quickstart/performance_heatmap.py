#!/usr/bin/env python3
"""
Performance heatmap from quickstart guide.
"""

import numpy as np
import pandas as pd

import rekha as rk


def create_performance_heatmap(dark_mode=False):
    """Create heatmap showing throughput for different configurations."""
    # Create performance matrix data
    np.random.seed(42)
    batch_sizes = [1, 2, 4, 8, 16, 32, 64]
    seq_lengths = [128, 256, 512, 1024, 2048, 4096]

    # Generate realistic throughput matrix
    throughput_matrix = []
    for seq_len in seq_lengths:
        row = []
        for batch_size in batch_sizes:
            # Realistic throughput calculation
            base_throughput = 1000 / (seq_len / 128) / np.sqrt(batch_size)
            noise = np.random.normal(0, base_throughput * 0.1)
            throughput = max(10, base_throughput + noise)
            row.append(int(throughput))
        throughput_matrix.append(row)

    throughput_df = pd.DataFrame(
        throughput_matrix,
        index=[f"{sl}" for sl in seq_lengths],
        columns=[f"{bs}" for bs in batch_sizes],
    )

    # Create heatmap showing throughput for different configurations
    fig = rk.heatmap(
        throughput_df,
        title="Throughput Heatmap: Batch Size × Sequence Length",
        labels={
            "x": "Batch Size",
            "y": "Sequence Length",
            "color": "Throughput (tokens/sec)",
        },
        dark_mode=dark_mode,
    )
    return fig


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Generate performance_heatmap plot examples"
    )
    parser.add_argument("--output", type=str, help="Output directory for plots")
    parser.add_argument(
        "--mode",
        choices=["light", "dark", "both"],
        default="both",
        help="Generate light, dark, or both variants",
    )
    args = parser.parse_args()

    print("Generating performance_heatmap plot examples...")

    plots = [
        ("create_performance_heatmap", create_performance_heatmap),
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
                    args.output, f"quickstart_heatmap_{mode_name}.png"
                )
                fig.save(output_file, format="social")
                print(f"✓ Saved: {output_file}")
            else:
                fig.show()

    print("\nAll performance_heatmap plot examples generated!")
