# Box Plots

Box plots are ideal for statistical summaries, outlier detection, and comparing distributions across groups. Rekha's box plots show quartiles, medians, and outliers with clean, informative visualizations.

## Basic Usage

```python
import rekha as rk
import pandas as pd
import numpy as np

# Simple box plot
data = np.random.normal(50, 15, 1000)
df = pd.DataFrame({'values': data})

fig = rk.box(df, y='values', title='Value Distribution')
fig.show()
```

## Examples Gallery

### Basic Box Plot

<div class="plot-container">
<img src="../../_static/plots/box_basic_light.png" alt="Basic Box Plot" class="plot-light">
<img src="../../_static/plots/box_basic_dark.png" alt="Basic Box Plot" class="plot-dark">
</div>

Single variable distribution summary:

```python
import rekha as rk
from examples.utils import get_iris

df = get_iris()

fig = rk.box(
    data=df,
    y='sepal_length',
    title='Sepal Length Distribution'
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/box/basic_box.py)

### Grouped Box Plot

<div class="plot-container">
<img src="../../_static/plots/box_grouped_light.png" alt="Grouped Box Plot" class="plot-light">
<img src="../../_static/plots/box_grouped_dark.png" alt="Grouped Box Plot" class="plot-dark">
</div>

Compare distributions across categories:

```python
fig = rk.box(
    data=df,
    x='species',
    y='petal_length',
    title='Petal Length by Species',
    labels={'species': 'Species', 'petal_length': 'Petal Length (cm)'}
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/box/basic_box.py)

## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.

## What Box Plots Show

- **Box**: Interquartile range (25th to 75th percentile)
- **Line in box**: Median (50th percentile)
- **Whiskers**: Extend to 1.5 × IQR from box edges
- **Points**: Outliers beyond whiskers

## See Also

- [Histograms](histogram.md) - For detailed distribution shapes
- [Scatter Plots](scatter.md) - For relationship exploration
- {doc}`API Reference <../../api/index>` - Complete parameter documentation