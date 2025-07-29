"""This module defines the `PyASTNode` base class for extracting and formatting AST nodes.

The `PyASTNode` base class provides shared functionality for extracting and formatting information
from different types of Abstract Syntax Tree (AST) nodes in Python files. Derived classes are
expected to implement their own `_extract` and `_format_context` methods to handle specific node
types.

Copyright (c) 2024 Neil Schneider
"""

import ast
from typing import Generic, TypeVar

from slimcontext.utils.logger import setup_logger

# Setup logger for the module
logger = setup_logger(__name__)

T = TypeVar('T', bound=ast.AST)
R = TypeVar('R')


class PyNodeBase(Generic[T, R]):
    """Base class for extracting and formatting information from AST nodes.

    Attributes:
        node (ast.AST): The AST node associated with the specific Python construct.
        extracted_data (Any): Extracted data specific to the AST node, as returned by `_extract`.
        context (list[str]): Formatted context as a list of strings, created by `_format_context`.
    """

    def __init__(self, node: T, source: str | None = None) -> None:
        """Initializes a `PyASTNode` instance with the given AST node.

        The constructor first calls `_extract` to gather relevant information from the node,
        then formats this information using `_format_context`.

        Args:
            node (ast.AST): The AST node representing a specific Python construct.
            source (optional str): Pass other keyword arguments.
        """
        self.node = node
        self.extracted_data = self._extract(source=source)
        self.context = self._format_context(source=source)

    def _extract(self, source: str | None = None) -> R:  # noqa: ARG002
        """Extracts relevant information from the AST node.

        This method should be overridden in subclasses to define how data is extracted from
        specific types of AST nodes.

        Returns:
            Any: Extracted information, specific to the subclass.
        """
        not_implemented_msg = f'This method should be overridden in subclasses. Node: {self.node}'
        raise NotImplementedError(not_implemented_msg)
        return 'Not Implemented'

    def _format_context(self, source: str | None = None) -> list[str]:  # noqa: ARG002
        """Formats the context of the node based on extracted data.

        This method should be overridden in subclasses to define how the context is formatted
        for specific types of AST nodes.

        Returns:
            list[str]: A list of formatted strings representing the context.
        """
        not_implemented_msg = f'This method should be overridden in subclasses. Node: {self.node}'
        raise NotImplementedError(not_implemented_msg)
        return ['Not Implemented']

    def get_context(self) -> list[str]:
        """Provides the formatted context for external use.

        Returns:
            list[str]: A list of strings representing the formatted context.
        """
        return self.context
