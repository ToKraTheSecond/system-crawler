# File system crawler sandbox project

## How to run

Prepare and activate dev env specified in `How to dev`. Then:

```bash
cd system-crawler
python src/main.py -h
```

Check help output or tests at `tests/` for further information.

It is possible to use async version of `scan` and `detect` commands. This requires change of `RUN_ASYNC` constant in `src/main.py` from `False` to `True`.

## How to dev

### Dev setup

Have installed poetry with `virtualenvs.in-project` set to `true`. Then:

```bash
cd system-crawler
poetry install
.venv/Scripts/activate
```

Venv activation will differ based on your OS.

Or create your own venv based on `pyproject.toml`

### Ruff and Mypy

Dev setup contains ruff (linter, formatter) and mypy (static type checker). Use it via IDE or manually via terminal.

## How to test

Prepare and activate dev env specified in `How to dev`. Then:

```bash
cd system-crawler
python -m unittest tests/test_functional.py
```
