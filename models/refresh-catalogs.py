#!/usr/bin/env python3
"""Refresh model metadata from local CLI caches and installations, without network calls."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib


class CatalogError(Exception):
    """A source could not be read safely as model metadata."""


def utc_timestamp(timestamp=None):
    value = datetime.now(timezone.utc) if timestamp is None else datetime.fromtimestamp(
        timestamp, timezone.utc
    )
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def read_object(path, *, optional=False, toml=False):
    try:
        raw = path.read_text(encoding="utf-8")
        data = tomllib.loads(raw) if toml else json.loads(raw)
    except FileNotFoundError:
        if optional:
            return {}, None
        raise CatalogError(f"missing source: {path}") from None
    except (ValueError, UnicodeError, RecursionError):
        kind = "TOML" if toml else "JSON"
        raise CatalogError(f"invalid {kind}: {path}") from None
    except OSError:
        raise CatalogError(f"cannot read source: {path}") from None
    if not isinstance(data, dict):
        raise CatalogError(f"expected an object: {path}")
    return data, {"path": str(path), "modified_at": utc_timestamp(path.stat().st_mtime)}


def optional_string(data, key, path):
    value = data.get(key)
    if value is not None and not isinstance(value, str):
        raise CatalogError(f"invalid {key}: {path}")
    return value


def string_list(value, key, path):
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise CatalogError(f"invalid {key}: {path}")
    return value


def openai_catalog(home):
    cache_path = home / "models_cache.json"
    cache, source = read_object(cache_path)
    entries = cache.get("models")
    if not isinstance(entries, list):
        raise CatalogError(f"missing or invalid models list: {cache_path}")
    source["fetched_at"] = optional_string(cache, "fetched_at", cache_path)
    models = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise CatalogError(f"invalid model entry: {cache_path}")
        if entry.get("visibility") != "list":
            continue
        model_id = optional_string(entry, "slug", cache_path)
        if not model_id:
            raise CatalogError(f"missing model slug: {cache_path}")
        context_window = entry.get("context_window")
        if context_window is not None and (
            type(context_window) is not int or context_window <= 0
        ):
            raise CatalogError(f"invalid context_window: {cache_path}")
        levels = entry.get("supported_reasoning_levels", [])
        if not isinstance(levels, list) or any(
            not isinstance(level, dict) or not isinstance(level.get("effort"), str)
            for level in levels
        ):
            raise CatalogError(f"invalid supported_reasoning_levels: {cache_path}")
        models.append({
            "id": model_id,
            "display_name": optional_string(entry, "display_name", cache_path),
            "description": optional_string(entry, "description", cache_path),
            "availability": "listed_in_codex_cache",
            "context_window_tokens": context_window,
            "context_window_source": "local_codex_cache",
            "input_modalities": string_list(
                entry.get("input_modalities", []), "input_modalities", cache_path
            ),
            "default_reasoning_effort": optional_string(
                entry, "default_reasoning_level", cache_path
            ),
            "supported_reasoning_efforts": [level["effort"] for level in levels],
        })

    config_path = home / "config.toml"
    config, config_source = read_object(config_path, optional=True, toml=True)
    return {
        "provider": "openai",
        "access_method": "codex_subscription",
        "generated_at": utc_timestamp(),
        "sources": [item for item in (source, config_source) if item is not None],
        "configured": {
            "model": optional_string(config, "model", config_path),
            "reasoning_effort": optional_string(config, "model_reasoning_effort", config_path),
        },
        "models": models,
    }


def anthropic_catalog(home, state_path):
    stats_path = home / "stats-cache.json"
    stats, source = read_object(stats_path)
    usage = stats.get("modelUsage")
    if not isinstance(usage, dict) or any(not model_id for model_id in usage):
        raise CatalogError(f"missing or invalid modelUsage object: {stats_path}")
    source["last_computed_date"] = optional_string(stats, "lastComputedDate", stats_path)
    settings_path = home / "settings.json"
    settings, settings_source = read_object(settings_path, optional=True)
    available_models = settings.get("availableModels")
    if available_models is not None:
        available_models = string_list(available_models, "availableModels", settings_path)

    state, state_source = read_object(state_path, optional=True)
    options = state.get("additionalModelOptionsCache", [])
    if not isinstance(options, list):
        raise CatalogError(f"invalid additionalModelOptionsCache: {state_path}")
    answered_at = state.get("additionalModelOptionsAnsweredAt")
    if answered_at is not None and (type(answered_at) is not int or answered_at < 0):
        raise CatalogError(f"invalid additionalModelOptionsAnsweredAt: {state_path}")
    if state_source is not None:
        state_source["additional_model_options_answered_at_unix_ms"] = answered_at
    models = {
        model_id: {
            "id": model_id,
            "availability": "historically_observed",
            "current_access_verified": False,
            "observed_in_history": True,
        }
        for model_id in usage
    }
    for option in options:
        if not isinstance(option, dict):
            raise CatalogError(f"invalid additional model option: {state_path}")
        model_id = optional_string(option, "value", state_path)
        if not model_id:
            raise CatalogError(f"missing additional model option value: {state_path}")
        models[model_id] = {
            "id": model_id,
            "display_name": optional_string(option, "label", state_path),
            "description": optional_string(option, "description", state_path),
            "availability": "listed_in_claude_picker_cache",
            "current_access_verified": False,
            "observed_in_history": model_id in usage,
        }
    return {
        "provider": "anthropic",
        "access_method": "claude_code_subscription",
        "generated_at": utc_timestamp(),
        "sources": [
            item for item in (source, settings_source, state_source) if item is not None
        ],
        "configured": {
            "model": optional_string(settings, "model", settings_path),
            "reasoning_effort": optional_string(settings, "effortLevel", settings_path),
        },
        "available_models_setting": available_models,
        "model_list_scope": (
            "Historical model IDs and additional picker options from local caches; "
            "not a complete current model list."
        ),
        "models": [models[model_id] for model_id in sorted(models)],
    }


def perplexity_local_metadata(binary, arguments):
    allowed = {
        ("--version",), ("search", "web", "--help"),
        ("content", "fetch", "--help"), ("content", "snippets", "--help"),
    }
    if arguments not in allowed:
        raise CatalogError("unsupported Perplexity metadata command")
    label = " ".join(("pplx", *arguments))
    # Inherit only basic process settings; API keys and tokens are excluded.
    environment = {
        key: os.environ[key] for key in ("PATH", "HOME", "LANG", "LC_ALL")
        if key in os.environ
    }
    try:
        with tempfile.TemporaryFile() as output:
            result = subprocess.run(
                [str(binary), *arguments], stdin=subprocess.DEVNULL,
                stdout=output, stderr=subprocess.DEVNULL, env=environment, timeout=10,
            )
            output.seek(0)
            captured = output.read(65537)
        if result.returncode != 0 or len(captured) > 65536:
            raise CatalogError(f"local metadata command failed or exceeded output limit: {label}")
        return captured.decode("utf-8")
    except (OSError, subprocess.SubprocessError, UnicodeError):
        raise CatalogError(f"cannot read local metadata: {label}") from None


def perplexity_catalog(binary, receipt_path):
    if binary is None:
        executable = shutil.which("pplx")
        if executable is None:
            raise CatalogError("Perplexity CLI is not installed or not on PATH")
        binary = Path(executable).resolve()
    version_output = perplexity_local_metadata(binary, ("--version",)).strip()
    version = re.fullmatch(r"pplx\s+([A-Za-z0-9][A-Za-z0-9.+_-]{0,127})", version_output)
    if version is None:
        raise CatalogError("unrecognized Perplexity CLI version output")
    metadata_commands = [["--version"]]
    tool_entries = []
    for tool_id, command in (
        ("web_search", ("search", "web")),
        ("content_fetch", ("content", "fetch")),
        ("content_snippets", ("content", "snippets")),
    ):
        arguments = (*command, "--help")
        help_output = perplexity_local_metadata(binary, arguments)
        usage = r"^Usage:\s+" + re.escape(" ".join(("pplx", *command))) + r"(?:\s|$)"
        if re.search(usage, help_output, re.MULTILINE) is None:
            raise CatalogError(f"unrecognized Perplexity CLI help: {' '.join(command)}")
        metadata_commands.append(list(arguments))
        tool_entries.append({
            "id": tool_id,
            "command": ["pplx", *command],
            "availability": "declared_by_installed_cli",
            "current_access_verified": False,
        })
    sources = [{
        "path": str(binary), "modified_at": utc_timestamp(binary.stat().st_mtime),
        "metadata_commands": metadata_commands,
    }]
    receipt, receipt_source = read_object(receipt_path, optional=True)
    if receipt_source is not None:
        if receipt.get("binary") != "pplx" or receipt.get("source") != "github:perplexityai/perplexity-cli":
            raise CatalogError(f"unrecognized Perplexity installation receipt: {receipt_path}")
        receipt_source["recorded_version"] = optional_string(receipt, "version", receipt_path)
        receipt_source["installation_source"] = receipt["source"]
        sources.append(receipt_source)
    return {
        "provider": "perplexity",
        "access_method": "perplexity_cli_api_key",
        "authentication_evidence": "operator_reported",
        "current_access_verified": False,
        "generated_at": utc_timestamp(),
        "client": {"name": "pplx", "version": version.group(1)},
        "sources": sources,
        "configured": {"model": None, "reasoning_effort": None},
        "model_list_scope": (
            "No model IDs discovered by this local metadata probe; "
            "the observed commands are search/content tools. "
            "Local help verifies command availability; API access has not been verified."
        ),
        "models": [],
        "tools": tool_entries,
    }


AGY_VERSION = r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]{1,64})?"
# Documented slugs look like gemini-3.8-flash-high. Slashes, colons and "@" are
# excluded, so resource names that embed a project ID cannot reach the catalog.
AGY_MODEL_ID = r"[a-z0-9][a-z0-9._-]{0,127}"
# Selection aliases, not models.
AGY_MODEL_ALIASES = {"auto", "recommended"}
AGY_OBSERVATION_FIELDS = {
    "schema_version", "observed_at", "evidence", "client_version", "list_complete", "models",
}


def is_label(value):
    """Accept a short, single-line display label such as `Gemini 3.8 Flash (High)`.

    Anything that looks like an email address, a URL or a Google API key is
    refused, as are control, format and invisible characters.
    """
    return (
        isinstance(value, str) and 0 < len(value) <= 128 and value == value.strip()
        and value.isprintable() and re.search(r"@|://|AIza", value) is None
    )


def find_antigravity_binary(binary):
    """Locate agy without running it: explicit path, then PATH, then the installer default."""
    if binary is not None:
        executable = Path(binary).resolve()
        if not executable.is_file():
            raise CatalogError(f"missing Antigravity CLI executable: {executable}")
        return executable
    executable = shutil.which("agy")
    if executable is not None:
        return Path(executable).resolve()
    default = Path.home() / ".local/bin/agy"
    if default.is_file() and os.access(default, os.X_OK):
        return default.resolve()
    return None


def antigravity_sandbox(binary, directory):
    """Build the bubblewrap command that runs `agy --version` offline and without the home.

    New user, network, PID, IPC and UTS namespaces leave the command only a
    loopback interface. The user's home directory, the per-user runtime
    directory (D-Bus and keyring sockets) and the temporary directories are
    replaced by empty file systems. Only the executable (read-only) and the
    throwaway home are mounted back. Without bubblewrap the command is not run.
    """
    bwrap = shutil.which("bwrap")
    if bwrap is None:
        raise CatalogError(
            "bubblewrap (bwrap) is required to run agy --version without network access"
        )
    private = [
        Path.home(), Path("/run/user") / str(os.getuid()), Path("/tmp"), Path("/var/tmp"),
        Path(tempfile.gettempdir()),
    ]
    if os.environ.get("XDG_RUNTIME_DIR"):
        private.append(Path(os.environ["XDG_RUNTIME_DIR"]))
    try:
        # agy looks up the account's home with getpwuid, whatever HOME says.
        private.append(Path(pwd.getpwuid(os.getuid()).pw_dir))
    except KeyError:
        pass
    hidden = []
    # Parents first; a directory inside one already hidden needs no mount of its own.
    for path in sorted({path.resolve() for path in private if path.is_dir()},
                       key=lambda path: (len(path.parts), str(path))):
        if path.parent != path and not any(path.is_relative_to(parent) for parent in hidden):
            hidden.append(path)
    command = [
        bwrap, "--die-with-parent", "--new-session",
        # Includes --unshare-net: the command sees only a loopback interface.
        "--unshare-all",
        "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
    ]
    for path in hidden:
        command += ["--tmpfs", str(path)]
    return command + [
        "--ro-bind", str(binary), str(binary),
        "--bind", directory, directory, "--chdir", directory,
        "--", str(binary), "--version",
    ]


def antigravity_version(binary):
    """Run only `agy --version`, in a network-less sandbox that hides the home directory.

    The sandbox from antigravity_sandbox enforces the isolation, so it does not
    depend on how a given agy release behaves; if bubblewrap is missing or
    cannot create the namespaces, agy does not run. HOME, the XDG directories
    and TMPDIR also point to a throwaway directory, the self-updater is
    switched off, and the environment excludes API keys, tokens and the D-Bus
    session address. A traced run of 1.2.12 showed that the command opens no
    network socket, writes no file and starts no other process.
    """
    environment = {
        key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL")
        if key in os.environ
    }
    try:
        with tempfile.TemporaryDirectory(prefix="agy-metadata-") as directory:
            home = Path(directory)
            environment.update({
                "HOME": directory,
                "XDG_CONFIG_HOME": str(home / ".config"),
                "XDG_CACHE_HOME": str(home / ".cache"),
                "XDG_DATA_HOME": str(home / ".local/share"),
                "XDG_STATE_HOME": str(home / ".local/state"),
                "XDG_RUNTIME_DIR": directory,
                "TMPDIR": directory,
                # Only the exact lowercase value disables the self-updater.
                "AGY_CLI_DISABLE_AUTO_UPDATE": "true",
            })
            command = antigravity_sandbox(binary, directory)
            with tempfile.TemporaryFile() as output:
                result = subprocess.run(
                    command, stdin=subprocess.DEVNULL,
                    stdout=output, stderr=subprocess.DEVNULL,
                    cwd=directory, env=environment, timeout=10,
                )
                output.seek(0)
                captured = output.read(65537)
        if result.returncode != 0 or len(captured) > 65536:
            raise CatalogError(
                "Antigravity CLI version command failed, could not be sandboxed "
                "or exceeded output limit"
            )
        version = re.fullmatch(f"({AGY_VERSION})\n?", captured.decode("utf-8"))
        if version is None:
            raise CatalogError("unrecognised Antigravity CLI version output")
        return version.group(1)
    except (OSError, subprocess.SubprocessError, UnicodeError):
        raise CatalogError("cannot read local Antigravity CLI version") from None


def antigravity_model_observations(path):
    """Validate an operator-recorded `agy models` snapshot; the refresh never lists models."""
    if path is None:
        return {}, None
    data, source = read_object(path, optional=True)
    if source is None:
        return data, source

    def invalid(field):
        raise CatalogError(f"invalid Antigravity model observations {field}: {path}") from None

    if set(data) != AGY_OBSERVATION_FIELDS:
        invalid("fields")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        invalid("schema_version")
    if data["evidence"] != "agy_models_command":
        invalid("evidence")
    observed_at = data["observed_at"]
    if not isinstance(observed_at, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)", observed_at,
    ):
        invalid("observed_at")
    try:
        observed = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError:
        invalid("observed_at")
    if observed > datetime.now(timezone.utc):
        invalid("observed_at")
    if not isinstance(data["client_version"], str) or not re.fullmatch(
        AGY_VERSION, data["client_version"]
    ):
        invalid("client_version")
    if type(data["list_complete"]) is not bool:
        invalid("list_complete")

    entries = data["models"]
    # An empty list is what agy returns before sign-in, so it is not evidence.
    if not isinstance(entries, list) or not entries:
        invalid("models")
    model_ids, labels = set(), set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "display_name"}:
            invalid("models entry")
        model_id = entry["id"]
        if (
            not isinstance(model_id, str) or model_id in model_ids
            or model_id in AGY_MODEL_ALIASES or not re.fullmatch(AGY_MODEL_ID, model_id)
        ):
            invalid("model id")
        model_ids.add(model_id)
        # Labels must be unique too: settings save a label, not a slug.
        label = entry["display_name"]
        if not is_label(label) or label in labels:
            invalid("display_name")
        labels.add(label)

    source.update({
        key: data[key] for key in ("schema_version", "observed_at", "evidence", "client_version")
    })
    return data, source


def antigravity_catalog(home, binary, observations_path=None):
    """Record the installed agy client and saved preferences without starting a session.

    Antigravity CLI shares ~/.gemini with the retired Gemini CLI. Only
    antigravity-cli/settings.json is read there; account, credential, log,
    conversation, project and legacy Gemini CLI files are not.
    """
    settings_path = home / "antigravity-cli" / "settings.json"
    settings, settings_source = read_object(settings_path, optional=True)
    model = settings.get("model")
    if model is not None and not is_label(model):
        raise CatalogError(f"invalid model: {settings_path}")
    # Only the exact string "gemini" selects the API-key route, and the CLI
    # ignores any other string. A non-string value is invalid settings.
    api_key_route = optional_string(settings, "modelProvider", settings_path) == "gemini"
    sources = [settings_source] if settings_source is not None else []
    observations, observation_source = antigravity_model_observations(observations_path)
    if observation_source is not None:
        sources.append(observation_source)

    executable = find_antigravity_binary(binary)
    version = None
    if executable is not None:
        version = antigravity_version(executable)
        sources.append({
            "path": str(executable),
            "modified_at": utc_timestamp(executable.stat().st_mtime),
            "evidence": "local_executable_present",
            "metadata_commands": [["--version"]],
        })

    catalog = {
        "provider": "google",
        "access_method": (
            "antigravity_cli_gemini_api_key" if api_key_route else "antigravity_cli"
        ),
        "authentication_evidence": (
            "settings_model_provider" if api_key_route else "not_checked"
        ),
        "current_access_verified": False,
        "generated_at": utc_timestamp(),
        "client": {
            "name": "Antigravity CLI",
            "installed": executable is not None,
            "version": version,
        },
        "sources": sources,
        "configured": {"model": model, "reasoning_effort": None},
        "model_list_scope": (
            "No model list recorded. Antigravity CLI keeps no local model list: agy "
            "fetches the signed-in account's models from Google at run time, and this "
            "refresh does not run agy models. An empty list means nothing was recorded, "
            "not that no models are available. configured.model is the picker label "
            "saved in antigravity-cli/settings.json, written only after the default is "
            "changed; project settings and the --model and --effort flags can override "
            "it. Authentication and model access have not been verified."
        ),
        "models": [],
    }
    if observation_source is not None:
        scope = (
            "Models from an operator-recorded agy models snapshot taken at "
            "model_list_observed_at. Refresh preserves the original observation "
            "time and does not query the account model list. The list depends on "
            "the account's plan and sign-in route; entries do not establish "
            "successful inference or current access, and account, plan, sign-in or "
            "client changes require a new observation. configured.model is the "
            "picker label saved in antigravity-cli/settings.json, not a model slug."
        )
        if version is not None and version != observations["client_version"]:
            scope += (
                f" The snapshot was recorded with agy {observations['client_version']}, "
                f"but agy {version} is installed, so a new observation is due."
            )
        catalog.update({
            "model_list_observed_at": observations["observed_at"],
            "model_list_complete": observations["list_complete"],
            "model_list_scope": scope,
            "models": [
                {
                    "id": entry["id"],
                    "display_name": entry["display_name"],
                    "availability": "listed_in_agy_model_list",
                    "observed_at": observations["observed_at"],
                    "current_access_verified": False,
                }
                for entry in observations["models"]
            ],
        })
    return catalog


def write_catalog(path, catalog):
    """Replace only complete outputs, preserving the previous file on failure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=".models-", delete=False
        ) as stream:
            temporary = Path(stream.name)
            json.dump(catalog, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    parser.add_argument("--claude-home", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--claude-state", type=Path, default=Path.home() / ".claude.json")
    parser.add_argument("--perplexity-binary", type=Path, help="Path to the pplx executable")
    parser.add_argument(
        "--perplexity-receipt", type=Path,
        default=Path.home() / ".config/pplx/pplx-receipt.json",
    )
    parser.add_argument(
        "--antigravity-home", type=Path, default=Path.home() / ".gemini",
        help="Directory Antigravity CLI shares with the retired Gemini CLI (default: ~/.gemini)",
    )
    parser.add_argument(
        "--antigravity-binary", type=Path,
        help="Path to the agy executable (default: agy on PATH, then ~/.local/bin/agy)",
    )
    parser.add_argument(
        "--antigravity-model-observations", type=Path,
        default=Path(__file__).resolve().parent / "antigravity/observed-models.json",
        help="Recorded agy models snapshot (optional if absent)",
    )
    parser.add_argument(
        "--check-antigravity-model-observations", type=Path, metavar="PATH",
        help="Validate an agy models snapshot and exit without refreshing any catalog",
    )
    args = parser.parse_args()
    if args.check_antigravity_model_observations is not None:
        path = args.check_antigravity_model_observations.expanduser().resolve()
        try:
            if antigravity_model_observations(path)[1] is None:
                raise CatalogError(f"missing source: {path}")
        except CatalogError as error:
            print(f"antigravity: {error}", file=sys.stderr)
            return 1
        print(f"antigravity: valid model observations: {path}")
        return 0
    destination = Path(__file__).resolve().parent
    failed = False
    for provider, builder, paths in (
        ("openai", openai_catalog, (args.codex_home,)),
        ("anthropic", anthropic_catalog, (args.claude_home, args.claude_state)),
        ("perplexity", perplexity_catalog, (args.perplexity_binary, args.perplexity_receipt)),
        ("antigravity", antigravity_catalog, (
            args.antigravity_home, args.antigravity_binary, args.antigravity_model_observations
        )),
    ):
        output = destination / provider / "models.json"
        try:
            catalog = builder(*(
                path.expanduser().resolve() if path is not None else None for path in paths
            ))
            write_catalog(output, catalog)
        except CatalogError as error:
            print(f"{provider}: {error}; catalog unchanged", file=sys.stderr)
            failed = True
        except OSError:
            print(f"{provider}: cannot read sources or write {output}; catalog unchanged", file=sys.stderr)
            failed = True
        else:
            counts = f"{len(catalog['models'])} models"
            if "tools" in catalog:
                counts += f" and {len(catalog['tools'])} tools"
            print(f"{provider}: wrote {counts} to {output}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
