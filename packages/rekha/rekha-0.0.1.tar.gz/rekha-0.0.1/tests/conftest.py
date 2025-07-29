"""Configuration file for pytest tests."""

import warnings

import matplotlib

# Configure matplotlib to use a non-interactive backend for testing
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Suppress matplotlib warnings during testing
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Configure plotting for headless testing
plt.ioff()  # Turn off interactive plotting
