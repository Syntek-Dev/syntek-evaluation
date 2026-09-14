# Model inventory

This directory records local model and research-tool discovery information for
Ollama, the Codex and Claude Code subscriptions, Gemini CLI, Perplexity CLI,
and GitHub Copilot CLI.

| Directory | Contents |
| --- | --- |
| [`ollama/`](ollama/) | Symlink to `/var/lib/ollama/models`, containing Ollama's blobs and manifests |
| [`openai/`](openai/README.md) | Codex model metadata, configuration notes, and source dates |
| [`anthropic/`](anthropic/README.md) | Claude Code model metadata, configuration notes, and source dates |
| [`gemini/`](gemini/README.md) | Google Gemini CLI model metadata, configured authentication method, and source dates |
| [`perplexity/`](perplexity/README.md) | Perplexity CLI search/content tools and operator-reported API-key access |
| [`github-copilot/`](github-copilot/README.md) | Observed Copilot account model list, CLI metadata, and saved model preferences |
| `colibri/` | Reserved directory; currently empty |

The hosted-provider directories hold metadata. Their model weights remain with
the provider. Authentication stays in each CLI's existing configuration.

## Refresh the catalogs

From the repository root, run:

```sh
python3 models/refresh-catalogs.py
```

Requires Python 3.11 or newer. This reads selected fields from local CLI caches,
settings, and installed package metadata and updates each provider's
`models.json`. For Perplexity it also runs local `pplx --version` and command
`--help` queries. It makes no API requests, runs no model prompts, and does not
read or copy credential files.
For Copilot, it checks executable presence, reads an installed `@github/copilot`
package manifest when available, and reads only model/reasoning preferences from
`settings.json`. For standalone installations, it queries only the local CLI
version with auto-update disabled and temporary settings. It also reads the
tracked `github-copilot/observed-models.json` account snapshot, retaining its
observation date. A missing CLI is recorded normally. Use `--copilot-home PATH`
and `--copilot-binary PATH` to inspect non-default installations, or
`--copilot-model-observations PATH` to supply a different model snapshot.
The provider README tables record the initial inventory on 2026-09-14; use the
JSON files for subsequently refreshed metadata.

## Interpret availability

- `listed_in_codex_cache`: visible in the locally cached Codex model list at
  its recorded fetch time.
- `listed_in_claude_picker_cache`: present in Claude Code's cache of additional
  model picker options. This cache does not contain its complete model list.
- `declared_by_installed_cli`: a model ID or tool command advertised by an
  installed CLI; this describes client support, not verified account access.
- `configured_model_preference`: a model ID saved in Copilot CLI settings;
  this records a preference without establishing account access.
- `listed_in_copilot_model_picker`: a model offered in the recorded Copilot CLI
  account session; the observation date remains separate from the refresh date.
- `blocked_by_copilot_plan`: a model the picker marked as excluded from the
  observed account's plan; these entries appear under `unavailable_models`.
- `historically_observed`: present in Claude Code's local model usage summary;
  this does not establish current access or the complete model selection.
- `configured.model`: the model preference in the user-level settings file;
  session, project, environment, and managed settings can override it.

Perplexity's installed `pplx` interface has search/content tools rather than
selectable generation models. Its catalog has an empty `models` list and a
separate `tools` list. Empty here means no model IDs established through this
CLI, not that the provider has no model APIs.

Refreshing these files does not refresh the CLI caches themselves. For Codex,
Claude Code, Gemini, and Copilot, open the CLI and use `/model` to inspect its current
selection. See
[Codex model selection](https://learn.chatgpt.com/docs/models),
[Claude Code model selection](https://code.claude.com/docs/en/model-config), and
[Gemini CLI model selection](https://geminicli.com/docs/cli/model/).
For Copilot, see the
[CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).
For Perplexity, inspect `pplx --help` and the
[official CLI documentation](https://docs.perplexity.ai/docs/cli/overview).

Codex and Claude Code are recorded for subscription use; Gemini CLI is recorded
with its configured authentication method, and Perplexity API-key access is
recorded as operator-reported. Copilot's README records the operator's login
confirmation; its automated catalog does not check authentication, subscription
plan, or model access. These local observations do not
establish successful live authentication, account access to every listed model,
remaining usage allowance, or whether a selected model requires extra credits.
