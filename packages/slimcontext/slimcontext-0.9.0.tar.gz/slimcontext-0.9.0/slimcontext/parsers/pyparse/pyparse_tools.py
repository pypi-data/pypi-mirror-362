"""This module provides utilities for parsing Python files into their Abstract Syntax Tree (AST).

Copyright (c) 2024. All rights reserved.
"""

import ast
from pathlib import Path

from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_file(file_path: Path) -> ast.AST:
    """Parse a Python file and return its Abstract Syntax Tree (AST).

    Args:
        file_path (Path): The path to the Python file to be parsed.

    Returns:
        ast.AST: The parsed abstract syntax tree of the file.

    Raises:
        SyntaxError: If there is a syntax error in the Python file.
    """
    try:
        with file_path.open('r', encoding='utf-8') as file:
            content = file.read()
        tree = ast.parse(content, filename=str(file_path))
        logger.debug('Parsed AST for file: %s', file_path)
    except SyntaxError as e:
        logger.warning('Syntax error while parsing %s: %s', file_path, e)
        raise
    except Exception:
        logger.exception('Unexpected error while parsing %s.', file_path)
        raise
    else:
        return tree


def safe_unparse(node: ast.AST) -> str:
    """Safely unparse an AST node to a string.

    Args:
        node (ast.AST): An AST node.

    Returns:
        str: The unparsed str from the AST node.
    """
    try:
        return ast.unparse(node)
    except (AttributeError, ValueError, TypeError) as e:
        logger.warning('Failed to unparse node: %s', e)
        return '<unparsable>'
