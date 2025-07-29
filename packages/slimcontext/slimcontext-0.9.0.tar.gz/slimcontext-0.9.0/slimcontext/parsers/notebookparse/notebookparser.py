"""Module for parsing Jupyter Notebook files and extracting structured information.

Copyright (c) 2024 Neil Schneider
"""

from pathlib import Path
from typing import ClassVar

import nbformat
from nbformat.reader import NotJSONError

from slimcontext.parsers.baseparser import BaseFileParser
from slimcontext.parsers.pyparse.pyparser import PyParser
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotebookParser(BaseFileParser):
    """Parses Jupyter Notebook files and extracts structured information."""

    extensions: ClassVar[list[str]] = ['.ipynb']

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize the NotebookParser instance.

        Args:
            root_dir (Path, optional): The repository's root directory. Defaults to None.
        """
        super().__init__(extensions=self.extensions, root_dir=root_dir)

        # Initialize sub-parsers for different languages
        self.parsers: dict[str, BaseFileParser] = {
            'python': PyParser(root_dir=self.root_dir),
            # Add other parsers here, e.g., 'r': RParser(root_dir=self.root_dir),
        }

    def context_body(self, source: str, file_path: Path) -> list[str]:
        """Extract comprehensive information from a Jupyter Notebook using nbformat.

        Args:
            source (str): The raw text of the notebook file.
            file_path (Path): The path to the notebook file.

        Returns:
            list[str]: A list of all the context extracted from the notebook.
        """
        nb = self._read_notebook(source, file_path)
        if not nb:
            return []

        context_lines: list[str] = self._extract_metadata(nb)
        for cell in nb.cells:
            context_lines.extend(self._process_cell(cell, nb, file_path))

        return context_lines

    @staticmethod
    def _read_notebook(source: str, file_path: Path) -> nbformat.NotebookNode | None:
        """Read and parse the notebook source.

        Args:
            source (str): The raw text of the notebook file.
            file_path (Path): The path to the notebook file.

        Returns:
            Optional[nbformat.NotebookNode]: The parsed notebook object or None if parsing fails.
        """
        try:
            return nbformat.reads(source, as_version=4)
        except NotJSONError as e:
            logger.warning('Invalid JSON in %s: %s', file_path, e)
        except nbformat.validator.ValidationError as e:
            logger.warning('Validation error in notebook %s: %s', file_path, e)
        except (RuntimeError, TypeError, NameError) as e:
            logger.warning('Unexpected error reading notebook %s: %s', file_path, e)
        return None

    @staticmethod
    def _extract_metadata(nb: nbformat.NotebookNode) -> list[str]:
        """Extract metadata from the notebook.

        Args:
            nb (nbformat.NotebookNode): The parsed notebook object.

        Returns:
            list[str]: Extracted metadata lines.
        """
        context_lines: list[str] = []
        module_docstring = nb.metadata.get('description') or nb.metadata.get('title')
        if module_docstring:
            context_lines.append(module_docstring)
        return context_lines

    def _process_cell(
        self,
        cell: nbformat.NotebookNode,
        notebook: nbformat.NotebookNode,
        file_path: Path,
    ) -> list[str]:
        """Process an individual cell in the notebook.

        Args:
            cell (nbformat.NotebookNode): A cell from the notebook.
            notebook (nbformat.NotebookNode): The entire notebook object.
            file_path (Path): The path to the notebook file.

        Returns:
            list[str]: Extracted context from the cell.
        """
        context_lines: list[str] = []
        if cell.cell_type == 'code':
            code_context = self._process_code_cell(cell, notebook, file_path)
            if code_context:
                context_lines.append(code_context)
        elif cell.cell_type == 'markdown':
            context_lines.append(cell.source)
        return context_lines

    def _process_code_cell(
        self,
        cell: nbformat.NotebookNode,
        notebook: nbformat.NotebookNode,
        file_path: Path,
    ) -> str | None:
        """Process a code cell and extract context.

        Args:
            cell (nbformat.NotebookNode): A code cell from the notebook.
            notebook (nbformat.NotebookNode): The entire notebook object.
            file_path (Path): The path to the notebook file.

        Returns:
            Optional[str]: Extracted context from the code cell.
        """
        language = self._determine_language(cell, notebook)
        code = cell.source

        parser = self.parsers.get(language)
        if not parser:
            logger.warning(
                "No parser available for language '%s' in notebook '%s'. Skipping cell.",
                language,
                file_path,
            )
            parsed_context = code

        try:
            if hasattr(parser, 'generate_slim_context'):
                parsed_context = parser.context_body(source=code, file_path=file_path)
                if isinstance(parsed_context, list):
                    parsed_context = '\n'.join(parsed_context)
            else:
                parsed_context = code
        except (ValueError, SyntaxError) as e:
            logger.warning(
                "Error parsing code cell in %s with language '%s': %s",
                file_path,
                language,
                e,
            )
            parsed_context = code
        except AttributeError as e:
            logger.warning(
                "Parser for language '%s' does not implement required methods: %s",
                language,
                e,
            )
            parsed_context = code
        except (RuntimeError, TypeError, NameError) as e:
            logger.warning(
                "Error parsing code cell in %s with language '%s': %s",
                file_path,
                language,
                e,
            )
            parsed_context = code
        else:
            return parsed_context
        return []

    def _determine_language(
        self,
        cell: nbformat.NotebookNode,
        notebook: nbformat.NotebookNode,
    ) -> str:
        """Determine the programming language of a code cell.

        Args:
            cell (nbformat.NotebookNode): A code cell from the notebook.
            notebook (nbformat.NotebookNode): The entire notebook object.

        Returns:
            str: The programming language of the cell.
        """
        # Default to the notebook's kernel language
        kernel_lang = (
            notebook.metadata.kernelspec.language.lower()
            if 'kernelspec' in notebook.metadata
            else 'python'
        )
        language = kernel_lang

        # Check for cell magic that specifies a different language
        lines = cell.source.strip().split('\n')

        first_line = lines[0].strip()
        if first_line.startswith('%%'):
            magic = first_line[2:].split()[0].lower()
            if magic in self.parsers:
                language = magic

        return language

    def generate_slim_context(self, source: str, file_path: Path) -> str:
        """Generate a slim textual context from the notebook for the LLM.

        Args:
            source (str): The raw text of the notebook file.
            file_path (Path): The path to the notebook file.

        Returns:
            str: A string representation of the notebook context.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.extend(self.context_body(source=source, file_path=file_path))

        logger.debug('Generated slim context for notebook.')
        return '\n'.join(context_lines)

    def generate_full_context(self, source: str, file_path: Path) -> str:
        """Return the entire content of a Jupyter Notebook.

        Args:
            source (str): The raw text of the notebook file.
            file_path (Path): The path to the notebook file.

        Returns:
            str: Full text content of the notebook.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.append(source)

        return '\n'.join(context_lines)


if __name__ == '__main__':

    def example_use() -> None:
        """Small example of how to use NotebookParser."""
        example_logger = setup_logger(f'Example use of {__name__}')
        parser = NotebookParser()

        notebook_path = Path('path/to/example_notebook.ipynb')
        if notebook_path.exists():
            try:
                with notebook_path.open('r', encoding='utf-8') as f:
                    source = f.read()
                context = parser.generate_context(source, notebook_path)
                example_logger.info('Example context generated by NotebookParser: %s', context)
            except FileNotFoundError:
                example_logger.warning('Notebook file does not exist: %s', notebook_path)
            except OSError as e:
                example_logger.warning('IO error reading notebook %s: %s', notebook_path, e)
        else:
            example_logger.warning('Notebook file does not exist: %s', notebook_path)

    example_use()
