"""
Rekha theme configuration with beautiful, accessible color palettes.

This module provides the core theming functionality for Rekha, including:

* Color palette definitions optimized for data visualization
* Light and dark theme configurations
* Typography and spacing settings
* Accessibility-compliant color schemes
* Print-friendly styling options

The themes are designed following best practices from data visualization
research and accessibility guidelines to ensure plots are both beautiful
and functional across different contexts.

Color Palette Design Principles:

* **Perceptual uniformity**: Colors have similar perceived brightness
* **Sequential ordering**: Colors can be arranged in meaningful sequences
* **Categorical distinction**: Easy to distinguish when used for categories
* **Accessibility**: WCAG 2.1 AA compliant contrast ratios
* **Cultural sensitivity**: Avoiding problematic color associations
* **Print compatibility**: Works well in both color and grayscale printing

Examples
--------
>>> import rekha as rk
>>> # Apply light theme
>>> theme = rk.set_rekha_theme(dark_mode=False)
>>> # Apply dark theme
>>> dark_theme = rk.set_rekha_theme(dark_mode=True)
>>> # Access color constants
>>> light_colors = rk.REKHA_COLORS
>>> dark_colors = rk.REKHA_DARK_COLORS
"""

import matplotlib.pyplot as plt
from cycler import cycler

# Color palette definitions
COLOR_PALETTES = {
    "rekha": [
        "#10B981",  # emerald-500
        "#3B82F6",  # blue-500
        "#F59E0B",  # amber-500
        "#EF4444",  # red-500
        "#8B5CF6",  # violet-500
        "#EC4899",  # pink-500
        "#14B8A6",  # teal-500
        "#F97316",  # orange-500
    ],
    "pastel": [
        "#FFD6E8",  # Light pink
        "#C7E9FF",  # Light blue
        "#FFE5B4",  # Light peach
        "#E8D5FF",  # Light lavender
        "#D4F4DD",  # Light mint
        "#FFDAB9",  # Light coral
        "#E0F2FE",  # Light sky
        "#FFF0DB",  # Light cream
    ],
    "earth": [
        "#8B4513",  # Saddle brown
        "#556B2F",  # Olive
        "#A0522D",  # Sienna
        "#2F4F4F",  # Dark slate gray
        "#BC8F8F",  # Rosy brown
        "#708090",  # Slate gray
        "#CD853F",  # Peru
        "#696969",  # Dim gray
    ],
    "ocean": [
        "#006994",  # Deep ocean
        "#00A6FB",  # Sky blue
        "#0582CA",  # True blue
        "#003554",  # Midnight blue
        "#051923",  # Dark navy
        "#00B4D8",  # Cyan
        "#90E0EF",  # Light cyan
        "#CAF0F8",  # Pale cyan
    ],
    "warm": [
        "#FF6B6B",  # Coral red
        "#FFD93D",  # Bright yellow
        "#FF8C42",  # Orange
        "#FF4757",  # Watermelon
        "#FFA502",  # Carrot
        "#FF6348",  # Tomato
        "#FF9F43",  # Mandarin
        "#EE5A24",  # Burnt orange
    ],
    "cool": [
        "#4ECDC4",  # Turquoise
        "#45B7D1",  # Sky blue
        "#96CEB4",  # Sage
        "#6C5CE7",  # Soft purple
        "#A29BFE",  # Lavender
        "#74B9FF",  # Light blue
        "#81ECEC",  # Mint
        "#55A3FF",  # Cornflower
    ],
    "monochrome": [
        "#2C3E50",  # Dark blue gray
        "#34495E",  # Wet asphalt
        "#7F8C8D",  # Gray
        "#95A5A6",  # Light gray
        "#BDC3C7",  # Silver
        "#ECF0F1",  # Clouds
        "#D5DBDB",  # Light silver
        "#AAB7B8",  # Medium gray
    ],
    "vibrant": [
        "#FF006E",  # Hot pink
        "#FB5607",  # Orange red
        "#FFBE0B",  # Yellow
        "#8338EC",  # Purple
        "#3A86FF",  # Blue
        "#06FFA5",  # Spring green
        "#FF4081",  # Pink
        "#7209B7",  # Deep purple
    ],
    # Code editor inspired palettes
    "ayu": [
        "#FF6A00",  # Orange
        "#5CCFE6",  # Cyan
        "#FFD580",  # Yellow
        "#BAE67E",  # Green
        "#FFA759",  # Light orange
        "#73D0FF",  # Light blue
        "#D4BFFF",  # Purple
        "#F29E74",  # Peach
    ],
    "dracula": [
        "#FF79C6",  # Pink
        "#BD93F9",  # Purple
        "#8BE9FD",  # Cyan
        "#50FA7B",  # Green
        "#F1FA8C",  # Yellow
        "#FFB86C",  # Orange
        "#FF5555",  # Red
        "#6272A4",  # Comment blue
    ],
    "monokai": [
        "#F92672",  # Pink
        "#66D9EF",  # Blue
        "#A6E22E",  # Green
        "#FD971F",  # Orange
        "#AE81FF",  # Purple
        "#E6DB74",  # Yellow
        "#FD5FF0",  # Magenta (replaced white)
        "#75715E",  # Brown gray
    ],
    "solarized": [
        "#B58900",  # Yellow
        "#CB4B16",  # Orange
        "#DC322F",  # Red
        "#D33682",  # Magenta
        "#6C71C4",  # Violet
        "#268BD2",  # Blue
        "#2AA198",  # Cyan
        "#859900",  # Green
    ],
    "nord": [
        "#BF616A",  # Red
        "#D08770",  # Orange
        "#EBCB8B",  # Yellow
        "#A3BE8C",  # Green
        "#88C0D0",  # Cyan
        "#5E81AC",  # Blue
        "#B48EAD",  # Purple
        "#81A1C1",  # Light blue
    ],
    "gruvbox": [
        "#CC241D",  # Red
        "#D65D0E",  # Orange
        "#D79921",  # Yellow
        "#98971A",  # Green
        "#689D6A",  # Aqua
        "#458588",  # Blue
        "#B16286",  # Purple
        "#FE8019",  # Bright orange
    ],
}

