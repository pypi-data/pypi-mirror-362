"""
Utility Functions for nb-ui
Convenient shortcuts and helper functions for data science notebooks
"""

from typing import List, Optional, Dict, Any, Union
from .components import Header, Card, Alert, Typography, CodeBlock, Container
from .theme import set_theme as theme_set_theme


# Convenience functions with simplified APIs
def header(title: str, subtitle: str = "", theme: str = "material", **kwargs):
    """Create a header with simplified API"""
    return Header(title, subtitle=subtitle, theme=theme, **kwargs)


def card(content: str, title: str = "", theme: str = "material", **kwargs):
    """Create a card with simplified API"""
    if title:
        # Create a card with header
        card_content = (
            f"<h3 style='margin: 0 0 1rem 0; font-weight: 600;'>{title}</h3>{content}"
        )
        return Card(card_content, theme=theme, **kwargs)
    return Card(content, theme=theme, **kwargs)


def alert(message: str, severity: str = "info", theme: str = "material", **kwargs):
    """Create an alert with simplified API"""
    return Alert(message, severity=severity, theme=theme, **kwargs)


def text(content: str, variant: str = "body1", theme: str = "material", **kwargs):
    """Create typography with simplified API"""
    return Typography(content, variant=variant, theme=theme, **kwargs)


def code(code_str: str, language: str = "python", theme: str = "material", **kwargs):
    """Create a code block with simplified API"""
    return CodeBlock(code_str, language=language, theme=theme, **kwargs)


# Semantic shortcuts for common alert types
def success(message: str, **kwargs):
    """Create a success alert"""
    return Alert(message, severity="success", **kwargs)


def error(message: str, **kwargs):
    """Create an error alert"""
    return Alert(message, severity="error", **kwargs)


def warning(message: str, **kwargs):
    """Create a warning alert"""
    return Alert(message, severity="warning", **kwargs)


def info(message: str, **kwargs):
    """Create an info alert"""
    return Alert(message, severity="info", **kwargs)


# Theme management shortcuts
def set_theme(theme_name: str):
    """Set the global theme"""
    theme_set_theme(theme_name)


def material_theme():
    """Set Material UI theme"""
    set_theme("material")


def antd_theme():
    """Set Ant Design theme"""
    set_theme("antd")


def dark_theme():
    """Set dark theme"""
    set_theme("dark")


# Component creation shortcuts
def create_dashboard(
    title: str, subtitle: str = "", content: str = "", theme: str = "material"
):
    """Create a dashboard layout with header and content"""
    # Header
    header(title, subtitle, theme=theme)

    # Main content
    if content:
        card(content, theme=theme)


def container(content: str, maxWidth: str = "lg", theme: str = "material"):
    """Wrap content in a container"""
    return Container(content, maxWidth=maxWidth, theme=theme).display()


# Notebook-specific utilities
def notebook_header(
    title: str, author: str = "", date: str = "", theme: str = "material"
):
    """Create a notebook header with metadata"""
    subtitle_parts = []
    if author:
        subtitle_parts.append(f"by {author}")
    if date:
        subtitle_parts.append(date)

    subtitle = " • ".join(subtitle_parts)
    return header(title, subtitle, theme=theme)


def code_result(
    code_str: str, result: str, language: str = "python", theme: str = "material"
):
    """Display code and its result"""
    code(code_str, language=language, theme=theme)
    card(f"<strong>Output:</strong><br>{result}", theme=theme)


def quick_table(
    data: List[List[str]], headers: Optional[List[str]] = None, theme: str = "material"
):
    """Create a simple HTML table"""
    from .theme import ThemeProvider

    theme_obj = ThemeProvider.get_theme(theme)

    table_html = (
        '<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">'
    )

    # Headers
    if headers:
        table_html += "<thead><tr>"
        for header in headers:
            table_html += f"""<th style="border: 1px solid {theme_obj.colors.get('divider', '#e0e0e0')}; 
                                       padding: 0.75rem; 
                                       background: {theme_obj.colors.get('background', '#f5f5f5')};
                                       text-align: left; font-weight: 600;">{header}</th>"""
        table_html += "</tr></thead>"

    # Rows
    table_html += "<tbody>"
    for row in data:
        table_html += "<tr>"
        for cell in row:
            table_html += f"""<td style="border: 1px solid {theme_obj.colors.get('divider', '#e0e0e0')}; 
                                       padding: 0.75rem;">{cell}</td>"""
        table_html += "</tr>"
    table_html += "</tbody></table>"

    card(table_html, theme=theme)


# Progress and loading utilities
def progress_bar(
    value: int, max_value: int = 100, label: str = "", theme: str = "material"
):
    """Create a progress bar"""
    from .theme import ThemeProvider

    theme_obj = ThemeProvider.get_theme(theme)

    percentage = (value / max_value) * 100 if max_value > 0 else 0
    primary_color = theme_obj.colors.get("primary", "#1976d2")

    progress_html = f"""
    <div style="margin: 1rem 0;">
        {f'<div style="margin-bottom: 0.5rem; font-weight: 500;">{label}</div>' if label else ''}
        <div style="background: {theme_obj.colors.get('divider', '#e0e0e0')}; 
                   height: 8px; border-radius: 4px; overflow: hidden;">
            <div style="background: {primary_color}; height: 100%; width: {percentage}%; 
                       transition: width 0.3s ease; border-radius: 4px;"></div>
        </div>
        <div style="text-align: right; font-size: 0.875rem; margin-top: 0.25rem; 
                   color: {theme_obj.colors.get('textSecondary', '#757575')};">
            {value}/{max_value} ({percentage:.1f}%)
        </div>
    </div>
    """

    card(progress_html, theme=theme)
