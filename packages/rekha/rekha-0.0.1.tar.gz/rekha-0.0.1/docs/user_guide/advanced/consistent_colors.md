# Consistent Colors and Ordering

Maintain consistent colors and category ordering across multiple plots.

## The Problem

Default colors and ordering can be confusing:

<div class="plot-container">
<img src="../../_static/plots/advanced_colors_bar_problem_light.png" alt="Problem: Mixed Order + Default Colors" class="plot-light">
<img src="../../_static/plots/advanced_colors_bar_problem_dark.png" alt="Problem: Mixed Order + Default Colors" class="plot-dark">
</div>

## Solution 1: Fix Colors

Use `color_mapping` to assign meaningful colors:

<div class="plot-container">
<img src="../../_static/plots/advanced_colors_bar_color_fixed_light.png" alt="Solution 1: Natural Colors" class="plot-light">
<img src="../../_static/plots/advanced_colors_bar_color_fixed_dark.png" alt="Solution 1: Natural Colors" class="plot-dark">
</div>

## Solution 2: Fix Colors and Order

Use both `color_mapping` and `category_order`:

<div class="plot-container">
<img src="../../_static/plots/advanced_colors_bar_both_fixed_light.png" alt="Solution 2: Correct Order + Natural Colors" class="plot-light">
<img src="../../_static/plots/advanced_colors_bar_both_fixed_dark.png" alt="Solution 2: Correct Order + Natural Colors" class="plot-dark">
</div>

```python
# Define natural colors
natural_colors = {
    'Orange': '#FF8C00',
    'Strawberry': '#DC143C',  
    'Watermelon': '#228B22'
}

# Fix colors only
fig = rk.bar(df, x='quarter', y='sales', color='fruit',
             color_mapping=natural_colors)

# Fix both colors and order
fig = rk.bar(df, x='quarter', y='sales', color='fruit',
             color_mapping=natural_colors,
             category_order=['Watermelon', 'Orange', 'Strawberry'])
```

## Works Across All Plot Types

### Line Plots
<div class="plot-container">
<img src="../../_static/plots/advanced_colors_line_both_fixed_light.png" alt="Line Plot - Both Fixed" class="plot-light">
<img src="../../_static/plots/advanced_colors_line_both_fixed_dark.png" alt="Line Plot - Both Fixed" class="plot-dark">
</div>

### Scatter Plots
<div class="plot-container">
<img src="../../_static/plots/advanced_colors_scatter_both_fixed_light.png" alt="Scatter Plot - Both Fixed" class="plot-light">
<img src="../../_static/plots/advanced_colors_scatter_both_fixed_dark.png" alt="Scatter Plot - Both Fixed" class="plot-dark">
</div>

## Consistent Configuration

```python
# Define once, use everywhere
color_mapping = {
    'Control': '#95A5A6',
    'Treatment A': '#3498DB',
    'Treatment B': '#E74C3C',
    'Treatment C': '#2ECC71'
}

category_order = ['Control', 'Treatment A', 'Treatment B', 'Treatment C']

# Apply to all plots
fig1 = rk.scatter(df1, x='x', y='y', color='treatment',
                  color_mapping=color_mapping,
                  category_order=category_order)

fig2 = rk.bar(df2, x='time', y='count', color='treatment',
              color_mapping=color_mapping,
              category_order=category_order)
```

<div class="plot-container">
<img src="../../_static/plots/advanced_grouped_colors_light.png" alt="Consistent Colors Example" class="plot-light">
<img src="../../_static/plots/advanced_grouped_colors_dark.png" alt="Consistent Colors Example" class="plot-dark">
</div>
