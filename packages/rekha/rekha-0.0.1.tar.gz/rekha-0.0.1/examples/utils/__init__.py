"""
Utility module for Rekha examples.
"""

from .data_generators import (
    get_benchmark_data,
    get_categorical_data,
    get_distribution_data,
    get_iris,
    get_model_performance_data,
    get_time_series_data,
    get_tips,
    get_training_metrics,
)

__all__ = [
    "get_time_series_data",
    "get_iris",
    "get_categorical_data",
    "get_tips",
    "get_distribution_data",
    "get_model_performance_data",
    "get_training_metrics",
    "get_benchmark_data",
]
