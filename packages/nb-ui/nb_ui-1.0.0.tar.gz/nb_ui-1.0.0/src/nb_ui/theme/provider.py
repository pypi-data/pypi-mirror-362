"""
Theme Provider
Centralized theme management for nb-ui
"""

from typing import Dict, Optional
from .core import Theme
from .material import create_material_theme
from .antd import create_antd_theme
from .dark import create_dark_theme


class ThemeProvider:
    """Centralized theme provider"""

    _themes: Dict[str, Theme] = {}
    _current_theme: str = "material"

    @classmethod
    def initialize(cls):
        """Initialize default themes"""
        if not cls._themes:
            cls._themes = {
                "material": create_material_theme(),
                "antd": create_antd_theme(),
                "dark": create_dark_theme(),
            }

    @classmethod
    def get_theme(cls, name: str) -> Theme:
        """Get theme by name"""
        cls.initialize()
        return cls._themes.get(name, cls._themes["material"])

    @classmethod
    def set_theme(cls, name: str):
        """Set current theme"""
        cls.initialize()
        if name in cls._themes:
            cls._current_theme = name
        else:
            raise ValueError(
                f"Theme '{name}' not found. Available themes: {list(cls._themes.keys())}"
            )

    @classmethod
    def get_current_theme(cls) -> Theme:
        """Get current theme"""
        cls.initialize()
        return cls._themes[cls._current_theme]

    @classmethod
    def get_current_theme_name(cls) -> str:
        """Get current theme name"""
        return cls._current_theme

    @classmethod
    def add_theme(cls, name: str, theme: Theme):
        """Add custom theme"""
        cls.initialize()
        cls._themes[name] = theme

    @classmethod
    def list_themes(cls) -> list:
        """List available themes"""
        cls.initialize()
        return list(cls._themes.keys())


# Convenience function for theme switching
def set_theme(theme_name: str):
    """Set global theme for all components"""
    ThemeProvider.set_theme(theme_name)


def get_theme() -> Theme:
    """Get current theme"""
    return ThemeProvider.get_current_theme()


def list_themes() -> list:
    """List available themes"""
    return ThemeProvider.list_themes()
