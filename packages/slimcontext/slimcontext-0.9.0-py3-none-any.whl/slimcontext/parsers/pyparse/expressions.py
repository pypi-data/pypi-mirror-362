"""This module provides classes and functions to parse and extract expressions from an AST.

Copyright (c) 2025 Neil Schneider
"""

import ast
from typing import TypedDict

from slimcontext.parsers.pyparse.pybase import PyNodeBase
from slimcontext.parsers.pyparse.pyparse_tools import safe_unparse
from slimcontext.utils.logger import setup_logger

# Setup logger for the module
logger = setup_logger(__name__)


class ExpressionInfo(TypedDict):
    """Dictionary structure to store expression information."""

    expr_type: str
    details: str | None


class PyExpression(PyNodeBase[ast.Expr, list[ExpressionInfo]]):
    """Extracts expression statements from an AST.

    Attributes:
        node (ast.Expr): The AST node representing an expression statement.
        expressions (List[ExpressionInfo]): A list of extracted expression details.
        context (List[str]): Formatted context of the expressions.
    """

    def _extract(
        self,
        source: str | None = None,  # noqa: ARG002
    ) -> list[ExpressionInfo]:
        """Extracts the expression details from the provided AST node, excluding docstrings.

        Args:
            source (Optional[str]): The raw source code.
            parent (Optional[ast.AST]): The parent AST node.

        Returns:
            List[ExpressionInfo]: A list of extracted expression details.
        """
        expressions: list[ExpressionInfo] = []

        expr = self.node.value
        expr_type = type(expr).__name__
        details = safe_unparse(expr)

        expression_info: ExpressionInfo = {
            'expr_type': expr_type,
            'details': details,
        }
        expressions.append(expression_info)
        logger.debug('Expression found: %s', expression_info)

        return expressions

    def _format_context(self, source: str | None = None) -> list[str]:
        """Formats a list of strings based on the extracted expressions.

        Args:
            source (Optional[str]): The raw source code.

        Returns:
            List[str]: A list of formatted strings representing the expressions.
        """
        if not isinstance(self.node, ast.Expr):
            return ['']

        if source:
            source_segment = ast.get_source_segment(source, self.node)
            if source_segment:
                return [source_segment.strip()]

        formatted_expressions = []
        for expr in self.extracted_data:
            if expr['details']:
                formatted_expressions.append(f'{expr["expr_type"]}: {expr["details"]}')
            else:
                formatted_expressions.append(f'{expr["expr_type"]}')

        return formatted_expressions
