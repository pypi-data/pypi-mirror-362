# Scatter Plots

Scatter plots are ideal for exploring relationships between variables, identifying patterns, clusters, and outliers. Rekha's scatter plots support multiple encoding channels (color, size, shape) to visualize multi-dimensional data effectively.

## Basic Usage

```python
import rekha as rk
import pandas as pd

# Simple scatter plot
df = pd.DataFrame({
    'height': [165, 170, 175, 180, 185],
    'weight': [60, 65, 70, 75, 80]
})

fig = rk.scatter(df, x='height', y='weight', title='Height vs Weight')
fig.show()
```

## Examples Gallery

### Basic Scatter Plot

<div class="plot-container">
<img src="../../_static/plots/scatter_basic_light.png" alt="Basic Scatter Plot" class="plot-light">
<img src="../../_static/plots/scatter_basic_dark.png" alt="Basic Scatter Plot" class="plot-dark">
</div>

Simple relationship visualization:

```python
import rekha as rk
from examples.utils import get_iris

df = get_iris()
fig = rk.scatter(
    data=df,
    x='sepal_length',
    y='sepal_width',
    title='Iris Sepal Dimensions',
    labels={
        'sepal_length': 'Sepal Length (cm)',
        'sepal_width': 'Sepal Width (cm)'
    }
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/scatter/basic_scatter.py)

### Color-Encoded Categories

<div class="plot-container">
<img src="../../_static/plots/scatter_colored_light.png" alt="Colored Scatter Plot" class="plot-light">
<img src="../../_static/plots/scatter_colored_dark.png" alt="Colored Scatter Plot" class="plot-dark">
</div>

Use color to distinguish categories:

```python
fig = rk.scatter(
    data=df,
    x='petal_length',
    y='petal_width',
    color='species',
    title='Iris Petal Dimensions by Species',
    labels={
        'petal_length': 'Petal Length (cm)',
        'petal_width': 'Petal Width (cm)',
        'species': 'Species'
    }
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/scatter/basic_scatter.py)

### Multi-Feature Encoding

<div class="plot-container">
<img src="../../_static/plots/scatter_sized_light.png" alt="Multi-Feature Scatter Plot" class="plot-light">
<img src="../../_static/plots/scatter_sized_dark.png" alt="Multi-Feature Scatter Plot" class="plot-dark">
</div>

Combine color, size, and shape for complex visualizations:

```python
fig = rk.scatter(
    data=df_tips,
    x='total_bill',
    y='tip',
    size='size',    # Party size
    color='time',   # Lunch vs Dinner
    title='Restaurant Tips Analysis',
    labels={
        'total_bill': 'Total Bill ($)',
        'tip': 'Tip ($)',
        'size': 'Party Size',
        'time': 'Meal Time'
    },
    alpha=0.7
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/scatter/basic_scatter.py)

## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.


## See Also

- [Line Plots](line.md) - For continuous trends over time
- [Histograms](histogram.md) - For distribution analysis
- {doc}`API Reference <../../api/index>` - Complete parameter documentation