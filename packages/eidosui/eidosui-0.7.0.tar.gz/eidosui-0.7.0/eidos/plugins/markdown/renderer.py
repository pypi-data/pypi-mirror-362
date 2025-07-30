"""Core markdown rendering with theme integration"""

import markdown

from .extensions.alerts import AlertExtension


class MarkdownRenderer:
    """Core markdown rendering with theme integration"""

    def __init__(self, extensions: list[str | markdown.Extension] | None = None):
        """Initialize the renderer with optional extensions.

        Args:
            extensions: List of markdown extension names or instances to enable
        """
        self.extensions = extensions or []
        # Add some useful default extensions
        default_extensions = [
            "fenced_code",
            "tables",
            "nl2br",
            "sane_lists",
            AlertExtension(),  # GitHub-style alerts
        ]
        self.extensions.extend(default_extensions)

        self.md = markdown.Markdown(extensions=self.extensions)

    def render(self, markdown_text: str) -> str:
        """Convert markdown to themed HTML.

        Args:
            markdown_text: Raw markdown text to render

        Returns:
            HTML string wrapped with eidos-md class for styling
        """
        self.md.reset()  # TODO: this is a hack to clear the state of the markdown processor

        html_content = self.md.convert(markdown_text)

        return f'<div class="eidos-md">{html_content}</div>'

    def add_extension(self, extension: str) -> None:
        """Add a markdown extension.

        Args:
            extension: Name of the markdown extension to add
        """
        if extension not in self.extensions:
            self.extensions.append(extension)
            self.md = markdown.Markdown(extensions=self.extensions)
