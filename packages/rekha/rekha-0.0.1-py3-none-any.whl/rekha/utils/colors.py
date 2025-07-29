"""
Color management utilities for Rekha plots.
"""

from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from ..theme import REKHA_COLORS, REKHA_DARK_COLORS


def get_color_palette(
    dark_mode: bool = False, n_colors: Optional[int] = None
) -> List[str]:
    """
    Get the Rekha color palette.

    Parameters
    ----------
    dark_mode : bool, default False
        Whether to use dark mode colors
    n_colors : int, optional
        Number of colors to return (cycles if more needed)

    Returns
    -------
    list
        List of color hex codes
    """
    colors = REKHA_DARK_COLORS if dark_mode else REKHA_COLORS
    color_list = colors["colors"]

    if n_colors is None:
        return color_list

    # Cycle through colors if more needed
    return [color_list[i % len(color_list)] for i in range(n_colors)]


def map_colors_to_categories(
    categories: List[str],
    color_mapping: Optional[Dict[str, str]] = None,
    category_order: Optional[List[str]] = None,
    dark_mode: bool = False,
) -> Tuple[List[str], List[str]]:
    """
    Map colors to categories with consistent ordering.

    Parameters
    ----------
    categories : list
        List of category names
    color_mapping : dict, optional
        Custom color mapping {category: color}
    category_order : list, optional
        Custom ordering for categories
    dark_mode : bool, default False
        Whether to use dark mode colors

    Returns
    -------
    tuple
        (ordered_categories, assigned_colors)
    """
    # Convert to list if needed
    if hasattr(categories, "tolist"):
        categories = categories.tolist()
    elif not isinstance(categories, list):
        categories = list(categories)

    # Apply custom ordering if specified
    if category_order:
        ordered_categories = []
        # First add categories in the specified order
        for cat in category_order:
            if cat in categories:
                ordered_categories.append(cat)
        # Then add any remaining categories
        for cat in categories:
            if cat not in ordered_categories:
                ordered_categories.append(cat)
        categories = ordered_categories
    else:
        # Default: sort alphabetically for consistency
        categories = sorted(categories)

    # Get color palette
    colors = get_color_palette(dark_mode=dark_mode)

    # Assign colors
    assigned_colors = []
    for i, cat in enumerate(categories):
        if color_mapping and str(cat) in color_mapping:
            # Use custom color mapping
            assigned_colors.append(color_mapping[str(cat)])
        else:
            # Use default color cycle
            assigned_colors.append(colors[i % len(colors)])

    return categories, assigned_colors


def get_colormap_for_numerical(
    dark_mode: bool = False, colormap: Optional[str] = None
) -> str:
    """
    Get appropriate colormap for numerical color mapping.

    Parameters
    ----------
    dark_mode : bool, default False
        Whether using dark mode
    colormap : str, optional
        Specific colormap name

    Returns
    -------
    str
        Colormap name
    """
    if colormap:
        return colormap

    return "plasma" if dark_mode else "viridis"


def validate_colors(colors: Union[str, List[str]]) -> List[str]:
    """
    Validate and normalize color specifications.

    Parameters
    ----------
    colors : str or list
        Color specification(s)

    Returns
    -------
    list
        Validated color list

    Raises
    ------
    ValueError
        If colors are invalid
    """
    import matplotlib.colors as mcolors

    if isinstance(colors, str):
        colors = [colors]

    validated = []
    for color in colors:
        try:
            # Try to validate the color
            mcolors.to_rgb(color)
            validated.append(color)
        except ValueError:
            raise ValueError(f"Invalid color specification: {color}")

    return validated


def blend_colors(color1: str, color2: str, weight: float = 0.5) -> str:
    """
    Blend two colors together.

    Parameters
    ----------
    color1 : str
        First color (hex or name)
    color2 : str
        Second color (hex or name)
    weight : float, default 0.5
        Weight for blending (0.0 = all color1, 1.0 = all color2)

    Returns
    -------
    str
        Blended color as hex string
    """
    import matplotlib.colors as mcolors

    # Convert to RGB
    rgb1 = np.array(mcolors.to_rgb(color1))
    rgb2 = np.array(mcolors.to_rgb(color2))

    # Blend
    blended = rgb1 * (1 - weight) + rgb2 * weight

    # Convert back to hex
    return mcolors.to_hex(blended)  # type: ignore[arg-type]


def generate_categorical_colors(
    n_categories: int, base_colors: Optional[List[str]] = None, dark_mode: bool = False
) -> List[str]:
    """
    Generate distinct colors for categorical data.

    Parameters
    ----------
    n_categories : int
        Number of categories to generate colors for
    base_colors : list, optional
        Base color palette to use
    dark_mode : bool, default False
        Whether to use dark mode optimized colors

    Returns
    -------
    list
        List of distinct colors
    """
    if base_colors is None:
        base_colors = get_color_palette(dark_mode=dark_mode)

    if n_categories <= len(base_colors):
        return base_colors[:n_categories]

    # If we need more colors than available, interpolate
    colors = []
    for i in range(n_categories):
        # Cycle through base colors and create variations
        base_idx = i % len(base_colors)
        base_color = base_colors[base_idx]

        if i < len(base_colors):
            colors.append(base_color)
        else:
            # Create variations by blending with accent color
            accent = (
                REKHA_DARK_COLORS["accent"] if dark_mode else REKHA_COLORS["accent"]
            )
            variation_weight = 0.3 * (
                (i // len(base_colors)) / (n_categories // len(base_colors))
            )
            colors.append(blend_colors(base_color, accent, variation_weight))

    return colors
