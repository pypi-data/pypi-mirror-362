# praicing

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Offline utility functions for estimating costs across different model providers.

- [Source code](https://github.com/joaopalmeiro/praicing)
- [PyPI package](https://pypi.org/project/praicing/)
- [Snyk Advisor](https://snyk.io/advisor/python/praicing)

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (if necessary):

```bash
curl -LsSf https://astral.sh/uv/0.7.19/install.sh | sh
```

```bash
uv python install
```

```bash
uv run python -c "from praicing import __version__; print(__version__)"
```

```bash
source .venv/bin/activate
```

```bash
mypy
```

```bash
ruff check --fix
```

```bash
ruff format
```

```bash
deactivate
```

## Deployment

```bash
uv version --bump patch
```

```bash
uv version --bump minor
```

```bash
uv version --bump major
```

```bash
uv build
```

```bash
echo "v$(uv version --short)" | pbcopy
```

- Commit and push changes.
- Create a tag on [GitHub Desktop](https://github.blog/2020-05-12-create-and-push-tags-in-the-latest-github-desktop-2-5-release/).
- Check [GitHub](https://github.com/joaopalmeiro/praicing/tags).

```bash
uv publish
```

- Check [PyPI](https://pypi.org/project/praicing/).
