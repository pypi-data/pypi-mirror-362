"""
Container Component
Layout container component for consistent content width and centering
"""

from typing import Optional, Union, List, Any
from .base import ComponentBase


class Container(ComponentBase):
    """Container component for consistent layout"""

    def __init__(
        self,
        children: Union[str, List[Any], Any] = "",
        maxWidth: str = "lg",
        fixed: bool = False,
        disableGutters: bool = False,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.children = children
        self.maxWidth = maxWidth  # xs, sm, md, lg, xl, false
        self.fixed = fixed
        self.disableGutters = disableGutters

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
        max_widths = {
            "xs": "444px",
            "sm": "600px",
            "md": "960px",
            "lg": "1280px",
            "xl": "1920px",
        }

        max_width = max_widths.get(self.maxWidth, "100%")
        padding = "0" if self.disableGutters else f'0 {self._get_spacing("md")}'
        width = max_width if self.fixed else "100%"

        return f"""
        <style>
            .container-{self.component_id} {{
                width: {width};
                max-width: {max_width};
                margin: 0 auto;
                padding: {padding};
                box-sizing: border-box;
            }}
        </style>
        <div class="nb-component container-{self.component_id}">
            {self._render_children()}
        </div>
        """
