"""
Base Component Class
Core functionality for all nb-ui components
"""

from IPython.display import HTML, display
from typing import Optional, Dict
import uuid
from abc import ABC, abstractmethod


class ComponentBase(ABC):
    """Base class for all components with theme integration"""

    def __init__(self, theme: Optional[str] = None, **props):
        self.props = props
        self.theme_name = theme or self._get_current_theme()
        self.theme = self._get_theme_object(self.theme_name)
        self.component_id = (
            f"nb-{self.__class__.__name__.lower()}-{uuid.uuid4().hex[:8]}"
        )

    @abstractmethod
    def render(self) -> str:
        """Render the component HTML"""
        pass

    def _get_current_theme(self) -> str:
        """Get current theme from theme provider"""
        try:
            from ..theme.provider import ThemeProvider

            return ThemeProvider._current_theme
        except ImportError:
            return "material"

    def _get_theme_object(self, theme_name: str):
        """Get theme object from theme provider"""
        try:
            from ..theme.provider import ThemeProvider

            return ThemeProvider.get_theme(theme_name)
        except ImportError:
            # Fallback for development
            return type(
                "Theme",
                (),
                {
                    "colors": {
                        "primary": "#1976d2",
                        "text": "#212121",
                        "surface": "#ffffff",
                    },
                    "spacing": {"md": "1rem", "sm": "0.5rem", "lg": "1.5rem"},
                    "typography": {"body1": {"fontSize": "1rem", "fontWeight": "400"}},
                    "shadows": {"sm": "0 1px 3px rgba(0,0,0,0.1)"},
                    "borders": {"radius": "4px", "thin": "1px solid"},
                },
            )()

    def _get_color(self, color_name: str) -> str:
        """Get color from theme with fallback"""
        if hasattr(self.theme.colors, "get"):  # type: ignore
            return self.theme.colors.get(color_name, self.theme.colors.get("primary", "#1976d2"))  # type: ignore
        else:
            return getattr(self.theme.colors, color_name, "#1976d2")  # type: ignore

    def _get_typography(self, variant: str) -> Dict[str, str]:
        """Get typography styles from theme"""
        if hasattr(self.theme.typography, "get"):  # type: ignore
            return self.theme.typography.get(variant, self.theme.typography.get("body1", {}))  # type: ignore
        else:
            return getattr(self.theme.typography, variant, {})  # type: ignore

    def _get_spacing(self, size: str) -> str:
        """Get spacing from theme"""
        if hasattr(self.theme.spacing, "get"):  # type: ignore
            return self.theme.spacing.get(size, self.theme.spacing.get("md", "1rem"))  # type: ignore
        else:
            return getattr(self.theme.spacing, size, "1rem")  # type: ignore

    def _get_shadow(self, level: str) -> str:
        """Get shadow from theme"""
        if hasattr(self.theme.shadows, "get"):  # type: ignore
            return self.theme.shadows.get(level, self.theme.shadows.get("sm", "none"))  # type: ignore
        else:
            return getattr(self.theme.shadows, level, "none")  # type: ignore

    def _get_border(self, style: str) -> str:
        """Get border from theme"""
        if hasattr(self.theme.borders, "get"):  # type: ignore
            return self.theme.borders.get(style, self.theme.borders.get("thin", "1px solid"))  # type: ignore
        else:
            return getattr(self.theme.borders, style, "1px solid")  # type: ignore

    def _get_base_styles(self) -> str:
        """Base styles for all components"""
        return f"""
        <style>
            .nb-component {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                box-sizing: border-box;
            }}
            
            .nb-component *, .nb-component *::before, .nb-component *::after {{
                box-sizing: inherit;
            }}
        </style>
        """

    def display(self):
        """Display the component"""
        html_content = f"{self._get_base_styles()}{self.render()}"
        display(HTML(html_content))
        return self

    def _repr_html_(self):
        """Return HTML representation for Jupyter auto-display"""
        html_content = f"{self._get_base_styles()}{self.render()}"
        return html_content
