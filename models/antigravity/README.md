# Google / Antigravity CLI

[`models.json`](models.json) records the installed Antigravity CLI (`agy`),
its version, the model preference saved in its settings, and the account's
model list once an operator has recorded one. Antigravity CLI replaced Gemini
CLI on this machine, and the earlier Gemini CLI catalog was removed.

## Initial observations: 2026-09-27

- Executable: `/home/sam-dev/.local/bin/agy`, a single binary installed with
  the official install script on 2026-09-27.
- Version: `1.2.12`, reported by `agy --version`.
- `~/.gemini/antigravity-cli/settings.json` has no `model` or `modelProvider`
  key. `configured.model` is therefore `null`, and the Gemini API-key route is
  not configured.
- The first session's log (22:32) records the selected model label
  `Gemini 3.8 Flash (High)`. No model preference had been saved, so this was
  most likely the default at the time. The refresh does not read logs, so this
  is recorded only here. The sign-in route and plan were not recorded: the
  catalog keeps `authentication_evidence: "not_checked"` and
  `current_access_verified: false`.
- No model list has been recorded yet. `observed-models.json` is absent, so
  `models` is empty.

## Where the model list comes from

No local file lists Antigravity models. After sign-in, `agy` asks Google for
the account's models at run time; its log records a `fetchAvailableModels`
request. Before sign-in it skips that request and has an empty list. The list
depends on the plan and the sign-in route. The
[models page](https://antigravity.google/docs/models) excludes third-party
models for Enterprise accounts, and the
[Enterprise page](https://antigravity.google/docs/enterprise) says sign-in with
Application Default Credentials excludes models older than Gemini 3 Flash. The
Gemini API-key route uses a model list built into the CLI.

Each reasoning-effort variant has its own slug and label, for example
`gemini-3.8-flash-high`, labelled `Gemini 3.8 Flash (High)`. The binary embeds
many model names, but they include legacy and internal names and say nothing
about the account's entitlement, so the refresh does not scan it.

The catalog's model entries therefore come only from an operator-recorded
snapshot of `agy models`, stored as `observed-models.json` in this directory
(see [below](#record-a-model-list-observation)).

## What the refresh reads

- `~/.gemini/antigravity-cli/settings.json`, if present. Only two keys are
  used:
  - `model` is the picker label that `/model` saves when the default is
    changed. This comes from reports in the CLI's issue tracker; the key has
    not yet been seen on this machine. It is copied to `configured.model` and
    is a display name, not a slug. The value must look like a label: at most
    128 printable characters on one line, with no surrounding spaces and
    nothing that looks like an email address, a URL or a Google API key
    (`@`, `://` or `AIza`). Any other value stops the refresh with an error
    that names only the key and the file, and the catalog is left unchanged.
  - `modelProvider` set to the string `gemini`, its only accepted value,
    selects the Gemini API-key route. The catalog then shows
    `access_method: "antigravity_cli_gemini_api_key"` and
    `authentication_evidence: "settings_model_provider"`. Any other string is
    ignored, as the CLI ignores it. A value that is not a string is treated
    as invalid settings, and the catalog is left unchanged.

  Nothing else is copied, so trusted workspace paths and display settings
  stay out of the catalog.
- The `agy` executable. The refresh looks for it in this order:
  `--antigravity-binary`, then `agy` on `PATH`, then `~/.local/bin/agy`. A
  missing CLI is recorded as `installed: false`. When the CLI is present, the
  refresh records its path and modification time and runs only
  `agy --version`, inside a
  [bubblewrap](https://github.com/containers/bubblewrap) (`bwrap`) sandbox:
  - new user, network, PID, IPC and UTS namespaces leave the command only a
    loopback interface, so it cannot reach the network;
  - the home directory is replaced by an empty file system, so the command
    cannot read or change `~/.gemini`, `~/.config/gcloud` or the keyring
    files. This covers both `$HOME` and the account's home directory, which
    `agy` looks up whatever `HOME` says;
  - `/run/user/<uid>`, which holds the D-Bus and keyring sockets, `/tmp`,
    `/var/tmp` and the temporary directory are replaced in the same way;
  - only the executable (read-only) and a throwaway directory are mounted
    back. `HOME`, the XDG directories, `TMPDIR` and the working directory
    point to that directory;
  - `AGY_CLI_DISABLE_AUTO_UPDATE=true`, the documented switch for the
    background self-updater, is set;
  - only `PATH`, `LANG` and `LC_ALL` are passed through, so no API key, token
    or D-Bus session address reaches the command;
  - input is closed, error output is discarded, the command has 10 seconds
    to finish, and its output is limited to 64 KiB;
  - the output is accepted only if it is a bare version such as `1.2.12`.

  If `bwrap` is missing or cannot create the namespaces, `agy` does not run:
  the refresh reports an error and leaves the Antigravity catalog unchanged.
  On Ubuntu, `bwrap` comes from the `bubblewrap` package. The sandbox does
  not depend on how a given `agy` release behaves, which matters because
  `agy` updates itself during interactive use. A traced run of version
  1.2.12 also showed that `agy --version` opens no network socket, writes no
  file and starts no other process.
- The model-list snapshot, if present: `observed-models.json` in this
  directory, or the file given with `--antigravity-model-observations`.

Reasoning effort has no separate settings key. It is part of the model slug
and label, or is set for a single run with `--effort`. The installed 1.2.12
help lists `low`, `medium`, `high` and `max`, while the
[headless guide](https://antigravity.google/docs/cli/headless) lists only the
first three. `configured.reasoning_effort` is therefore always `null`.

## What it does not read or establish

Antigravity CLI shares `~/.gemini` with the retired Gemini CLI, so
`--antigravity-home` defaults to that directory. Antigravity keeps its own
state in `~/.gemini/antigravity-cli/` and `~/.gemini/config/`. The Gemini CLI
files, such as its own `settings.json`, `google_accounts.json`,
`installation_id`, `history/` and `tmp/`, remain alongside them. The refresh
reads none of these; its only read under `~/.gemini` is
`antigravity-cli/settings.json`. In particular, it does not read:

- account and credential data: `google_accounts.json`, which holds account
  email addresses; OAuth tokens, which the CLI keeps in the operating
  system's keyring or, without D-Bus, in files under `antigravity-cli/`; and
  `~/.gemini/antigravity/mcp_oauth_tokens.json`;
- installation and project identifiers, including `~/.gemini/config/projects/`,
  whose per-project settings can override `settings.json`;
- logs, which hold workspace paths and conversation, project and trace
  identifiers;
- conversations: `conversation_summaries.db`, `conversations/`,
  `history.jsonl` and the protobuf state files;
- MCP configuration in `~/.gemini/config/mcp_config.json`. It describes
  tools, not models, and its `env` and header entries can carry tokens.

The catalog does not establish sign-in, plan, quota, model access or
successful inference. `current_access_verified` stays `false`.

## Record a model-list observation

The refresh never runs `agy models`, because the command needs a signed-in
session, contacts Google and can take several seconds. The operator runs it
instead, from the repository root in a signed-in terminal:

```sh
(
  set -eu
  snapshot=$(mktemp)
  trap 'rm -f "$snapshot"' EXIT
  observed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  client_version=$(AGY_CLI_DISABLE_AUTO_UPDATE=true agy --version)
  AGY_CLI_DISABLE_AUTO_UPDATE=true agy --output-format json models </dev/null |
    jq -e --arg observed_at "$observed_at" --arg client_version "$client_version" '
      .command.data.models as $models
      | if .status != "SUCCESS" or .command.name != "models"
          or ($models | type) != "array" or ($models | length) == 0
          or any($models[]; (.id | type) != "string" or (.label | type) != "string")
        then error("unexpected agy models output")
        else {
          schema_version: 1,
          observed_at: $observed_at,
          evidence: "agy_models_command",
          client_version: $client_version,
          list_complete: true,
          models: [$models[] | select(.id | IN("auto", "recommended") | not)
                   | {id, display_name: .label}]
        } end' >"$snapshot"
  python3 models/refresh-catalogs.py --check-antigravity-model-observations "$snapshot"
  mv "$snapshot" models/antigravity/observed-models.json
  python3 models/refresh-catalogs.py
)
```

`--output-format json` must come before `models`. Closing standard input
avoids a hang that some versions show on an open pipe. The steps run in a
subshell with `set -eu`, so the first failure stops them, including the final
refresh. Do not chain the subshell with `&&` or `||`: the shell then ignores
`set -e` inside it. The jq filter stops
with an error unless the output matches the format reported for Antigravity
CLI 1.1.12 and later and holds a non-empty list whose entries all have a
string `id` and `label`. It keeps only each model's slug and label, and leaves
out the selection aliases `auto` and `recommended` in case the list includes
them. The refresh script then checks the temporary file against the rules
below. The tracked snapshot is replaced only when both checks pass. Otherwise
the earlier snapshot is left in place, and the temporary file is always
removed.

Plain `agy models` prints the same list, one slug and label per line. A
hand-copied list uses the same file format, with `list_complete: false` if any
entries were left out. Check it with
`python3 models/refresh-catalogs.py --check-antigravity-model-observations PATH`
before it replaces the tracked file.

The refresh validates the snapshot strictly, and the check option applies the
same rules without refreshing anything:

- it must contain exactly these six fields;
- `observed_at` must be in UTC and not in the future;
- `client_version` must be a bare version number;
- `models` must be a non-empty list whose entries hold only an `id` and a
  `display_name`;
- each `id` must be a unique slug of at most 128 lower-case letters, digits,
  `.`, `_` and `-`, such as `gemini-3.8-flash-high`. Anything containing
  `/`, `:` or `@` is refused, including resource names such as
  `projects/…/models/…` that can embed a Google Cloud project ID. The
  selection aliases `auto` and `recommended` are refused too;
- each `display_name` must be unique, because settings save a label rather
  than a slug, and must look like a label: at most 128 printable characters
  on one line, with no surrounding spaces and nothing that looks like an
  email address, a URL or a Google API key.

An empty list is rejected, because `agy` returns one before sign-in. Each
model becomes an entry with `availability: "listed_in_agy_model_list"`, the
snapshot's `observed_at` and `current_access_verified: false`. The catalog
also gains `model_list_observed_at` and `model_list_complete`. Refreshing keeps
the original observation time, while `generated_at` records when the catalog
was written. If the installed client's version differs from the snapshot's
`client_version`, `model_list_scope` says so.

The snapshot does not record the sign-in route or plan, so note both here
when recording one. Record a new snapshot after any change to the account,
plan, sign-in route or client.

## Select a model

In an interactive `agy` session, `/model` opens the picker and saves the
choice as the default. For a single run, pass a slug from `agy models`, or a
base name with `--effort`. The changelog says `--effort` selects the
model's effort variant, but the documented examples use full slugs, and the
base-name form has not been tried on this machine:

```sh
agy --model gemini-3.8-flash-high
agy --model gemini-3.1-pro --effort low
```

For benchmarks, record the client version, the requested slug and the effort,
not just the label. See the
[CLI overview](https://antigravity.google/docs/cli/overview), the
[headless guide](https://antigravity.google/docs/cli/headless),
[installation and sign-in](https://antigravity.google/docs/cli/install) and
[migrating from Gemini CLI](https://antigravity.google/docs/cli/gcli-migration).

The [Antigravity terms](https://antigravity.google/terms) forbid using
third-party software to access the service with an Antigravity sign-in, so
only `agy` itself should use this machine's sign-in. For third-party coding
agents, the [FAQ](https://antigravity.google/docs/faq) recommends a Gemini
Enterprise or Google AI Studio API key. The current
`experiments/run-benchmark.sh` runner supports llama.cpp only. This catalog
does not add Antigravity benchmark runs.

## Refresh

Refresh all local catalogs from the repository root:

```sh
python3 models/refresh-catalogs.py
```

Use `--antigravity-home PATH` for a different shared home (default
`~/.gemini`), `--antigravity-binary PATH` to choose the executable, and
`--antigravity-model-observations PATH` to use a different snapshot.
`--check-antigravity-model-observations PATH` validates a snapshot and exits
without refreshing any catalog. When `agy` is installed, the refresh needs
`bwrap` for the version probe.
