"""Main entry point for the SlimContext project.

This script extracts project structure from a Git repository or a directory and generates context
for an LLM model.

Copyright (c) 2024 Neil Schneider
"""

import sys
from pathlib import Path

import click

from slimcontext.parsers.parser import ProjectParser
from slimcontext.utils.gitrepo_tools import GitRepository
from slimcontext.utils.logger import setup_logger
from slimcontext.utils.token_counter import TokenCounter

# Initialize a global logger
logger = setup_logger(__name__)


def gather_files_from_directory(directory: Path) -> list[Path]:
    """Recursively gather all file paths from a directory.

    Args:
        directory (Path): The root directory to traverse.

    Returns:
        List[Path]: List of file paths.
    """
    return [file_path for file_path in directory.rglob('*') if file_path.is_file()]


def gather_files(
    repo_path: Path | None,
    directory: Path | None,
    output_path: Path | None,
) -> list[Path]:
    """Gather files from a Git repository or a regular directory based on priority.

    Priority:
        1. directory
        2. repo_path
        3. current directory ('.')

    Args:
        repo_path (Path | None): Path to the Git repository.
        directory (Path | None): Path to the directory.
        output_path (Path | None): Path to the output file to exclude from processing.

    Returns:
        List[Path]: List of file paths to process.
    """
    if directory:
        logger.info('Gathering files from specified directory: %s', directory)
        files = gather_files_from_directory(directory)
        root_for_output = directory
    elif repo_path:
        try:
            git_repo = GitRepository(repo_dir=repo_path)
            logger.info('Path is a Git repository: %s', repo_path)
            files = git_repo.get_absolute_file_paths()
            root_for_output = repo_path
        except ValueError:
            logger.info('Provided repo path is not a Git repository: %s', repo_path)
            logger.info('Falling back to treat repo path as a regular directory.')
            files = gather_files_from_directory(repo_path)
            root_for_output = repo_path
    else:
        default_path = Path()
        try:
            git_repo = GitRepository(repo_dir=default_path)
            logger.info('Default path is a Git repository.')
            files = git_repo.get_absolute_file_paths()
            root_for_output = default_path
        except ValueError:
            logger.info('Default path is not a Git repository. Traversing as a regular directory.')
            files = gather_files_from_directory(default_path)
            root_for_output = default_path

    # Resolve output_path based on whether it's absolute or relative
    if output_path:
        if output_path.is_absolute():
            resolved_output_path = output_path.resolve()
        else:
            resolved_output_path = (root_for_output / output_path).resolve()

        logger.debug('Resolved output path: %s', resolved_output_path)

        # Exclude the output file if it's within the processed directory
        try:
            resolved_output_path.relative_to(root_for_output.resolve())
            files.remove(resolved_output_path)
            logger.info('Excluded output file from processing: %s', resolved_output_path)
        except ValueError:
            # The output_path is not inside the root_for_output
            logger.debug('Output path is not within the gathered files.')

    return files


def generate_context(parser: ProjectParser, files: list[Path], context_level: str) -> str:
    """Generate the combined context from all files.

    Args:
        parser (ProjectParser): The ProjectParser instance.
        files (list[Path]): List of file paths to parse.
        context_level (str): The context level, either 'full' or 'slim'.

    Returns:
        str: The combined context.
    """
    logger.info("Generating '%s' context for %d files.", context_level, len(files))
    context = parser.generate_repo_context(files, context_level)
    logger.info('Context generation completed.')
    return context


def count_tokens(context: str, model: str = 'gpt-4') -> int:
    """Count the tokens in the given context.

    Args:
        context (str): Generated context.
        model (str): Model name for token counting.

    Returns:
        int: Total token count.

    Raises:
        click.ClickException: If token counting fails.
    """
    try:
        token_counter = TokenCounter(model=model)
        return token_counter.count_tokens(context)
    except Exception as err:
        logger.exception('Error during token counting.')
        error_message = 'Token counting failed.'
        raise click.ClickException(error_message) from err


def write_output(context: str, output_path: Path | None) -> None:
    """Write the generated context to a file or stdout.

    Args:
        context (str): Generated context.
        output_path (Path | None): Path to the output file, or None for stdout.

    Raises:
        click.ClickException: If writing to the output file fails.
    """
    if output_path:
        try:
            with output_path.open('w', encoding='utf-8') as f:
                f.write(context)
            logger.info('Context successfully written to %s', output_path)
        except Exception as err:
            logger.exception('Failed to write to output file: %s', output_path)
            error_message = f'Failed to write to output file: {output_path}'
            raise click.ClickException(error_message) from err
    else:
        sys.stdout.write(context + '\n')


def normalize_extensions(exts: tuple[str]) -> list[str]:
    """Normalize file extensions by ensuring they start with a dot.

    Args:
        exts (tuple[str]): Tuple of file extensions.

    Returns:
        list[str]: List of normalized file extensions.
    """
    return [e if e.startswith('.') else f'.{e}' for e in exts]


