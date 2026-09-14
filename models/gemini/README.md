# Google / Gemini CLI

[`models.json`](models.json) records Gemini model IDs declared in the installed
CLI package, the CLI version, and selected user-level settings.

## Initial observations: 2026-09-14

Gemini CLI `0.59.0` is installed. `~/.gemini/settings.json` selects
`security.auth.selectedType = "gemini-api-key"`, matching the API-key setup
reported by the operator. It contains no explicit `model.name` preference.

The installed CLI defaults to the `auto` selection alias. The model actually
used can depend on runtime settings, routing, and access. This inventory does
not resolve an exact model or snapshot from that alias.

| Model ID | Evidence |
| --- | --- |
| `gemini-3.5-flash` | Bundled CLI model constant |
| `gemini-3.1-pro-preview` | Bundled CLI model constant |
| `gemini-3.1-pro-preview-customtools` | Bundled CLI model constant |
| `gemini-3.1-flash-lite` | Bundled CLI model constant |
| `gemini-3-pro-preview` | Bundled CLI model constant |
| `gemini-3-flash-preview` | Bundled CLI model constant |
| `gemini-3-flash` | Bundled CLI model constant |
| `gemini-2.5-pro` | Bundled CLI model constant |
| `gemini-2.5-flash` | Bundled CLI model constant |

The initial model source is the `packages/core/dist/src/config/models.js`
section of the installed package's `bundle/chunk-YSBB75DZ.js`. The refresh
command discovers the package from the `gemini` executable and reads Gemini
IDs referenced by its `VALID_GEMINI_MODELS` set. It does not execute the bundle.

This is a scoped inventory of client declarations. Other models may appear
in dynamic CLI configuration or the provider catalog. Gemma models, placeholder
values, and the separate embedding constant are outside this inventory.

Every listed entry has `availability: "declared_by_installed_cli"` and
`current_access_verified: false`. A bundled identifier does not establish
that the configured API key can use it today. Authentication success, quota,
pricing, and measured capabilities have not been checked by this refresh.

## Select and refresh

Start `gemini` and enter `/model` to inspect its selection dialog. You can
also supply a model at startup with `gemini --model MODEL_ID`. For evaluations,
record the requested identifier and the actual returned model, including any
routing or fallback, rather than treating `auto` as an exact model version.

See the official [model selection](https://geminicli.com/docs/cli/model/),
[model routing](https://geminicli.com/docs/cli/model-routing/), and
[authentication](https://geminicli.com/docs/get-started/authentication/) guides.

Refresh the local catalogs from the repository root:

```sh
python3 models/refresh-catalogs.py
```

The refresh command reads model metadata and the authentication method name.
It does not retrieve, print, or copy the API key, and makes no inference or
model-list API requests.
