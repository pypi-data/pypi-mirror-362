# SlimContext

SlimContext is a powerful tool designed to extract project structure and generate context for LLM models, offering seamless integration with Git repositories and directories.

## Features

- **Git Repository Integration**: Extract context directly from Git repositories.
- **Directory Traversal**: Supports context generation from a directory of files.
- **File with Imports**: Supports context generation from a file with locally imported modules.
- **Customizable Context Levels**: Generate either `full` or `slim` context based on your needs.
- **Token Counting**: Calculate token usage for popular LLM models like `gpt-4` and `gpt-3.5-turbo`.
- **Flexible Output Options**: Save context to a file or output it to stdout.

## Installation

To install SlimContext, use the following command:

```bash
pip install slimcontext
```

Or install directly from GitLab:

```bash
pip install git+https://gitlab.com/notorious-community/slimcontext.git
```

## Usage

SlimContext can be run via the command line:

```bash
slimcontext --repo-path /path/to/your/git/repo
```

### Options

- `--repo-path, -p`: Path to the Git repository. Defaults to the current directory if not provided.
- `--directory, -d`: Path to a directory to gather files from. **Takes priority over `--repo-path`**.
- `--file, -f`: Path to a file to generate context for. **Takes priority over `--repo-path` and `-directory`**.
- `--context-level, -c`: Level of context to generate (`full` or `slim`). Default is `full`.
- `--output, -o`: Path to save the output file. Defaults to stdout if not provided.
- `--token-model, -t`: Model name for token counting (`gpt-4`, `gpt-3.5-turbo`, or `none`). Default is `gpt-4`.
- `--include-ext, -x`: Additional file extensions (e.g., `.txt`, `.cfg`) to include alongside default recognized code files.
- `--only-ext, -X`: Restrict context generation to only the specified extensions. This overrides the default extension behavior.
- `--verbose, -v`: Increase verbosity (use `-v` for INFO and `-vv` for DEBUG).

### Example

```bash
slimcontext -d /path/to/directory -c slim -o output.txt -t gpt-4 -v
```

This command generates a slim context from the specified directory, counts tokens using `gpt-4`, and saves the result to `output.txt`.

### Directory Support

SlimContext supports extracting context directly from directories:

- Use `--directory` to specify the directory.
- All files within the directory (and subdirectories) will be processed.

Example:

```bash
slimcontext --directory /path/to/files -c full -o context.txt
```

### File Support

SlimContext supports extracting context directly from file and modules imported in that file:

- Use `--file` to specify the direcfiletory.
- All local modules loaded in the file will also be included in the output.

Example:

```bash
slimcontext --file /path/to/file.py -c full -o context.txt
```

### Extension Filtering

SlimContext allows fine-grained control over which file types to include:

- Use `--include-ext` to **add additional file extensions** to the default list (e.g., `.txt`, `.cfg`).
- Use `--only-ext` to **limit output strictly to certain extensions**, overriding all default behavior.

#### Example: Include additional file types

```bash
slimcontext --directory ./my_project -x .cfg -x .txt
```

This will include `.cfg` and `.txt` files in addition to the default recognized file types.

#### Example: Restrict to specific file types

```bash
slimcontext --directory ./my_project -X .py -X .ts
```

This will only include .py and .ts files in the output, skipping all others.

## Logging

Use the `-v` or `-vv` flags to control verbosity:

- `-v`: INFO level logs.
- `-vv`: DEBUG level logs.

## Development

### Setting Up the Development Environment

1. **Clone the Repository:**

    ```bash
    git clone https://gitlab.com/notorious-community/slimcontext.git
    cd slimcontext
    ```

2. **Install Dependencies:**

    Ensure you have `poetry` installed. Then run:

    ```bash
    poetry install
    ```

### Running Tests

The package includes a comprehensive test suite using `pytest`.

```bash
poetry run pytest
```

### Linting and Formatting

Ensure code quality and consistency with `ruff`.

```bash
poetry run ruff check .
```

### Running Nox Sessions

Automate development tasks across multiple Python environments using `nox`.

```bash
nox -s tests
```

## Project Structure

```
slimcontext/
├── slimcontext/
│   ├── main.py
│   ├── managers/  # Houses various managers for languages.
│   ├── parsers/  # Houses the code to parse and extract key context by language.
│   └── utils/  # Various utilities used across code base.
├── tests/ 
├── gitlab-ci.yml
├── CHANGELOG
├── LICENSE
├── noxfile.py
├── pyproject.toml
└── README.md
```

## Contributions

Contributions are welcome! Whether it's reporting bugs, suggesting features, or submitting pull requests, your help is appreciated. Please follow these steps to contribute:

1. **Fork the Repository:**

    Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork:**

    ```bash
    git clone https://gitlab.com/your-username/slimcontext.git
    cd slimcontext
    ```

3. **Create a New Branch:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

4. **Make Your Changes:**

    Implement your feature or bug fix.

5. **Commit Your Changes:**

    ```bash
    git commit -m "Title of your changes" -m "Describe **Why** you made this change."
    ```

6. **Push to Your Fork:**

    ```bash
    git push origin feature/your-feature-name
    ```

7. **Create a Merge Request:**

    Go to the original repository and create a merge request from your fork.

Please ensure all tests pass and adhere to the project's coding standards before submitting your merge request.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

**Copyright (c) 2024 Neil Schneider**
