# Perplexity / pplx CLI

[`models.json`](models.json) records the installed Perplexity CLI and its
research tools. The installed CLI does not expose selectable generation models,
so its `models` list is empty and the observed operations appear under `tools`.

## Initial observations: 2026-09-14

- Executable: `/home/sam-dev/.local/bin/pplx`.
- Build version: `2026.07.30.1785394496+1b7382b`, reported by `pplx --version`.
- Installer receipt: `~/.config/pplx/pplx-receipt.json`.
- Installer source: `github:perplexityai/perplexity-cli`.
- API-key authentication: reported by the operator; successful authentication
  and account access were not tested.

| Operation | Command | Local evidence |
| --- | --- | --- |
| Web search | `pplx search web` | Command help advertises structured search results |
| Query-relevant page snippets | `pplx content snippets` | Command help advertises snippets from supplied URLs |
| Page content fetching | `pplx content fetch` | Command remains present in this installed build |

Perplexity's documentation deprecates `content fetch` and directs new usage to
`content snippets`. Its CLI documentation describes search and snippet access;
it does not establish access to particular Sonar or third-party generation
models. See the [official CLI guide](https://docs.perplexity.ai/docs/cli/overview).

The provider also has separate model APIs. Registering those requires evidence
for the relevant endpoint and callable model IDs; installing this CLI alone
does not supply that evidence. See the [API overview](https://docs.perplexity.ai/docs/getting-started/quickstart).

## Inspect and refresh

Local help is available without submitting a research query:

```sh
pplx --help
pplx search web --help
pplx content snippets --help
```

Refresh all local catalogs from the repository root:

```sh
python3 models/refresh-catalogs.py
```

For Perplexity, the refresh inspects version/help output and selected receipt
metadata. It does not run search, fetch pages, generate snippets, or authenticate
with the API. The catalog records API-key access as `operator_reported` and
leaves `current_access_verified` false. No key is copied into this directory.

When evaluating a model with Perplexity search, record the model's identity
separately from the tool version, search configuration, and retrieved context.
This keeps model-only and model-plus-tools evaluations distinguishable.
