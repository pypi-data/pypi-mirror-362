# Grayscale Friendly Mode

Create plots that work perfectly in grayscale printing and for color vision accessibility.

```python
import rekha as rk
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'product_a': [100, 120, 140, 110, 160],
    'product_b': [80, 90, 100, 120, 130],
    'product_c': [60, 70, 85, 95, 100]
})

# Reshape for grouped bars
df_long = pd.melt(df, id_vars=['month'], var_name='product', value_name='sales')
df_long['product'] = df_long['product'].str.replace('product_', 'Product ').str.upper()

# Create a bar plot optimized for grayscale printing
fig = rk.bar(df_long, x='month', y='sales', color='product',
             title='Monthly Sales by Product',
             labels={'month': 'Month', 'sales': 'Sales ($)', 'product': 'Product'},
             grayscale_friendly=True)
fig.show()
```

<div class="plot-container">
<img src="../../_static/plots/advanced_bw_bar_light.png" alt="Grayscale Friendly Chart Example" class="plot-light">
<img src="../../_static/plots/advanced_bw_bar_dark.png" alt="Grayscale Friendly Bar Chart Example" class="plot-dark">
</div>

## Line Plots

```python
# Time series with multiple lines
fig = rk.line(time_series_df, x='date', y='value', color='category',
              title='Trends Over Time',
              grayscale_friendly=True,
              markers=True)  # Adds distinct markers
```

<div class="plot-container">
<img src="../../_static/plots/advanced_bw_line_light.png" alt="Grayscale Line Chart" class="plot-light">
<img src="../../_static/plots/advanced_bw_line_dark.png" alt="Grayscale Line Chart" class="plot-dark">
</div>

## Bar Plots

```python
# Grouped bars with patterns
fig = rk.bar(sales_df, x='region', y='sales', color='product',
             title='Sales by Region and Product',
             grayscale_friendly=True)
```

## Scatter Plots

```python
# Scatter with shape encoding
fig = rk.scatter(data_df, x='x', y='y', color='group',
                 title='Data Point Distribution',
                 grayscale_friendly=True,
                 point_size=120)  # Larger markers for clarity
```

<div class="plot-container">
<img src="../../_static/plots/advanced_bw_scatter_light.png" alt="Grayscale Scatter Plot" class="plot-light">
<img src="../../_static/plots/advanced_bw_scatter_dark.png" alt="Grayscale Scatter Plot" class="plot-dark">
</div>

## Other Plot Types

```python
# Overlapping histograms with patterns
fig = rk.histogram(dist_df, x='value', color='distribution',
                   title='Distribution Comparison',
                   grayscale_friendly=True,
                   alpha=0.7)  # Transparency for overlaps

# Box plots
fig = rk.box(stats_df, x='category', y='value',
             title='Value Distribution by Category',
             grayscale_friendly=True)
```

## How It Works

When `grayscale_friendly=True`, Rekha automatically:
- Applies different fill patterns (hatching) for bars and areas
- Uses varied line styles (solid, dashed, dotted) for lines
- Assigns distinct marker shapes for scatter plots
- Increases contrast between elements

Works with all Rekha features including dark mode and faceting.
