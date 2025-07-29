"""
Data preparation and validation utilities.
"""

from typing import Any, List, Optional, Tuple, Union

import numpy as np
import pandas as pd


def prepare_data(
    data: Union[pd.DataFrame, dict, None],
    x: Union[str, List, np.ndarray, None] = None,
    y: Union[str, List, np.ndarray, None] = None,
) -> Tuple[Any, Any]:
    """
    Extract x and y data from various input formats.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data source
    x, y : str, list, array, or None
        Column names or data arrays

    Returns
    -------
    tuple
        (x_data, y_data) arrays
    """
    if isinstance(data, pd.DataFrame):
        x_data = data[x] if isinstance(x, str) else x
        y_data = data[y] if isinstance(y, str) else y
    elif isinstance(data, dict):
        x_data = data.get(x, x) if isinstance(x, str) else x
        y_data = data.get(y, y) if isinstance(y, str) else y
    else:
        x_data = x
        y_data = y

    # Validate that x_data and y_data have matching lengths if both are arrays
    if x_data is not None and y_data is not None:
        if hasattr(x_data, "__len__") and hasattr(y_data, "__len__"):
            if len(x_data) != len(y_data):
                raise ValueError(
                    f"x and y data must have same length: {len(x_data)} vs {len(y_data)}"
                )

    return x_data, y_data


def validate_data(
    data: Union[pd.DataFrame, dict, None],
    x: Union[str, List, np.ndarray, None] = None,
    y: Union[str, List, np.ndarray, None] = None,
    required_columns: Optional[List[str]] = None,
) -> bool:
    """
    Validate data and column specifications.

    Parameters
    ----------
    data : DataFrame, dict, or None
        The data source
    x, y : str, list, array, or None
        Column names or data arrays
    required_columns : list, optional
        List of required column names

    Returns
    -------
    bool
        True if data is valid

    Raises
    ------
    ValueError
        If data validation fails
    """
    # Allow case where all are None (return True for valid empty case)
    if data is None and x is None and y is None:
        return True

    if data is None and (x is None or y is None):
        raise ValueError("Either data with column names or x/y arrays must be provided")

    if isinstance(data, pd.DataFrame):
        if isinstance(x, str) and x not in data.columns:
            raise ValueError(f"Column '{x}' not found in data")
        if isinstance(y, str) and y not in data.columns:
            raise ValueError(f"Column '{y}' not found in data")

        if required_columns:
            missing = [col for col in required_columns if col not in data.columns]
            if missing:
                raise ValueError(f"Required columns missing: {missing}")

    return True


def detect_data_types(data: pd.DataFrame, columns: List[str]) -> dict:
    """
    Detect data types for specified columns.

    Parameters
    ----------
    data : DataFrame
        The data to analyze
    columns : list
        Column names to analyze

    Returns
    -------
    dict
        Mapping of column names to data types ('numerical', 'categorical', 'datetime')
    """
    types = {}

    for col in columns:
        if col not in data.columns:
            continue

        if pd.api.types.is_numeric_dtype(data[col]):
            types[col] = "numerical"
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            types[col] = "datetime"
        else:
            types[col] = "categorical"

    return types


def prepare_categorical_data(
    data: pd.DataFrame, column: str, category_order: Optional[List[str]] = None
) -> Tuple[List[str], pd.Series]:
    """
    Prepare categorical data with optional ordering.

    Parameters
    ----------
    data : DataFrame
        The data containing the categorical column
    column : str
        Name of the categorical column
    category_order : list, optional
        Custom ordering for categories

    Returns
    -------
    tuple
        (ordered_categories, reordered_series)
    """
    unique_categories = data[column].unique().tolist()

    if category_order:
        # Apply custom ordering
        ordered_categories = []
        # Add categories in specified order
        for cat in category_order:
            if cat in unique_categories:
                ordered_categories.append(cat)
        # Add remaining categories
        for cat in unique_categories:
            if cat not in ordered_categories:
                ordered_categories.append(cat)
    else:
        # Default alphabetical ordering
        ordered_categories = sorted(unique_categories)

    # Create ordered categorical
    ordered_series = pd.Categorical(
        data[column], categories=ordered_categories, ordered=True
    )

    return ordered_categories, ordered_series


def prepare_size_data(
    data: pd.DataFrame,
    size_column: Union[str, List, np.ndarray, None],
    base_size: float = 100,
    max_size: float = 200,
) -> Union[float, np.ndarray]:
    """
    Prepare size data for scatter plots.

    Parameters
    ----------
    data : DataFrame
        The data containing size information
    size_column : str, list, array, or None
        Size specification
    base_size : float, default 100
        Base size for points
    max_size : float, default 200
        Maximum size for numerical scaling

    Returns
    -------
    float or array
        Size values for plotting
    """
    if size_column is None:
        return base_size

    if isinstance(size_column, str) and size_column in data.columns:
        size_values = data[size_column]

        if pd.api.types.is_numeric_dtype(size_values):
            # Numerical size: scale between base_size and max_size
            size_min, size_max = size_values.min(), size_values.max()
            if size_max > size_min:
                return base_size + (size_values - size_min) / (size_max - size_min) * (
                    max_size - base_size
                )
            else:
                return base_size
        else:
            # Categorical size: different fixed sizes
            return (
                size_values.astype("category").cat.codes * (base_size / 5) + base_size
            )

    elif isinstance(size_column, (list, np.ndarray)):
        return np.array(size_column) * (base_size / 5) + base_size

    return base_size
