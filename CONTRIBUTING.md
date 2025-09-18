# Contributing

[`Dishka`](https://github.com/reagento/dishka) and his integrations is an opensource project, and we are welcome the new developers to join us.

## Getting started

1. Fork [`starlette-dishka`](https://github.com/reagento/starlette-dishka)

2. Clone your fork:
```bash
git clone https://github.com/<USERNAME>/starlette-dishka.git
cd starlette-dishka
```

3. Create and activate virtual environment:
```bash
# Linux / MacOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
py -m venv .venv
.venv\scripts\activate
```

4. Install development dependencies and project itself:
```
uv pip install -e . --group dev
```

## Running linters
Currently we use [`ruff`](https://github.com/astral-sh/ruff) to check code. To run it do:
```bash
ruff check
```
We do not use ruff formatter for all code, so ensure that you formatted only your part of code proposing new changes. 
We have a lot of checks enabled and some of them can be false positive. 
Double check your code before suppressing any linter warning.

## Running type checker

Currently we use [`mypy`](https://github.com/python/mypy) to check types. To run it do:
```bash
mypy
```

## Running tests

Currently we use [`nox`](https://github.com/wntrblm/nox) for tests. To run it do:
```bash
nox
```

If you want to run tests for a particular version you can do so:
```bash
nox -t ci # run test with `starlette==0.27.0`
nox -t latest # run test with latest `starlette`
```