# Use Ruff to lint the whole project, given the rules in pyproject.toml
[group('util')]
[arg("fix", long, short='f', value="--fix", help="Check for linter errors and fix them")]
lint fix='':
    @uv run ruff check {{fix}}


# Use Ruff to format the whole project
[group('util')]
format:
    @uv run ruff format
