# Rekha Examples

This directory contains example scripts and utilities for the Rekha plotting library.

## Directory Structure

```
examples/
├── utils.py                    # Data generation utilities
├── generate_docs_plots.py      # Script to generate all documentation plots
├── plots/                      # Individual plot type examples
│   ├── line/
│   │   └── basic_line.py      # Line plot examples
│   ├── scatter/
│   │   └── basic_scatter.py   # Scatter plot examples
│   ├── bar/
│   │   ├── basic_bar.py       # Bar plot examples
│   │   └── stacked_bar.py     # Stacked bar example
│   ├── histogram/
│   │   └── basic_histogram.py # Histogram examples
│   ├── box/
│   │   └── basic_box.py       # Box plot examples
│   └── heatmap/
│       └── basic_heatmap.py   # Heatmap examples
└── quickstart/                 # Quickstart guide examples (future)
```

## Running Examples

### Individual Plot Examples

Each plot type has its own example file that can be run independently:

```bash
# Run line plot examples
python examples/plots/line/basic_line.py

# Run scatter plot examples  
python examples/plots/scatter/basic_scatter.py

# Run bar plot examples
python examples/plots/bar/basic_bar.py
```

### Generate Documentation Plots

To generate all plots for the documentation:

```bash
# From the project root
python examples/generate_docs_plots.py

# Or use the convenient shell script
./generate_docs_plots.sh
```

## Data Generation Utilities

The `utils.py` file contains functions to generate sample datasets used throughout the examples:

- `get_time_series_data()` - Time series data for line plots
- `get_iris()` - Iris-like dataset for scatter plots and classification examples
- `get_categorical_data()` - Sales data for bar plots
- `get_tips()` - Restaurant tips dataset for multi-dimensional analysis
- `get_distribution_data()` - Various distributions for histogram examples
- `get_model_performance_data()` - AI/ML performance metrics
- `get_training_metrics()` - Model training progress data
- `get_benchmark_data()` - Benchmark comparison data

## Adding New Examples

To add a new example:

1. Create a new Python file in the appropriate `plots/` subdirectory
2. Import `rekha` and any needed utilities from `examples.utils`
3. Define functions that create and return figure objects
4. Include a `__main__` block to run the examples standalone
5. Update the documentation to reference your example

Example structure:

```python
#!/usr/bin/env python3
"""
Description of your example.
"""

import rekha as rk
from examples.utils import get_some_data

def example_plot():
    """Create an example plot."""
    data = get_some_data()
    
    fig = rk.plot_type(
        data=data,
        x='column1',
        y='column2',
        title='Example Plot'
    )
    return fig

if __name__ == "__main__":
    fig = example_plot()
    fig.show()
```

## Documentation Integration

These examples are referenced in the Rekha documentation. When updating examples:

1. Ensure the code matches what's shown in the docs
2. Test that the example runs without errors
3. Regenerate documentation plots if visual output changes
4. Update documentation links if file paths change

The documentation references examples using GitHub links like:
```
[Full example](https://github.com/project-vajra/rekha/blob/main/examples/plots/line/basic_line.py)
```