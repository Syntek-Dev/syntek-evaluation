"""Offline checks for the Antigravity CLI catalog reader.

Run: python -m unittest discover -s models -p 'test_*.py'
"""

import builtins
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).with_name("refresh-catalogs.py")
DELETE = object()


class AntigravityCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("refresh_catalogs", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "dot-gemini"
        (self.home / "antigravity-cli").mkdir(parents=True)
        self.settings = self.home / "antigravity-cli" / "settings.json"
        # Keep the ~/.local/bin/agy fallback inside the temporary tree.
        user_home = mock.patch.object(self.module.Path, "home", return_value=self.root)
        user_home.start()
        self.addCleanup(user_home.stop)
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

    def use_bubblewrap(self):
        """Let the sandbox find bwrap; subprocess.run is mocked, so it never runs."""
        bwrap = "/sandbox-tools/bwrap"
        self.which.side_effect = lambda name: bwrap if name == "bwrap" else None
        return bwrap

    def sandboxed_command(self, command, binary):
        """Split a sandbox command into its options and the command it runs."""
        self.assertIn("--", command)
        separator = command.index("--")
        self.assertEqual(command[separator + 1:], [str(binary), "--version"])
        return command[:separator]

    def executable(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\nexit 90\n", encoding="utf-8")
        path.chmod(0o755)
        return path

    def snapshot(self):
        return {
            "schema_version": 1,
            "observed_at": "2026-09-27T21:45:00Z",
            "evidence": "agy_models_command",
            "client_version": "1.2.12",
            "list_complete": True,
            "models": [
                {"id": "example-flash-high", "display_name": "Example Flash (High)"},
                {"id": "example-flash-low", "display_name": "Example Flash (Low)"},
                {"id": "example-pro-high", "display_name": "Example Pro (High)"},
            ],
        }

    def test_missing_cli_is_recorded_as_not_installed(self):
        catalog = self.module.antigravity_catalog(self.home, None)

        self.which.assert_called_once_with("agy")
        self.assertEqual(catalog["provider"], "google")
        self.assertEqual(catalog["access_method"], "antigravity_cli")
        self.assertEqual(catalog["authentication_evidence"], "not_checked")
        self.assertIs(catalog["current_access_verified"], False)
        self.assertEqual(catalog["client"], {
            "name": "Antigravity CLI", "installed": False, "version": None,
        })
        self.assertEqual(catalog["configured"], {"model": None, "reasoning_effort": None})
        self.assertEqual(catalog["sources"], [])
        self.assertEqual(catalog["models"], [])
        self.assertIn("does not run agy models", catalog["model_list_scope"])
        self.assertNotIn("model_list_observed_at", catalog)

    def test_non_executable_default_location_is_not_treated_as_installed(self):
        default = self.root / ".local" / "bin" / "agy"
        default.parent.mkdir(parents=True)
        default.write_text("not a program", encoding="utf-8")
        default.chmod(0o644)

        catalog = self.module.antigravity_catalog(self.home, None)

        self.assertIs(catalog["client"]["installed"], False)

    def test_installer_default_location_is_used_when_agy_is_not_on_path(self):
        binary = self.executable(self.root / ".local" / "bin" / "agy")

        with mock.patch.object(self.module, "antigravity_version", return_value="1.2.3") as probe:
            catalog = self.module.antigravity_catalog(self.home, None)

        self.which.assert_called_once_with("agy")
        probe.assert_called_once_with(binary.resolve())
        self.assertEqual(catalog["client"], {
            "name": "Antigravity CLI", "installed": True, "version": "1.2.3",
        })
        self.assertEqual(catalog["sources"], [{
            "path": str(binary.resolve()),
            "modified_at": self.module.utc_timestamp(binary.stat().st_mtime),
            "evidence": "local_executable_present",
            "metadata_commands": [["--version"]],
        }])

    def test_path_lookup_resolves_symlinks_and_explicit_binary_skips_lookup(self):
        binary = self.executable(self.root / "install" / "agy")
        link = self.root / "bin" / "agy"
        link.parent.mkdir()
        link.symlink_to(binary)
        self.which.return_value = str(link)
        with mock.patch.object(self.module, "antigravity_version", return_value="1.2.3") as probe:
            self.module.antigravity_catalog(self.home, None)
        probe.assert_called_once_with(binary.resolve())

        self.which.reset_mock()
        with mock.patch.object(self.module, "antigravity_version", return_value="1.2.4") as probe:
            catalog = self.module.antigravity_catalog(self.home, binary)
        self.which.assert_not_called()
        probe.assert_called_once_with(binary.resolve())
        self.assertEqual(catalog["client"]["version"], "1.2.4")

    def test_missing_explicit_executable_is_rejected(self):
        with self.assertRaises(self.module.CatalogError):
            self.module.antigravity_catalog(self.home, self.root / "missing-agy")
        self.which.assert_not_called()

    def test_version_probe_uses_isolated_home_and_environment(self):
        binary = self.executable(self.root / "install" / "agy")
        self.use_bubblewrap()
        real_home = self.root / "real-home"
        private_environment = {
            "HOME": str(real_home),
            "XDG_CONFIG_HOME": str(real_home / ".config"),
            "XDG_RUNTIME_DIR": str(real_home / "run"),
            "GEMINI_API_KEY": "private-token-sentinel-1",
            "GOOGLE_API_KEY": "private-token-sentinel-2",
            "GOOGLE_APPLICATION_CREDENTIALS": "/private-credentials-sentinel.json",
            "AGY_ADC_AUTH": "true",
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/private-bus-sentinel",
            "GH_TOKEN": "private-token-sentinel-3",
        }
        allowed = {
            "PATH", "LANG", "LC_ALL", "HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
            "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_RUNTIME_DIR", "TMPDIR",
            "AGY_CLI_DISABLE_AUTO_UPDATE",
        }
        isolated_paths = []

        def version_command(command, **kwargs):
            self.sandboxed_command(command, binary)
            self.assertEqual(kwargs["stdin"], self.module.subprocess.DEVNULL)
            self.assertEqual(kwargs["stderr"], self.module.subprocess.DEVNULL)
            self.assertEqual(kwargs["timeout"], 10)
            environment = kwargs["env"]
            self.assertLessEqual(set(environment), allowed)
            self.assertEqual(environment["AGY_CLI_DISABLE_AUTO_UPDATE"], "true")
            isolated_home = Path(environment["HOME"])
            self.assertTrue(isolated_home.is_dir())
            self.assertEqual(list(isolated_home.iterdir()), [])
            self.assertNotEqual(isolated_home, real_home)
            self.assertNotEqual(isolated_home, self.home)
            self.assertEqual(Path(kwargs["cwd"]), isolated_home)
            for key in allowed - {"PATH", "LANG", "LC_ALL", "AGY_CLI_DISABLE_AUTO_UPDATE"}:
                self.assertTrue(
                    Path(environment[key]).is_relative_to(isolated_home),
                    f"{key} must point inside the temporary home",
                )
            self.assertFalse(set(private_environment) - {
                "HOME", "XDG_CONFIG_HOME", "XDG_RUNTIME_DIR",
            } & set(environment), "credential and session variables must not be passed")
            for value in private_environment.values():
                if "sentinel" in value or value.startswith(str(real_home)):
                    self.assertNotIn(value, environment.values())
            isolated_paths.append(isolated_home)
            kwargs["stdout"].write(b"1.2.12\n")
            return self.module.subprocess.CompletedProcess(command, 0)

        with mock.patch.dict(self.module.os.environ, private_environment), mock.patch.object(
            self.module.subprocess, "run", side_effect=version_command
        ) as run:
            version = self.module.antigravity_version(binary)

        run.assert_called_once()
        self.assertEqual(version, "1.2.12")
        self.assertEqual(len(isolated_paths), 1)
        self.assertFalse(isolated_paths[0].exists(), "the temporary home must be removed")

    def sandbox_probe(self, binary, account_home, environment_home, runtime):
        """Run the version probe with a mocked subprocess and return its command."""
        commands = []

        def version_command(command, **kwargs):
            commands.append((command, kwargs["env"]["HOME"]))
            kwargs["stdout"].write(b"1.2.12\n")
            return self.module.subprocess.CompletedProcess(command, 0)

        with contextlib.ExitStack() as stack:
            # Pretend every candidate exists so that the hidden set is predictable.
            stack.enter_context(mock.patch.object(self.module.Path, "is_dir", return_value=True))
            stack.enter_context(mock.patch.object(
                self.module.Path, "home", return_value=environment_home
            ))
            stack.enter_context(mock.patch.object(
                self.module.pwd, "getpwuid", return_value=mock.Mock(pw_dir=str(account_home))
            ))
            stack.enter_context(mock.patch.dict(
                self.module.os.environ, {"XDG_RUNTIME_DIR": str(runtime)}
            ))
            stack.enter_context(mock.patch.object(
                self.module.subprocess, "run", side_effect=version_command
            ))
            self.assertEqual(self.module.antigravity_version(binary), "1.2.12")
        (command, temporary_home), = commands
        return command, temporary_home

    def test_sandbox_never_hides_the_root_directory(self):
        binary = self.executable(self.root / "install" / "agy")
        self.use_bubblewrap()
        # Some service accounts have / as their home directory.
        command, _ = self.sandbox_probe(binary, Path("/"), Path("/"), Path("/run/user/0"))
        options = self.sandboxed_command(command, binary)
        hidden = [options[i + 1] for i, option in enumerate(options) if option == "--tmpfs"]
        self.assertNotIn("/", hidden)
        self.assertIn("/tmp", hidden)

    def test_version_probe_runs_offline_in_a_sandbox_that_hides_the_home(self):
        binary = self.executable(self.root / ".local" / "bin" / "agy")
        bwrap = self.use_bubblewrap()
        account_home = Path("/home/account-home-sentinel")
        environment_home = Path("/srv/environment-home-sentinel")
        runtime = Path("/run/user/runtime-sentinel")
        command, temporary_home = self.sandbox_probe(
            binary, account_home, environment_home, runtime
        )
        options = self.sandboxed_command(command, binary)
        self.assertEqual(options[0], bwrap)
        # --unshare-all includes --unshare-net, leaving only a loopback interface.
        for flag in ("--unshare-all", "--die-with-parent", "--new-session"):
            self.assertIn(flag, options)
        self.assertNotIn("--share-net", options)
        arity = {"--ro-bind": 2, "--bind": 2, "--tmpfs": 1, "--dev": 1, "--proc": 1, "--chdir": 1}
        mounts, index = [], 1
        while index < len(options):
            count = arity.get(options[index], 0)
            mounts.append(tuple(options[index:index + 1 + count]))
            index += 1 + count
        hidden = [Path(mount[1]) for mount in mounts if mount[0] == "--tmpfs"]
        self.assertNotIn(Path("/"), hidden)
        for private in (
            account_home, account_home / ".gemini", account_home / ".config" / "gcloud",
            environment_home, runtime, Path(f"/run/user/{self.module.os.getuid()}"),
            Path("/tmp"), Path("/var/tmp"), Path(temporary_home),
        ):
            self.assertTrue(
                any(private.is_relative_to(path) for path in hidden),
                f"{private} must be hidden by an empty file system",
            )
        root = mounts.index(("--ro-bind", "/", "/"))
        tmpfs = [position for position, mount in enumerate(mounts) if mount[0] == "--tmpfs"]
        executable = mounts.index(("--ro-bind", str(binary), str(binary)))
        writable = mounts.index(("--bind", temporary_home, temporary_home))
        self.assertLess(root, min(tmpfs))
        self.assertGreater(min(executable, writable), max(tmpfs))
        self.assertEqual(
            [mount for mount in mounts if mount[0] in {"--bind", "--ro-bind"}],
            [("--ro-bind", "/", "/"), ("--ro-bind", str(binary), str(binary)),
             ("--bind", temporary_home, temporary_home)],
            "only the executable and the temporary home may be mounted back",
        )
        self.assertIn(("--chdir", temporary_home), mounts)

    def test_version_probe_fails_closed_without_bubblewrap(self):
        binary = self.executable(self.root / "install" / "agy")
        with mock.patch.object(self.module.subprocess, "run") as run:
            with self.assertRaises(self.module.CatalogError) as error:
                self.module.antigravity_version(binary)
        run.assert_not_called()
        self.which.assert_called_with("bwrap")
        self.assertIn("bwrap", str(error.exception))

    def test_version_probe_accepts_only_a_bare_version(self):
        binary = self.executable(self.root / "install" / "agy")
        self.use_bubblewrap()
        for output, expected in (
            (b"1.2.12\n", "1.2.12"),
            (b"1.2.12", "1.2.12"),
            (b"2.0.0-rc.1\n", "2.0.0-rc.1"),
        ):
            with self.subTest(output=output):
                def version_command(command, **kwargs):
                    kwargs["stdout"].write(output)
                    return self.module.subprocess.CompletedProcess(command, 0)

                with mock.patch.object(self.module.subprocess, "run", side_effect=version_command):
                    self.assertEqual(self.module.antigravity_version(binary), expected)

    def test_version_probe_rejects_failed_or_malformed_output_without_exposing_it(self):
        binary = self.executable(self.root / "install" / "agy")
        self.use_bubblewrap()
        malformed = [
            b"private-output-sentinel\n",
            b"agy private-output-sentinel\n",
            b"1.2.12\nprivate-output-sentinel\n",
            b"private-output-sentinel\n1.2.12\n",
            b" 1.2.12 private-output-sentinel\n",
            b"\xffprivate-output-sentinel\n",
            b"1.2.12\n" + b"private-output-sentinel" * 3000,
            b"",
        ]
        cases = [(output, 0, None) for output in malformed] + [
            # A valid version is still refused when agy or the sandbox fails.
            (b"1.2.12\n", 1, None),
            (b"1.2.12\nprivate-output-sentinel\n", 1, None),
            (b"private-output-sentinel", 0, "timeout"),
            (b"", 0, "oserror"),
        ]
        for index, (output, returncode, failure) in enumerate(cases):
            with self.subTest(case=index):
                def version_command(command, **kwargs):
                    kwargs["stdout"].write(output)
                    if failure == "timeout":
                        raise self.module.subprocess.TimeoutExpired(command, 10, output=output)
                    if failure == "oserror":
                        raise PermissionError("private-output-sentinel")
                    return self.module.subprocess.CompletedProcess(command, returncode)

                with mock.patch.object(self.module.subprocess, "run", side_effect=version_command):
                    with self.assertRaises(self.module.CatalogError) as error:
                        self.module.antigravity_version(binary)
                self.assertNotIn("private-output-sentinel", str(error.exception))
                # Tracebacks must not chain the original exception, which may hold output.
                self.assertIsNone(error.exception.__cause__)
                self.assertTrue(
                    error.exception.__context__ is None or error.exception.__suppress_context__
                )

    def test_saved_model_label_is_read_and_private_settings_are_excluded(self):
        self.write_json(self.settings, {
            "model": "Example Pro (Low)",
            "colorScheme": "private-colour-sentinel",
            "trustedWorkspaces": ["/private-workspace-sentinel"],
        })

        catalog = self.module.antigravity_catalog(self.home, None)

        self.assertEqual(catalog["configured"], {
            "model": "Example Pro (Low)", "reasoning_effort": None,
        })
        self.assertEqual(catalog["access_method"], "antigravity_cli")
        self.assertEqual(catalog["authentication_evidence"], "not_checked")
        self.assertEqual(catalog["models"], [], "a saved label is not a model list entry")
        self.assertEqual(catalog["sources"], [{
            "path": str(self.settings),
            "modified_at": self.module.utc_timestamp(self.settings.stat().st_mtime),
        }])
        exported = json.dumps(catalog)
        self.assertNotIn("private-colour-sentinel", exported)
        self.assertNotIn("private-workspace-sentinel", exported)

    def test_model_provider_setting_selects_only_the_api_key_route(self):
        for provider, access_method, evidence in (
            ("gemini", "antigravity_cli_gemini_api_key", "settings_model_provider"),
            ("Gemini", "antigravity_cli", "not_checked"),
            ("other-provider", "antigravity_cli", "not_checked"),
        ):
            with self.subTest(provider=provider):
                self.write_json(self.settings, {"modelProvider": provider})
                catalog = self.module.antigravity_catalog(self.home, None)
                self.assertEqual(catalog["access_method"], access_method)
                self.assertEqual(catalog["authentication_evidence"], evidence)
                self.assertIs(catalog["current_access_verified"], False)
                self.assertNotIn(provider, json.dumps(catalog["configured"]))

    def test_invalid_settings_are_rejected_without_echoing_their_contents(self):
        invalid_settings = [
            json.dumps({key: invalid})
            for key in ("model", "modelProvider")
            for invalid in (["private-value-sentinel"], {"private-value-sentinel": 1}, 42)
        ] + [
            # configured.model is committed, so it must look like a picker label.
            json.dumps({"model": invalid}, ensure_ascii=False)
            for invalid in (
                "",
                "x" * 107 + "private-value-sentinel",
                " private-value-sentinel",
                "Label\nprivate-value-sentinel",
                "Label​private-value-sentinel",
                "https://example.invalid/?key=private-value-sentinel",
                "private-value-sentinel@example.invalid",
                "AIzaprivate-value-sentinel",
            )
        ] + [
            '{"model": "private-value-sentinel"',
            '["private-value-sentinel"]',
            '"private-value-sentinel"',
            '{"model": ' + "[" * 100000 + "]" * 100000 + "}",
        ]
        for raw in invalid_settings:
            with self.subTest(settings=raw):
                self.settings.write_text(raw, encoding="utf-8")
                with self.assertRaises(self.module.CatalogError) as error:
                    self.module.antigravity_catalog(self.home, None)
                self.assertNotIn("private-value-sentinel", str(error.exception))
                self.assertIsNone(error.exception.__cause__)

    def test_saved_model_label_may_use_the_full_length(self):
        label = "Example Pro (High) " + "x" * 109
        self.write_json(self.settings, {"model": label})
        catalog = self.module.antigravity_catalog(self.home, None)
        self.assertEqual(len(label), 128)
        self.assertEqual(catalog["configured"]["model"], label)

    def test_credential_log_conversation_and_legacy_files_are_never_opened(self):
        self.write_json(self.settings, {"model": "Example Pro (Low)"})
        observations = self.root / "observed-models.json"
        self.write_json(observations, self.snapshot())
        binary = self.executable(self.root / "install" / "agy")
        state = self.home / "antigravity-cli"
        forbidden = {
            self.home / "google_accounts.json": '{"active": null, "old": ["private-email-sentinel"]}',
            self.home / "oauth_creds.json": '{"access_token": "private-token-sentinel"}',
            self.home / "settings.json": '{"model": {"name": "legacy-model-sentinel"}}',
            self.home / "installation_id": "private-installation-sentinel",
            self.home / "projects.json": '{"projects": {"/private-path-sentinel": "x"}}',
            self.home / "config" / "mcp_config.json": '{"mcpServers": {"x": {"env": {"TOKEN": "private-token-sentinel"}}}}',
            self.home / "config" / "projects" / "default-cli-project.json": '{"id": "private-project-sentinel"}',
            self.home / "antigravity" / "mcp_oauth_tokens.json": '{"token": "private-token-sentinel"}',
            state / "installation_id": "private-installation-sentinel",
            state / "jetski_state.pbtxt": 'installation_uuid: "private-installation-sentinel"',
            state / "cache" / "default_project_id.txt": "private-project-sentinel",
            state / "cache" / "last_conversations.json": '{"/private-path-sentinel": "private-conversation-sentinel"}',
            state / "history.jsonl": '{"display": "private-prompt-sentinel"}',
            state / "conversation_summaries.db": "private-conversation-sentinel",
            state / "log" / "cli-20260927_223250.log": (
                "I0927 server.go:1635] Language server version: 9.9.9\n"
                "applyAuthResult: email=private-email-sentinel\n"
                'Propagating selected model override to backend: label="log-model-sentinel"\n'
            ),
        }
        for path, content in forbidden.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        (state / "cli.log").symlink_to(state / "log" / "cli-20260927_223250.log")
        opened = []
        original_io_open, original_builtin_open = io.open, builtins.open

        def spy(original):
            def record(file, *args, **kwargs):
                if isinstance(file, (str, Path)):
                    opened.append(Path(file).resolve())
                return original(file, *args, **kwargs)
            return record

        with mock.patch("io.open", spy(original_io_open)), mock.patch(
            "builtins.open", spy(original_builtin_open)
        ), mock.patch.object(self.module, "antigravity_version", return_value="1.2.12"):
            catalog = self.module.antigravity_catalog(self.home, binary, observations)

        self.assertEqual(set(opened), {self.settings.resolve(), observations.resolve()})
        self.assertEqual(
            {source["path"] for source in catalog["sources"]},
            {str(self.settings), str(observations), str(binary.resolve())},
        )
        exported = json.dumps(catalog)
        for private_value in (
            "private-email-sentinel", "private-token-sentinel", "legacy-model-sentinel",
            "private-installation-sentinel", "private-project-sentinel",
            "private-path-sentinel", "private-conversation-sentinel",
            "private-prompt-sentinel", "log-model-sentinel", "9.9.9",
        ):
            self.assertNotIn(private_value, exported)

    def test_snapshot_is_merged_with_its_observation_time(self):
        snapshot = self.snapshot()
        path = self.root / "observed-models.json"
        self.write_json(path, snapshot)
        self.write_json(self.settings, {"model": "Example Pro (High)"})

        catalog = self.module.antigravity_catalog(self.home, None, path)

        self.assertEqual(catalog["model_list_observed_at"], snapshot["observed_at"])
        self.assertIs(catalog["model_list_complete"], True)
        self.assertEqual(catalog["configured"]["model"], "Example Pro (High)")
        self.assertEqual(catalog["models"], [
            {
                "id": entry["id"],
                "display_name": entry["display_name"],
                "availability": "listed_in_agy_model_list",
                "observed_at": snapshot["observed_at"],
                "current_access_verified": False,
            }
            for entry in snapshot["models"]
        ])
        observation_source = catalog["sources"][1]
        self.assertEqual(observation_source["path"], str(path))
        for key in ("schema_version", "observed_at", "evidence", "client_version"):
            self.assertEqual(observation_source[key], snapshot[key])
        self.assertIn("operator-recorded agy models snapshot", catalog["model_list_scope"])
        self.assertIs(catalog["current_access_verified"], False)
        self.assertEqual(catalog["authentication_evidence"], "not_checked")

    def test_refresh_preserves_the_snapshot_and_its_observation_time(self):
        path = self.root / "observed-models.json"
        self.write_json(path, self.snapshot())
        original_bytes, original_mtime = path.read_bytes(), path.stat().st_mtime_ns
        with mock.patch.object(self.module, "utc_timestamp", return_value="2026-09-28T12:00:00Z"):
            first = self.module.antigravity_catalog(self.home, None, path)
        with mock.patch.object(self.module, "utc_timestamp", return_value="2026-09-29T12:00:00Z"):
            second = self.module.antigravity_catalog(self.home, None, path)

        self.assertNotEqual(first["generated_at"], second["generated_at"])
        for key in ("models", "model_list_observed_at", "model_list_complete"):
            self.assertEqual(first[key], second[key])
        self.assertEqual(second["model_list_observed_at"], "2026-09-27T21:45:00Z")
        self.assertEqual(path.read_bytes(), original_bytes)
        self.assertEqual(path.stat().st_mtime_ns, original_mtime)

    def test_snapshot_variants_are_accepted_and_kept_verbatim(self):
        path = self.root / "observed-models.json"
        longest = {"id": "a" * 128, "display_name": "Example " + "x" * 120}
        for observed_at, list_complete in (
            ("2026-09-27T21:45:00.5Z", False),
            ("2026-09-27T21:45:00+00:00", True),
        ):
            with self.subTest(observed_at=observed_at):
                snapshot = self.snapshot()
                snapshot.update(observed_at=observed_at, list_complete=list_complete)
                snapshot["models"].append(longest)
                self.write_json(path, snapshot)
                catalog = self.module.antigravity_catalog(self.home, None, path)
                self.assertEqual(catalog["model_list_observed_at"], observed_at)
                self.assertIs(catalog["model_list_complete"], list_complete)
                self.assertEqual(
                    [(entry["id"], entry["display_name"]) for entry in catalog["models"]],
                    [(entry["id"], entry["display_name"]) for entry in snapshot["models"]],
                )
                self.assertEqual(
                    {entry["observed_at"] for entry in catalog["models"]}, {observed_at}
                )

    def test_snapshot_from_another_client_version_is_flagged(self):
        path = self.root / "observed-models.json"
        self.write_json(path, self.snapshot())
        binary = self.executable(self.root / "install" / "agy")
        note = "The snapshot was recorded with agy 1.2.12, but agy 1.3.0 is installed"
        for installed, flagged in (("1.2.12", False), ("1.3.0", True)):
            with self.subTest(installed=installed):
                with mock.patch.object(self.module, "antigravity_version", return_value=installed):
                    catalog = self.module.antigravity_catalog(self.home, binary, path)
                self.assertEqual(note in catalog["model_list_scope"], flagged)
                self.assertEqual(catalog["client"]["version"], installed)
        catalog = self.module.antigravity_catalog(self.home, None, path)
        self.assertNotIn("but agy", catalog["model_list_scope"])

    def test_absent_snapshot_leaves_an_empty_model_list(self):
        for path in (None, self.root / "missing-observed-models.json"):
            with self.subTest(path=path):
                catalog = self.module.antigravity_catalog(self.home, None, path)
                self.assertEqual(catalog["models"], [])
                self.assertEqual(catalog["sources"], [])
                self.assertNotIn("model_list_observed_at", catalog)
                self.assertNotIn("model_list_complete", catalog)
                self.assertIn("No model list recorded", catalog["model_list_scope"])

    def test_invalid_snapshots_are_rejected_without_echoing_their_contents(self):
        path = self.root / "observed-models.json"
        invalid_fields = [
            (("schema_version",), 2),
            (("schema_version",), True),
            (("schema_version",), "1"),
            (("schema_version",), DELETE),
            (("observed_at",), "private-value-sentinel"),
            (("observed_at",), "2026-09-27T21:45:00"),
            (("observed_at",), "2026-09-27T21:45:00+01:00"),
            (("observed_at",), "2026-02-30T21:45:00Z"),
            (("observed_at",), "2099-01-01T00:00:00Z"),
            (("observed_at",), 1790545500),
            (("evidence",), "private-value-sentinel"),
            (("client_version",), 42),
            (("client_version",), "private-value-sentinel"),
            (("client_version",), "1.2"),
            (("list_complete",), "true"),
            (("list_complete",), 1),
            (("list_complete",), DELETE),
            (("models",), []),
            (("models",), {"private-value-sentinel": 1}),
            (("models", 0), "private-value-sentinel"),
            (("models", 0, "id"), ""),
            (("models", 0, "id"), None),
            (("models", 0, "id"), " example-flash-high"),
            (("models", 0, "id"), "private value sentinel"),
            (("models", 1, "id"), "example-flash-high"),
            (("models", 0, "id"), "a" * 107 + "private-value-sentinel"),
            (("models", 0, "id"), "Private-value-sentinel"),
            (("models", 0, "id"), "projects/private-value-sentinel/models/example-flash"),
            (("models", 0, "id"), "private-value-sentinel@example.invalid"),
            (("models", 0, "id"), "example:private-value-sentinel"),
            (("models", 0, "id"), "auto"),
            (("models", 0, "id"), "recommended"),
            (("models", 0, "display_name"), ""),
            (("models", 0, "display_name"), None),
            (("models", 0, "display_name"), " private-value-sentinel "),
            (("models", 0, "display_name"), "private-value-sentinel\nsecond line"),
            (("models", 0, "display_name"), "x" * 107 + "private-value-sentinel"),
            (("models", 0, "display_name"), "private-value-sentinel\x85"),
            (("models", 0, "display_name"), "​"),
            (("models", 0, "display_name"), "Example‮ private-value-sentinel"),
            (("models", 0, "display_name"), "Example private-value-sentinel"),
            (("models", 0, "display_name"), "Shared by private-value-sentinel@example.invalid"),
            (("models", 0, "display_name"), "https://example.invalid/private-value-sentinel"),
            (("models", 1, "display_name"), "Example Flash (High)"),
            (("models", 0, "display_name"), DELETE),
            (("models", 0, "label"), "private-value-sentinel"),
            (("models", 0, "selectable"), True),
            (("conversation_id",), "private-value-sentinel"),
            (("usage",), {"private-value-sentinel": 1}),
        ]
        for keys, value in invalid_fields:
            with self.subTest(field=keys, value=value):
                snapshot = self.snapshot()
                target = snapshot
                for key in keys[:-1]:
                    target = target[key]
                if value is DELETE:
                    del target[keys[-1]]
                else:
                    target[keys[-1]] = value
                self.write_json(path, snapshot)
                with self.assertRaises(self.module.CatalogError) as error:
                    self.module.antigravity_catalog(self.home, None, path)
                self.assertNotIn("private-value-sentinel", str(error.exception))
        for raw in ("{", '["private-value-sentinel"]', "[" * 100000 + "]" * 100000):
            with self.subTest(raw=raw):
                path.write_text(raw, encoding="utf-8")
                with self.assertRaises(self.module.CatalogError) as error:
                    self.module.antigravity_catalog(self.home, None, path)
                self.assertNotIn("private-value-sentinel", str(error.exception))

    def test_invalid_snapshot_is_rejected_before_the_cli_runs(self):
        path = self.root / "observed-models.json"
        snapshot = self.snapshot()
        snapshot["evidence"] = "hand_typed"
        self.write_json(path, snapshot)
        binary = self.executable(self.root / "install" / "agy")
        with mock.patch.object(self.module, "antigravity_version") as probe:
            with self.assertRaises(self.module.CatalogError):
                self.module.antigravity_catalog(self.home, binary, path)
        probe.assert_not_called()

    def test_main_passes_antigravity_options_and_writes_its_catalog(self):
        observations = self.root / "observed.json"
        binary = self.root / "install" / "agy"
        builders = {
            name: mock.patch.object(self.module, name, return_value={"models": []})
            for name in (
                "openai_catalog", "anthropic_catalog", "perplexity_catalog",
                "antigravity_catalog",
            )
        }
        with contextlib.ExitStack() as stack:
            mocks = {name: stack.enter_context(patch) for name, patch in builders.items()}
            writer = stack.enter_context(mock.patch.object(self.module, "write_catalog"))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(mock.patch.object(sys, "argv", [
                "refresh-catalogs.py",
                "--antigravity-home", str(self.home),
                "--antigravity-binary", str(binary),
                "--antigravity-model-observations", str(observations),
            ]))
            self.assertEqual(self.module.main(), 0)

        mocks["antigravity_catalog"].assert_called_once_with(
            self.home.resolve(), binary.resolve(), observations.resolve()
        )
        written = [call.args[0] for call in writer.call_args_list]
        self.assertIn(SCRIPT.resolve().parent / "antigravity" / "models.json", written)

    def test_main_defaults_to_shared_gemini_home_and_tracked_snapshot(self):
        with contextlib.ExitStack() as stack:
            for name in ("openai_catalog", "anthropic_catalog", "perplexity_catalog"):
                stack.enter_context(
                    mock.patch.object(self.module, name, return_value={"models": []})
                )
            builder = stack.enter_context(
                mock.patch.object(self.module, "antigravity_catalog", return_value={"models": []})
            )
            stack.enter_context(mock.patch.object(self.module, "write_catalog"))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(mock.patch.object(sys, "argv", ["refresh-catalogs.py"]))
            self.module.main()

        builder.assert_called_once_with(
            (self.root / ".gemini").resolve(), None,
            SCRIPT.resolve().parent / "antigravity" / "observed-models.json",
        )

    def test_check_option_validates_a_snapshot_without_refreshing(self):
        path = self.root / "candidate.json"
        invalid = self.snapshot()
        invalid["models"] = []
        for content, expected in ((self.snapshot(), 0), (invalid, 1), (None, 1)):
            with self.subTest(expected=expected, missing=content is None):
                if content is None:
                    path.unlink()
                else:
                    self.write_json(path, content)
                with contextlib.ExitStack() as stack:
                    builders = [
                        stack.enter_context(mock.patch.object(self.module, name))
                        for name in (
                            "openai_catalog", "anthropic_catalog", "perplexity_catalog",
                            "antigravity_catalog", "write_catalog",
                        )
                    ]
                    stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
                    stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
                    stack.enter_context(mock.patch.object(sys, "argv", [
                        "refresh-catalogs.py",
                        "--check-antigravity-model-observations", str(path),
                    ]))
                    self.assertEqual(self.module.main(), expected)
                for builder in builders:
                    builder.assert_not_called()


if __name__ == "__main__":
    unittest.main()
