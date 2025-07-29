# Color Palettes

Choose from professional color palettes designed for different contexts and data types.

## Available Palettes

### Rekha (Default)
A vibrant, balanced palette suitable for most visualizations.

```python
fig = rk.bar(df, x='category', y='value',
             palette='rekha')  # This is the default
```

<div class="plot-container">
<img src="../../_static/plots/palette_rekha_light.png" alt="Rekha Palette" class="plot-light">
<img src="../../_static/plots/palette_rekha_dark.png" alt="Rekha Palette" class="plot-dark">
</div>

### Pastel
Soft, muted colors ideal for presentations and reports.

```python
fig = rk.scatter(df, x='x', y='y', color='category',
                 palette='pastel')
```

<div class="plot-container">
<img src="../../_static/plots/palette_pastel_light.png" alt="Pastel Palette" class="plot-light">
<img src="../../_static/plots/palette_pastel_dark.png" alt="Pastel Palette" class="plot-dark">
</div>

### Earth
Natural, earthy tones perfect for environmental or organic data.

```python
fig = rk.line(df, x='year', y='temperature', color='region',
              palette='earth')
```

<div class="plot-container">
<img src="../../_static/plots/palette_earth_light.png" alt="Earth Palette" class="plot-light">
<img src="../../_static/plots/palette_earth_dark.png" alt="Earth Palette" class="plot-dark">
</div>

### Ocean
Blues and aquatic colors for marine or water-related data.

```python
fig = rk.bar(df, x='depth', y='pressure',
             palette='ocean')
```

<div class="plot-container">
<img src="../../_static/plots/palette_ocean_light.png" alt="Ocean Palette" class="plot-light">
<img src="../../_static/plots/palette_ocean_dark.png" alt="Ocean Palette" class="plot-dark">
</div>

### Warm
Reds, oranges, and yellows for heat-related or energetic visualizations.

```python
fig = rk.heatmap(correlation_matrix,
                 palette='warm')
```

<div class="plot-container">
<img src="../../_static/plots/palette_warm_light.png" alt="Warm Palette" class="plot-light">
<img src="../../_static/plots/palette_warm_dark.png" alt="Warm Palette" class="plot-dark">
</div>

### Cool
Blues, greens, and purples for calm, professional visualizations.

```python
fig = rk.scatter(df, x='x', y='y', color='group',
                 palette='cool')
```

<div class="plot-container">
<img src="../../_static/plots/palette_cool_light.png" alt="Cool Palette" class="plot-light">
<img src="../../_static/plots/palette_cool_dark.png" alt="Cool Palette" class="plot-dark">
</div>

### Monochrome
Grayscale variations for grayscale printing or minimalist design.

```python
fig = rk.bar(df, x='category', y='value', color='type',
             palette='monochrome')
```

<div class="plot-container">
<img src="../../_static/plots/palette_monochrome_light.png" alt="Monochrome Palette" class="plot-light">
<img src="../../_static/plots/palette_monochrome_dark.png" alt="Monochrome Palette" class="plot-dark">
</div>

### Vibrant
High-contrast, bright colors for maximum visual impact.

```python
fig = rk.scatter(df, x='x', y='y', color='cluster',
                 palette='vibrant')
```

<div class="plot-container">
<img src="../../_static/plots/palette_vibrant_light.png" alt="Vibrant Palette" class="plot-light">
<img src="../../_static/plots/palette_vibrant_dark.png" alt="Vibrant Palette" class="plot-dark">
</div>

## Code Editor Palettes

Popular editor themes adapted for data visualization.

### Ayu
Warm and vibrant colors from the Ayu theme.

```python
fig = rk.bar(df, x='category', y='value', color='type',
             palette='ayu')
```

<div class="plot-container">
<img src="../../_static/plots/palette_ayu_light.png" alt="Ayu Palette" class="plot-light">
<img src="../../_static/plots/palette_ayu_dark.png" alt="Ayu Palette" class="plot-dark">
</div>

### Dracula
Dark theme with vibrant accents.

```python
fig = rk.scatter(df, x='x', y='y', color='category',
                 palette='dracula')
```

<div class="plot-container">
<img src="../../_static/plots/palette_dracula_light.png" alt="Dracula Palette" class="plot-light">
<img src="../../_static/plots/palette_dracula_dark.png" alt="Dracula Palette" class="plot-dark">
</div>

### Monokai
Classic syntax highlighting colors.

```python
fig = rk.line(df, x='time', y='value', color='series',
              palette='monokai')
```

<div class="plot-container">
<img src="../../_static/plots/palette_monokai_light.png" alt="Monokai Palette" class="plot-light">
<img src="../../_static/plots/palette_monokai_dark.png" alt="Monokai Palette" class="plot-dark">
</div>

### Solarized
Carefully chosen colors with precise contrast ratios.

```python
fig = rk.bar(df, x='month', y='sales', color='product',
             palette='solarized')
```

<div class="plot-container">
<img src="../../_static/plots/palette_solarized_light.png" alt="Solarized Palette" class="plot-light">
<img src="../../_static/plots/palette_solarized_dark.png" alt="Solarized Palette" class="plot-dark">
</div>

### Nord
Arctic, north-bluish color palette.

```python
fig = rk.scatter(df, x='x', y='y', color='group',
                 palette='nord')
```

<div class="plot-container">
<img src="../../_static/plots/palette_nord_light.png" alt="Nord Palette" class="plot-light">
<img src="../../_static/plots/palette_nord_dark.png" alt="Nord Palette" class="plot-dark">
</div>

### Gruvbox
Retro groove colors with warm hues.

```python
fig = rk.line(df, x='date', y='metric', color='category',
              palette='gruvbox')
```

<div class="plot-container">
<img src="../../_static/plots/palette_gruvbox_light.png" alt="Gruvbox Palette" class="plot-light">
<img src="../../_static/plots/palette_gruvbox_dark.png" alt="Gruvbox Palette" class="plot-dark">
</div>

## Usage

```python
# Specify palette parameter
fig = rk.bar(df, x='month', y='sales', color='product',
             palette='ocean')

# Works with dark mode
fig = rk.line(df, x='time', y='value', color='series',
              palette='cool',
              dark_mode=True)

# Override specific colors
fig = rk.scatter(df, x='x', y='y', color='category',
                 palette='earth',
                 color_mapping={'Special': '#FF0000'})

# Combine with grayscale patterns
fig = rk.bar(df, x='category', y='value', color='type',
             palette='cool',
             grayscale_friendly=True)
```
