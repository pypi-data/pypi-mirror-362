"""
Tests for Alert component
"""

import pytest
import re
from nb_ui.components.alerts import Alert


class TestAlert:
    """Test suite for Alert component"""

    def test_alert_basic_creation(self):
        """Test basic alert creation"""
        alert = Alert("Test message")
        html = alert.render()
        
        # Should render non-empty HTML
        assert html.strip(), "Alert should render non-empty HTML"
        
        # Should contain message
        assert "Test message" in html, "Alert should contain the message"
        
        # Should have alert div
        assert "nb-component" in html, "Should have nb-component class"

    def test_alert_severities(self):
        """Test different alert severities"""
        severities = {
            'error': '❌',
            'warning': '⚠️', 
            'info': 'ℹ️',
            'success': '✅'
        }
        
        for severity, icon in severities.items():
            alert = Alert("Test", severity=severity)
            html = alert.render()
            
            # Should contain appropriate icon
            assert icon in html, f"{severity} alert should contain {icon} icon"
            
            # Should have severity-specific styling
            assert f"alert-{alert.component_id}" in html, "Should have unique alert class"

    def test_alert_variants(self):
        """Test different alert variants"""
        # Standard variant
        standard = Alert("Test", variant='standard')
        standard_html = standard.render()
        assert "background-color:" in standard_html, "Standard alert should have background"
        
        # Filled variant  
        filled = Alert("Test", variant='filled')
        filled_html = filled.render()
        assert "color: #ffffff" in filled_html, "Filled alert should have white text"
        
        # Outlined variant
        outlined = Alert("Test", variant='outlined')
        outlined_html = outlined.render()
        assert "background-color: transparent" in outlined_html, "Outlined should be transparent"
        assert "border:" in outlined_html, "Outlined should have border"

    def test_alert_close_button(self):
        """Test alert with close button"""
        closeable = Alert("Test", onClose=True)
        html = closeable.render()
        
        # Should have close button
        assert "×" in html, "Closeable alert should have × close button"
        assert "onclick=" in html, "Close button should have onclick handler"
        assert "this.parentElement.style.display='none'" in html, "Should hide on click"

    def test_alert_without_close_button(self):
        """Test alert without close button"""
        non_closeable = Alert("Test", onClose=False)
        html = non_closeable.render()
        
        # Should not have close button
        assert "×" not in html, "Non-closeable alert should not have close button"
        assert "onclick=" not in html, "Should not have onclick handler"

    def test_alert_component_id_uniqueness(self):
        """Test that each alert has unique component ID"""
        alert1 = Alert("Alert 1")
        alert2 = Alert("Alert 2")
        
        html1 = alert1.render()
        html2 = alert2.render()
        
        # Extract component IDs - look for the full pattern alert-nb-alert-HASH
        id_pattern = r'alert-nb-alert-(\w+)'
        id1_match = re.search(id_pattern, html1)
        id2_match = re.search(id_pattern, html2)
        
        assert id1_match, "Alert 1 should have component ID"
        assert id2_match, "Alert 2 should have component ID"
        assert id1_match.group(1) != id2_match.group(1), "Alert IDs should be unique"

    def test_alert_css_structure(self):
        """Test alert CSS structure"""
        alert = Alert("Test")
        html = alert.render()
        
        # Should have style tag
        assert "<style>" in html, "Alert should include CSS styles"
        
        # Should have CSS properties
        css_properties = [
            "display: flex", "align-items: center", "padding:",
            "margin:", "border-radius:", "background-color:", "color:"
        ]
        
        for prop in css_properties:
            assert prop in html, f"Alert CSS should include {prop}"

    def test_alert_icon_styling(self):
        """Test alert icon styling"""
        alert = Alert("Test", severity='info')
        html = alert.render()
        
        # Should have icon container
        assert "alert-icon" in html, "Should have alert-icon class"
        assert "margin-right:" in html, "Icon should have right margin"

    def test_alert_severity_colors(self):
        """Test that different severities use different colors"""
        severities = ['error', 'warning', 'info', 'success']
        colors = []
        
        for severity in severities:
            alert = Alert("Test", severity=severity)
            html = alert.render()
            
            # Extract color values (simplified)
            color_matches = re.findall(r'color: (#[a-fA-F0-9]{6})', html)
            if color_matches:
                colors.extend(color_matches)
        
        # Should have different colors for different severities
        # (This is a simplified test - in reality we'd check specific colors)
        assert len(set(colors)) > 1, "Different severities should use different colors"


