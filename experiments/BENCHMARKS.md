# Syntek benchmark fixtures

`populate-benchmarks.py` is a standalone, standard-library Python 3.10+ script
for Linux/AI-01. It embeds 135 authored scenarios across 15 domains and creates
`.md` files with YAML frontmatter. It requires no network access, model downloads
or additional data files.

From the repository root:

```sh
python3 experiments/populate-benchmarks.py --dry-run
python3 experiments/populate-benchmarks.py
```

From `experiments`, use `python3 populate-benchmarks.py`. The default destination
is `prompts` beside the script, regardless of the shell's working directory.
For another destination:

```sh
python3 experiments/populate-benchmarks.py --prompt-dir /tmp/syntek-prompts
```

The original tree had 134 paths. The additional fixture is
`reasoning/probability-calibration.md`, testing base rates and uncertainty.

## Markdown format

```markdown
---
benchmark: coding--python-refactor
version: 2
domain: coding
capability: refactoring
jurisdiction: UK
expected_output: analysis-and-code
scoring: qualitative
---
# Task

...

# Constraints

- ...

# Evaluation criteria

1. ...
```

The frontmatter contract is a flat YAML mapping: scalar strings and a
non-negative integer `version`. All seven fields shown above are required.
Unquoted strings, YAML single-quoted strings, JSON-style double-quoted strings,
blank lines and full-line comments are supported. Unquoted strings must start
with a letter; quote strings that resemble numbers or booleans. Nested mappings,
lists, multiline scalars, aliases, tags
and inline comments are unsupported and rejected; no YAML package is required.

The runner reads metadata separately and sends only the body to Ollama. It
records `fixture_metadata`, `fixture_sha256` (the complete Markdown file) and
`input_sha256` (the exact text sent). Final LF characters are removed from the
body to preserve the previous runner's shell convention; other whitespace and
internal Markdown horizontal rules are retained. Invalid frontmatter fails
before runtime calls or result creation.

To inspect the parsed input without running a model:

```sh
python3 experiments/populate-benchmarks.py --read-prompt experiments/prompts/coding/python-refactor.md
```

## Migrating an existing text tree

```sh
python3 experiments/populate-benchmarks.py --migrate-txt --dry-run
python3 experiments/populate-benchmarks.py --migrate-txt
```

Migration recognises the former generated version-1 text, converts its metadata
to YAML and its section titles to Markdown, and records version 2 because the
model-facing format changes. Scenario facts, constraints and criteria are retained.
Custom UTF-8 text is wrapped with version-0 frontmatter and its exact original
bytes as the body. Non-UTF-8 sources and conflicts with existing non-empty
Markdown files stop migration before writes. Text sources are removed only after
their matching Markdown files have been successfully written and checked.

The two original validated fixtures are wrapped with version-0 frontmatter:

- `coding/python-production-code-review.md`
- `linux/process-thread.md`

Their original body bytes and exact model inputs are preserved, allowing
comparison with prior runs. Version 0 identifies preserved, previously
unversioned content; it does not mean a regenerated version-2 fixture. If a
legacy fixture is absent or empty when populating a fresh tree, the generator
creates a version-2 fixture using its original task and additional criteria.

## Preservation and repeatability

Normal population fills zero-byte Markdown files and creates missing known paths.
Every non-empty Markdown file is preserved byte-for-byte, including whitespace-only
files and custom fixtures. There is no overwrite flag. Existing text files require
the explicit migration option. Unknown `.md`/`.txt` paths and symlinked paths fail
validation before population begins, so adding another filename requires authoring
its scenario in the script first. A dry run creates nothing.

The script coordinates concurrent population runs with advisory file locks;
avoid editing fixtures while it runs. An I/O error exits unsuccessfully and may
leave earlier files populated. Migration can resume when a text file and its
complete matching Markdown both exist. Review any partial non-empty destination
before retrying, because preservation applies to it too.

## Assessment

Export references separately from model inputs:

```sh
python3 experiments/populate-benchmarks.py --export-rubrics experiments/benchmark-rubrics.json
```

The schema-version-2 JSON records `sha256` for complete fixture files and
`input_sha256` for the text sent to the model, alongside fixture version/status,
criteria, reference notes and a common 0–2 scale for each of five criteria (10
maximum). It includes checked answers for numerical and finite reasoning tasks.
References accept justified alternatives where the task involves judgement.

Never send the rubric JSON to the model being benchmarked. The `.md` prompts
contain requirements and evaluation criteria, but exclude the assessor answers.
References live in the population script as well, so give a benchmarked agent
only its prompt rather than access to this repository.

Rubrics recognise the exact original legacy bodies under their version-0 wrappers.
Custom non-empty prompts
are preserved and marked `preserved-unrecognised`, with no applicable score or
reference attached. An existing identical rubric export is preserved. A different
non-empty export causes an error before population; use a new export filename
when making a new assessment snapshot. The repository's former text-format
rubrics are retained in `benchmark-rubrics-v1.json`; `benchmark-rubrics.json`
describes the current Markdown tree.

Legal, HR and financial scenarios request preliminary analysis or decision
support, distinguish professional advice, and use supplied synthetic rules and
figures. Research tasks use labelled evidence packets. These closed-book fixtures
measure reasoning from fixed inputs rather than current-law recall or live search.

Record criterion-level scores and material errors alongside the model, runtime,
input hash, latency and resource measurements. Use domain/capability results and
repeat runs to inform routing; a total alone can hide failures on security,
privacy, invented evidence or required output format. Legacy prompts have their
own assessment criteria and retain their original instructions.

The runner accepts a domain-relative prompt name, without `.md`, for
example `coding/python-refactor`. Population does not run any model benchmarks.

## Checks

```sh
python3 -m unittest discover -s experiments -p 'test_*.py'
bash -n experiments/run-benchmark.sh
```

Checks run entirely in temporary directories and cover inventory, metadata,
standalone execution, migration, exact body preservation, dry-run behaviour,
repeatability, hashes, unknown paths and symlink rejection. Runner integration
checks mock Ollama, network requests and hardware telemetry; no model runs occur.