def configure_log_level(verbose: int) -> None:
    """Configure the logging level based on verbosity.

    Args:
        verbose (int): Verbosity level (0, 1, or 2).
    """
    log_level = 'DEBUG' if verbose >= 2 else 'INFO' if verbose == 1 else 'WARNING'  # noqa: PLR2004
    logger.setLevel(log_level)
    for handler in logger.handlers:
        handler.setLevel(log_level)
    logger.debug('Log level set to %s', log_level)


def determine_root_dir(repo_path: Path | None, directory: Path | None, file: Path | None) -> Path:
    """Determine the root directory for file processing.

    Args:
        repo_path (Path | None): Path to the Git repository.
        directory (Path | None): Path to the directory.
        file (Path | None): Path to the starting file.

    Returns:
        Path: The root directory for file processing.
    """
    if directory:
        return directory
    if repo_path:
        return repo_path
    if file:
        return file.parent
    return Path()


def register_missing_extensions(
    parser: ProjectParser,
    *ext_groups: tuple[str],
    default_parser: str = 'unassigned',
) -> None:
    """Register fallback handlers for provided extensions if not already assigned."""
    for group in ext_groups:
        for ext in group:
            if ext not in parser.extension_assignments:
                parser.extension_assignments[ext] = default_parser


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option(
    '--repo-path',
    '-p',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    show_default=False,
    help=(
        'Path to the local Git repository. If not provided, the script will attempt to use the '
        'current directory as a Git repository.'
    ),
)
@click.option(
    '--directory',
    '-d',
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    show_default=False,
    help='Path to a directory to gather files from. This option takes priority over --repo-path.',
)
@click.option(
    '--file',
    '--f',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    default=None,
    help='Path to the starting file for recursive context generation.',
)
@click.option(
    '--context-level',
    '-c',
    type=click.Choice(['full', 'slim'], case_sensitive=False),
    default='full',
    show_default=True,
    help="Level of context to generate. Choices are 'full' or 'slim'.",
)
@click.option(
    '-s',
    '--slim',
    is_flag=True,
    help='Shortcut for generating slim context (equivalent to "-c slim").',
)
@click.option(
    '--output',
    '--out',
    '-o',
    type=click.Path(file_okay=True, dir_okay=False, writable=True, path_type=Path),
    default=None,
    help='Output file path. If not provided, outputs to stdout.',
)
@click.option(
    '--token-model',
    '-t',
    type=click.Choice(['gpt-4', 'gpt-3.5-turbo', 'none'], case_sensitive=False),
    default='gpt-4',
    show_default=True,
    help=("Model name to use for token counting. Choose 'none' to skip token counting."),
)
@click.option(
    '--include-ext',
    '-x',
    multiple=True,
    type=str,
    help='Additional file extensions (e.g., .txt, .cfg) to include in the output.',
)
@click.option(
    '--only-ext',
    '-X',
    multiple=True,
    type=str,
    help='Restrict parsing to only these file extensions (e.g., .py, .html). Overrides default '
    'behavior.',
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    help='Increase verbosity level. Use -v for INFO and -vv for DEBUG.',
)
def main(  # noqa: PLR0913, PLR0917 # ignore complexity because of click decorators
    repo_path: Path | None,
    directory: Path | None,
    file: Path | None,
    context_level: str,
    slim: bool,  # noqa: FBT001
    output: Path,
    token_model: str,
    include_ext: tuple[str],
    only_ext: tuple[str],
    verbose: int,
) -> None:
    """Main entry point of the script.

    Generate context from multiple files in a Git repository or directory and save it to an output
    file.
    """
    # If the slim flag is provided, override the context level to 'slim'
    if slim:
        context_level = 'slim'
        logger.debug('Slim flag detected. Setting context level to "slim".')

    configure_log_level(verbose)

    root_dir = determine_root_dir(repo_path, directory, file)

    parser = ProjectParser(root_dir=root_dir)

    include_ext = normalize_extensions(include_ext)
    only_ext = normalize_extensions(only_ext)

    register_missing_extensions(parser, include_ext, only_ext)

    if file:
        # Recursive processing for a single file
        logger.info('Processing file %s and its dependencies recursively.', file)
        context = parser.generate_recursive_context(file, context_level.lower(), output)
    else:
        # Existing behavior for repo or directory
        logger.info('Gathering files...')
        files = gather_files(repo_path, directory, output)
        if not files:
            logger.warning('No files found to parse. Exiting.')
            sys.exit(0)
        if only_ext:
            files = [f for f in files if f.suffix.lower() in only_ext]
        logger.info('Total files to parse: %d', len(files))
        context = generate_context(parser, files, context_level.lower())

    if not context:
        sys.stdout.write('No context was found or generated.')
        sys.exit(0)

    # Token counting
    if token_model.lower() != 'none':
        token_count_value = count_tokens(context, token_model.lower())
        logger.info('Total tokens in context: %d', token_count_value)
        sys.stdout.write(f'Total tokens in context: {token_count_value}\n')

    # Write output
    write_output(context, output)


if __name__ == '__main__':
    main()
