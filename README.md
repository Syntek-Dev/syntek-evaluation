# Syntek Evaluation

Model evaluation tools, benchmark prompts, assessment rubrics, recorded results,
and local model catalogs for Syntek.

## Setup

From the repository root, create a Python 3.14 environment:

```sh
python3.14 -m venv .venv
source .venv/bin/activate
```

The Python scripts use only the standard library; no additional Python packages
are required. The benchmark runner uses Bash, `jq`, `curl`, Ollama, and local
system/GPU telemetry tools, including `nvidia-smi`.

## Benchmarks

See [the benchmark documentation](experiments/BENCHMARKS.md) for prompt formats,
rubrics, and evaluation guidance. Preview fixture population with:

```sh
python experiments/populate-benchmarks.py --dry-run
```

Run a benchmark against a locally available Ollama model:

```sh
bash experiments/run-benchmark.sh <model> coding/python-refactor
```

Recorded runs and model responses live in `experiments/results/`.

## Model catalogs

See [the model inventory](models/README.md) for provider metadata and the catalog
refresh command. Local model weights, caches, datasets, and credentials are
excluded from Git.

## Checks

With the environment activated:

```sh
python -m unittest discover -s experiments -p 'test_*.py'
python -m unittest discover -s models -p 'test_*.py'
bash -n experiments/run-benchmark.sh
```

These tests run offline and mock model requests and hardware telemetry. They
require Bash and `jq`.
