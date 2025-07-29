"""
Header Component
Page header component with clean Material UI style
"""

from typing import Optional
from .base import ComponentBase


class Header(ComponentBase):
    """Header component with clean Material UI style"""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        variant: str = "h1",
        level: Optional[str] = None,
        color: str = "primary",
        align: str = "center",
        divider: bool = True,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.title = title
        self.subtitle = subtitle
        # Support both variant and level parameters for backward compatibility
        self.variant = level if level is not None else variant
        self.color = color
        self.align = align
        self.divider = divider

    def render(self) -> str:
        color_value = self._get_color(self.color)
        typo_styles = self._get_typography(self.variant)

        subtitle_html = ""
        if self.subtitle:
            subtitle_typo = self._get_typography("subtitle1")
            subtitle_html = f"""
            <p style="color: {self._get_color('textSecondary')}; 
                     font-size: {subtitle_typo.get('fontSize', '1rem')};
                     font-weight: {subtitle_typo.get('fontWeight', '400')};
                     line-height: {subtitle_typo.get('lineHeight', '1.5')};
                     margin: {self._get_spacing('sm')} 0 0 0;
                     text-align: {self.align};">
                {self.subtitle}
            </p>
            """

        divider_html = ""
        if self.divider:
            divider_html = f"""
            <hr style="border: none; 
                      height: 2px; 
                      background: linear-gradient(90deg, {color_value}, {color_value}40);
                      margin: {self._get_spacing('lg')} auto;
                      width: 60px;
                      border-radius: 2px;">
            """

        return f"""
        <style>
            .header-{self.component_id} {{
                text-align: {self.align};
                margin: {self._get_spacing('xl')} 0;
                padding: {self._get_spacing('lg')} 0;
            }}
            
            .header-{self.component_id} h1,
            .header-{self.component_id} h2,
            .header-{self.component_id} h3,
            .header-{self.component_id} h4,
            .header-{self.component_id} h5,
            .header-{self.component_id} h6 {{
                color: {color_value};
                font-size: {typo_styles.get('fontSize', '2.5rem')};
                font-weight: {typo_styles.get('fontWeight', '300')};
                line-height: {typo_styles.get('lineHeight', '1.2')};
                margin: 0;
                letter-spacing: -0.01562em;
            }}
        </style>
        <div class="nb-component header-{self.component_id}">
            <{self.variant}>{self.title}</{self.variant}>
            {subtitle_html}
            {divider_html}
        </div>
        """
