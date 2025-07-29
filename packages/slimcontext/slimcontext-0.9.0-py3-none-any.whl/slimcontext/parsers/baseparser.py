"""This module provides the BaseFileParser class for extracting and formatting textual context.

Subclasses should override the slim/full context methods to provide file-type-specific logic.

Copyright (c) 2024 Neil Schneider
"""

from pathlib import Path

from slimcontext.parsers.utils import generate_context_header
from slimcontext.utils.gitrepo_tools import GitRepository
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseFileParser:
    """Base class for extracting and formatting textual context from files.

    Subclasses should override the slim/full context methods to provide
    file-type-specific logic (e.g. AST parsing for Python, or DOM parsing for HTML).
    """

    def __init__(self, extensions: list[str], root_dir: Path | None = None) -> None:
        """Initialize the parser with an optional root directory."""
        if not root_dir:
            try:
                git_root: Path | None = GitRepository().root
            except ValueError:
                git_root = None
        self.root_dir = root_dir or git_root or Path.cwd()
        self.extensions = extensions

    def context_header(self, file_path: Path) -> list[str]:
        """Generate a standard header that includes the relative or absolute path.

        Returns:
            list[str]: A list containing the header lines.
        """
        return generate_context_header(file_path, self.root_dir)

    def context_body(self, source: str, file_path: Path) -> list[str]:
        """Extract comprehensive information from a Python source file using AST.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            list[str]: A list of all the context from the module.
        """

    def generate_slim_context(self, source: str, file_path: Path) -> str:
        """Return a 'slim' textual context for the file.

        Subclasses should override this for specialized logic (e.g. AST).
        """
        # Fallback: Just read lines and limit them or do minimal extraction
        # This is a placeholder for demonstration
        header = self.context_header(file_path)
        return '\n'.join([*header, source])

    def generate_full_context(self, source: str, file_path: Path) -> str:
        """Return the entire content of a file plus the header.

        Subclasses can override for any advanced "full" logic if needed.
        """
        header = self.context_header(file_path)
        return '\n'.join([*header, source])

    def generate_context(self, file_path: Path, *, full_text: bool = False) -> str:
        """High-level method to read the file and produce either full or slim context.

        Args:
            file_path (Path): The path to the Python source file.
            full_text (bool, optional): Whether to return the full text of the file.
                Defaults to False.

        Returns:
            str: A string representation of the repository context.
        """
        try:
            with file_path.open('r', encoding='utf-8') as file:
                source = file.read()
        except (OSError, FileNotFoundError, PermissionError, UnicodeDecodeError):
            logger.exception('Error reading from %s. Will not be included in context.', file_path)
            header = self.context_header(file_path)
            header_str = '\n'.join([*header])
            return f'{header_str}[Error reading file]\n'

        if full_text:
            return self.generate_full_context(source=source, file_path=file_path)
        return self.generate_slim_context(source=source, file_path=file_path)
