"""
Material UI Theme
Material Design-inspired theme for nb-ui
"""

from .core import Theme, DesignTokens


def create_material_theme() -> Theme:
    """Create Material UI theme"""

    tokens = DesignTokens(
        colors={
            "primary": "#1976d2",
            "secondary": "#dc004e",
            "success": "#2e7d32",
            "warning": "#ed6c02",
            "error": "#d32f2f",
            "info": "#0288d1",
            "text": "#212121",
            "textSecondary": "#757575",
            "surface": "#ffffff",
            "background": "#fafafa",
            "border": "#e0e0e0",
            "divider": "#e0e0e0",
            "disabled": "#bdbdbd",
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
                "fontSize": "2.125rem",
                "fontWeight": "300",
                "lineHeight": "1.167",
                "letterSpacing": "-0.01562em",
            },
            "h2": {
                "fontSize": "1.5rem",
                "fontWeight": "300",
                "lineHeight": "1.2",
                "letterSpacing": "-0.00833em",
            },
            "h3": {
                "fontSize": "1.25rem",
                "fontWeight": "400",
                "lineHeight": "1.167",
                "letterSpacing": "0em",
            },
            "h4": {
                "fontSize": "1.125rem",
                "fontWeight": "400",
                "lineHeight": "1.235",
                "letterSpacing": "0.00735em",
            },
            "h5": {
                "fontSize": "1rem",
                "fontWeight": "400",
                "lineHeight": "1.334",
                "letterSpacing": "0em",
            },
            "h6": {
                "fontSize": "0.875rem",
                "fontWeight": "500",
                "lineHeight": "1.6",
                "letterSpacing": "0.0075em",
            },
            "body1": {
                "fontSize": "1rem",
                "fontWeight": "400",
                "lineHeight": "1.5",
                "letterSpacing": "0.00938em",
            },
            "body2": {
                "fontSize": "0.875rem",
                "fontWeight": "400",
                "lineHeight": "1.43",
                "letterSpacing": "0.01071em",
            },
            "caption": {
                "fontSize": "0.75rem",
                "fontWeight": "400",
                "lineHeight": "1.66",
                "letterSpacing": "0.03333em",
            },
            "button": {
                "fontSize": "0.875rem",
                "fontWeight": "500",
                "lineHeight": "1.75",
                "letterSpacing": "0.02857em",
                "textTransform": "uppercase",
            },
        },
        shadows={
            "none": "none",
            "sm": "0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24)",
            "md": "0px 3px 6px rgba(0,0,0,0.16), 0px 3px 6px rgba(0,0,0,0.23)",
            "lg": "0px 10px 20px rgba(0,0,0,0.19), 0px 6px 6px rgba(0,0,0,0.23)",
            "xl": "0px 14px 28px rgba(0,0,0,0.25), 0px 10px 10px rgba(0,0,0,0.22)",
        },
        borders={
            "radius": "4px",
            "radiusLg": "8px",
            "radiusSm": "2px",
            "thin": "1px solid",
            "thick": "2px solid",
            "none": "none",
        },
        breakpoints={
            "xs": "0px",
            "sm": "600px",
            "md": "900px",
            "lg": "1200px",
            "xl": "1536px",
        },
    )

    return Theme(tokens)
