# Nix Survey Analysis

## Set up

```
poetry install
```

Copy CSV files to a new `data` folder.

## Usage

Currently needs `data/results-survey2023.csv`.

```
poetry run python ./scripts/questions.py
poetry run python ./scripts/analysis.py
```