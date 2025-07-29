"""
Tests for Card component
"""

import pytest
from nb_ui.components.cards import Card


class TestCard:
    """Test suite for Card component"""

    def test_card_basic_creation(self):
        """Test basic card creation"""
        card = Card("Hello Card!")
        html = card.render()
        
        # Should contain the content
        assert "Hello Card!" in html
        assert "nb-component" in html
        assert "card-" in html
        
    def test_card_with_title(self):
        """Test card with title parameter"""  
        card = Card("Card content", title="My Title")
        html = card.render()
        
        # Should contain title
        assert "My Title" in html
        assert "Card content" in html
        
    def test_card_elevation_levels(self):
        """Test different card elevation levels"""
        for elevation in range(7):  # 0-6
            card = Card("Content", elevation=elevation)
            html = card.render()
            
            # Should contain card content
            assert "Content" in html
            
            if elevation > 0:
                # Should have box-shadow for elevation > 0
                # Note: actual shadow styling depends on theme
                assert "box-shadow:" in html, f"Card elevation {elevation} should have box-shadow"
            else:
                # Elevation 0 might not have box-shadow or have none
                pass
                
    def test_card_variants(self):
        """Test card variants"""
        # Elevation variant (default)
        elevation_card = Card("Content", variant="elevation", elevation=2)
        elevation_html = elevation_card.render()
        assert "box-shadow:" in elevation_html, "Elevation variant should have box-shadow"
        
        # Outlined variant
        outlined_card = Card("Content", variant="outlined")
        outlined_html = outlined_card.render()
        assert "border:" in outlined_html, "Outlined variant should have border"
        
    def test_card_square_borders(self):
        """Test card with square borders"""
        square_card = Card("Content", square=True)
        square_html = square_card.render()
        
        # Should have border-radius: 0 for square cards
        assert "border-radius: 0" in square_html, "Square card should have no border radius"
        
        # Regular card should have border radius
        regular_card = Card("Content", square=False)
        regular_html = regular_card.render()
        assert "border-radius: 0" not in regular_html, "Regular card should have border radius"

    def test_card_css_structure(self):
        """Test card CSS structure and classes"""
        card = Card("Test content")
        html = card.render()
        
        # Should have proper CSS structure
        css_properties = [
            "background-color:", "color:", "border:", "border-radius:",
            "box-shadow:", "transition:", "margin:"
        ]
        
        for prop in css_properties:
            assert prop in html, f"Card should have {prop} styling"
    
    def test_card_theming(self):
        """Test card with different themes"""
        themes = ['material', 'antd', 'dark']
        
        for theme in themes:
            card = Card("Themed content", theme=theme)
            html = card.render()
            
            # Should contain content and basic structure
            assert "Themed content" in html
            assert "nb-component" in html

    def test_multiple_cards(self):
        """Test multiple cards have unique IDs"""
        card1 = Card("Card 1")
        card2 = Card("Card 2")
        
        html1 = card1.render()
        html2 = card2.render()
        
        # Should have different component IDs
        assert card1.component_id != card2.component_id
        assert "Card 1" in html1
        assert "Card 2" in html2 