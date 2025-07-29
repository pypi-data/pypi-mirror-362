# Save Formats

Rekha provides intelligent save modes optimized for different use cases.

## Quick Save

```python
import rekha as rk

# Create a plot
fig = rk.scatter(df, x='x', y='y', title='My Plot')

# Auto-detection based on file extension
fig.save('my_plot.png')   # Uses 'social' format
fig.save('my_plot.svg')   # Uses 'web' format
fig.save('my_plot.pdf')   # Uses 'paper' format
```

## Save Modes

### Web Format
Optimized for websites and online sharing:

```python
fig.save('plot.svg', format='web')
```

- **Format**: SVG
- **Background**: Transparent by default
- **Use cases**: Websites, documentation, README files

### Paper Format
Optimized for academic publications:

```python
fig.save('figure1.pdf', format='paper')
```

- **Format**: PDF
- **Background**: Solid white by default
- **Use cases**: Journal articles, conference papers, thesis

### Social Format
Optimized for social media and general sharing:

```python
fig.save('chart.png', format='social')
```

- **Format**: PNG
- **DPI**: 300 (high resolution)
- **Background**: Transparent by default
- **Use cases**: Twitter/X, LinkedIn, blog posts, presentations

### Presentation Format
Optimized for slides:

```python
fig.save('slide.png', format='presentation')
```

- **Format**: PNG
- **DPI**: 150 (balanced quality/size)
- **Background**: Transparent by default
- **Use cases**: PowerPoint, Keynote, Google Slides

## Custom Options

Override defaults for specific needs:

```python
# Force solid background
fig.save('solid_bg.png', format='social', transparent=False)

# Higher resolution
fig.save('high_res.png', format='social', dpi=450)

# Custom padding
fig.save('tight.pdf', format='paper', pad_inches=0.05)

# Combine options
fig.save('custom.png', 
         format='social',
         dpi=600,
         transparent=False,
         bbox_inches='tight')
```

## Batch Saving

Save in multiple formats at once:

```python
# Save in all common formats
fig.save_all_formats('my_plot')
# Creates: my_plot_web.svg, my_plot_paper.pdf, my_plot_social.png

# Or manually save multiple formats
for fmt, ext in [('web', 'svg'), ('paper', 'pdf'), ('social', 'png')]:
    fig.save(f'plot.{ext}', format=fmt)
```

## Format Comparison

| Format | File Type | DPI | Transparent | Best For |
|--------|-----------|-----|-------------|----------|
| web | SVG | - | Yes | Websites, docs |
| paper | PDF | - | No | Publications |
| social | PNG | 300 | Yes | Social media |
| presentation | PNG | 150 | Yes | Slides |

*Note: All formats use `bbox_inches='tight'` to remove excess whitespace.*