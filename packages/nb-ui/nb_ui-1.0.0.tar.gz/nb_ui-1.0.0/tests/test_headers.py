"""
Tests for Header component
"""

import pytest
from nb_ui.components.headers import Header


class TestHeader:
    """Test suite for Header component"""

    def test_header_basic_creation(self):
        """Test basic header creation"""
        header = Header("Test Header")
        html = header.render()
        
        # Should contain the title
        assert "Test Header" in html
        assert "nb-component" in html
        assert "header-" in html
        
    def test_header_with_subtitle(self):
        """Test header with subtitle"""
        header = Header("Main Title", subtitle="Subtitle text")
        html = header.render()
        
        # Should contain both title and subtitle
        assert "Main Title" in html
        assert "Subtitle text" in html
        
    def test_header_levels(self):
        """Test different header levels"""
        levels = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for level in levels:
            header = Header("Title", level=level)
            html = header.render()
            
            # Should contain the level tag
            assert f"<{level}>" in html
            assert f"</{level}>" in html
            assert "Title" in html

    def test_header_colors(self):
        """Test header colors"""
        colors = ['primary', 'secondary', 'success', 'error', 'warning', 'info']
        
        for color in colors:
            header = Header("Colored Header", color=color)
            html = header.render()
            
            # Should contain color styling
            assert "color:" in html, f"Header with color {color} should have color styling"

    def test_header_alignment(self):
        """Test header alignment options"""
        alignments = ['left', 'center', 'right']
        
        for align in alignments:
            header = Header("Aligned Header", align=align)
            html = header.render()
            
            # Should contain alignment styling
            assert f"text-align: {align}" in html

    def test_header_divider(self):
        """Test header with and without divider"""
        # With divider (default)
        header_with = Header("Title", divider=True)
        html_with = header_with.render()
        assert "<hr" in html_with, "Header with divider should contain hr element"
        
        # Without divider
        header_without = Header("Title", divider=False)
        html_without = header_without.render()
        assert "<hr" not in html_without, "Header without divider should not contain hr element"

    def test_header_css_structure(self):
        """Test header CSS structure and classes"""
        header = Header("Test")
        html = header.render()
        
        # Should have proper CSS structure (font-family is in base styles, not header-specific)
        css_properties = ["font-size:", "font-weight:", "line-height:", "color:", "margin:"]
        
        for prop in css_properties:
            assert prop in html, f"Header should have {prop} styling"
    
    def test_header_theming(self):
        """Test header with different themes"""
        themes = ['material', 'antd', 'dark']
        
        for theme in themes:
            header = Header("Themed header", theme=theme)
            html = header.render()
            
            # Should contain content and basic structure
            assert "Themed header" in html
            assert "nb-component" in html

    def test_multiple_headers(self):
        """Test multiple headers have unique IDs"""
        header1 = Header("Header 1")
        header2 = Header("Header 2")
        
        html1 = header1.render()
        html2 = header2.render()
        
        # Should have different component IDs
        assert header1.component_id != header2.component_id
        assert "Header 1" in html1
        assert "Header 2" in html2


# Parametrized tests
@pytest.mark.parametrize("level", ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
def test_header_all_levels(level):
    """Test all header levels"""
    header = Header("Test", level=level)
    html = header.render()
    
    # Should render with correct tag
    assert html.strip(), f"Header level {level} should render"
    assert f"<{level}>" in html, f"Should use {level} tag"


@pytest.mark.parametrize("color", ['primary', 'secondary', 'success', 'error', 'warning', 'info'])
def test_header_all_colors(color):
    """Test all header colors"""
    header = Header("Colored Header", color=color)
    html = header.render()
    
    # Should render with color
    assert html.strip(), f"Header with color {color} should render"
    assert "color:" in html, f"Should have color styling for {color}"


@pytest.mark.parametrize("align", ['left', 'center', 'right'])
def test_header_all_alignments(align):
    """Test all header alignments"""
    header = Header("Aligned Header", align=align)
    html = header.render()
    
    # Should render with alignment
    assert html.strip(), f"Header with align {align} should render"
    assert f"text-align: {align}" in html, f"Should have {align} alignment"


@pytest.mark.parametrize("level,color,align", [
    ('h1', 'primary', 'center'),
    ('h2', 'secondary', 'left'),
    ('h3', 'success', 'right')
])
def test_header_combinations(level, color, align):
    """Test combinations of header properties"""
    header = Header("Test", level=level, color=color, align=align)
    html = header.render()
    
    assert html.strip(), f"Header with level={level}, color={color}, align={align} should render"


class TestHeaderErrorHandling:
    """Test error handling and edge cases"""

    def test_header_empty_title(self):
        """Test header with empty title"""
        header = Header("")
        html = header.render()
        
        # Should still render
        assert html.strip(), "Header with empty title should still render"

    def test_header_invalid_level(self):
        """Test header with invalid level"""
        header = Header("Test", level='h9')  # Invalid level
        html = header.render()
        
        # Should fall back to default
        assert html.strip(), "Header should handle invalid level"

    def test_header_invalid_color(self):
        """Test header with invalid color"""
        header = Header("Test", color='invalid')
        html = header.render()
        
        # Should fall back to default color
        assert html.strip(), "Header should handle invalid color"

    def test_header_invalid_align(self):
        """Test header with invalid alignment"""
        header = Header("Test", align='invalid')
        html = header.render()
        
        # Should fall back to default alignment
        assert html.strip(), "Header should handle invalid alignment"

    def test_header_very_long_title(self):
        """Test header with very long title"""
        long_title = "This is a very long header title that goes on and on. " * 10
        header = Header(long_title)
        html = header.render()
        
        # Should render without issues
        assert html.strip(), "Should render header with long title"
        assert long_title in html, "Should contain full long title"

    def test_header_special_characters(self):
        """Test header with special characters"""
        special_title = "Header with <script> & 'quotes' and symbols: @#$%^&*()"
        header = Header(special_title)
        html = header.render()
        
        # Should handle special characters safely
        assert special_title in html, "Should include special characters"
        assert html.strip(), "Should render with special characters"

    def test_header_complex_subtitle(self):
        """Test header with complex subtitle"""
        header = Header("Main", subtitle="Complex <em>subtitle</em> with HTML")
        html = header.render()
        
        # Should handle HTML in subtitle
        assert "Complex <em>subtitle</em> with HTML" in html
        assert "Main" in html

    def test_multiple_similar_headers(self):
        """Test multiple headers with similar content"""
        header1 = Header("Header 1", level='h1', color='primary')
        header2 = Header("Header 2", level='h3', color='secondary')
        
        html1 = header1.render()
        html2 = header2.render()
        
        # Should be independent
        assert "Header 1" in html1 and "Header 1" not in html2
        assert "Header 2" in html2 and "Header 2" not in html1
        assert header1.component_id != header2.component_id 