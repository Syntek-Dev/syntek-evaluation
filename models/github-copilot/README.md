# GitHub / Copilot CLI

[`models.json`](models.json) records the observed account model list, local
GitHub Copilot CLI installation metadata, and explicit model preferences.
This catalog covers the CLI;
Copilot in VS Code and other clients can offer different model selections.

## Initial observations: 2026-09-14

- Standalone executable: `/home/sam-dev/.local/bin/copilot`.
- Installed version: `1.0.83`, observed using the local `--version` option.
- Login was confirmed by the operator on 2026-09-14 and is recorded here.
  The automated catalog keeps `authentication_evidence: "not_checked"`, because
  refreshing local metadata does not verify authentication. The subscription
  plan is unknown (`null`), and `current_access_verified` remains `false`.
- `~/.copilot/settings.json` was absent. The existing `config.json` was not read.
- The authenticated CLI's model picker showed **17 available models** and
  **10 models excluded by the account's plan**.
- The initial session default was `gpt-5.6-terra` with `medium` reasoning.
  This appears as `observed_selection`; the `configured` fields remain `null`
  because no saved preference was read from `settings.json`.

The picker and the `/model` command's validation response supplied the model
names and exact IDs. The check used no generation prompts. The session was
closed after inspection.

| Available model ID | Picker name |
| --- | --- |
| `claude-sonnet-5` | Claude Sonnet 5 |
| `claude-haiku-4.5` | Claude Haiku 4.5 |
| `gpt-5.6-terra` | GPT-5.6 Terra |
| `gpt-5.6-luna` | GPT-5.6 Luna |
| `gpt-5.4` | GPT-5.4 |
| `gpt-5.4-mini` | GPT-5.4 mini |
| `gpt-5.3-codex` | GPT-5.3-Codex |
| `gpt-5-mini` | GPT-5 mini |
| `mai-code-1.1-flash` | MAI-Code-1.1-Flash |
| `gemini-3.8-flash` | Gemini 3.8 Flash |
| `gemini-3.7-flash` | Gemini 3.7 Flash |
| `gemini-3.6-flash` | Gemini 3.6 Flash |
| `gemini-3.5-flash` | Gemini 3.5 Flash |
| `grok-4.5` | Grok 4.5 |
| `kimi-k3` | Kimi K3 |
| `kimi-k2.7-code` | Kimi K2.7 Code |
| `grok-4.6` | Grok 4.6 |

The picker marked these models as outside the current plan:
`claude-fable-5.1`, `claude-fable-5`, `claude-opus-5`, `claude-opus-4.8`,
`claude-opus-4.8-fast`, `claude-opus-4.7`, `claude-sonnet-4.6`, `gpt-5.6-sol`,
`gpt-5.5`, and `mai-code-1-flash-picker`. They appear under `unavailable_models`
in the generated catalog. `auto` is recorded separately as a routing selector.

`access_method: "github_copilot_cli"` identifies the client route. The reported
login and picker listing do not establish successful inference for each model.

Available models depend on the Copilot plan, client, administrator policies,
and current provider availability. See [model availability](https://docs.github.com/en/copilot/concepts/models/overview).
The account's plan can be checked in GitHub Settings under Billing & licensing;
see [viewing your Copilot plan](https://docs.github.com/en/copilot/how-tos/manage-your-account/view-and-change-your-copilot-plan).

## Inspect and refresh

Refresh all local catalogs from the repository root:

```sh
python3 models/refresh-catalogs.py
```

For Copilot, the refresh checks executable presence and reads an ancestor
`package.json` for the `@github/copilot` package's version when available.
For standalone installations, it runs only `--no-auto-update --version`, using
a temporary `COPILOT_HOME` and working directory, `CI=1`, and an environment
that excludes authentication tokens. Both installation types are supported by
the [official installation guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli).

The optional `settings.json` file supports JSON with comments. Only `model`
and `effortLevel` are copied into the configured model and reasoning fields.
`--copilot-home` overrides the directory, which defaults to `COPILOT_HOME`
when set, otherwise `~/.copilot`. `--copilot-binary` overrides executable
discovery. See the [configuration reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference).

[`observed-models.json`](observed-models.json) is the input snapshot from the
interactive check. Refreshing reads it and retains its original `observed_at`
timestamp; `generated_at` records when the catalog was written. Use
`--copilot-model-observations PATH` to supply a different snapshot. Update the
snapshot after checking the picker again, especially after account, plan, policy,
or client changes. An offline refresh does not establish a fresh account list.

The refresh does not start a Copilot session, authenticate, submit a model
request, or read `config.json` or credential files. It avoids the separate
`version` subcommand, which checks for updates. No documented offline account
model inventory command was identified; generic help examples are not model
evidence.
Snapshot entries use `listed_in_copilot_model_picker` or `blocked_by_copilot_plan`
as their availability evidence. Every entry retains
`current_access_verified: false` because inference was not tested. An additional
explicit model preference becomes an entry with
`availability: "configured_model_preference"` and
`current_access_verified: false`; a saved preference does not establish access.
`auto` remains a configured selector and is excluded from model IDs.

In an authenticated Copilot CLI session, enter `/model` to inspect the models
offered to that account. See the
[CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).
For VS Code, use the Chat model picker or `Chat: Manage Language Models`;
its provider list can include separately configured models. See
[VS Code language models](https://code.visualstudio.com/docs/agent-customization/language-models).

For benchmarks, record the client and version, requested model, actual model
used, and relevant tool settings. Resolve any automatic selection or fallback
in the run record. The current `experiments/run-benchmark.sh` runner supports
Ollama only; adding this catalog does not add Copilot benchmark execution.
