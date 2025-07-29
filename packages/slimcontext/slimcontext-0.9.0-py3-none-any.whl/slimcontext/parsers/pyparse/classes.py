"""This module provides functionality for extracting class information.

Copyright (c) 2024 by Neil Schneider
"""

import ast
from typing import TypedDict

from slimcontext.utils.logger import setup_logger

from .assignments import PyAssignment
from .functions import PyFunction
from .pybase import PyNodeBase

logger = setup_logger(__name__)


class ClassInfo(TypedDict):
    """Dictionary structure to store class information."""

    type: str
    name: str
    docstring: str | None
    methods: list[list[str]]
    attributes: list[str]


class PyClass(PyNodeBase[ast.ClassDef, ClassInfo]):
    """Extracts Class definitions from an AST."""

    def _extract(self, source: str | None = None) -> ClassInfo:
        """Extract the Class definition from an AST node.

        Returns:
            dict[str, Any]: A dictionary with Class information, including type, name, signature,
                and docstring.
        """
        class_info: ClassInfo = ClassInfo(
            type='Class',
            name=self.node.name,
            docstring=ast.get_docstring(self.node),
            methods=[],
            attributes=[],
        )
        for item in self.node.body:
            if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                method_info = PyFunction(node=item, source=source)
                formatted_methods = [
                    '\n'.join(f'    {line}' for line in method.splitlines())
                    for method in method_info.context
                ]
                class_info['methods'].append(formatted_methods)
            elif isinstance(item, ast.Assign | ast.AnnAssign):
                assignment_info = PyAssignment(node=item, source=source)
                formatted_attributes = [
                    f'{"    " if i == 0 else "      "}{line}'
                    for i, line in enumerate(assignment_info.context)
                ]
                class_info['attributes'].extend(formatted_attributes)

        return class_info

    def _format_context(self, source: str | None = None) -> list[str]:  # noqa: ARG002
        """Helper method to format classes.

        Args:
            source (optional str): Not used for method.

        Returns:
            list[str]: A list of all the text strings which define the class.
        """
        class_context = []
        class_context.append(f'class {self.extracted_data["name"]}:')
        if self.extracted_data.get('docstring'):
            docstring = self.extracted_data.get('docstring')

            indented_docstring = (
                '    """'
                + '\n'.join(f'    {line}' for line in docstring.splitlines())
                + '\n    """\n'
            )
            class_context.append(f'{indented_docstring}')
        if self.extracted_data.get('attributes'):
            class_context.extend(self.extracted_data['attributes'])
        if self.extracted_data.get('methods'):
            for method in self.extracted_data['methods']:
                class_context.extend(method)

        return class_context
