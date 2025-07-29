"""
Ant Design Theme
Ant Design-inspired theme for nb-ui
"""

from .core import Theme, DesignTokens


def create_antd_theme() -> Theme:
    """Create Ant Design theme"""

    tokens = DesignTokens(
        colors={
            "primary": "#1890ff",
            "secondary": "#722ed1",
            "success": "#52c41a",
            "warning": "#faad14",
            "error": "#f5222d",
            "info": "#1890ff",
            "text": "#000000d9",
            "textSecondary": "#00000073",
            "surface": "#ffffff",
            "background": "#f0f2f5",
            "border": "#d9d9d9",
            "divider": "#f0f0f0",
            "disabled": "#00000040",
        },
        spacing={
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
            "xxl": "3rem",
        },
        typography={
            "h1": {
                "fontSize": "2.25rem",
                "fontWeight": "600",
                "lineHeight": "1.23",
                "color": "#000000d9",
            },
            "h2": {
                "fontSize": "1.875rem",
                "fontWeight": "600",
                "lineHeight": "1.35",
                "color": "#000000d9",
            },
            "h3": {
                "fontSize": "1.5rem",
                "fontWeight": "600",
                "lineHeight": "1.35",
                "color": "#000000d9",
            },
            "h4": {
                "fontSize": "1.25rem",
                "fontWeight": "600",
                "lineHeight": "1.4",
                "color": "#000000d9",
            },
            "h5": {
                "fontSize": "1rem",
                "fontWeight": "600",
                "lineHeight": "1.5",
                "color": "#000000d9",
            },
            "h6": {
                "fontSize": "0.875rem",
                "fontWeight": "600",
                "lineHeight": "1.5",
                "color": "#000000d9",
            },
            "body1": {
                "fontSize": "0.875rem",
                "fontWeight": "400",
                "lineHeight": "1.5715",
                "color": "#000000d9",
            },
            "body2": {
                "fontSize": "0.75rem",
                "fontWeight": "400",
                "lineHeight": "1.5715",
                "color": "#00000073",
            },
            "caption": {
                "fontSize": "0.75rem",
                "fontWeight": "400",
                "lineHeight": "1.5715",
                "color": "#00000073",
            },
            "button": {
                "fontSize": "0.875rem",
                "fontWeight": "400",
                "lineHeight": "1.5715",
            },
        },
        shadows={
            "none": "none",
            "sm": "0 2px 8px rgba(0, 0, 0, 0.15)",
            "md": "0 4px 12px rgba(0, 0, 0, 0.15)",
            "lg": "0 6px 16px rgba(0, 0, 0, 0.08)",
            "xl": "0 9px 28px 8px rgba(0, 0, 0, 0.05)",
        },
        borders={
            "radius": "6px",
            "radiusLg": "8px",
            "radiusSm": "4px",
            "thin": "1px solid",
            "thick": "2px solid",
            "none": "none",
        },
        breakpoints={
            "xs": "0px",
            "sm": "576px",
            "md": "768px",
            "lg": "992px",
            "xl": "1200px",
        },
    )

    return Theme(tokens)
