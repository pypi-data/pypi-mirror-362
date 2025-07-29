"""
nb-ui: Essential UI Components for Data Science Notebooks

A clean, Material UI inspired component library that makes
your Jupyter notebooks look professional without requiring HTML/CSS knowledge.
Perfect for data scientists who want to create beautiful reports and presentations.

Usage:
    from nb_ui import Header, Card, Alert, Typography

    Header("Data Analysis Results", subtitle="Customer Churn Prediction").display()
    Card("Model achieved 94.2% accuracy", title="Key Findings")
"""

# Core theme system
from .theme import set_theme, get_theme, list_themes

# Essential components for data science
from .components import (
    ComponentBase,
    Typography,
    Header,
    Card,
    Alert,
    CodeBlock,
    Container,
)

# Utility functions
from .utils import success, error, warning, info

__version__ = "1.0.0"

# Essential exports for data science notebooks
__all__ = [
    # Theme
    "set_theme",
    "get_theme",
    "list_themes",
    # Essential Components
    "ComponentBase",
    "Typography",
    "Header",
    "Card",
    "Alert",
    "CodeBlock",
    "Container",
    # Utility Functions
    "success",
    "error",
    "warning",
    "info",
]
