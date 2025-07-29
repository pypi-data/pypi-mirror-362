"""MultiFileContextParser is responsible for parsing multiple file types and generating context.

Copyright (c) 2024 Neil Schneider
"""

from pathlib import Path

from slimcontext.parsers.htmlparse.htmlparser import HtmlParser
from slimcontext.parsers.notebookparse.notebookparser import NotebookParser
from slimcontext.parsers.pyparse.pyparser import PyParser
from slimcontext.parsers.utils import generate_context_header
from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class ProjectParser:
    """A high-level parser that delegates to specialized sub-parsers for certain file extensions.

    Uses fallback "read the entire file" for unknown types.
    """

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize the ProjectParser with an optional root directory."""
        self.root_dir = root_dir or Path.cwd()

        # Initialize extension assignments
        self.extension_assignments = {
            '.py': 'unassigned',
            '.js': 'unassigned',
            '.jsx': 'unassigned',
            '.ts': 'unassigned',
            '.tsx': 'unassigned',
            '.c': 'unassigned',
            '.cpp': 'unassigned',
            '.h': 'unassigned',
            '.hpp': 'unassigned',
            '.java': 'unassigned',
            '.go': 'unassigned',
            '.rs': 'unassigned',
            '.sh': 'unassigned',
            '.rb': 'unassigned',
            '.swift': 'unassigned',
            '.php': 'unassigned',
            '.kt': 'unassigned',
            '.kts': 'unassigned',
            '.html': 'unassigned',
            '.htm': 'unassigned',
            '.css': 'unassigned',
            '.scss': 'unassigned',
            '.sass': 'unassigned',
            '.yaml': 'unassigned',
            '.yml': 'unassigned',
            '.json': 'unassigned',
            '.toml': 'unassigned',
            '.xml': 'unassigned',
            '.tf': 'unassigned',
            '.ipynb': 'unassigned',
            '.jinja': 'unassigned',
            '.jinja2': 'unassigned',
            '.j2': 'unassigned',
        }
        self.extensionless_assignments = {
            'dockerfile': 'unassigned',
            'makefile': 'unassigned',
        }

        # Load language parsers
        self.languages = {
            'py_parser': PyParser(root_dir=self.root_dir),
            'html_parser': HtmlParser(root_dir=self.root_dir),
            'notebook_parser': NotebookParser(root_dir=self.root_dir),
        }

        # Update extension assignments based on each parser's supported extensions
        self._update_extension_assignments()

    def _update_extension_assignments(self) -> None:
        """Internal method to update extension assignments based on available parsers.

        Raises:
            ValueError: If an extension is already assigned to a different parser.
        """
        for parser_key, parser in self.languages.items():
            for ext in parser.extensions:
                ext_lower = ext.lower()
                if ext_lower not in self.extension_assignments:
                    logger.info(
                        "Extension '%s' is not recognized and will be added to the extensions.",
                        ext_lower,
                    )
                    self.extension_assignments[ext_lower] = 'unassigned'

                if self.extension_assignments[ext_lower] == 'unassigned':
                    self.extension_assignments[ext_lower] = parser_key
                    logger.debug("Assigned extension '%s' to parser '%s'.", ext_lower, parser_key)
                elif self.extension_assignments[ext_lower] != parser_key:
                    logger.error(
                        "Extension '%s' is already assigned to parser '%s'. "
                        "Cannot assign to parser '%s'.",
                        ext_lower,
                        self.extension_assignments[ext_lower],
                        parser_key,
                    )
                    error_message = (
                        f"Extension '{ext_lower}' is already assigned to parser "
                        f"'{self.extension_assignments[ext_lower]}'."
                    )
                    raise ValueError(error_message)
                else:
                    logger.debug(
                        "Extension '%s' is already assigned to parser '%s'.",
                        ext_lower,
                        parser_key,
                    )

    def generate_file_context(self, file_path: Path, context_level: str) -> str:
        """Given a single file_path and context_level ('full' or 'slim'), generate text context.

        Returns a string with the header + the file's context.

        Args:
            file_path (Path): The path to the file to parse.
            context_level (str): The context level, either 'full' or 'slim'.

        Returns:
            str: The generated context as a string.
        """
        # Common header for all file types
        header_lines = generate_context_header(file_path, self.root_dir)

        # Decide how to parse the file
        extension = file_path.suffix.lower()
        context = ''
        try:
            if not extension:
                parser_key = self.extensionless_assignments.get(file_path.name.lower(), 'none')
            else:
                parser_key = self.extension_assignments.get(extension, 'none')
            if parser_key == 'none':
                logger.info("Skipping: '%s' not a recognized code file.", file_path)
                return ''
            if parser_key != 'unassigned':
                parser = self.languages.get(parser_key)
                if parser:
                    if context_level == 'slim' and hasattr(parser, 'generate_slim_context'):
                        context = parser.generate_slim_context(
                            file_path.read_text(encoding='utf-8', errors='replace'),
                            file_path,
                        )
                    elif context_level == 'full' and hasattr(parser, 'generate_full_context'):
                        context = parser.generate_full_context(
                            file_path.read_text(encoding='utf-8', errors='replace'),
                            file_path,
                        )
                    else:
                        # Fallback to reading the entire file
                        file_text = file_path.read_text(encoding='utf-8', errors='replace')
                        context = '\n'.join([*header_lines, file_text])
                else:
                    logger.warning(
                        "Parser '%s' not found for extension '%s'. Falling back to full read.",
                        parser_key,
                        extension,
                    )
                    file_text = file_path.read_text(encoding='utf-8', errors='replace')
                    context = '\n'.join([*header_lines, file_text])
            else:
                # Handle unassigned extensions
                logger.debug(
                    "No specific parser assigned for extension '%s'. Reading entire file.",
                    extension,
                )
                file_text = file_path.read_text(encoding='utf-8', errors='replace')
                context = '\n'.join([*header_lines, file_text])
            context += '\n'
        except (UnicodeDecodeError, FileNotFoundError, PermissionError) as e:
            logger.warning('Skipping file due to read error %s: %s', file_path, e)
            context = ''

        return context

    def generate_repo_context(self, file_paths: list[Path], context_level: str) -> str:
        """Walk multiple files, gather all contexts, and combine them.

        Returns:
            str: The combined context of all files as a single string.
        """
        all_contexts = []
        for fp in file_paths:
            context = self.generate_file_context(fp, context_level)
            if context:
                all_contexts.append(context)

        return '\n'.join(all_contexts)

    @staticmethod
    def resolve_module_to_path(module_name: str) -> Path | None:
        """Resolve a module name to a file path within the root directory.

        Args:
            module_name (str): The module name (e.g., 'a.b.c').

        Returns:
            Path | None: The resolved file path or None if not found.
        """
        # Convert module name to a relative path (e.g., 'a.b.c' -> 'a/b/c.py')
        parts = module_name.split('.')
        possible_path = Path('/'.join(parts)).with_suffix('.py')
        if possible_path.exists():
            logger.debug('Resolved module %s to %s', module_name, possible_path)
            return possible_path
        logger.info('Module %s not found at %s', module_name, possible_path)
        return None

    def generate_recursive_context(
        self,
        file_path: Path,
        context_level: str,
        exclude_path: Path | None = None,
        processed: set[Path] | None = None,
        search_depth: int = 1,
    ) -> str:
        """Recursively generates context for a file by analyzing its content and dependencies.

        This method processes a given file and, if it's a Python file, recursively includes
        context from its imported modules. It avoids circular dependencies and exclusions
        by tracking processed files.

        Args:
            file_path (Path): The path to the file to generate context for.
            context_level (str): The level of context detail to generate.
            exclude_path (Path | None, optional): A path to exclude from processing. Default: None.
            processed (set[Path] | None, optional): A set of already processed file paths.
                Defaults to None, in which case a new set is created.
            search_depth (int): Current depth of the file. Limits recursive file context to only
                the first file.

        Returns:
            str: The generated context string, including content from the file and its dependencies.
        """
        if processed is None:
            processed = set()

        if file_path in processed or file_path == exclude_path:
            logger.debug('Skipping already processed or excluded file: %s', file_path)
            return ''

        logger.info('Processing file: %s', file_path)
        processed.add(file_path)
        context = self.generate_file_context(file_path, context_level)

        if file_path.suffix in self.languages['py_parser'].extensions and search_depth == 1:
            parser = self.languages['py_parser']
            imports = parser.get_imports(file_path)
            for imp in imports:
                imp_path = self.resolve_module_to_path(imp)
                if imp_path:
                    if imp_path in processed or imp_path == exclude_path:
                        logger.debug(
                            'Skipping dependency due to prior processing or exclusion: %s',
                            imp_path,
                        )
                    else:
                        context += self.generate_recursive_context(
                            file_path=imp_path,
                            context_level=context_level,
                            exclude_path=exclude_path,
                            processed=processed,
                            search_depth=search_depth + 1,
                        )

        return context
