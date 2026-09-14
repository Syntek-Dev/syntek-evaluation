#!/usr/bin/env python3
"""Refresh model metadata from local CLI caches and installations, without network calls."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
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
    except (ValueError, UnicodeError):
        raise CatalogError(f"invalid {'TOML' if toml else 'JSON'}: {path}") from None
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


def find_gemini_package():
    executable = shutil.which("gemini")
    if executable is None:
        raise CatalogError("Gemini CLI is not installed or not on PATH")
    for directory in Path(executable).resolve().parents:
        manifest = directory / "package.json"
        if manifest.is_file():
            package, _ = read_object(manifest)
            if package.get("name") == "@google/gemini-cli":
                return directory
    raise CatalogError("cannot locate the Gemini CLI package from its executable")


def bundled_gemini_models(package_path):
    """Read only literal constants and the declared set; never execute JavaScript."""
    for bundle_path in sorted((package_path / "bundle").glob("*.js")):
        try:
            raw = bundle_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise CatalogError(f"cannot read Gemini CLI bundle: {bundle_path}") from None
        section = re.search(
            r"^// packages/core/dist/src/config/models\.js\r?\n(.*?)"
            r"(?=^// [^\n]+\.js\r?$|\Z)", raw, re.MULTILINE | re.DOTALL
        )
        if section is None:
            continue
        body = section.group(1)
        constants = {
            name: value for name, _, value in re.findall(
                r"^(?:var|const|let)\s+([A-Z][A-Z0-9_]*)\s*=\s*"
                r"(['\"])([A-Za-z0-9._-]+)\2\s*;", body, re.MULTILINE
            )
        }
        model_set = re.search(
            r"\b(?:var|const|let)\s+VALID_GEMINI_MODELS\s*=\s*"
            r"(?:/\*\s*@__PURE__\s*\*/\s*)?new\s+Set\s*\(\s*\[(.*?)\]\s*\)\s*;",
            body, re.DOTALL
        )
        if model_set is None:
            continue
        references = [item.strip() for item in model_set.group(1).split(",")]
        if references and not references[-1]:
            references.pop()
        if not references or any(
            not re.fullmatch(r"[A-Z][A-Z0-9_]*", name) or name not in constants
            for name in references
        ):
            continue
        model_ids = sorted({
            constants[name] for name in references if constants[name].startswith("gemini-")
        })
        if not model_ids:
            continue
        aliases = sorted({
            value for name, value in constants.items()
            if name.startswith("GEMINI_MODEL_ALIAS_")
            or name in ("PREVIEW_GEMINI_MODEL_AUTO", "DEFAULT_GEMINI_MODEL_AUTO")
        })
        return model_ids, aliases, {
            "path": str(bundle_path),
            "modified_at": utc_timestamp(bundle_path.stat().st_mtime),
        }
    raise CatalogError(f"missing or unsupported VALID_GEMINI_MODELS declaration: {package_path}")


def gemini_catalog(home, package_path):
    settings_path = home / "settings.json"
    settings, settings_source = read_object(settings_path)
    model_settings = settings.get("model", {})
    security = settings.get("security", {})
    if not isinstance(model_settings, dict) or not isinstance(security, dict):
        raise CatalogError(f"invalid model or security settings: {settings_path}")
    auth = security.get("auth", {})
    if not isinstance(auth, dict):
        raise CatalogError(f"invalid security.auth settings: {settings_path}")
    auth_type = optional_string(auth, "selectedType", settings_path)
    access_method = {
        "gemini-api-key": "gemini_cli_api_key",
        None: "gemini_cli_unconfigured",
    }.get(auth_type, "gemini_cli_other_auth")
    package_path = package_path or find_gemini_package()
    manifest_path = package_path / "package.json"
    package, package_source = read_object(manifest_path)
    version = optional_string(package, "version", manifest_path)
    if package.get("name") != "@google/gemini-cli" or not version:
        raise CatalogError(f"invalid Gemini CLI package name or version: {manifest_path}")
    model_ids, aliases, bundle_source = bundled_gemini_models(package_path)
    return {
        "provider": "google",
        "access_method": access_method,
        "generated_at": utc_timestamp(),
        "client": {"name": "@google/gemini-cli", "version": version},
        "sources": [settings_source, package_source, bundle_source],
        "configured": {
            "model": optional_string(model_settings, "name", settings_path),
            "reasoning_effort": None,
        },
        "cli_default_alias": "auto" if "auto" in aliases else None,
        "aliases": aliases,
        "model_list_scope": (
            "Gemini model IDs declared in the installed CLI's VALID_GEMINI_MODELS set; "
            "not the full provider catalog or dynamic configuration. Aliases are CLI "
            "selectors, not resolved model IDs. API access has not been verified."
        ),
        "models": [
            {
                "id": model_id,
                "availability": "declared_by_installed_cli",
                "current_access_verified": False,
            }
            for model_id in model_ids
        ],
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
    parser.add_argument("--gemini-home", type=Path, default=Path.home() / ".gemini")
    parser.add_argument("--gemini-package", type=Path, help="Gemini CLI npm package directory")
    parser.add_argument("--perplexity-binary", type=Path, help="Path to the pplx executable")
    parser.add_argument(
        "--perplexity-receipt", type=Path,
        default=Path.home() / ".config/pplx/pplx-receipt.json",
    )
    args = parser.parse_args()
    destination = Path(__file__).resolve().parent
    failed = False
    for provider, builder, paths in (
        ("openai", openai_catalog, (args.codex_home,)),
        ("anthropic", anthropic_catalog, (args.claude_home, args.claude_state)),
        ("gemini", gemini_catalog, (args.gemini_home, args.gemini_package)),
        ("perplexity", perplexity_catalog, (args.perplexity_binary, args.perplexity_receipt)),
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
