"""
CodeBlock Component
Code display component with syntax highlighting and line numbers
"""

from typing import Optional
from .base import ComponentBase


class CodeBlock(ComponentBase):
    """Code block component with syntax highlighting theme"""

    def __init__(
        self,
        code: str,
        language: str = "python",
        showLineNumbers: bool = False,
        theme: Optional[str] = None,
        **props,
    ):
        super().__init__(theme, **props)
        self.code = code
        self.language = language
        self.showLineNumbers = showLineNumbers

    def render(self) -> str:
        line_numbers = ""
        if self.showLineNumbers:
            lines = self.code.split("\n")
            line_numbers = "\n".join(str(i + 1) for i in range(len(lines)))
            line_numbers_html = f"""
            <div style="background: #f8f9fa; 
                       border-right: 1px solid #e9ecef;
                       color: #6c757d;
                       padding: {self._get_spacing('md')};
                       text-align: right;
                       user-select: none;
                       font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
                       font-size: 0.875rem;
                       line-height: 1.5;
                       white-space: pre;">
                {line_numbers}
            </div>
            """
        else:
            line_numbers_html = ""

        return f"""
        <style>
            .code-block-{self.component_id} {{
                display: flex;
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: {self._get_border('radius')};
                margin: {self._get_spacing('md')} 0;
                overflow-x: auto;
                box-shadow: {self._get_shadow('sm')};
            }}
            
            .code-block-{self.component_id} pre {{
                flex: 1;
                margin: 0;
                padding: {self._get_spacing('md')};
                background: transparent;
                color: #212529;
                font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
                font-size: 0.875rem;
                line-height: 1.5;
                overflow: visible;
            }}
        </style>
        <div class="nb-component code-block-{self.component_id}">
            {line_numbers_html}
            <pre><code>{self.code}</code></pre>
        </div>
        """
