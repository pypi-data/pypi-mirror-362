"""
Alert Component
Material UI style alert component for notifications and messages
"""

from typing import Optional
from .base import ComponentBase


class Alert(ComponentBase):
    """Alert component with Material UI style"""

    def __init__(
        self,
        message: str,
        severity: str = "info",
        variant: str = "standard",
        onClose: bool = False,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.message = message
        self.severity = severity  # error, warning, info, success
        self.variant = variant  # standard, filled, outlined
        self.onClose = onClose

    def render(self) -> str:
        # Severity configurations
        severity_configs = {
            "error": {"color": self._get_color("error"), "icon": "❌"},
            "warning": {"color": self._get_color("warning"), "icon": "⚠️"},
            "info": {"color": self._get_color("info"), "icon": "ℹ️"},
            "success": {"color": self._get_color("success"), "icon": "✅"},
        }

        config = severity_configs.get(self.severity, severity_configs["info"])
        color = config["color"]
        icon = config["icon"]

        # Variant styles
        if self.variant == "filled":
            bg_color = color
            text_color = "#ffffff"
            border = "none"
        elif self.variant == "outlined":
            bg_color = "transparent"
            text_color = color
            border = f"1px solid {color}"
        else:  # standard
            bg_color = f"{color}08"
            text_color = color
            border = "none"

        close_button = ""
        if self.onClose:
            close_button = f"""
            <button style="background: none; border: none; color: {text_color}; 
                          cursor: pointer; padding: 0; margin-left: auto; 
                          font-size: 1.2rem; opacity: 0.7;"
                    onclick="this.parentElement.style.display='none';">×</button>
            """

        return f"""
        <style>
            .alert-{self.component_id} {{
                display: flex;
                align-items: center;
                padding: {self._get_spacing('sm')} {self._get_spacing('md')};
                margin: {self._get_spacing('md')} 0;
                border-radius: {self._get_border('radius')};
                background-color: {bg_color};
                color: {text_color};
                border: {border};
                font-size: 0.875rem;
                line-height: 1.43;
            }}
            
            .alert-{self.component_id} .alert-icon {{
                margin-right: {self._get_spacing('sm')};
                font-size: 1.2rem;
            }}
        </style>
        <div class="nb-component alert-{self.component_id}">
            <span class="alert-icon">{icon}</span>
            <span style="flex: 1;">{self.message}</span>
            {close_button}
        </div>
        """
