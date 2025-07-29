"""Module for parsing Python source files and extracting structured information using AST.

Copyright (c) 2024 Neil Schneider
"""

import ast
from pathlib import Path
from typing import ClassVar

from slimcontext.parsers.baseparser import BaseFileParser
from slimcontext.parsers.pyparse.assignments import PyAssignment
from slimcontext.parsers.pyparse.classes import PyClass
from slimcontext.parsers.pyparse.expressions import PyExpression
from slimcontext.parsers.pyparse.functions import PyFunction
from slimcontext.parsers.pyparse.imports import PyImport
from slimcontext.parsers.pyparse.pybase import PyNodeBase
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class PyParser(BaseFileParser):
    """Parses Python source files and extracts structured information using AST."""

    extensions: ClassVar[list[str]] = ['.py']

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize the PyParser instance.

        Args:
            root_dir (Path, optional): The git repo's root directory. Defaults to None.
        """
        super().__init__(extensions=self.extensions, root_dir=root_dir)

    def context_body(self, source: str, file_path: Path) -> list[str]:
        """Extract comprehensive information from a Python source file using AST.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            list[str]: A list of all the context from the module.
        """
        try:
            tree = ast.parse(source=source, filename=str(file_path))
        except SyntaxError as e:
            logger.warning('Syntax error in %s: %s', file_path, e)
            tree = None

        all_nodes: list = []
        if tree:
            # Retrieve module docstring and skip it in child nodes
            module_docstring = ast.get_docstring(tree)
            body_nodes = tree.body
            # If the first node is a docstring, skip it
            start_index = 1 if body_nodes and self._is_docstring(body_nodes[0]) else 0

            # Process remaining nodes, skipping docstrings
            for node in body_nodes[start_index:]:
                processed_node = self._process_node(node=node, source=source)
                if processed_node:
                    all_nodes.append(processed_node)

        processed_nodes: list[PyNodeBase] = all_nodes

        body: list[str] = []
        module_docstring: str | None = ast.get_docstring(tree) if tree else None
        if module_docstring:
            body.append(module_docstring)
        for node in processed_nodes:
            body.extend(node.context)

        return body

    @staticmethod
    def _is_docstring(node: ast.AST) -> bool:
        """Determine if a node is a docstring.

        Args:
            node (ast.AST): The AST node to check.

        Returns:
            bool: True if the node is a docstring, False otherwise.
        """
        return (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )

    @staticmethod
    def _process_node(node: ast.AST, source: str) -> PyNodeBase | None:
        """Process a single AST node and extract relevant information.

        Args:
            node (ast.AST): The AST node to process.
            source (str): The raw text of the source file.

        Returns:
            One of the PyNode objects built from PyNodeBase.
        """
        if isinstance(node, ast.Import | ast.ImportFrom):
            return PyImport(node=node, source=source)
        if isinstance(node, ast.Assign):
            return PyAssignment(node=node, source=source)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            return PyFunction(node=node, source=source)
        if isinstance(node, ast.ClassDef):
            return PyClass(node=node, source=source)
        if isinstance(node, ast.Expr):
            return PyExpression(node=node, source=source)
        logger.debug('Found uncategorized node type: %s', type(node))
        return None

    def generate_slim_context(self, source: str, file_path: Path) -> str:
        """Generate a slim textual context from the repository information for the LLM.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            str: A string representation of the repository context.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.extend(self.context_body(source=source, file_path=file_path))

        logger.debug('Generated slim context for LLM.')
        return '\n'.join(context_lines)

    def generate_full_context(self, source: str, file_path: Path) -> str:
        """Return the entire content of a Python source file.

        Args:
            source (str): The raw text of the source file.
            file_path (Path): The path to the Python source file.

        Returns:
            str: Full text content of the file.
        """
        context_lines: list[str] = []
        context_lines.extend(self.context_header(file_path=file_path))
        context_lines.append(source)

        return '\n'.join(context_lines)

    @staticmethod
    def get_imports(file_path: Path) -> list[str]:
        """Extract module names from import statements in a Python file.

        Args:
            file_path (Path): Path to the Python file.

        Returns:
            list[str]: List of unique module names imported.
        """
        try:
            with file_path.open('r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filename=str(file_path))
        except (OSError, SyntaxError) as e:
            logger.warning('Failed to parse %s for imports: %s', file_path, e)
            return []

        imports = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module)

        return list(imports)


if __name__ == '__main__':

    def example_use() -> None:
        """Small example of how to use PyParser."""
        logger_ex = setup_logger(f'Example use of {__name__}')
        parser = PyParser()
        # Sample file path for demonstration purposes
        file_path = Path('slimcontext/parsers/pyparse/pyparser.py')
        context = parser.generate_slim_context(source=file_path.read_text(), file_path=file_path)
        logger_ex.info('Example context generated by PyParser: %s', context)

    example_use()
