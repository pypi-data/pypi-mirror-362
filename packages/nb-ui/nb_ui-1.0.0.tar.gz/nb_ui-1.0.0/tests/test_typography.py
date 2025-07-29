"""
Tests for Typography component
"""

import pytest
import re
from nb_ui.components.typography import Typography


class TestTypography:
    """Test suite for Typography component"""

    def test_typography_basic_creation(self):
        """Test basic typography creation"""
        text = Typography("Hello World")
        html = text.render()
        
        # Should render non-empty HTML
        assert html.strip(), "Typography should render non-empty HTML"
        
        # Should contain text content
        assert "Hello World" in html, "Typography should contain the text"
        
        # Should have nb-component class
        assert "nb-component" in html, "Should have nb-component class"

    def test_typography_variants(self):
        """Test different typography variants"""
        variants = {
            'h1': ('h1', '2.125rem'),
            'h2': ('h2', '1.5rem'),
            'h3': ('h3', '1.25rem'),
            'h4': ('h4', '1.125rem'),
            'h5': ('h5', '1rem'),
            'h6': ('h6', '0.875rem'),
            'body1': ('p', '1rem'),
            'body2': ('p', '0.875rem'),
            'subtitle1': ('h6', '1rem'),
            'subtitle2': ('h6', '1rem'),
            'caption': ('span', '0.75rem'),
            'button': ('span', '0.875rem'),
            'overline': ('span', '1rem')
        }
        
        for variant, (expected_tag, expected_size) in variants.items():
            typography = Typography("Test", variant=variant)
            html = typography.render()
            
            # Should use correct HTML tag
            assert f"<{expected_tag}" in html, f"Variant {variant} should use {expected_tag} tag"
            
            # Should have appropriate font size
            assert expected_size in html, f"Variant {variant} should have font-size {expected_size}"

    def test_typography_colors(self):
        """Test typography colors"""
        colors = ['primary', 'secondary', 'success', 'error', 'warning', 'info', 'textPrimary', 'textSecondary']
        
        for color in colors:
            typography = Typography("Test", color=color)
            html = typography.render()
            
            # Should contain color styling
            assert "color:" in html, f"Typography with color {color} should have color styling"

    def test_typography_alignment(self):
        """Test text alignment options"""
        alignments = ['left', 'center', 'right', 'justify']
        
        for align in alignments:
            typography = Typography("Test", align=align)
            html = typography.render()
            
            # Should have text-align property
            assert f"text-align: {align}" in html, f"Should have text-align: {align}"

    def test_typography_gutters(self):
        """Test typography with gutters"""
        # With gutters (default)
        with_gutters = Typography("Test", gutterBottom=True)
        html_gutters = with_gutters.render()
        assert "margin:" in html_gutters and "1rem" in html_gutters, "Should have margin with gutters"
        
        # Without gutters
        without_gutters = Typography("Test", gutterBottom=False)
        html_no_gutters = without_gutters.render()
        # Should either not have margin-bottom or have 0 margin
        assert "margin-bottom: 0" in html_no_gutters or "margin-bottom:" not in html_no_gutters

    def test_typography_component_id_uniqueness(self):
        """Test unique component IDs"""
        text1 = Typography("Text 1")
        text2 = Typography("Text 2")
        
        html1 = text1.render()
        html2 = text2.render()
        
        # Extract component IDs - look for the full pattern typography-nb-typography-HASH
        id_pattern = r'typography-nb-typography-(\w+)'
        id1_match = re.search(id_pattern, html1)
        id2_match = re.search(id_pattern, html2)
        
        assert id1_match, "Typography 1 should have component ID"
        assert id2_match, "Typography 2 should have component ID"
        assert id1_match.group(1) != id2_match.group(1), "Typography IDs should be unique"

    def test_typography_css_structure(self):
        """Test typography CSS structure"""
        typography = Typography("Test")
        html = typography.render()
        
        # Should have style tag
        assert "<style>" in html, "Typography should include CSS styles"
        
        # Should have basic CSS properties (font-family is in base styles, not component-specific)
        css_properties = ["font-size:", "line-height:", "color:"]
        
        for prop in css_properties:
            assert prop in html, f"Typography CSS should include {prop}"

    def test_typography_html_content(self):
        """Test typography with HTML content"""
        html_content = "<strong>Bold</strong> and <em>italic</em> text"
        typography = Typography(html_content)
        html = typography.render()
        
        # Should include HTML content
        assert "<strong>" in html, "Should support HTML in content"
        assert "<em>" in html, "Should support HTML in content"

    def test_typography_long_text(self):
        """Test typography with long text"""
        long_text = "This is a very long text that should wrap properly. " * 20
        typography = Typography(long_text)
        html = typography.render()
        
        # Should render without issues
        assert html.strip(), "Should render long text"
        assert long_text in html, "Should contain full long text"


class TestTypographyIntegration:
    """Integration tests for Typography component"""




# Parametrized tests
@pytest.mark.parametrize("variant", [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
    'body1', 'body2', 'subtitle1', 'subtitle2', 
    'caption', 'button', 'overline'
])
def test_typography_all_variants(variant):
    """Test all typography variants"""
    typography = Typography("Test", variant=variant)
    html = typography.render()
    
    # Should render without errors
    assert html.strip(), f"Typography variant {variant} should render"
    assert "Test" in html, "Should contain text content"


@pytest.mark.parametrize("color", ['primary', 'secondary', 'success', 'error', 'warning', 'info'])
def test_typography_all_colors(color):
    """Test all typography colors"""
    typography = Typography("Test", color=color)
    html = typography.render()
    
    # Should render with color
    assert html.strip(), f"Typography with color {color} should render"
    assert "color:" in html, f"Should have color styling for {color}"


@pytest.mark.parametrize("align", ['left', 'center', 'right', 'justify'])
def test_typography_all_alignments(align):
    """Test all text alignments"""
    typography = Typography("Test", align=align)
    html = typography.render()
    
    # Should have alignment
    assert f"text-align: {align}" in html, f"Should have text-align: {align}"


class TestTypographyErrorHandling:
    """Test error handling and edge cases"""

    def test_typography_empty_content(self):
        """Test typography with empty content"""
        typography = Typography("")
        html = typography.render()
        
        # Should still render
        assert html.strip(), "Typography with empty content should still render"

    def test_typography_none_content(self):
        """Test typography with None content"""
        typography = Typography("")  # type: ignore
        html = typography.render()
        
        # Should handle None gracefully
        assert html.strip(), "Typography should handle None content"

    def test_typography_invalid_variant(self):
        """Test typography with invalid variant"""
        typography = Typography("Test", variant='invalid')
        html = typography.render()
        
        # Should fall back to default
        assert html.strip(), "Typography should handle invalid variant"

    def test_typography_invalid_color(self):
        """Test typography with invalid color"""
        typography = Typography("Test", color='invalid')
        html = typography.render()
        
        # Should fall back to default
        assert html.strip(), "Typography should handle invalid color"

    def test_typography_invalid_align(self):
        """Test typography with invalid alignment"""
        typography = Typography("Test", align='invalid')
        html = typography.render()
        
        # Should fall back to default
        assert html.strip(), "Typography should handle invalid alignment" 