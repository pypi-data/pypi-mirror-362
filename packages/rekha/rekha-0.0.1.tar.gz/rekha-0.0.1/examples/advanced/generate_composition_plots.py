#!/usr/bin/env python3
"""Generate composition examples for documentation."""

from pathlib import Path

import numpy as np
import pandas as pd

import rekha as rk

# Set random seed for reproducibility
np.random.seed(42)

# Create output directory
output_dir = Path("docs/_static/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# Use high-res PNG instead of SVG

print("Generating composition examples for documentation...")

# 1. Bar + Line Composition Example
print("\n1. Generating bar + line composition example...")
sales_data = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "actual": [100, 120, 115, 130, 125, 140],
        "forecast": [105, 118, 120, 128, 130, 135],
        "target": [110, 115, 120, 125, 130, 135],
    }
)

# Light mode
bar_plot = rk.bar(
    sales_data,
    x="month",
    y="actual",
    title="Sales Performance with Forecast",
    labels={"month": "Month", "actual": "Sales ($k)"},
)
line_plot = rk.line(
    sales_data,
    x="month",
    y="forecast",
    base_plot=bar_plot,
    markers=True,
    label="Forecast",
)
target_plot = rk.line(
    sales_data,
    x="month",
    y="target",
    base_plot=line_plot,
    line_style="--",
    label="Target",
)
target_plot.ax.legend()
target_plot.save(str(output_dir / "bar_line_composition_light.png"), format="social")

# Dark mode
bar_plot_dark = rk.bar(
    sales_data,
    x="month",
    y="actual",
    title="Sales Performance with Forecast",
    labels={"month": "Month", "actual": "Sales ($k)"},
    dark_mode=True,
)
line_plot_dark = rk.line(
    sales_data,
    x="month",
    y="forecast",
    base_plot=bar_plot_dark,
    markers=True,
    label="Forecast",
)
target_plot_dark = rk.line(
    sales_data,
    x="month",
    y="target",
    base_plot=line_plot_dark,
    line_style="--",
    label="Target",
)
target_plot_dark.ax.legend()
target_plot_dark.save(
    str(output_dir / "bar_line_composition_dark.png"), format="social"
)

# 2. Scatter + Line Composition Example
print("\n2. Generating scatter + line composition example...")
np.random.seed(42)
n_points = 50
x = np.linspace(0, 10, n_points)
y = 2 * x + 1 + np.random.normal(0, 2, n_points)
scatter_data = pd.DataFrame({"x": x, "y": y})

# Calculate regression line
z = np.polyfit(x, y, 1)
x_line = np.array([x.min(), x.max()])
y_line = z[0] * x_line + z[1]
line_data = pd.DataFrame({"x": x_line, "y": y_line})

# Light mode
scatter_plot = rk.scatter(
    scatter_data, x="x", y="y", title="Linear Regression Example", alpha=0.6
)
line_plot = rk.line(
    line_data,
    x="x",
    y="y",
    base_plot=scatter_plot,
    line_width=3,
    label=f"y = {z[0]:.2f}x + {z[1]:.2f}",
)
line_plot.ax.legend()
line_plot.save(str(output_dir / "scatter_line_composition_light.png"), format="social")

# Dark mode
scatter_plot_dark = rk.scatter(
    scatter_data,
    x="x",
    y="y",
    title="Linear Regression Example",
    alpha=0.6,
    dark_mode=True,
)
line_plot_dark = rk.line(
    line_data,
    x="x",
    y="y",
    base_plot=scatter_plot_dark,
    line_width=3,
    label=f"y = {z[0]:.2f}x + {z[1]:.2f}",
)
line_plot_dark.ax.legend()
line_plot_dark.save(
    str(output_dir / "scatter_line_composition_dark.png"), format="social"
)

# 3. Box + Scatter Composition Example
print("\n3. Generating box + scatter composition example...")
# Generate data with outliers
groups = []
values = []
for i, group in enumerate(["A", "B", "C"]):
    # Normal data
    normal_data = np.random.normal(10 + i * 5, 2, 100)
    groups.extend([group] * 100)
    values.extend(normal_data)
    # Add outliers
    outliers = np.random.uniform(20 + i * 5, 25 + i * 5, 5)
    groups.extend([group] * 5)
    values.extend(outliers)

box_data = pd.DataFrame({"group": groups, "value": values})

# Identify outliers using IQR method
outliers_data = []
for group in ["A", "B", "C"]:
    group_data = box_data[box_data["group"] == group]["value"]
    Q1 = group_data.quantile(0.25)
    Q3 = group_data.quantile(0.75)
    IQR = Q3 - Q1
    outlier_mask = (group_data < Q1 - 1.5 * IQR) | (group_data > Q3 + 1.5 * IQR)
    outliers = group_data[outlier_mask]
    for val in outliers:
        outliers_data.append({"group": group, "value": val})

outliers_df = pd.DataFrame(outliers_data)

# Light mode
box_plot = rk.box(
    box_data, x="group", y="value", title="Distribution with Outliers Highlighted"
)
if len(outliers_df) > 0:
    scatter_plot = rk.scatter(
        outliers_df,
        x="group",
        y="value",
        base_plot=box_plot,
        point_size=100,
        label="Outliers",
    )
    scatter_plot.ax.legend()
    final_plot = scatter_plot
else:
    final_plot = box_plot
final_plot.save(str(output_dir / "box_scatter_composition_light.png"), format="social")

# Dark mode
box_plot_dark = rk.box(
    box_data,
    x="group",
    y="value",
    title="Distribution with Outliers Highlighted",
    dark_mode=True,
)
if len(outliers_df) > 0:
    scatter_plot_dark = rk.scatter(
        outliers_df,
        x="group",
        y="value",
        base_plot=box_plot_dark,
        point_size=100,
        label="Outliers",
    )
    scatter_plot_dark.ax.legend()
    final_plot_dark = scatter_plot_dark
