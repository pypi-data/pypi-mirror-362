"""
Card Component
Material UI style card component for content grouping
"""

from typing import Optional, Union, List, Any
from .base import ComponentBase


class Card(ComponentBase):
    """Card component with Material UI style"""

    def __init__(
        self,
        children: Union[str, List[Any], Any] = "",
        title: Optional[str] = None,
        variant: str = "elevation",
        elevation: int = 1,
        square: bool = False,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.children = children
        self.title = title
        self.variant = variant  # elevation, outlined
        self.elevation = elevation
        self.square = square
        self._header = None
        self._content = None
        self._actions = None

    def _render_children(self) -> str:
        """Render children whether they're strings, components, or lists"""
        if isinstance(self.children, list):
            # Render each component in the list
            rendered_children = []
            for child in self.children:
                if hasattr(child, "render"):
                    rendered_children.append(child.render())  # type: ignore
                else:
                    rendered_children.append(str(child))
            return "\n".join(rendered_children)
        elif hasattr(self.children, "render"):
            # Single component with render method
            return self.children.render()  # type: ignore
        else:
            # String or other content
            return str(self.children)

    def render(self) -> str:
        # Shadow based on elevation
        shadow_levels = ["none", "xs", "sm", "md", "lg", "xl", "xxl"]
        shadow = self._get_shadow(shadow_levels[min(self.elevation, 6)])

        if self.variant == "outlined":
            border = f"1px solid {self._get_color('divider')}"
            shadow = "none"
        else:
            border = "none"

        border_radius = "0" if self.square else self._get_border("radius")

        content_html = ""
        if self._header or self.title:
            title_html = ""
            if self.title:
                typo_styles = self._get_typography("h6")
                title_html = f"""
                <div style="padding: {self._get_spacing('md')} {self._get_spacing('md')} 0 {self._get_spacing('md')};
                           border-bottom: 1px solid {self._get_color('divider')};">
                    <h6 style="margin: 0 0 {self._get_spacing('sm')} 0;
                              color: {self._get_color('text')};
                              font-size: {typo_styles.get('fontSize', '1.25rem')};
                              font-weight: {typo_styles.get('fontWeight', '500')};
                              line-height: {typo_styles.get('lineHeight', '1.6')};">
                        {self.title}
                    </h6>
                </div>
                """
            content_html += (self._header or "") + title_html
        if self._content or self.children:
            content_html += f"""
            <div style="padding: {self._get_spacing('md')};">
                {self._content or self._render_children()}
            </div>
            """
        if self._actions:
            content_html += self._actions

        return f"""
        <style>
            .card-{self.component_id} {{
                background-color: {self._get_color('surface')};
                color: {self._get_color('text')};
                border: {border};
                border-radius: {border_radius};
                box-shadow: {shadow};
                overflow: hidden;
                transition: box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
                margin: {self._get_spacing('md')} 0;
            }}
        </style>
        <div class="nb-component card-{self.component_id}">
            {content_html}
        </div>
        """
