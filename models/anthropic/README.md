# Anthropic / Claude Code subscription

[`models.json`](models.json) records model IDs found in Claude Code's local
usage summary and additional picker cache, plus selected user-level settings.

## Initial observations: 2026-09-14

| Model ID | Evidence |
| --- | --- |
| `claude-fable-5-1[1m]` | Cached additional picker option, labelled Fable |
| `claude-fable-5` | Historical local usage |
| `claude-opus-5` | Historical local usage |
| `claude-opus-4-8` | Historical local usage |
| `claude-haiku-4-5-20251001` | Historical local usage |

Source: the model IDs in `~/.claude/stats-cache.json`, last computed on
`2026-09-13`. Usage amounts and conversation history are not copied.
The Fable 5.1 entry comes from `additionalModelOptionsCache` in
`~/.claude.json`, with a recorded cache time of `2026-09-14T14:53:51.145Z`.
This cache contains additional picker options, not the complete selection.

`~/.claude/settings.json` sets effort to `xhigh` and has no explicit `model`
or `availableModels` setting. Claude Code reported being logged in through
`claude.ai`, with the first-party provider. Credentials are not part of this
inventory.

These observations do not establish which models the subscription can use
today. Each entry has `current_access_verified: false`. Models
that have never been used may also be available.

## Inspect current selection and refresh

Start Claude Code and enter `/model` to open its current picker. The picker
also provides access and usage-credit information when applicable. A model
can be selected at startup, for example:

```sh
claude --model opus
```

Aliases such as `opus`, `sonnet`, `haiku`, and `fable` can resolve differently
as the CLI and provider change. Record the resolved full model ID when
comparing benchmark results. See the [official model configuration documentation](https://code.claude.com/docs/en/model-config).

After Claude Code updates its local usage summary, refresh the inventory
from the workspace:

```sh
python3 models/refresh-catalogs.py
```

The refresh command imports local observations; it does not query the live
picker or turn historical records into verified current access.
