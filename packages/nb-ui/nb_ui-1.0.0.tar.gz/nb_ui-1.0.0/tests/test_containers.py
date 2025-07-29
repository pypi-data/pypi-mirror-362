"""
Tests for Container component
"""

import pytest
import re
from nb_ui.components.containers import Container


class TestContainer:
    """Test suite for Container component"""

    def test_container_basic_creation(self):
        """Test basic container creation"""
        container = Container()
        html = container.render()
        
        # Should render non-empty HTML
        assert html.strip(), "Container should render non-empty HTML"
        
        # Should have nb-component class
        assert "nb-component" in html, "Should have nb-component class"
        
        # Should use div element
        assert "<div" in html, "Container should render as div"

    def test_container_sizes(self):
        """Test different container sizes"""
        sizes = {
            'xs': '444px',
            'sm': '600px',
            'md': '960px',
            'lg': '1280px',
            'xl': '1920px'
        }
        
        for size, expected_width in sizes.items():
            container = Container(maxWidth=size)
            html = container.render()
            
            # Should have correct max-width
            assert f"max-width: {expected_width}" in html, f"Container size {size} should have max-width {expected_width}"

    def test_container_centering(self):
        """Test container centering"""
        container = Container()
        html = container.render()
        
        # Should be centered with auto margins
        assert "margin: 0 auto" in html, "Container should be centered with auto margins"

    def test_container_with_content(self):
        """Test container with content"""
        container = Container("Container content")
        html = container.render()
        
        # Should contain content
        assert "Container content" in html, "Container should contain the content"

    def test_container_component_id_uniqueness(self):
        """Test unique component IDs"""
        container1 = Container()
        container2 = Container()
        
        html1 = container1.render()
        html2 = container2.render()
        
        # Extract component IDs - look for the full pattern container-nb-container-HASH
        id_pattern = r'container-nb-container-(\w+)'
        id1_match = re.search(id_pattern, html1)
        id2_match = re.search(id_pattern, html2)
        
        assert id1_match, "Container 1 should have component ID"
        assert id2_match, "Container 2 should have component ID"
        assert id1_match.group(1) != id2_match.group(1), "Container IDs should be unique"

    def test_container_css_structure(self):
        """Test container CSS structure"""
        container = Container()
        html = container.render()
        
        # Should have style tag
        assert "<style>" in html, "Container should include CSS styles"
        
        # Should have basic CSS properties
        css_properties = ["max-width:", "margin:", "padding:"]
        
        for prop in css_properties:
            assert prop in html, f"Container CSS should include {prop}"

    def test_container_responsive_behavior(self):
        """Test container responsive behavior"""
        container = Container(maxWidth='lg')
        html = container.render()
        
        # Should have responsive padding
        assert "padding:" in html, "Container should have responsive padding"
        
        # Should be responsive on smaller screens
        assert "width: 100%" in html, "Container should be full width on small screens"


class TestContainerIntegration:
    """Integration tests for Container component"""

    def test_nested_containers(self):
        """Test nested containers"""
        inner_container = Container("Inner content", maxWidth='sm')
        outer_container = Container([inner_container], maxWidth='lg')
        html = outer_container.render()
        
        # Should handle nested containers
        assert "Inner content" in html, "Should contain inner container content"
        assert "max-width: 1280px" in html, "Should have outer container width"
        assert "max-width: 600px" in html, "Should have inner container width"


# Parametrized tests
@pytest.mark.parametrize("size", ['xs', 'sm', 'md', 'lg', 'xl'])
def test_container_all_sizes(size):
    """Test all container sizes"""
    container = Container(maxWidth=size)
    html = container.render()
    
    # Should render without errors
    assert html.strip(), f"Container size {size} should render"


@pytest.mark.parametrize("size,expected_width", [
    ('xs', '444px'), ('sm', '600px'), ('md', '960px'),
    ('lg', '1280px'), ('xl', '1920px')
])
def test_container_size_widths(size, expected_width):
    """Test container sizes have correct widths"""
    container = Container(maxWidth=size)
    html = container.render()
    
    # Should have correct max-width
    assert f"max-width: {expected_width}" in html, f"Container {size} should have max-width {expected_width}"


class TestContainerErrorHandling:
    """Test error handling and edge cases"""

    def test_container_invalid_size(self):
        """Test container with invalid size"""
        container = Container(maxWidth='invalid')
        html = container.render()
        
        # Should fall back to default size
        assert html.strip(), "Container should handle invalid size"
        assert "max-width:" in html, "Should have some max-width value"

    def test_container_empty_content(self):
        """Test container with empty content"""
        container = Container("")
        html = container.render()
        
        # Should still render
        assert html.strip(), "Container with empty content should still render"

    def test_container_none_content(self):
        """Test container with None content"""
        container = Container(None)
        html = container.render()
        
        # Should handle None gracefully
        assert html.strip(), "Container should handle None content"

    def test_container_with_children_list(self):
        """Test container with list of children"""
        from nb_ui.components.typography import Typography
        
        children = [
            Typography("First item"),
            Typography("Second item"),
            Typography("Third item")
        ]
        
        container = Container(children, maxWidth='md')
        html = container.render()
        
        # Should contain all children
        assert "First item" in html, "Should contain first item"
        assert "Second item" in html, "Should contain second item"
        assert "Third item" in html, "Should contain third item"

    def test_multiple_containers_styling_isolation(self):
        """Test that multiple containers don't interfere"""
        container1 = Container("Content 1", maxWidth='xs')
        container2 = Container("Content 2", maxWidth='lg')
        container3 = Container("Content 3", maxWidth='xl')
        
        htmls = [container.render() for container in [container1, container2, container3]]
        
        # Each should have unique styling
        for i, html in enumerate(htmls):
            assert html.strip(), f"Container {i + 1} should render"
            assert f"Content {i + 1}" in html, f"Should contain content {i + 1}"
        
        # Should have different max-widths
        assert "max-width: 444px" in htmls[0], "First container should be xs size"
        assert "max-width: 1280px" in htmls[1], "Second container should be lg size"
        assert "max-width: 1920px" in htmls[2], "Third container should be xl size"

    def test_container_responsive_padding(self):
        """Test container responsive padding"""
        container = Container("Test content")
        html = container.render()
        
        # Should have responsive padding for mobile
        assert "@media" in html or "padding:" in html, "Should have responsive padding" 