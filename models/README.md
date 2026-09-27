# Model inventory

This directory records model and research-tool discovery information for the
Codex and Claude Code subscriptions, Google's Antigravity CLI, and Perplexity
CLI.

| Directory | Contents |
| --- | --- |
| [`openai/`](openai/README.md) | Codex model metadata, configuration notes, and source dates |
| [`anthropic/`](anthropic/README.md) | Claude Code model metadata, configuration notes, and source dates |
| [`antigravity/`](antigravity/README.md) | Antigravity CLI version, saved model preference, and operator-recorded account model list |
| [`perplexity/`](perplexity/README.md) | Perplexity CLI search/content tools and operator-reported API-key access |

The hosted-provider directories hold metadata. Their model weights remain with
the provider. Authentication stays in each CLI's existing configuration.

Self-hosted models served through llama.cpp are not catalogued here yet. A
benchmark record carries the serving details for its run instead: the
`llama_server` block names the model file, context size and slots (see
[the benchmark documentation](../experiments/BENCHMARKS.md)).

## Refresh the catalogs

From the repository root, run:

```sh
python3 models/refresh-catalogs.py
```

Requires Python 3.11 or newer, plus bubblewrap (`bwrap`) when Antigravity CLI
is installed. This reads selected fields from local CLI caches,
settings, and installed package metadata and updates each provider's
`models.json`. For Perplexity it also runs local `pplx --version` and command
`--help` queries. It makes no API requests, runs no model prompts, and does not
read or copy credential files.
For Antigravity CLI, it reads only the `model` and `modelProvider` settings
from `~/.gemini/antigravity-cli/settings.json` (Antigravity CLI shares
`~/.gemini` with the retired Gemini CLI). It runs local `agy --version` in a
bubblewrap sandbox with no network access, the home directory hidden and
auto-update disabled. Without bubblewrap it does not run `agy`, and it leaves
the Antigravity catalog unchanged. It also reads the tracked
`antigravity/observed-models.json` snapshot when present, keeping its
observation time. It never runs `agy models`, which contacts Google, so the
Antigravity model list stays empty until an operator records a snapshot. A
missing CLI is recorded normally. Use `--antigravity-home PATH`,
`--antigravity-binary PATH` and `--antigravity-model-observations PATH` for
other locations.
The provider READMEs record the initial inventory on 2026-09-14
(2026-09-27 for Antigravity); use the JSON files for subsequently refreshed
metadata.

## Interpret availability

- `listed_in_codex_cache`: visible in the locally cached Codex model list at
  its recorded fetch time.
- `listed_in_claude_picker_cache`: present in Claude Code's cache of additional
  model picker options. This cache does not contain its complete model list.
- `listed_in_agy_model_list`: listed by `agy models` in an operator-recorded
  Antigravity snapshot; the observation time is kept separate from the
  refresh time, and the list depends on the account's plan and sign-in route.
- `declared_by_installed_cli`: a tool command advertised by an installed CLI;
  this describes client support, not verified account access.
- `historically_observed`: present in Claude Code's local model usage summary;
  this does not establish current access or the complete model selection.
- `configured.model`: the model preference in the user-level settings file;
  session, project, environment, and managed settings can override it.
  Antigravity CLI saves the picker label here, such as
  `Gemini 3.8 Flash (High)`, rather than a model slug.

Perplexity's installed `pplx` interface has search/content tools rather than
selectable generation models. Its catalog has an empty `models` list and a
separate `tools` list. Empty here means no model IDs established through this
CLI, not that the provider has no model APIs.

Refreshing these files does not refresh the CLI caches themselves. For Codex,
Claude Code, and Antigravity CLI, open the CLI and use `/model` to inspect its
current selection. See
[Codex model selection](https://learn.chatgpt.com/docs/models),
[Claude Code model selection](https://code.claude.com/docs/en/model-config), and
[Antigravity models](https://antigravity.google/docs/models).
For Antigravity, the operator records the account's list with `agy models`
as described in [its README](antigravity/README.md#record-a-model-list-observation).
For Perplexity, inspect `pplx --help` and the
[official CLI documentation](https://docs.perplexity.ai/docs/cli/overview).

Codex and Claude Code are recorded for subscription use, and Perplexity API-key
access is recorded as operator-reported. Antigravity CLI is recorded with
`authentication_evidence: "not_checked"`, unless its settings select the
Gemini API-key route. These local observations do not
establish successful live authentication, account access to every listed model,
remaining usage allowance, or whether a selected model requires extra credits.
