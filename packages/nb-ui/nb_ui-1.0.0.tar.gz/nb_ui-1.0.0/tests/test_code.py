"""
Tests for CodeBlock component
"""

import pytest
import re
from nb_ui.components.code import CodeBlock


class TestCodeBlock:
    """Test suite for CodeBlock component"""

    def test_code_block_basic_creation(self):
        """Test basic code block creation"""
        code = CodeBlock("print('Hello World')")
        html = code.render()
        
        # Should render non-empty HTML
        assert html.strip(), "CodeBlock should render non-empty HTML"
        
        # Should contain code content
        assert "print('Hello World')" in html, "CodeBlock should contain the code"
        
        # Should have nb-component class
        assert "nb-component" in html, "Should have nb-component class"
        
        # Should use pre/code elements
        assert "<pre" in html or "<code" in html, "CodeBlock should use pre or code element"

    def test_code_block_languages(self):
        """Test different programming languages"""
        languages = ['python', 'javascript', 'java', 'sql', 'bash', 'json', 'yaml', 'css', 'html']
        test_code = "var x = 1;"
        
        for language in languages:
            code_block = CodeBlock(test_code, language=language)
            html = code_block.render()
            
            # Should render successfully
            assert html.strip(), f"CodeBlock with language {language} should render"
            assert test_code in html, f"Should contain code for {language}"

    def test_code_block_line_numbers(self):
        """Test code block with line numbers"""
        multi_line_code = """def hello():
    print("Hello")
    return True"""
        
        # With line numbers
        with_lines = CodeBlock(multi_line_code, showLineNumbers=True)
        html_with = with_lines.render()
        
        # Should have line number indicators
        assert "1" in html_with, "Should show line number 1"
        assert "2" in html_with, "Should show line number 2"
        assert "3" in html_with, "Should show line number 3"
        
        # Without line numbers
        without_lines = CodeBlock(multi_line_code, showLineNumbers=False)
        html_without = without_lines.render()
        
        # Should contain code but structured differently
        assert "def hello():" in html_without, "Should contain code without line numbers"

    def test_code_block_syntax_highlighting(self):
        """Test syntax highlighting for different languages"""
        # Python code
        python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        python_block = CodeBlock(python_code, language='python')
        python_html = python_block.render()
        
        # Should have syntax highlighting styles
        assert "color:" in python_html, "Python code should have syntax highlighting"
        
        # JavaScript code
        js_code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
"""
        js_block = CodeBlock(js_code, language='javascript')
        js_html = js_block.render()
        
        # Should have syntax highlighting
        assert "color:" in js_html, "JavaScript code should have syntax highlighting"

    def test_code_block_themes(self):
        """Test code block with different themes"""
        code = "SELECT * FROM users;"
        
        # Test with light theme
        light_block = CodeBlock(code, language='sql', theme='light')
        light_html = light_block.render()
        
        # Test with dark theme
        dark_block = CodeBlock(code, language='sql', theme='dark')
        dark_html = dark_block.render()
        
        # Both should render
        assert light_html.strip(), "Light theme code block should render"
        assert dark_html.strip(), "Dark theme code block should render"
        
        # Should have different background colors
        assert "background" in light_html, "Light theme should have background"
        assert "background" in dark_html, "Dark theme should have background"

    def test_code_block_component_id_uniqueness(self):
        """Test unique component IDs"""
        code1 = CodeBlock("code 1")
        code2 = CodeBlock("code 2")
        
        html1 = code1.render()
        html2 = code2.render()
        
        # Extract component IDs
        id_pattern = r'codeblock-(\w+)'
        id1_match = re.search(id_pattern, html1)
        id2_match = re.search(id_pattern, html2)
        
        assert id1_match, "CodeBlock 1 should have component ID"
        assert id2_match, "CodeBlock 2 should have component ID"
        assert id1_match.group(1) != id2_match.group(1), "CodeBlock IDs should be unique"

    def test_code_block_css_structure(self):
        """Test code block CSS structure"""
        code_block = CodeBlock("test code")
        html = code_block.render()
        
        # Should have style tag
        assert "<style>" in html, "CodeBlock should include CSS styles"
        
        # Should have basic CSS properties
        css_properties = [
            "font-family:", "font-size:", "background:", 
            "padding:", "border-radius:", "overflow:"
        ]
        
        for prop in css_properties:
            assert prop in html, f"CodeBlock CSS should include {prop}"

    def test_code_block_long_code(self):
        """Test code block with long code"""
        long_code = "print('This is a very long line of code')\n" * 50
        code_block = CodeBlock(long_code, language='python')
        html = code_block.render()
        
        # Should render without issues
        assert html.strip(), "Should render long code"
        assert "overflow:" in html, "Should handle overflow for long code"

    def test_code_block_special_characters(self):
        """Test code block with special characters"""
        special_code = """
