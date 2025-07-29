"""This module defines the `PyImport` class, which extracts import statements from an AST node.

Copyright (c) 2024 Neil Schneider
"""

import ast
from typing import TypedDict

from slimcontext.parsers.pyparse.pybase import PyNodeBase
from slimcontext.utils.logger import setup_logger

# Setup logger for the module
logger = setup_logger(__name__)


class ImportInfo(TypedDict):
    """Dictionary structure to store class information."""

    module: str
    alias: str


class PyImport(PyNodeBase[ast.Import | ast.ImportFrom, list[ImportInfo]]):
    """Extracts import statements from an AST.

    Attributes:
        node (ast.Import | ast.ImportFrom): The AST node representing an import statement.
        import_list (list[str]): A list of extracted import statements.
        context (str): Formatted context of the import list.
    """

    def _extract(self, source: str | None = None) -> list[ImportInfo]:  # noqa: ARG002
        """Extracts the import statements from the provided AST node.

        Returns:
            list[str]: A list of extracted import statements.
        """
        imports: list[ImportInfo] = []
        if isinstance(self.node, ast.Import):
            for alias in self.node.names:
                import_info = ImportInfo(
                    module=alias.name,
                    alias='',
                )
                imports.append(import_info)
                logger.debug('Imported: %s', import_info['module'])
        elif isinstance(self.node, ast.ImportFrom):
            module = self.node.module or ''
            for alias in self.node.names:
                import_info = ImportInfo(
                    module=module,
                    alias=alias.name,
                )
                imports.append(import_info)
                logger.debug('Imported from %s: %s', import_info['module'], import_info['alias'])
        return imports

    def _format_context(self, source: str | None = None) -> list[str]:
        """Formats a list of strings based on the provided context type.

        Returns:
            list[str]: A list of formatted strings based on the context type.
        """
        if not isinstance(self.node, ast.Import | ast.ImportFrom):
            return ['']

        if source:
            source_lines = ast.get_source_segment(source=source, node=self.node)
            if source_lines:
                return [source_lines]

        imports = []
        for import_info in self.extracted_data:
            if import_info['module'] and import_info['alias']:
                imports.append(f'from {import_info["module"]} import {import_info["alias"]}')
            else:
                imports.append(f'import {import_info["module"] or import_info["alias"]}')

        return imports
