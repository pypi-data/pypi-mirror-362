"""This module defines the `PyAssignment` class, which extracts global assignment statements.

Copyright (c) 2024 Neil Schneider
"""

import ast
from typing import TypedDict

from slimcontext.parsers.pyparse.pyparse_tools import safe_unparse
from slimcontext.utils.logger import setup_logger

from .pybase import PyNodeBase

logger = setup_logger(__name__)


class AssignmentInfo(TypedDict):
    """Dictionary structure to store class information."""

    name: str
    value: str | None


class PyAssignment(PyNodeBase[ast.Assign | ast.AnnAssign, list[AssignmentInfo]]):
    """Extracts assignments, distinguishing between attributes and constants."""

    def _extract(self, source: str | None = None) -> list[AssignmentInfo]:  # noqa: ARG002
        assignments = []

        def _extract_assignment(target: ast.expr, node_value: ast.expr | None) -> None:
            value = safe_unparse(node_value) if node_value else None
            assignment = AssignmentInfo(
                name=safe_unparse(target),
                value=value,
            )
            assignments.append(assignment)
            logger.debug('Attribute found: %s', assignment)

        if isinstance(self.node, ast.Assign):
            for target in self.node.targets:
                _extract_assignment(target=target, node_value=self.node.value)
        elif isinstance(self.node, ast.AnnAssign):
            _extract_assignment(target=self.node.target, node_value=self.node.value)

        return assignments

    def _format_context(self, source: str | None = None) -> list[str]:
        """Formats a list of strings based on the provided context type.

        Returns:
            list[str]: A list of formatted strings based on the context type.
        """
        if not isinstance(self.node, ast.Assign | ast.AnnAssign):
            return ['']

        if source:
            source_lines = ast.get_source_segment(source, self.node)
            if source_lines:
                return [source_lines]

        # Fallback formatting
        return [f'{const["name"]} = {const["value"]}' for const in self.extracted_data]