# Special characters: <>&"'
def test():
    return "Hello & <world>"
"""
        code_block = CodeBlock(special_code, language='python')
        html = code_block.render()
        
        # Should handle special characters safely
        assert html.strip(), "Should render code with special characters"


class TestCodeBlockIntegration:
    """Integration tests for CodeBlock component"""

    def test_code_blocks_in_cards(self):
        """Test code blocks in card components"""
        from nb_ui.components.cards import Card
        from nb_ui.components.typography import Typography
        
        title = Typography("Code Example", variant='h3')
        code = CodeBlock("print('Hello World')", language='python')
        
        card = Card([title, code])
        html = card.render()
        
        # Should contain both components
        assert "Code Example" in html, "Should contain title"
        assert "print('Hello World')" in html, "Should contain code"


# Parametrized tests
@pytest.mark.parametrize("language", [
    'python', 'javascript', 'java', 'sql', 'bash', 'json', 'yaml', 'css', 'html', 'xml'
])
def test_code_block_all_languages(language):
    """Test all supported languages"""
    code_block = CodeBlock("test code", language=language)
    html = code_block.render()
    
    # Should render without errors
    assert html.strip(), f"CodeBlock with language {language} should render"
    assert "test code" in html, "Should contain code content"


@pytest.mark.parametrize("show_lines", [True, False])
def test_code_block_line_number_options(show_lines):
    """Test line number options"""
    code = "line 1\nline 2\nline 3"
    code_block = CodeBlock(code, showLineNumbers=show_lines)
    html = code_block.render()
    
    # Should render successfully
    assert html.strip(), f"CodeBlock with showLineNumbers={show_lines} should render"
    assert "line 1" in html, "Should contain code content"


@pytest.mark.parametrize("language,show_lines", [
    ('python', True), ('python', False),
    ('javascript', True), ('javascript', False),
    ('sql', True), ('sql', False)
])
def test_code_block_language_line_combinations(language, show_lines):
    """Test combinations of language and line numbers"""
    code_block = CodeBlock("test code", language=language, showLineNumbers=show_lines)
    html = code_block.render()
    
    # Should render without errors
    assert html.strip(), f"CodeBlock with language={language}, showLineNumbers={show_lines} should render"
    assert "test code" in html, "Should contain code content"


class TestCodeBlockErrorHandling:
    """Test error handling and edge cases"""

    def test_code_block_empty_code(self):
        """Test code block with empty code"""
        code_block = CodeBlock("")
        html = code_block.render()
        
        # Should still render
        assert html.strip(), "CodeBlock with empty code should still render"

    def test_code_block_none_code(self):
        """Test code block with None/empty code"""
        code_block = CodeBlock("")
        html = code_block.render()
        
        # Should handle empty code gracefully
        assert html.strip(), "CodeBlock should handle empty code"

    def test_code_block_invalid_language(self):
        """Test code block with invalid language"""
        code_block = CodeBlock("test code", language='invalid')
        html = code_block.render()
        
        # Should fall back to default or plain text
        assert html.strip(), "CodeBlock should handle invalid language"
        assert "test code" in html, "Should contain code content"

    def test_code_block_very_long_lines(self):
        """Test code block with very long lines"""
        long_line = "x = " + "1 + " * 200 + "1"
        code_block = CodeBlock(long_line, language='python')
        html = code_block.render()
        
        # Should handle long lines
        assert html.strip(), "Should render code with long lines"
        assert "overflow:" in html, "Should have overflow handling"

    def test_code_block_many_lines(self):
        """Test code block with many lines"""
        many_lines = "\n".join([f"line_{i} = {i}" for i in range(100)])
        code_block = CodeBlock(many_lines, language='python', showLineNumbers=True)
        html = code_block.render()
        
        # Should render many lines
        assert html.strip(), "Should render code with many lines"
        assert "line_99 = 99" in html, "Should contain last line"

    def test_code_block_unicode_characters(self):
        """Test code block with unicode characters"""
        unicode_code = """
# Unicode test: 你好世界 🌍 🐍
def hello():
    print("Hello 世界! 🎉")
"""
        code_block = CodeBlock(unicode_code, language='python')
        html = code_block.render()
        
        # Should handle unicode
        assert html.strip(), "Should render code with unicode"
        assert "你好世界" in html, "Should contain unicode characters"
        assert "🌍" in html, "Should contain emoji" 