"""Offline checks for the GitHub Copilot CLI catalog reader.

Run: python -m unittest discover -s models -p 'test_*.py'
"""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).with_name("refresh-catalogs.py")


class CopilotCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("refresh_catalogs", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "copilot-home"
        self.home.mkdir()
        discovery = mock.patch.object(self.module.shutil, "which", return_value=None)
        self.which = discovery.start()
        self.addCleanup(discovery.stop)
        process = mock.patch.object(
            self.module.subprocess, "Popen",
            side_effect=AssertionError("offline tests must not execute the CLI"),
        )
        process.start()
        self.addCleanup(process.stop)

    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def executable(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\nexit 90\n", encoding="utf-8")
        path.chmod(0o755)
        return path

    def picker_snapshot(self):
        return {
            "schema_version": 1,
            "observed_at": "2026-09-14T12:00:00Z",
            "evidence": "copilot_cli_model_picker",
            "model_id_source": "copilot_model_command_validation",
            "client_version": "1.0.83",
            "list_complete": True,
            "selected": {"model": "example-model", "reasoning_effort": "medium"},
            "aliases": ["auto"],
            "models": [
                {"id": "example-model", "display_name": "Example Model",
                 "selectable": True, "restriction": None},
                {"id": "other-model", "display_name": "Other Model",
                 "selectable": True, "restriction": None},
                {"id": "restricted-model", "display_name": "Restricted Model",
                 "selectable": False, "restriction": "not_in_current_plan"},
            ],
        }

    def test_missing_cli_and_settings_produce_unverified_empty_inventory(self):
        catalog = self.module.copilot_catalog(self.home, None)

        self.which.assert_called_once_with("copilot")
        self.assertEqual(catalog["provider"], "github")
        self.assertEqual(catalog["access_method"], "github_copilot_cli")
        self.assertEqual(catalog["client"]["name"], "GitHub Copilot CLI")
        self.assertIs(catalog["client"]["installed"], False)
        self.assertIsNone(catalog["client"]["version"])
        self.assertEqual(catalog["configured"], {"model": None, "reasoning_effort": None})
        self.assertEqual(catalog["models"], [])
        self.assertIsNone(catalog["subscription_plan"])
        self.assertEqual(catalog["authentication_evidence"], "not_checked")
        self.assertIs(catalog["current_access_verified"], False)

    def test_path_symlink_resolves_to_npm_package_version(self):
        package = self.root / "node_modules" / "@github" / "copilot"
        binary = self.executable(package / "bin" / "copilot")
        self.write_json(package / "package.json", {
            "name": "@github/copilot", "version": "1.2.3",
        })
        link = self.root / "bin" / "copilot"
        link.parent.mkdir()
        link.symlink_to(binary)
        self.which.return_value = str(link)

        catalog = self.module.copilot_catalog(self.home, None)

        self.which.assert_called_once_with("copilot")
        self.assertIs(catalog["client"]["installed"], True)
        self.assertEqual(catalog["client"]["version"], "1.2.3")
        self.assertEqual(catalog["models"], [])
        self.assertIs(catalog["current_access_verified"], False)

    def test_standalone_executable_does_not_inherit_unrelated_package_version(self):
        binary = self.executable(self.root / "standalone" / "copilot")
        self.write_json(binary.parent / "package.json", {
            "name": "unrelated-project", "version": "9.8.7",
        })

        with mock.patch.object(self.module, "copilot_version", return_value="1.2.3") as probe:
            catalog = self.module.copilot_catalog(self.home, binary)

        self.which.assert_not_called()
        probe.assert_called_once_with(binary.resolve())
        self.assertIs(catalog["client"]["installed"], True)
        self.assertEqual(catalog["client"]["version"], "1.2.3")

    def test_saved_model_is_only_a_preference_and_private_settings_are_excluded(self):
        settings = self.home / "settings.json"
        settings.write_text('''{
            // Copilot settings permit comments and trailing commas.
            "model": "example-model",
            "effortLevel": "high", /* saved reasoning preference */
            "github_token": "private-token-sentinel/*literal*/",
            "logged_in_users": [{"login": "private-account-sentinel",}],
            "trusted_folders": ["/private-folder-sentinel",],
            "unrelated_url": "https://example.invalid/a//b",
        }''', encoding="utf-8")
        self.write_json(self.home / "config.json", {"model": "legacy-model-sentinel"})
        self.write_json(self.home / "credentials.json", {"token": "credential-sentinel"})
        original_read = Path.read_text

        def read_settings_only(path, *args, **kwargs):
            self.assertEqual(path, settings, "only current settings may be read")
            return original_read(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", read_settings_only):
            catalog = self.module.copilot_catalog(self.home, None)

        self.assertEqual(catalog["configured"], {
            "model": "example-model", "reasoning_effort": "high",
        })
        self.assertEqual(len(catalog["models"]), 1)
        self.assertEqual(catalog["models"][0]["id"], "example-model")
        self.assertEqual(catalog["models"][0]["availability"], "configured_model_preference")
        self.assertIs(catalog["models"][0]["current_access_verified"], False)
        self.assertIs(catalog["current_access_verified"], False)
        exported = json.dumps(catalog)
        for private_value in (
            "private-token-sentinel", "private-account-sentinel", "private-folder-sentinel",
            "legacy-model-sentinel", "credential-sentinel", "https://example.invalid",
        ):
            self.assertNotIn(private_value, exported)

    def test_auto_selection_does_not_create_an_underlying_model(self):
        self.write_json(self.home / "settings.json", {"model": "auto"})

        catalog = self.module.copilot_catalog(self.home, None)

        self.assertEqual(catalog["configured"]["model"], "auto")
        self.assertEqual(catalog["models"], [])

    def test_invalid_settings_are_rejected_without_echoing_their_contents(self):
        invalid_settings = [
            json.dumps({key: invalid})
            for key in ("model", "effortLevel")
            for invalid in (["private-value-sentinel"], {"private-value-sentinel": 1}, 42)
        ] + [
            '{"model": "private-value-sentinel" /* unterminated comment',
            '{"model": "private-value-sentinel}',
            '{"model": "private-value-sentinel" "effortLevel": "high"}',
        ]
        for raw in invalid_settings:
            with self.subTest(settings=raw):
                (self.home / "settings.json").write_text(raw, encoding="utf-8")
                with self.assertRaises(self.module.CatalogError) as error:
                    self.module.copilot_catalog(self.home, None)
                self.assertNotIn("private-value-sentinel", str(error.exception))

    def test_missing_explicit_executable_is_rejected(self):
        with self.assertRaises(self.module.CatalogError):
            self.module.copilot_catalog(self.home, self.root / "missing-copilot")
        self.which.assert_not_called()

    def test_recognised_npm_package_without_version_is_rejected(self):
        package = self.root / "node_modules" / "@github" / "copilot"
        binary = self.executable(package / "bin" / "copilot")
        self.write_json(package / "package.json", {"name": "@github/copilot"})

        with self.assertRaises(self.module.CatalogError):
            self.module.copilot_catalog(self.home, binary)

    def test_picker_snapshot_separates_available_models_and_observed_selection(self):
        snapshot = self.picker_snapshot()
        path = self.root / "observations.json"
        self.write_json(path, snapshot)
        self.write_json(self.home / "settings.json", {"model": "other-model", "effortLevel": "high"})

        catalog = self.module.copilot_catalog(self.home, None, path)

        self.assertEqual(catalog["configured"], {"model": "other-model", "reasoning_effort": "high"})
        self.assertEqual(catalog["observed_selection"], snapshot["selected"])
        self.assertEqual(catalog["aliases"], ["auto"])
        self.assertEqual(catalog["model_list_observed_at"], snapshot["observed_at"])
        self.assertIs(catalog["model_list_complete"], True)
        self.assertEqual({model["id"] for model in catalog["models"]}, {"example-model", "other-model"})
        self.assertEqual([model["id"] for model in catalog["unavailable_models"]], ["restricted-model"])
        for model in catalog["models"]:
            self.assertEqual(model["availability"], "listed_in_copilot_model_picker")
        for model in catalog["unavailable_models"]:
            self.assertEqual(model["availability"], "blocked_by_copilot_plan")
            self.assertEqual(model["restriction"], "not_in_current_plan")
        for model in catalog["models"] + catalog["unavailable_models"]:
            self.assertEqual(model["observed_at"], snapshot["observed_at"])
            self.assertIs(model["current_access_verified"], False)
        self.assertIs(catalog["current_access_verified"], False)
        self.assertIsNone(catalog["subscription_plan"])

    def test_refresh_preserves_picker_observation_and_merges_only_eligible_preferences(self):
        snapshot = self.picker_snapshot()
        path = self.root / "observations.json"
        self.write_json(path, snapshot)
        original_bytes, original_mtime = path.read_bytes(), path.stat().st_mtime_ns
        with mock.patch.object(self.module, "utc_timestamp", return_value="2026-09-15T12:00:00Z"):
            first = self.module.copilot_catalog(self.home, None, path)
        with mock.patch.object(self.module, "utc_timestamp", return_value="2026-09-16T12:00:00Z"):
            second = self.module.copilot_catalog(self.home, None, path)
        self.assertNotEqual(first["generated_at"], second["generated_at"])
        for key in ("models", "unavailable_models", "observed_selection", "model_list_observed_at"):
            self.assertEqual(first[key], second[key])
        self.assertEqual(second["model_list_observed_at"], snapshot["observed_at"])

        for preference in ("example-model", "new-preference", "restricted-model"):
            with self.subTest(preference=preference):
                self.write_json(self.home / "settings.json", {"model": preference})
                catalog = self.module.copilot_catalog(self.home, None, path)
                models = {model["id"]: model for model in catalog["models"]}
                expected = {"example-model", "other-model"}
                if preference == "new-preference":
                    expected.add(preference)
                    self.assertEqual(models[preference]["availability"], "configured_model_preference")
                self.assertEqual(set(models), expected)
                self.assertEqual(models["example-model"]["availability"], "listed_in_copilot_model_picker")
                self.assertEqual(models["example-model"]["observed_at"], snapshot["observed_at"])
                self.assertEqual(catalog["unavailable_models"], first["unavailable_models"])
                self.assertEqual(catalog["observed_selection"], snapshot["selected"])
                self.assertEqual(catalog["configured"]["model"], preference)
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(path.stat().st_mtime_ns, original_mtime)

    def test_missing_picker_snapshot_keeps_configured_preference_behavior(self):
        self.write_json(self.home / "settings.json", {"model": "example-model"})
        for path in (None, self.root / "missing-observations.json"):
            with self.subTest(path=path):
                catalog = self.module.copilot_catalog(self.home, None, path)
                self.assertEqual([model["id"] for model in catalog["models"]], ["example-model"])
                self.assertEqual(catalog["models"][0]["availability"], "configured_model_preference")
                self.assertIsNone(catalog.get("model_list_observed_at"))
                self.assertEqual(catalog.get("unavailable_models", []), [])
                self.assertIs(catalog["current_access_verified"], False)

    def test_invalid_picker_snapshots_are_rejected(self):
        path = self.root / "observations.json"
        invalid_fields = [
            (("schema_version",), 2),
            (("schema_version",), True),
            (("observed_at",), "private-value-sentinel"),
            (("observed_at",), "2026-09-14T12:00:00"),
            (("observed_at",), "2026-09-14T12:00:00+01:00"),
            (("evidence",), "private-value-sentinel"),
            (("model_id_source",), "private-value-sentinel"),
            (("client_version",), 42),
            (("list_complete",), "true"),
            (("selected", "model"), None),
            (("selected", "reasoning_effort"), 42),
            (("aliases",), ["auto", "auto"]),
            (("models", 0, "selectable"), 1),
            (("models", 0, "restriction"), "not_in_current_plan"),
            (("models", 2, "restriction"), None),
            (("models", 0, "display_name"), None),
            (("models", 1, "id"), "example-model"),
            (("models", 0, "id"), "auto"),
        ]
        for keys, value in invalid_fields:
            with self.subTest(field=keys, value=value):
                snapshot = self.picker_snapshot()
                target = snapshot
                for key in keys[:-1]:
                    target = target[key]
                target[keys[-1]] = value
                self.write_json(path, snapshot)
                with self.assertRaises(self.module.CatalogError) as error:
                    self.module.copilot_catalog(self.home, None, path)
                self.assertNotIn("private-value-sentinel", str(error.exception))
        path.write_text("{", encoding="utf-8")
        with self.assertRaises(self.module.CatalogError):
            self.module.copilot_catalog(self.home, None, path)

    def test_version_probe_uses_isolated_settings_and_environment(self):
        binary = self.executable(self.root / "standalone" / "copilot")
        isolated_paths = []

        def version_command(command, **kwargs):
            self.assertEqual(command, [str(binary), "--no-auto-update", "--version"])
            self.assertEqual(kwargs["stdin"], self.module.subprocess.DEVNULL)
            self.assertEqual(kwargs["stderr"], self.module.subprocess.DEVNULL)
            self.assertEqual(kwargs["timeout"], 10)
            environment = kwargs["env"]
            self.assertLessEqual(set(environment), {"PATH", "LANG", "LC_ALL", "COPILOT_HOME", "CI"})
            self.assertEqual(environment["CI"], "1")
            isolated_home = Path(environment["COPILOT_HOME"])
            isolated_cwd = Path(kwargs["cwd"])
            self.assertTrue(isolated_home.is_dir())
            self.assertTrue(isolated_cwd.is_dir())
            self.assertTrue(isolated_home.is_relative_to(isolated_cwd))
            self.assertNotEqual(isolated_home, self.home)
            self.assertEqual(list(isolated_home.iterdir()), [])
            isolated_paths.extend((isolated_home, isolated_cwd))
            output = kwargs["stdout"]
            self.assertGreaterEqual(output.fileno(), 0)
            output.write(b"GitHub Copilot CLI 1.2.3.\nprivate-output-sentinel\n")
            return self.module.subprocess.CompletedProcess(command, 0)

        with mock.patch.dict(self.module.os.environ, {
            "GH_TOKEN": "private-token-sentinel",
            "COPILOT_HOME": str(self.home),
        }), mock.patch.object(self.module.subprocess, "run", side_effect=version_command) as run:
            version = self.module.copilot_version(binary)

        run.assert_called_once()
        self.assertEqual(version, "1.2.3")
        for path in isolated_paths:
            self.assertFalse(path.exists(), "temporary version-probe files must be removed")

    def test_version_probe_rejects_failed_or_malformed_output_without_exposing_it(self):
        binary = self.executable(self.root / "standalone" / "copilot")
        invalid_output = [
            b"private-output-sentinel\nGitHub Copilot CLI 1.2.3.\n",
            b"GitHub Copilot CLI private-output-sentinel.\n",
            b"\xffprivate-output-sentinel\n",
            b"GitHub Copilot CLI 1.2.3.\n" + b"x" * 65536,
        ]
        cases = [(output, 0, False) for output in invalid_output] + [
            (b"GitHub Copilot CLI 1.2.3.\nprivate-output-sentinel\n", 1, False),
            (b"private-output-sentinel", 0, True),
        ]
        for index, (output, returncode, timed_out) in enumerate(cases):
            with self.subTest(case=index):
                def version_command(command, **kwargs):
                    kwargs["stdout"].write(output)
                    if timed_out:
                        raise self.module.subprocess.TimeoutExpired(command, 10, output=output)
                    return self.module.subprocess.CompletedProcess(command, returncode)

                with mock.patch.object(self.module.subprocess, "run", side_effect=version_command):
                    with self.assertRaises(self.module.CatalogError) as error:
                        self.module.copilot_version(binary)
                self.assertNotIn("private-output-sentinel", str(error.exception))


if __name__ == "__main__":
    unittest.main()