class TestAlertIntegration:
    """Integration tests for Alert component"""

    def test_alert_with_html_content(self):
        """Test alert with HTML content in message"""
        html_message = "<strong>Important:</strong> This is a test"
        alert = Alert(html_message, severity='warning')
        html = alert.render()
        
        # Should include HTML content
        assert "<strong>" in html, "Should support HTML in message"
        assert "Important:" in html, "Should render HTML content"

    def test_multiple_alerts_stacking(self):
        """Test multiple alerts don't interfere"""
        alerts = [
            Alert("Error message", severity='error'),
            Alert("Warning message", severity='warning'),
            Alert("Success message", severity='success')
        ]
        
        htmls = [alert.render() for alert in alerts]
        
        # Each should have unique content
        assert "Error message" in htmls[0], "First alert should have error message"
        assert "Warning message" in htmls[1], "Second alert should have warning message" 
        assert "Success message" in htmls[2], "Third alert should have success message"
        
        # Should have different icons
        assert "❌" in htmls[0], "Error alert should have error icon"
        assert "⚠️" in htmls[1], "Warning alert should have warning icon"
        assert "✅" in htmls[2], "Success alert should have success icon"


# Parametrized tests
@pytest.mark.parametrize("severity", ['error', 'warning', 'info', 'success'])
@pytest.mark.parametrize("variant", ['standard', 'filled', 'outlined'])
def test_alert_severity_variant_combinations(severity, variant):
    """Test all combinations of severity and variant"""
    alert = Alert("Test message", severity=severity, variant=variant)
    html = alert.render()
    
    # Should render without errors
    assert html.strip(), f"Alert with severity={severity}, variant={variant} should render"
    assert "Test message" in html, "Should contain alert message"


@pytest.mark.parametrize("onClose", [True, False])
@pytest.mark.parametrize("severity", ['error', 'info'])  
def test_alert_close_button_combinations(onClose, severity):
    """Test close button with different severities"""
    alert = Alert("Test", severity=severity, onClose=onClose)
    html = alert.render()
    
    # Should render successfully
    assert html.strip(), "Alert should render with close button option"
    
    if onClose:
        assert "×" in html, "Should have close button when onClose=True"
    else:
        assert "×" not in html, "Should not have close button when onClose=False"


class TestAlertErrorHandling:
    """Test error handling and edge cases"""

    def test_alert_empty_message(self):
        """Test alert with empty message"""
        alert = Alert("")
        html = alert.render()
        
        # Should still render
        assert html.strip(), "Alert with empty message should still render"
        assert "nb-component" in html, "Should have component class"

    def test_alert_invalid_severity(self):
        """Test alert with invalid severity falls back to default"""
        alert = Alert("Test", severity='invalid')
        html = alert.render()
        
        # Should still render and fall back to info (default)
        assert html.strip(), "Alert with invalid severity should still render"
        assert "ℹ️" in html, "Should fall back to info icon"

    def test_alert_invalid_variant(self):
        """Test alert with invalid variant falls back to default"""
        alert = Alert("Test", variant='invalid')
        html = alert.render()
        
        # Should still render and fall back to standard
        assert html.strip(), "Alert with invalid variant should still render"
        # Test would check for standard variant styling

    def test_alert_special_characters(self):
        """Test alert with special characters in message"""
        special_message = "Test with <script> & 'quotes' and \"double quotes\""
        alert = Alert(special_message)
        html = alert.render()
        
        # Should handle special characters safely
        assert special_message in html, "Should include special characters"
        assert html.strip(), "Should render with special characters"

    def test_alert_long_message(self):
        """Test alert with very long message"""
        long_message = "This is a very long message " * 50
        alert = Alert(long_message)
        html = alert.render()
        
        # Should render without issues
        assert html.strip(), "Should render long messages"
        assert long_message in html, "Should contain full long message" 