else:
    final_plot_dark = box_plot_dark
final_plot_dark.save(
    str(output_dir / "box_scatter_composition_dark.png"), format="social"
)

# 4. Histogram + Line (KDE) Composition Example
print("\n4. Generating histogram + density curve composition example...")
from scipy import stats

# Generate sample data
hist_data = pd.DataFrame({"values": np.random.normal(100, 15, 1000)})

# Calculate KDE
kde = stats.gaussian_kde(hist_data["values"])
x_range = np.linspace(hist_data["values"].min(), hist_data["values"].max(), 200)
kde_values = kde(x_range)

# Scale KDE to match histogram
n_bins = 30
hist_values, bin_edges = np.histogram(hist_data["values"], bins=n_bins)
bin_width = bin_edges[1] - bin_edges[0]
kde_scaled = kde_values * len(hist_data) * bin_width

kde_data = pd.DataFrame({"x": x_range, "y": kde_scaled})

# Light mode
hist_plot = rk.histogram(
    hist_data,
    x="values",
    nbins=n_bins,
    title="Distribution with Density Curve",
    alpha=0.7,
)
line_plot = rk.line(
    kde_data, x="x", y="y", base_plot=hist_plot, line_width=3, label="Density"
)
line_plot.ax.legend()
line_plot.save(
    str(output_dir / "histogram_line_composition_light.png"), format="social"
)

# Dark mode
hist_plot_dark = rk.histogram(
    hist_data,
    x="values",
    nbins=n_bins,
    title="Distribution with Density Curve",
    alpha=0.7,
    dark_mode=True,
)
line_plot_dark = rk.line(
    kde_data, x="x", y="y", base_plot=hist_plot_dark, line_width=3, label="Density"
)
line_plot_dark.ax.legend()
line_plot_dark.save(
    str(output_dir / "histogram_line_composition_dark.png"), format="social"
)

# 5. CDF Composition Example
print("\n5. Generating CDF composition example...")
# Generate two distributions
dist1 = pd.DataFrame({"values": np.random.normal(0, 1, 1000)})
dist2 = pd.DataFrame({"values": np.random.normal(2, 1.5, 1000)})

# Light mode
cdf_plot1 = rk.cdf(
    dist1,
    x="values",
    title="CDF Comparison",
    labels={"values": "Value", "y": "Cumulative Probability"},
)
cdf_plot2 = rk.cdf(dist2, x="values", base_plot=cdf_plot1, label="Distribution 2")
# Add first distribution label
cdf_plot1.ax.get_lines()[0].set_label("Distribution 1")
cdf_plot2.ax.legend()
cdf_plot2.save(str(output_dir / "cdf_composition_light.png"), format="social")

# Dark mode
cdf_plot1_dark = rk.cdf(
    dist1,
    x="values",
    title="CDF Comparison",
    labels={"values": "Value", "y": "Cumulative Probability"},
    dark_mode=True,
)
cdf_plot2_dark = rk.cdf(
    dist2, x="values", base_plot=cdf_plot1_dark, label="Distribution 2"
)
cdf_plot1_dark.ax.get_lines()[0].set_label("Distribution 1")
cdf_plot2_dark.ax.legend()
cdf_plot2_dark.save(str(output_dir / "cdf_composition_dark.png"), format="social")

# 6. Histogram + CDF Composition Example
print("\n6. Generating histogram + CDF overlay example...")
# Use same data as histogram example
hist_cdf_data = pd.DataFrame({"values": np.random.normal(100, 15, 1000)})

# Light mode
hist_plot = rk.histogram(
    hist_cdf_data,
    x="values",
    nbins=30,
    title="Distribution with CDF Overlay",
    alpha=0.7,
)
# Create secondary y-axis for CDF
ax2 = hist_plot.ax.twinx()
# Plot CDF on secondary axis
sorted_values = np.sort(hist_cdf_data["values"])
cdf_values = np.arange(1, len(sorted_values) + 1) / len(sorted_values)
ax2.plot(sorted_values, cdf_values, color="red", linewidth=2, label="CDF")
ax2.set_ylabel("Cumulative Probability", fontsize=12, fontweight="bold")
ax2.set_ylim(0, 1)
# Combine legends
h1, l1 = hist_plot.ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
hist_plot.ax.legend(h1 + h2, ["Histogram"] + l2, loc="upper left")
hist_plot.save(str(output_dir / "histogram_cdf_composition_light.png"), format="social")

# Dark mode
hist_plot_dark = rk.histogram(
    hist_cdf_data,
    x="values",
    nbins=30,
    title="Distribution with CDF Overlay",
    alpha=0.7,
    dark_mode=True,
)
ax2_dark = hist_plot_dark.ax.twinx()
ax2_dark.plot(sorted_values, cdf_values, color="red", linewidth=2, label="CDF")
ax2_dark.set_ylabel("Cumulative Probability", fontsize=12, fontweight="bold")
ax2_dark.set_ylim(0, 1)
# Style secondary axis for dark mode
ax2_dark.tick_params(colors="white")
ax2_dark.yaxis.label.set_color("white")
ax2_dark.spines["right"].set_color("white")
# Combine legends
h1, l1 = hist_plot_dark.ax.get_legend_handles_labels()
h2, l2 = ax2_dark.get_legend_handles_labels()
hist_plot_dark.ax.legend(h1 + h2, ["Histogram"] + l2, loc="upper left")
hist_plot_dark.save(
    str(output_dir / "histogram_cdf_composition_dark.png"), format="social"
)

print("\nAll composition examples generated successfully!")
print(f"Output directory: {output_dir}")
