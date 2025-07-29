"""
Utility functions for generating sample data for Rekha examples.
These functions are referenced in the documentation code examples.
"""

import numpy as np
import pandas as pd


def get_time_series_data(n_days=100, seed=42):
    """Generate time series data for line plot examples."""
    np.random.seed(seed)
    dates = pd.date_range("2023-01-01", periods=n_days, freq="D")

    df = pd.DataFrame(
        {
            "date": dates,
            "users": np.cumsum(np.random.randn(n_days)) * 100 + 5000,
            "sessions": np.cumsum(np.random.randn(n_days)) * 150 + 7000,
            "pageviews": np.cumsum(np.random.randn(n_days)) * 200 + 10000,
            "revenue": np.cumsum(np.random.randn(n_days)) * 50 + 2000,
        }
    )
    return df


def get_iris(seed=42):
    """Generate iris-like dataset for scatter and other plot examples."""
    np.random.seed(seed)

    # Simulate iris dataset with 3 species
    species = np.repeat(["setosa", "versicolor", "virginica"], 50)

    sepal_length = np.concatenate(
        [
            np.random.normal(5.0, 0.35, 50),
            np.random.normal(5.9, 0.51, 50),
            np.random.normal(6.5, 0.63, 50),
        ]
    )

    sepal_width = np.concatenate(
        [
            np.random.normal(3.4, 0.38, 50),
            np.random.normal(2.8, 0.31, 50),
            np.random.normal(3.0, 0.32, 50),
        ]
    )

    petal_length = np.concatenate(
        [
            np.random.normal(1.5, 0.17, 50),
            np.random.normal(4.3, 0.47, 50),
            np.random.normal(5.5, 0.55, 50),
        ]
    )

    petal_width = np.concatenate(
        [
            np.random.normal(0.2, 0.10, 50),
            np.random.normal(1.3, 0.20, 50),
            np.random.normal(2.0, 0.27, 50),
        ]
    )

    return pd.DataFrame(
        {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width,
            "species": species,
        }
    )


def get_categorical_data(seed=42):
    """Generate categorical data for bar plot examples."""
    np.random.seed(seed)

    regions = ["North", "South", "East", "West"]
    products = ["Product A", "Product B", "Product C", "Product D"]
    quarters = ["Q1", "Q2", "Q3", "Q4"]

    data = []
    for region in regions:
        for product in products:
            for quarter in quarters:
                base_sales = np.random.uniform(10000, 50000)
                sales = base_sales * (1 + np.random.uniform(-0.2, 0.3))
                data.append(
                    {
                        "region": region,
                        "product": product,
                        "quarter": quarter,
                        "sales": sales,
                    }
                )

    return pd.DataFrame(data)


def get_tips(seed=42):
    """Generate tips dataset for heatmap and multi-dimensional examples."""
    np.random.seed(seed)
    n_tips = 200

    days = ["Thur", "Fri", "Sat", "Sun"]
    times = ["Lunch", "Dinner"]

    df = pd.DataFrame(
        {
            "total_bill": np.random.lognormal(3.0, 0.5, n_tips),
            "tip": np.random.lognormal(1.0, 0.4, n_tips),
            "size": np.random.choice(
                [1, 2, 3, 4, 5, 6], n_tips, p=[0.05, 0.4, 0.3, 0.15, 0.07, 0.03]
            ),
            "time": np.random.choice(times, n_tips, p=[0.4, 0.6]),
            "day": np.random.choice(days, n_tips, p=[0.15, 0.25, 0.35, 0.25]),
            "smoker": np.random.choice(["Yes", "No"], n_tips, p=[0.3, 0.7]),
        }
    )

    # Make tips proportional to bill
    df["tip"] = df["tip"] * 0.15 * df["total_bill"]

    return df


def get_distribution_data(dist_type="normal", n_points=1000, seed=42):
    """Generate various distribution types for histogram examples."""
    np.random.seed(seed)

    if dist_type == "normal":
        return np.random.normal(100, 15, n_points)
    elif dist_type == "skewed":
        return np.random.gamma(2, 2, n_points) * 10 + 60
    elif dist_type == "bimodal":
        return np.concatenate(
            [
                np.random.normal(80, 10, n_points // 2),
                np.random.normal(120, 10, n_points // 2),
            ]
        )
    elif dist_type == "uniform":
        return np.random.uniform(50, 150, n_points)
    else:
        raise ValueError(f"Unknown distribution type: {dist_type}")


def get_model_performance_data(seed=42):
    """Generate AI/ML model performance data for impressive visualizations."""
    np.random.seed(seed)

    # Model performance comparison data
    model_data = pd.DataFrame(
        {
            "model_size": [7, 13, 30, 65, 175, 540] * 3,
            "throughput": [950, 680, 420, 280, 150, 85]
            + [720, 510, 320, 210, 120, 65]
            + [580, 410, 260, 170, 95, 50],
            "framework": ["Rekha"] * 6 + ["PyTorch"] * 6 + ["TensorFlow"] * 6,
            "memory_gb": [8, 15, 32, 68, 145, 380]
            + [12, 22, 45, 89, 195, 520]
            + [15, 28, 52, 98, 215, 580],
            "accuracy": [92.3, 94.1, 95.8, 96.9, 97.5, 98.1] * 3,
        }
    )

    return model_data


def get_training_metrics(n_epochs=100, n_models=3, seed=42):
    """Generate training metrics data for model comparison."""
    np.random.seed(seed)

    models = ["GPT-4", "LLaMA-2", "PaLM"]
    epochs = list(range(1, n_epochs + 1))

    data = []
    for i, model in enumerate(models[:n_models]):
        # Different convergence rates for each model
        base_loss = 4.5 - i * 0.3
        decay_rate = 0.08 - i * 0.02
        noise_level = 0.02 + i * 0.01

        for epoch in epochs:
            loss = (
                base_loss * np.exp(-decay_rate * epoch)
                + 0.1
                + np.random.normal(0, noise_level)
            )
            data.append(
                {
                    "epoch": epoch,
                    "loss": max(0.05, loss),  # Ensure positive loss
                    "model": model,
                    "val_loss": max(
                        0.05, loss + np.random.normal(0, noise_level * 1.5)
                    ),
                }
            )

    return pd.DataFrame(data)


def get_benchmark_data(seed=42):
    """Generate benchmark comparison data."""
    np.random.seed(seed)

    tasks = [
        "Language\nModeling",
        "Question\nAnswering",
        "Text\nSummarization",
        "Code\nGeneration",
        "Translation",
        "Sentiment\nAnalysis",
    ]

    # Rekha consistently performs better
    rekha_scores = [94.2, 91.8, 89.5, 92.1, 88.7, 95.3]
    baseline_scores = [87.5, 84.2, 81.9, 85.6, 82.1, 89.7]

    data = []
    for task, rekha, baseline in zip(tasks, rekha_scores, baseline_scores):
        data.append({"task": task, "method": "Rekha", "score": rekha})
        data.append({"task": task, "method": "Baseline", "score": baseline})

    return pd.DataFrame(data)
