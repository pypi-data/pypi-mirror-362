"""Git Repository Manager.

Copyright (c) 2024 Neil Schneider
"""

import shutil
import subprocess  # noqa: S404
from pathlib import Path

from slimcontext.utils.logger import setup_logger

logger = setup_logger(__name__)


class GitRepository:
    """Represents a Git repository and provides methods to interact with it."""

    def __init__(self, repo_dir: Path | None = None, git_path: Path | None = None) -> None:
        """Initialize the GitRepository instance.

        Args:
            repo_dir (Optional[Path]): Directory of the repository, defaults to current directory.
            git_path (Optional[Path]): This is a path to git.exe or None.

        Raises:
            ValueError: When .git isn't found in directory path.
        """
        self.repo_dir: Path = repo_dir or Path.cwd()
        self.git_path = self.find_git_path(git_path=git_path)
        self.root = self.get_git_root()
        if not self.root:
            not_git_repo = f'Git repository root not found directory path: {repo_dir}.'
            logger.error(not_git_repo)
            raise ValueError(not_git_repo)
        self.repo_files = self.get_repo_files()

    @staticmethod
    def find_git_path(git_path: Path | None = None) -> Path | None:
        """Returns a path to git.exe.

        Args:
            git_path (Optional[Path]): This is a path to git.exe or None.

        Returns:
            A path for git.exe
        """
        if not git_path:
            check_path = shutil.which('git')
            if check_path:
                git_path = Path(check_path)
            else:
                no_git = 'Git executable not found in PATH or provided.'
                logger.info(no_git)
                git_path = None
        elif git_path.is_file() and git_path.name.lower() == 'git.exe':
            logger.debug('Valid git executable provided: %s', git_path)
        else:
            logger.warning('Invalid git path provided: %s', git_path)
            git_path = None

        return git_path

    def get_git_root(self) -> Path | None:
        """Get the root directory of the current Git project.

        Returns:
            Optional[Path]: The root path of the Git repository, or None if not inside a Git repo.
        """
        if self.git_path:
            try:
                result = subprocess.run(  # noqa: S603
                    [self.git_path, 'rev-parse', '--show-toplevel'],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                git_root = Path(result.stdout.strip())
                logger.debug('Git root found at: %s', git_root)
            except subprocess.CalledProcessError:
                logger.exception("Error running 'git rev-parse'.")
                return None
            else:
                return git_root
        else:
            logger.info(
                'No git.exe found to locate root, using current directoy: %s',
                Path.cwd(),
            )
            return Path.cwd()

    def get_repo_files(self) -> list[Path]:
        """Get all relevant files in the current Git repository.

        Returns:
            List[Path]: A list of Path objects representing the files in the repository.
        """
        if self.git_path:
            try:
                result_tracked = subprocess.run(  # noqa: S603
                    [self.git_path, 'ls-files', '--full-name'],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                tracked_files = result_tracked.stdout.splitlines()

                result_removed = subprocess.run(  # noqa: S603
                    [self.git_path, 'ls-files', '--deleted'],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                deleted_files = result_removed.stdout.splitlines()
                present_files = [file for file in tracked_files if file not in deleted_files]

                result_untracked = subprocess.run(  # noqa: S603
                    [self.git_path, 'ls-files', '--others', '--exclude-standard'],
                    cwd=self.repo_dir,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                untracked_files = result_untracked.stdout.splitlines()
            except subprocess.CalledProcessError:
                logger.exception("Error running 'git ls-files'.")
                return []
            else:
                all_files = present_files + untracked_files
                return [Path(file) for file in all_files]
        return []

    def get_files_by_suffix(self, suffixes: list[str]) -> list[Path]:
        """Return a subset of repository files that match the given suffixes.

        Args:
            suffixes (List[str]): List of file suffixes (extensions) to filter by.
                                  Each suffix should include the leading dot, e.g., '.py', '.md'.

        Returns:
            List[Path]: List of Path objects that have a suffix in the provided list.
        """
        # Normalize suffixes to ensure they start with a dot
        normalized_suffixes = [s if s.startswith('.') else f'.{s}' for s in suffixes]
        filtered_files = [
            file
            for file in self.repo_files
            if file.suffix.lower() in map(str.lower, normalized_suffixes)
        ]
        logger.debug(
            'Filtered %s files by suffixes %s.',
            len(filtered_files),
            normalized_suffixes,
        )
        return filtered_files

    def get_absolute_file_paths(self) -> list[Path]:
        """Return a list of absolute file paths from a list of relative file paths.

        Args:
            file_paths (List[str]): List of relative file paths.

        Returns:
            List[Path]: List of absolute file paths.
        """
        return [self.repo_dir / Path(file_path) for file_path in self.repo_files]


def is_ignore_file(file_path: Path, ignore_files: list[str]) -> bool:
    """Determine if a file should be ignored based on ignore patterns.

    Args:
        file_path (Path): The path to the file.
        ignore_files (List[str]): The list of ignore patterns (can include filenames or partial
            paths).

    Returns:
        bool: True if the file should be ignored, False otherwise.
    """
    for pattern in ignore_files:
        if pattern.endswith('/'):
            # Pattern is a directory; match any files under directories named dir_pattern
            dir_pattern = pattern.rstrip('/')
            if file_path.match(f'{dir_pattern}/**') or file_path.match(f'/{dir_pattern}/**'):
                logger.debug(
                    'Ignoring file: %s due to directory pattern match: %s',
                    file_path,
                    pattern,
                )
                return True
        if file_path.match(pattern):
            logger.debug(
                'Ignoring file: %s due to pattern match: %s',
                file_path,
                pattern,
            )
            return True

    return False


if __name__ == '__main__':

    def example_usage() -> None:
        """Example usage of gitrepo_tools."""
        logger_ex = setup_logger(f'Example use of {__name__}')
        repo = GitRepository()
        files = repo.get_repo_files()
        logger_ex.info('Found %s files in %s.', len(files), repo.repo_dir)

        filtered_files = repo.get_files_by_suffix(['.py', '.md'])
        logger_ex.info(
            'Found %s Python or Markdown files in %s.',
            len(filtered_files),
            repo.repo_dir,
        )
        for file in filtered_files:
            logger_ex.info(' - %s', file)
