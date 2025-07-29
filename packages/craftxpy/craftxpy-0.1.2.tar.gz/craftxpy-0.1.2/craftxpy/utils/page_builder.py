"""CraftX.py Page Builder Module

HTML page building utilities for web interfaces.
"""

from typing import Dict, List, Optional

class PageBuilder:
    """HTML page builder for creating web interfaces."""
    
    def __init__(self, title: str = "CraftX.py"):
        """Initialize the page builder.
        
        Args:
            title: Page title
        """
        self.title = title
        self.head_content: List[str] = []
        self.body_content: List[str] = []
        self.css_styles: List[str] = []
        self.js_scripts: List[str] = []
    
    def add_css(self, css: str) -> None:
        """Add CSS styles.
        
        Args:
            css: CSS content
        """
        self.css_styles.append(css)
    
    def add_js(self, js: str) -> None:
        """Add JavaScript.
        
        Args:
            js: JavaScript content
        """
        self.js_scripts.append(js)
    
    def add_content(self, content: str) -> None:
        """Add body content.
        
        Args:
            content: HTML content
        """
        self.body_content.append(content)
    
    def build(self) -> str:
        """Build the complete HTML page.
        
        Returns:
            Complete HTML page as string
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"    <title>{self.title}</title>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        ]
        
        # Add CSS
        if self.css_styles:
            html_parts.append("    <style>")
            html_parts.extend(f"        {css}" for css in self.css_styles)
            html_parts.append("    </style>")
        
        html_parts.extend([
            "</head>",
            "<body>",
        ])
        
        # Add body content
        html_parts.extend(f"    {content}" for content in self.body_content)
        
        # Add JavaScript
        if self.js_scripts:
            html_parts.append("    <script>")
            html_parts.extend(f"        {js}" for js in self.js_scripts)
            html_parts.append("    </script>")
        
        html_parts.extend([
            "</body>",
            "</html>"
        ])
        
        return "\n".join(html_parts)
