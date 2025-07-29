"""Module for parsing HTML files and extracting structured information.

Copyright (c) 2024 Neil Schneider
"""

from pathlib import Path
from typing import ClassVar

from bs4 import BeautifulSoup

from slimcontext.parsers.baseparser import BaseFileParser
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class HtmlParser(BaseFileParser):
    """Parses HTML files and extracts structured information."""

    # Define the extensions this parser can handle
    extensions: ClassVar[list[str]] = ['.html', '.htm']

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize the HtmlParser instance.

        Args:
            root_dir (Path, optional): The git repo's root directory. Defaults to None.
        """
        parser_extensions = self.extensions
        super().__init__(extensions=parser_extensions, root_dir=root_dir)

    def generate_slim_context(self, source: str, file_path: Path) -> str:
        """Generate a slim textual context from the HTML content.

        Args:
            source (str): The raw HTML content of the file.
            file_path (Path): The path to the HTML file.

        Returns:
            str: A slimmed-down representation of the HTML content.
        """
        soup = BeautifulSoup(source, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_content = meta_desc['content'] if meta_desc else 'No Description'

        context_lines = self.context_header(file_path=file_path)
        context_lines.append(f'Title: {title}')
        context_lines.append(f'Meta Description: {meta_desc_content}')

        logger.debug('Generated slim context for HTML.')
        return '\n'.join(context_lines)

    def generate_full_context(self, source: str, file_path: Path) -> str:
        """Return the entire content of an HTML file.

        Args:
            source (str): The raw HTML content of the file.
            file_path (Path): The path to the HTML file.

        Returns:
            str: Full text content of the HTML file.
        """
        context_lines = self.context_header(file_path=file_path)
        context_lines.append(source)
        return '\n'.join(context_lines)
