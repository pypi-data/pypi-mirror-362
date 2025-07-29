"""This module contains utility functions for the slimcontext parsers.

Copyright (c) 2024 Neil Schneider
"""

from pathlib import Path


def generate_context_header(file_path: Path, root_dir: Path | None = None) -> list[str]:
    """Generate the standard context header with a relative path (if possible).

    Returns:
        String - File break and path relative to project root.
    """
    resolved_file_path = file_path.resolve()
    if root_dir:
        resolved_root_dir = root_dir.resolve()
        try:
            relative_path = resolved_file_path.relative_to(resolved_root_dir)
        except ValueError:
            relative_path = file_path
    else:
        relative_path = file_path

    return [f'||| File: {relative_path}\n']
