# lyrically

Lyrically is a high-performance, asynchronous Python tool designed to fetch entire artist lyrical discographies, storing them locally in a structured SQLite database.

---

## Features

*   **Development Tools:** Includes uv, mypy, ruff, pre-commit, and commitizen

---

## Installation


### From PyPI (Recommended)

```bash
pip install lyrically
```

### From Source


You can install lyrically by cloning the repository directly.

**Prerequisites:** This project requires [uv](https://github.com/astral-sh/uv) for dependency management.

1. Clone the repository:
   ```bash
   git clone https://github.com/filming/lyrically.git
   cd lyrically
   ```

2. Install the project and its dependencies:
   ```bash
   uv sync
   ```

---

## Usage

```
Usage examples wiil be added later.
```

---

## Development

This project uses modern Python development tools:

- **[uv](https://github.com/astral-sh/uv)** for dependency management
- **[ruff](https://github.com/astral-sh/ruff)** for linting and formatting  
- **[mypy](https://mypy.readthedocs.io/)** for type checking
- **[pre-commit](https://pre-commit.com/)** for git hooks
- **[commitizen](https://commitizen-tools.github.io/commitizen/)** for conventional commits

### Setting up for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/filming/lyrically.git
   cd lyrically
   ```

2. Install dependencies (including dev tools):
   ```bash
   uv sync --extra dev
   ```

3. Set up pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```
   
4. Start developing!

---

## Dependencies

All project dependencies are managed via [`pyproject.toml`](pyproject.toml) and use Python 3.10+.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions, bug reports, and feature requests are welcome!
Please open an issue or submit a pull request on [GitHub](https://github.com/filming/lyrically).
