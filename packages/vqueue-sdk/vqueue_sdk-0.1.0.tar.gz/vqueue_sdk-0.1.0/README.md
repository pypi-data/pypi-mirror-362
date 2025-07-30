# Virtual Queue Python SDK

SDK to communicate with Virtual Queue's API in Python projects.

## Development

Some development notes

### Coding style guidelines

The configurations in [.editorconfig](./.editorconfig) and some in [pyproject.toml](./pyptoject.toml) are put in place in order to format and check compliance with [PEP 8](https://pep8.org) (with some exceptions).

[.pre-commit-config.yaml](./.pre-commit-config.yaml) defines a set of hooks to be executed right before each commit so that [ruff](https://docs.astral.sh/ruff/) (a blazingly fast linter and formatter) is called on the changes made.

This project uses [`uv`](https://docs.astral.sh/uv/) as package and project manager. To set it up:

1. Create a virtual environment and install the packages:
    ```shell
    uv sync
    ```
2. Install the hooks running:
    ```shell
    uvx pre-commit install
    ```
3. Now on every `git commit` the `pre-commit` hook (inside `.git/hooks/`) will be run.

#### Configuring your editor

To configure your code editor [read `ruff`'s documentation about it](https://docs.astral.sh/ruff/editors/).
