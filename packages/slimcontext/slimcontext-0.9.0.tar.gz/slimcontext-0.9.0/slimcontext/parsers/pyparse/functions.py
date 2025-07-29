"""This module provides functionality for extracting function definitions and signatures.

Copyright (c) 2024 by Neil Schneider. All rights reserved.
"""

import ast
from typing import Literal, TypedDict

from slimcontext.parsers.pyparse.pybase import PyNodeBase
from slimcontext.parsers.pyparse.pyparse_tools import safe_unparse
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class FunctionInfo(TypedDict):
    """Dictionary structure to store class information."""

    type: str
    name: str
    func_info: str


class PyFunction(PyNodeBase[ast.FunctionDef | ast.AsyncFunctionDef, FunctionInfo]):
    """Extracts function definitions from an AST."""

    def _extract(self, source: str | None = None) -> FunctionInfo:
        """Extract the function definition from an AST node.

        Returns:
            dict[str, Any]: A dictionary with function information, including type, name, signature,
                and docstring.
        """
        func_type: Literal['AsyncFunction', 'Function'] = (
            'AsyncFunction' if isinstance(self.node, ast.AsyncFunctionDef) else 'Function'
        )
        if source:
            source_lines = source.splitlines()
            signature = '\n'.join(
                source_lines[(self.node.lineno - 1) : (self.node.body[0].lineno - 1)],
            )
        else:
            source_lines = ['']
            signature = SignatureExtractor.get_signature(self.node, func_type)

        docstring = ast.get_docstring(self.node) or ''
        if docstring:
            indented_docstring = (
                '    """'
                + '\n'.join(f'    {line}' for line in docstring.splitlines())
                + '\n    """\n'
            )
        else:
            indented_docstring = ''

        func_info = f'{signature.strip()}\n{indented_docstring}    ...code...'
        logger.debug('Extracted %s: %s', func_type, self.node.name)
        return FunctionInfo(
            type=func_type,
            name=self.node.name,
            func_info=func_info,
        )

    def _format_context(self, source: str | None = None) -> list[str]:  # noqa: ARG002
        """Formats a list of strings based on the provided context type.

        Args:
            source (optional str): Not used for method.

        Returns:
            list[str]: A list of formatted strings based on the context type.
        """
        return [self.extracted_data['func_info']]


class SignatureExtractor:
    """Handles extraction of function signatures."""

    @staticmethod
    def get_signature(
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        func_type: Literal['AsyncFunction', 'Function'],
    ) -> str:
        """Extract the function signature from an AST FunctionDef or AsyncFunctionDef node.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.
            func_type (Literal[str]): Either AsyncFunction or function, used to id sync of function.

        Returns:
            str: The extracted function signature.
        """
        args = SignatureExtractor._extract_arguments(node)
        return_annotation = SignatureExtractor._extract_return_annotation(node)
        async_prefix = 'async ' if func_type == 'AsyncFunction' else ''
        signature = f'{async_prefix}def {node.name}({", ".join(args)}){return_annotation}:'
        logger.debug('Extracted signature: %s for function %s', signature, node.name)
        return signature

    @staticmethod
    def _extract_arguments(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract arguments from the function definition.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            list[str]: A list of extracted arguments as strings.
        """
        args = []
        args += SignatureExtractor._extract_positional_args(node)
        varargs = SignatureExtractor._extract_varargs(node)
        args += varargs
        kwonlyargs = SignatureExtractor._extract_kwonlyargs(node)
        if not varargs and kwonlyargs:
            args.append('*')
        args += kwonlyargs
        args += SignatureExtractor._extract_kwargs(node)
        return args

    @staticmethod
    def _extract_positional_args(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract positional arguments with defaults.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            list[str]: A list of extracted positional arguments as strings.
        """
        args = []
        num_defaults = len(node.args.defaults)
        num_args = len(node.args.args)

        for i, arg in enumerate(node.args.args):
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f': {safe_unparse(arg.annotation)}'

            # Add default value if applicable
            if i >= num_args - num_defaults:
                default_index = i - (num_args - num_defaults)
                default_value = node.args.defaults[default_index]
                arg_str += f'={safe_unparse(default_value)}'

            args.append(arg_str)
        return args

    @staticmethod
    def _extract_varargs(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract *args.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            list[str]: A list containing the extracted *args string if applicable.
        """
        args = []
        if node.args.vararg:
            vararg_str = f'*{node.args.vararg.arg}'
            if node.args.vararg.annotation:
                vararg_str += f': {safe_unparse(node.args.vararg.annotation)}'
            args.append(vararg_str)
        return args

    @staticmethod
    def _extract_kwonlyargs(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract keyword-only arguments with defaults.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            list[str]: A list of extracted keyword-only arguments as strings.
        """
        args = []
        for i, arg in enumerate(node.args.kwonlyargs):
            kwarg_str = arg.arg
            if arg.annotation:
                kwarg_str += f': {safe_unparse(arg.annotation)}'

            kw_default = node.args.kw_defaults[i]
            if kw_default:
                kwarg_str += f'={safe_unparse(kw_default)}'

            args.append(kwarg_str)
        return args

    @staticmethod
    def _extract_kwargs(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract **kwargs.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            list[str]: A list containing the extracted **kwargs string if applicable.
        """
        args = []
        if node.args.kwarg:
            kwarg_str = f'**{node.args.kwarg.arg}'
            if node.args.kwarg.annotation:
                kwarg_str += f': {safe_unparse(node.args.kwarg.annotation)}'
            args.append(kwarg_str)
        return args

    @staticmethod
    def _extract_return_annotation(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Extract the return annotation of a function.

        Args:
            node (ast.FunctionDef | ast.AsyncFunctionDef): The function definition node.

        Returns:
            str: The extracted return annotation as a string, or an empty string if none exists.
        """
        if node.returns:
            return f' -> {safe_unparse(node.returns)}'
        return ''
