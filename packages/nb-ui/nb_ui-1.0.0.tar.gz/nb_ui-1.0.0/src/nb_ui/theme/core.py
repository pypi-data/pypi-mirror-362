"""
Core Theme Classes
Base theme structure and types for nb-ui
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DesignTokens:
    """Design tokens for consistent theming"""

    # Colors
    colors: Dict[str, str]

    # Spacing
    spacing: Dict[str, str]  # xs, sm, md, lg, xl

    # Typography
    typography: Dict[str, Dict[str, str]]  # h1, h2, body1, body2, etc.

    # Shadows
    shadows: Dict[str, str]  # sm, md, lg

    # Borders
    borders: Dict[str, str]  # radius, thin, thick

    # Breakpoints
    breakpoints: Dict[str, str]  # xs, sm, md, lg, xl


class Theme:
    """Base theme class"""

    def __init__(self, tokens: DesignTokens):
        self.tokens = tokens
        self.colors = tokens.colors
        self.spacing = tokens.spacing
        self.typography = tokens.typography
        self.shadows = tokens.shadows
        self.borders = tokens.borders
        self.breakpoints = tokens.breakpoints
