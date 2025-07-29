# Line Plots

Line plots are perfect for visualizing trends over time, continuous data relationships, and comparing multiple series.

## Basic Usage

```python
import rekha as rk
import pandas as pd

# Simple line plot
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 6]
})

fig = rk.line(df, x='x', y='y', title='Simple Line Plot')
fig.show()
```

## Examples Gallery

### Multiple Series

<div class="plot-container">
<img src="../../_static/plots/line_multiple_light.png" alt="Multiple Lines" class="plot-light">
<img src="../../_static/plots/line_multiple_dark.png" alt="Multiple Lines" class="plot-dark">
</div>

Compare multiple time series by using the `color` parameter:

```python
# Time series comparison
fig = rk.line(df, x='date', y='value', color='metric',
              title='Performance Metrics Over Time')
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/line/multiple_lines.py)

### With Markers

<div class="plot-container">
<img src="../../_static/plots/line_markers_light.png" alt="Line with Markers" class="plot-light">
<img src="../../_static/plots/line_markers_dark.png" alt="Line with Markers" class="plot-dark">
</div>

Add markers for sparse data or emphasis:

```python
# Monthly data with markers
fig = rk.line(df, x='month', y='sales', markers=True,
              title='Monthly Sales')
```


## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.

## See Also

- {doc}`scatter` - For examining relationships between variables
- {doc}`bar` - For categorical comparisons
- {doc}`../advanced/plot_composition` - For layering multiple plot types