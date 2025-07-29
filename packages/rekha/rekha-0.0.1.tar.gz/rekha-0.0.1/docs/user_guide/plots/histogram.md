# Histograms

Histograms are essential for understanding data distributions, identifying patterns like skewness and multimodality, and comparing distributions across groups. Rekha's histograms offer flexible binning, density estimation, and comparison features.

## Basic Usage

```python
import rekha as rk
import pandas as pd
import numpy as np

# Simple histogram
data = np.random.normal(50, 15, 1000)
df = pd.DataFrame({'values': data})

fig = rk.histogram(df, x='values', title='Distribution of Values')
fig.show()
```

## Examples Gallery

### Basic Histogram

<div class="plot-container">
<img src="../../_static/plots/histogram_basic_light.png" alt="Basic Histogram" class="plot-light">
<img src="../../_static/plots/histogram_basic_dark.png" alt="Basic Histogram" class="plot-dark">
</div>

Simple distribution visualization:

```python
import rekha as rk
import numpy as np

# Generate normal distribution
np.random.seed(42)
data = np.random.normal(100, 15, 1000)
df = pd.DataFrame({'values': data})

fig = rk.histogram(
    data=df,
    x='values',
    title='Normal Distribution',
    labels={'values': 'Value'},
    nbins=30
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/histogram/basic_histogram.py)

### Distribution Comparison

<div class="plot-container">
<img src="../../_static/plots/histogram_comparison_light.png" alt="Distribution Comparison" class="plot-light">
<img src="../../_static/plots/histogram_comparison_dark.png" alt="Distribution Comparison" class="plot-dark">
</div>

Compare multiple distributions side by side:

```python
# Create multiple distributions for comparison
data_long = pd.melt(
    df[['normal', 'skewed_right']],
    var_name='distribution',
    value_name='value'
)

fig = rk.histogram(
    data=data_long,
    x='value',
    facet_col='distribution',
    title='Distribution Comparison',
    labels={'value': 'Value', 'distribution': 'Type'},
    nbins=25
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/histogram/basic_histogram.py)

### Grouped by Category

<div class="plot-container">
<img src="../../_static/plots/histogram_grouped_light.png" alt="Grouped Histogram" class="plot-light">
<img src="../../_static/plots/histogram_grouped_dark.png" alt="Grouped Histogram" class="plot-dark">
</div>

Compare distributions across groups:

```python
fig = rk.histogram(
    data=df_iris,
    x='petal_length',
    color='species',
    title='Petal Length by Species',
    labels={'petal_length': 'Petal Length (cm)', 'species': 'Species'},
    alpha=0.8,
    nbins=20
)
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/histogram/basic_histogram.py)

## Parameters

See the {doc}`API Reference <../../api/index>` for complete parameter documentation.


## See Also

- [Box Plots](box.md) - For statistical summaries
- [CDF Plots](cdf.md) - For cumulative distributions
- {doc}`API Reference <../../api/index>` - Complete parameter documentation