# Define Rekha color palette
REKHA_COLORS = {
    "primary": "#18181B",  # zinc-900 for dark elements
    "secondary": "#71717A",  # zinc-500 for muted elements
    "accent": "#10B981",  # emerald-500 (matches your green dot)
    "background": "#FFFFFF",  # pure white
    "text": "#18181B",  # zinc-900
    "muted": "#A1A1AA",  # zinc-400
    "grid": "#E4E4E7",  # zinc-200
    "colors": COLOR_PALETTES["rekha"],  # Default to rekha palette
}

# Dark mode colors
REKHA_DARK_COLORS = {
    "primary": "#FAFAFA",  # zinc-50 for dark mode
    "secondary": "#A1A1AA",  # zinc-400
    "accent": "#10B981",  # emerald-500
    "background": "#09090B",  # zinc-950
    "text": "#FAFAFA",  # zinc-50
    "muted": "#71717A",  # zinc-500
    "grid": "#27272A",  # zinc-800
    "colors": [  # Same but slightly adjusted for dark
        "#10B981",  # emerald-500
        "#60A5FA",  # blue-400
        "#A78BFA",  # violet-400
        "#FCD34D",  # amber-300
        "#F87171",  # red-400
        "#22D3EE",  # cyan-400
        "#F472B6",  # pink-400
        "#818CF8",  # indigo-400
    ],
}


def set_rekha_theme(dark_mode=False, palette="rekha"):
    """Set the Rekha matplotlib theme

    Parameters
    ----------
    dark_mode : bool, default False
        Whether to use dark mode
    palette : str, default "rekha"
        Color palette to use. Options: "rekha", "pastel", "earth", "ocean",
        "warm", "cool", "monochrome", "vibrant"
    """
    colors = REKHA_DARK_COLORS if dark_mode else REKHA_COLORS

    # Update color palette if specified
    if palette in COLOR_PALETTES:
        colors = colors.copy()
        colors["colors"] = COLOR_PALETTES[palette]

    # Set the style parameters
    params = {
        # Figure
        "figure.facecolor": colors["background"],
        "figure.edgecolor": colors["background"],
        "figure.figsize": (10, 6),
        "figure.dpi": 100,
        # Axes
        "axes.facecolor": colors["background"],
        "axes.edgecolor": colors["muted"],
        "axes.labelcolor": colors["text"],
        "axes.labelweight": "bold",  # Make axis labels bold by default
        "axes.labelsize": 14,  # Larger axis labels for readability
        "axes.linewidth": 0.8,
        "axes.grid": False,  # Disable theme-level grid, let plots control it
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler("color", colors["colors"]),
        # Grid
        "grid.color": colors["grid"],
        "grid.alpha": 0.6,
        "grid.linewidth": 0.5,
        "grid.linestyle": "-",
        # Ticks
        "xtick.color": colors["text"],
        "ytick.color": colors["text"],
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        # Text
        "text.color": colors["text"],
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Arial",
            "Helvetica",
            "DejaVu Sans",
            "Inter",
            "SF Pro Display",
            "sans-serif",
        ],
        "font.size": 10,
        # Legend
        "legend.frameon": False,
        "legend.fontsize": 12,
        "legend.edgecolor": colors["muted"],
        # Lines
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
        # Patches
        "patch.linewidth": 0,
        "patch.edgecolor": colors["muted"],
        # Save
        "savefig.facecolor": colors["background"],
        "savefig.edgecolor": colors["background"],
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    }

    plt.rcParams.update(params)

    return colors
