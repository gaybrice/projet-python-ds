#!/bin/bashc

uv sync
uv run quarto render notebooks/main.ipynb --execute --output-dir ../rendered
uv run quarto render notebooks/dvf.ipynb --execute --output-dir ../rendered
uv run quarto render notebooks/idfm.ipynb --execute --output-dir ../rendered
