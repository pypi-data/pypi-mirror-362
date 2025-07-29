"""
Dark Theme
Dark mode theme for nb-ui
"""

from .core import Theme, DesignTokens


def create_dark_theme() -> Theme:
    """Create Dark theme"""

    tokens = DesignTokens(
        colors={
            "primary": "#90caf9",
            "secondary": "#f48fb1",
            "success": "#81c784",
            "warning": "#ffb74d",
            "error": "#f44336",
            "info": "#64b5f6",
            "text": "#ffffff",
            "textSecondary": "#b3b3b3",
            "surface": "#424242",
            "background": "#303030",
            "border": "#616161",
            "divider": "#616161",
            "disabled": "#757575",
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
                "color": "#ffffff",
            },
            "h2": {
                "fontSize": "1.5rem",
                "fontWeight": "300",
                "lineHeight": "1.2",
                "letterSpacing": "-0.00833em",
                "color": "#ffffff",
            },
            "h3": {
                "fontSize": "1.25rem",
                "fontWeight": "400",
                "lineHeight": "1.167",
                "letterSpacing": "0em",
                "color": "#ffffff",
            },
            "h4": {
                "fontSize": "1.125rem",
                "fontWeight": "400",
                "lineHeight": "1.235",
                "letterSpacing": "0.00735em",
                "color": "#ffffff",
            },
            "h5": {
                "fontSize": "1rem",
                "fontWeight": "400",
                "lineHeight": "1.334",
                "letterSpacing": "0em",
                "color": "#ffffff",
            },
            "h6": {
                "fontSize": "0.875rem",
                "fontWeight": "500",
                "lineHeight": "1.6",
                "letterSpacing": "0.0075em",
                "color": "#ffffff",
            },
            "body1": {
                "fontSize": "1rem",
                "fontWeight": "400",
                "lineHeight": "1.5",
                "letterSpacing": "0.00938em",
                "color": "#ffffff",
            },
            "body2": {
                "fontSize": "0.875rem",
                "fontWeight": "400",
                "lineHeight": "1.43",
                "letterSpacing": "0.01071em",
                "color": "#b3b3b3",
            },
            "caption": {
                "fontSize": "0.75rem",
                "fontWeight": "400",
                "lineHeight": "1.66",
                "letterSpacing": "0.03333em",
                "color": "#b3b3b3",
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
            "sm": "0px 1px 3px rgba(0,0,0,0.5), 0px 1px 2px rgba(0,0,0,0.6)",
            "md": "0px 3px 6px rgba(0,0,0,0.6), 0px 3px 6px rgba(0,0,0,0.7)",
            "lg": "0px 10px 20px rgba(0,0,0,0.7), 0px 6px 6px rgba(0,0,0,0.8)",
            "xl": "0px 14px 28px rgba(0,0,0,0.8), 0px 10px 10px rgba(0,0,0,0.9)",
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
