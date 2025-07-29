# Heatmaps

Heatmaps are perfect for visualizing 2D data, correlation matrices, confusion matrices, and pivot tables. Rekha's heatmaps offer intuitive color mapping, text annotations, and customizable color scales.

## Basic Usage

```python
import rekha as rk
import pandas as pd
import numpy as np

# Simple correlation heatmap
df = pd.DataFrame(np.random.randn(50, 4), columns=['A', 'B', 'C', 'D'])
correlation_matrix = df.corr()

fig = rk.heatmap(correlation_matrix, title='Correlation Matrix', text_auto=True)
fig.show()
```

## Examples Gallery

### Correlation Matrix

<div class="plot-container">
<img src="../../_static/plots/heatmap_correlation_light.png" alt="Correlation Heatmap" class="plot-light">
<img src="../../_static/plots/heatmap_correlation_dark.png" alt="Correlation Heatmap" class="plot-dark">
</div>

Feature correlation analysis:

```python
import rekha as rk
from examples.utils import get_iris, get_tips

df = get_iris()
numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
correlation_matrix = df[numeric_cols].corr()

# Pretty column names
correlation_matrix.index = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
correlation_matrix.columns = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']

fig = rk.heatmap(
    data=correlation_matrix,
    title='Feature Correlations',
    text_auto=True
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/heatmap/basic_heatmap.py)

### Pivot Table Visualization

<div class="plot-container">
<img src="../../_static/plots/heatmap_pivot_light.png" alt="Pivot Table Heatmap" class="plot-light">
<img src="../../_static/plots/heatmap_pivot_dark.png" alt="Pivot Table Heatmap" class="plot-dark">
</div>

Visualize pivot table data:

```python
df_tips = get_tips()
pivot_table = df_tips.pivot_table(
    values='tip',
    index='day',
    columns='time',
    aggfunc='mean'
)

fig = rk.heatmap(
    data=pivot_table,
    title='Average Tip by Day and Time',
    text_auto=True
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/heatmap/basic_heatmap.py)

## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.


## See Also

- [Bar Plots](bar.md) - For categorical comparisons
- [Scatter Plots](scatter.md) - For relationship exploration
- {doc}`API Reference <../../api/index>` - Complete parameter documentation