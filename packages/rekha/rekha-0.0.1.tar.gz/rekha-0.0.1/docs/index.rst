.. Rekha documentation master file

=====================================
Rekha: Semantic Plotting for Python
=====================================

**Rekha** is a modern plotting library that combines an intuitive API with publication-quality output. Create beautiful, customizable visualizations with minimal code.

.. image:: https://img.shields.io/pypi/v/rekha.svg
   :target: https://pypi.org/project/rekha/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
   :alt: License

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue.svg
   :target: https://python.org
   :alt: Python Version

The Problem
===========

**Matplotlib** is powerful but requires reinventing the wheel for every plot—no semantic interface.

**Plotly Express** has great semantics but limited customization and poor aesthetics for publications.

**Seaborn** has good defaults but restrictive API and complicated to use.

The Solution
============

**Rekha** delivers Plotly Express simplicity with matplotlib's publication-quality output and unlimited customization, plus modern features like unit humanization and grayscale optimization.

From 15 lines to 1 line:

.. code-block:: python

   # Before: Typical matplotlib plotting
   import matplotlib.pyplot as plt
   fig, ax = plt.subplots(figsize=(10, 6))
   for category in df['category'].unique():
       data = df[df['category'] == category]
       ax.scatter(data['x'], data['y'], label=category, s=50, alpha=0.7)
   ax.set_xlabel('X Values')
   ax.set_ylabel('Y Values') 
   ax.set_title('Scatter Plot by Category')
   ax.legend()
   ax.grid(True, alpha=0.3)
   plt.tight_layout()
   plt.show()

   # After: Rekha plotting
   import rekha as rk
   fig = rk.scatter(df, x='x', y='y', color='category', title='Scatter Plot by Category')
   fig.show()

.. raw:: html

   <div class="plot-container">
   <img src="_static/plots/scatter_colored_light.png" alt="Beautiful Scatter Plot" class="plot-light">
   <img src="_static/plots/scatter_colored_dark.png" alt="Beautiful Scatter Plot" class="plot-dark">
   </div>

Key Features
============

🎨 **Beautiful Defaults**
   Pre-configured themes optimized for both light and dark modes

📊 **Unified Interface**  
   Consistent API across all plot types with uniform styling options

🖨️ **Print-Ready**
   Built-in support for grayscale printing with patterns and enhanced contrast

⚡ **Performance**
   Optimized for both interactive exploration and production use

🔧 **Customizable**
   Full access to matplotlib's powerful customization while maintaining simplicity

Quick Start
===========

Installation
------------

.. code-block:: bash

   pip install rekha

Basic Usage
-----------

.. code-block:: python

   import rekha as rk
   import pandas as pd

   # Your data (CSV, database, anywhere)
   df = pd.read_csv('your_data.csv')
   
   # One line = beautiful plot
   fig = rk.scatter(df, x='column1', y='column2', color='category')
   fig.show()

Save and Export
~~~~~~~~~~~~~~~

.. code-block:: python

   # Optimized formats for different use cases
   fig.save('plot.svg', format='web')      # Web-ready SVG
   fig.save('plot.pdf', format='paper')    # Publication PDF
   fig.save('plot.png', format='social')   # High-res PNG

Plot Types
==========

Rekha supports all major statistical visualizations with a unified interface:

.. raw:: html

   <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
   
   <div style="text-align: center;">
   <h4><a href="user_guide/plots/line.html" style="text-decoration: none; color: inherit;">📈 Line Plots</a></h4>
   <p><strong>Time series, trends</strong></p>
   <a href="user_guide/plots/line.html">
   <img src="_static/plots/line_basic_light.png" alt="Line Plot" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/line_basic_dark.png" alt="Line Plot" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.line(df, x='date', y='price')</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/scatter.html" style="text-decoration: none; color: inherit;">🔵 Scatter Plots</a></h4>
   <p><strong>Relationships, correlations</strong></p>
   <a href="user_guide/plots/scatter.html">
   <img src="_static/plots/scatter_colored_light.png" alt="Scatter Plot" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/scatter_colored_dark.png" alt="Scatter Plot" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.scatter(df, x='x', y='y', color='group')</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/bar.html" style="text-decoration: none; color: inherit;">📊 Bar Charts</a></h4>
   <p><strong>Categorical comparisons</strong></p>
   <a href="user_guide/plots/bar.html">
   <img src="_static/plots/bar_grouped_light.png" alt="Bar Chart" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/bar_grouped_dark.png" alt="Bar Chart" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.bar(df, x='category', y='sales')</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/histogram.html" style="text-decoration: none; color: inherit;">📊 Histograms</a></h4>
   <p><strong>Data distributions</strong></p>
   <a href="user_guide/plots/histogram.html">
   <img src="_static/plots/histogram_comparison_light.png" alt="Histogram" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/histogram_comparison_dark.png" alt="Histogram" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.histogram(df, x='value', color='type')</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/box.html" style="text-decoration: none; color: inherit;">📦 Box Plots</a></h4>
   <p><strong>Statistical summaries</strong></p>
   <a href="user_guide/plots/box.html">
   <img src="_static/plots/box_grouped_light.png" alt="Box Plot" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/box_grouped_dark.png" alt="Box Plot" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.box(df, x='group', y='value')</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/heatmap.html" style="text-decoration: none; color: inherit;">🔥 Heatmaps</a></h4>
   <p><strong>2D data, correlations</strong></p>
   <a href="user_guide/plots/heatmap.html">
   <img src="_static/plots/heatmap_correlation_light.png" alt="Heatmap" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/heatmap_correlation_dark.png" alt="Heatmap" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.heatmap(correlation_matrix)</code></p>
   </div>

   <div style="text-align: center;">
   <h4><a href="user_guide/plots/cdf.html" style="text-decoration: none; color: inherit;">📈 CDFs</a></h4>
   <p><strong>Cumulative distributions</strong></p>
   <a href="user_guide/plots/cdf.html">
   <img src="_static/plots/cdf_comparison_light.png" alt="CDF Plot" class="plot-light" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   <img src="_static/plots/cdf_comparison_dark.png" alt="CDF Plot" class="plot-dark" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
   </a>
   <p><code>rk.cdf(df, x='response_time')</code></p>
   </div>

   </div>

**Every plot type. Same simple API. Beautiful results.**

See the :doc:`user_guide/plots/index` for detailed guides and examples.

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   quickstart
   user_guide/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`