"""
Typography Component
Text display component with Material UI style variants
"""

from typing import Optional, Dict
from .base import ComponentBase


class Typography(ComponentBase):
    """Typography component with Material UI style variants"""

    def __init__(
        self,
        text: str,
        variant: str = "body1",
        color: str = "text",
        align: str = "left",
        gutterBottom: bool = False,
        noWrap: bool = False,
        weight: Optional[str] = None,
        style: Optional[str] = None,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.text = text
        self.variant = variant
        self.color = color
        self.align = align
        self.gutterBottom = gutterBottom
        self.noWrap = noWrap
        self.weight = weight  # bold, normal, light, etc.
        self.style = style  # italic, normal, etc.

    def render(self) -> str:
        typo_styles = self._get_typography(self.variant)
        color_value = self._get_color(self.color)

        # Determine HTML tag based on variant
        tag_map = {
            "h1": "h1",
            "h2": "h2",
            "h3": "h3",
            "h4": "h4",
            "h5": "h5",
            "h6": "h6",
            "body1": "p",
            "body2": "p",
            "subtitle1": "h6",
            "subtitle2": "h6",
            "caption": "span",
            "button": "span",
            "overline": "span",
        }
        tag = tag_map.get(self.variant, "p")

        margin_bottom = self._get_spacing("md") if self.gutterBottom else "0"
        overflow = "hidden" if self.noWrap else "visible"
        white_space = "nowrap" if self.noWrap else "normal"
        text_overflow = "ellipsis" if self.noWrap else "clip"

        # Override font weight and style if provided
        font_weight = (
            self.weight if self.weight else typo_styles.get("fontWeight", "400")
        )
        font_style = self.style if self.style else "normal"

        return f"""
        <style>
            .typography-{self.component_id} {{
                font-size: {typo_styles.get('fontSize', '1rem')};
                font-weight: {font_weight};
                font-style: {font_style};
                line-height: {typo_styles.get('lineHeight', '1.5')};
                color: {color_value};
                text-align: {self.align};
                margin: 0 0 {margin_bottom} 0;
                overflow: {overflow};
                white-space: {white_space};
                text-overflow: {text_overflow};
            }}
        </style>
        <{tag} class="nb-component typography-{self.component_id}">{self.text}</{tag}>
        """
