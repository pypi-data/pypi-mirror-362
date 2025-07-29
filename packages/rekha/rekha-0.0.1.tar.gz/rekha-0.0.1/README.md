<div align="center">

# Rekha

*The semantic plotting library for Python with publication-quality output*

[![Documentation](https://img.shields.io/badge/📖_Documentation-blue?style=for-the-badge)](https://project-vajra.github.io/rekha/)
[![Discord](https://img.shields.io/badge/💬_Discord-7289da?style=for-the-badge)](https://discord.gg/wjaSvGgsNN)
[![PyPI](https://img.shields.io/pypi/v/rekha?style=for-the-badge&color=green)](https://pypi.org/project/rekha/)

---

**One line of code. Publication-ready plots.**

Rekha combines Plotly Express's intuitive API with matplotlib's powerful rendering engine, giving you beautiful visualizations without the boilerplate.

</div>

## 🚀 Quick Start

### Installation

```bash
pip install rekha
```

### Basic Usage

```python
import rekha as rk
import pandas as pd

# Your data (any pandas DataFrame)
df = pd.read_csv('your_data.csv')

# One line = beautiful plot
fig = rk.scatter(df, x='x', y='y', color='category')
fig.show()
```

**That's it!** You now have publication-ready visualizations with zero configuration.

## 📊 Sample Graphs

<div align="center">

### Scatter Plot
```python
rk.scatter(df, x='x', y='y', color='species')
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/plots/scatter_colored_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/plots/scatter_colored_light.png">
  <img src="docs/_static/plots/scatter_colored_light.png" width="450">
</picture>

### Line Plot  
```python
rk.line(df, x='date', y='price', color='stock')
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/plots/line_basic_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/plots/line_basic_light.png">
  <img src="docs/_static/plots/line_basic_light.png" width="450">
</picture>

### Bar Chart
```python
rk.bar(df, x='category', y='sales', color='region')
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/plots/bar_grouped_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/plots/bar_grouped_light.png">
  <img src="docs/_static/plots/bar_grouped_light.png" width="450">
</picture>

### Heatmap
```python
rk.heatmap(correlation_matrix, text_auto=True)
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/_static/plots/heatmap_correlation_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/_static/plots/heatmap_correlation_light.png">
  <img src="docs/_static/plots/heatmap_correlation_light.png" width="450">
</picture>

**Every plot type. Same simple API. Beautiful results.**

📖 **[See all plot types in our documentation →](https://project-vajra.github.io/rekha/)**

</div>

## Why Rekha Exists

**The Plotting Library Dilemma:**

- **Matplotlib** = Powerful but painful. Every plot requires 20+ lines of boilerplate.
- **Plotly Express** = has great semantics but limited customization and poor aesthetics for publications.
- **Seaborn** = Good defaults but restrictive API and complicated to use.

**Rekha's Solution:** Get the best of all worlds. Plotly Express semantics + matplotlib quality + unlimited customization.

## ✨ What Makes Rekha Special

🎯 **One-Line Plots** - Create publication-ready visualizations with a single function call  
🎨 **Intelligent Defaults** - Beautiful themes that work in light mode, dark mode, and print  
📊 **All Plot Types** - Line, scatter, bar, histogram, box, heatmap, CDF - unified API  
🖨️ **Print Perfection** - Automatic grayscale optimization with patterns for accessibility  
⚡ **Zero Config** - Works beautifully out of the box, customize when you need to  
🔧 **Unlimited Power** - Full matplotlib access when you need advanced customization

## Plot Types

Rekha supports all major statistical visualizations with a unified interface:

- **Line plots** - Time series, trends, multiple series
- **Scatter plots** - Relationships, correlations, bubble charts  
- **Bar charts** - Categorical comparisons, grouped/stacked bars
- **Histograms** - Data distributions, density plots
- **Box plots** - Statistical summaries, outlier detection
- **Heatmaps** - 2D data, correlation matrices
- **CDF plots** - Cumulative distributions, percentile analysis

## Key Features

### Smart Export Formats
```python
fig.save('plot.pdf', format='paper')    # Publication PDF
fig.save('plot.svg', format='web')      # Web-ready SVG  
fig.save('plot.png', format='social')   # High-res PNG
```

### Theme Support
```python
fig = rk.scatter(df, x='x', y='y', dark_mode=True)           # Dark theme
fig = rk.bar(df, x='cat', y='val', grayscale_friendly=True)  # Print-ready
```

### Full Matplotlib Access
```python
fig = rk.scatter(df, x='x', y='y')
fig.get_axes()[0].axhline(y=0, color='red', linestyle='--')  # Custom elements
```

## 📖 Documentation

Comprehensive documentation is available at: **https://project-vajra.github.io/rekha/**

- **[Quick Start Guide](https://project-vajra.github.io/rekha/quickstart.html)** - Get up and running in minutes
- **[User Guide](https://project-vajra.github.io/rekha/user_guide/)** - Comprehensive feature documentation
- **[API Reference](https://project-vajra.github.io/rekha/api/)** - Complete function reference

## Philosophy

Rekha follows these principles:

1. **Beautiful defaults** - Plots should look professional without tweaking
2. **Simple API** - Common tasks should be one-liners
3. **Full control** - Complex customization should be possible
4. **Performance** - No unnecessary overhead

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:

- Setting up development environment
- Code style and testing requirements
- Documentation standards
- Pull request process

### Quick Development Setup

```bash
git clone https://github.com/project-vajra/rekha.git
cd rekha

# Install in development mode
make install-dev

# Install pre-commit hooks
pre-commit install

# Verify setup works
make format && make lint && make test

# See all available development commands
make help
```

## Related Projects

Rekha is part of the Project Vajra ecosystem:

- **[Vajra](https://github.com/project-vajra/vajra)** - High-performance inference engine for large language models
- **[Rekha](https://github.com/project-vajra/rekha)** - Beautiful matplotlib visualizations (this project)

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Etymology

*Rekha* (रेखा) is a Sanskrit/Hindi word meaning "line", "stroke", or "diagram". It seemed fitting for a library focused on creating beautiful line plots, scatter plots, and other visualizations.
