# Bar Plots

Bar plots are essential for comparing categorical data, showing distributions across groups, and visualizing survey results. Rekha's bar plots support vertical and horizontal orientations, grouping, stacking, and custom styling.

## Basic Usage

```python
import rekha as rk
import pandas as pd

# Simple bar plot
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [23, 45, 12, 67]
})

fig = rk.bar(df, x='category', y='value', title='Simple Bar Plot')
fig.show()
```

## Examples Gallery

### Basic Vertical Bar Plot

<div class="plot-container">
<img src="../../_static/plots/bar_basic_light.png" alt="Basic Bar Plot" class="plot-light">
<img src="../../_static/plots/bar_basic_dark.png" alt="Basic Bar Plot" class="plot-dark">
</div>

Simple categorical comparison:

```python
import rekha as rk
from examples.utils import get_categorical_data

df = get_categorical_data()
region_sales = df.groupby('region')['sales'].sum().reset_index()

fig = rk.bar(
    data=region_sales,
    x='region',
    y='sales',
    title='Sales by Region',
    labels={'region': 'Region', 'sales': 'Total Sales ($)'}
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/bar/basic_bar.py)

### Grouped Bar Plot

<div class="plot-container">
<img src="../../_static/plots/bar_grouped_light.png" alt="Grouped Bar Plot" class="plot-light">
<img src="../../_static/plots/bar_grouped_dark.png" alt="Grouped Bar Plot" class="plot-dark">
</div>

Compare multiple categories side by side:

```python
quarter_region = df.groupby(['region', 'quarter'])['sales'].sum().reset_index()

fig = rk.bar(
    data=quarter_region,
    x='region',
    y='sales',
    color='quarter',
    title='Quarterly Sales by Region',
    labels={'region': 'Region', 'sales': 'Sales ($)', 'quarter': 'Quarter'}
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/bar/basic_bar.py)

### Horizontal Bar Plot

<div class="plot-container">
<img src="../../_static/plots/bar_horizontal_light.png" alt="Horizontal Bar Plot" class="plot-light">
<img src="../../_static/plots/bar_horizontal_dark.png" alt="Horizontal Bar Plot" class="plot-dark">
</div>

Better for long category names:

```python
product_sales = df.groupby('product')['sales'].sum().reset_index().sort_values('sales')

fig = rk.bar(
    data=product_sales,
    x='sales',
    y='product',
    orientation='h',
    title='Sales by Product',
    labels={'sales': 'Total Sales ($)', 'product': 'Product'}
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/bar/basic_bar.py)

### Stacked Bar Plot

<div class="plot-container">
<img src="../../_static/plots/bar_stacked_light.png" alt="Stacked Bar Plot" class="plot-light">
<img src="../../_static/plots/bar_stacked_dark.png" alt="Stacked Bar Plot" class="plot-dark">
</div>

Show component contributions with stacked bars:

```python
# Prepare data for stacking
sales_by_component = df.groupby(['month', 'component'])['sales'].sum().reset_index()

fig = rk.bar(
    data=sales_by_component,
    x='month',
    y='sales',
    color='component',
    barmode="stack",
    title='Monthly Sales Breakdown by Component',
    labels={'month': 'Month', 'sales': 'Sales ($)', 'component': 'Component'}
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/bar/stacked_bar.py)

## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.


## See Also

- [Histograms](histogram.md) - For continuous data distributions
- [Heatmaps](heatmap.md) - For 2D categorical data
- {doc}`API Reference <../../api/index>` - Complete parameter documentation