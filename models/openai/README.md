# OpenAI / Codex subscription

[`models.json`](models.json) contains the model entries visible in the local
Codex cache, along with selected configuration and capability fields.

## Initial inventory: 2026-09-14

| Model ID | Description from the local cache |
| --- | --- |
| `gpt-6-astra` | Complex, demanding work |
| `gpt-5.6-sol` | General agentic work |
| `gpt-5.6-terra` | Everyday coding |
| `gpt-5.6-luna` | Fast, economical coding |
| `gpt-5.5` | Previous generation coding and general work |

The user configuration selects `gpt-6-astra` with `ultra` reasoning effort.
Codex authentication was observed in `chatgpt` mode; credentials are not part
of this inventory.

Source: `~/.codex/models_cache.json`, fetched at
`2026-09-14T15:38:17.021232058Z` by client version `0.154.0`, plus selected
fields from `~/.codex/config.toml`. Entries hidden by the cache are omitted.

Context-window and reasoning fields in the JSON describe this local Codex
cache. They are not a statement of the maximum capacity available through
other OpenAI products. A cached listing does not guarantee a request will
succeed under the account's current limits.

## Select and refresh

Open Codex and use `/model` to inspect its model picker. To start with a
specific model:

```sh
codex --model gpt-6-astra
```

After the CLI updates its cache, refresh this inventory from the workspace:

```sh
python3 models/refresh-catalogs.py
```

See the [official model and selection documentation](https://learn.chatgpt.com/docs/models)
for selection commands and current availability rules. The machine's observed
list above is intentionally based on its local cache.
