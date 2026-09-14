"""Safety and integration checks for the standalone fixture population script.

Run: python3 -m unittest discover -s experiments -p 'test_populate_benchmarks.py'
All writes occur in temporary directories, never in the real prompt tree.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name('populate-benchmarks.py')


class PopulateBenchmarksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('populate_benchmarks', SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.prompts = self.root / 'prompts'

    def run_script(self, *arguments, success=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--prompt-dir', str(self.prompts), *arguments],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def hashes(self):
        return {p.relative_to(self.prompts).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.prompts.rglob('*.md')}

    def read_prompt(self, path, *, success=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--read-prompt', str(path)],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return json.loads(result.stdout) if success else result

    def write_prompt(self, relative, content):
        path = self.prompts / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def frontmatter(self, *, version='2'):
        return (
            '---\n'
            'benchmark: coding--python-refactor\n'
            f'version: {version}\n'
            'domain: coding\n'
            'capability: refactoring\n'
            'jurisdiction: UK\n'
            'expected_output: analysis-and-code\n'
            'scoring: qualitative\n'
            '---\n'
        )

    def test_dry_run_has_no_filesystem_side_effects(self):
        export = self.root / 'new-directory' / 'rubrics.json'
        result = self.run_script('--dry-run', '--export-rubrics', str(export))
        self.assertIn('135 would populate, 0 preserved', result.stdout)
        self.assertFalse(self.prompts.exists())
        self.assertFalse(export.parent.exists())

    def test_full_inventory_metadata_and_assessor_export(self):
        export = self.root / 'rubrics.json'
        self.run_script('--export-rubrics', str(export))
        files = sorted(self.prompts.rglob('*.md'))
        self.assertEqual(len(files), 135)
        self.assertEqual(len({p.parent.name for p in files}), 15)
        self.assertEqual(list(self.prompts.rglob('*.txt')), [])
        document = json.loads(export.read_text())
        self.assertEqual(document['schema_version'], 2)
        self.assertEqual(document['fixture_version'], 2)
        self.assertEqual(len(document['benchmarks']), 135)
        self.assertEqual(len({e['benchmark'] for e in document['benchmarks']}), 135)
        for entry in document['benchmarks']:
            content = (self.prompts / entry['path']).read_bytes()
            self.assertEqual(entry['sha256'], hashlib.sha256(content).hexdigest())
            self.assertEqual(entry['status'], 'versioned')
            self.assertEqual(entry['version'], 2)
            self.assertEqual(len(entry['criteria']), 5)
            self.assertGreaterEqual(len(entry['reference']), 3)
            text = content.decode('utf-8')
            self.assertTrue(text.startswith('---\n'))
            frontmatter, body = text[4:].split('\n---\n', 1)
            for field in ('benchmark:', 'version: 2', 'domain:', 'capability:',
                          'jurisdiction:', 'expected_output:', 'scoring:'):
                self.assertIn(field, frontmatter)
            for section in ('# Task\n', '\n# Constraints\n', '\n# Evaluation criteria\n'):
                self.assertIn(section, text)
            self.assertEqual(entry['input_sha256'],
                             hashlib.sha256(body.rstrip('\n').encode()).hexdigest())
            self.assertNotIn('ASSESSOR REFERENCE', text)

    def test_repeat_run_preserves_bytes_and_timestamps(self):
        export = self.root / 'rubrics.json'
        self.run_script('--export-rubrics', str(export))
        before = self.hashes()
        timestamps = {p: p.stat().st_mtime_ns for p in self.prompts.rglob('*.md')}
        export_before = export.read_bytes(), export.stat().st_mtime_ns
        result = self.run_script('--export-rubrics', str(export))
        self.assertIn('0 populated, 135 preserved', result.stdout)
        self.assertEqual(before, self.hashes())
        self.assertEqual(timestamps, {p: p.stat().st_mtime_ns for p in timestamps})
        self.assertEqual(export_before, (export.read_bytes(), export.stat().st_mtime_ns))

    def test_concurrent_runs_produce_complete_identical_files(self):
        export = self.root / 'rubrics.json'
        processes = [subprocess.Popen(
            [sys.executable, str(SCRIPT), '--prompt-dir', str(self.prompts),
             '--export-rubrics', str(export)], cwd=self.root,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ) for _ in range(3)]
        try:
            for process in processes:
                stdout, stderr = process.communicate(timeout=30)
                self.assertEqual(process.returncode, 0, stdout + stderr)
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.communicate()
        self.assertEqual(len(self.hashes()), 135)
        for entry in json.loads(export.read_text())['benchmarks']:
            self.assertEqual(entry['status'], 'versioned')
            content = (self.prompts / entry['path']).read_bytes()
            self.assertEqual(entry['sha256'], hashlib.sha256(content).hexdigest())

    def test_existing_nonempty_bytes_are_preserved_and_not_misgraded(self):
        path = self.prompts / 'coding' / 'python-refactor.md'
        path.parent.mkdir(parents=True)
        sentinel = b'\xff\r\nExisting validated fixture\x00'
        path.write_bytes(sentinel)
        path.chmod(0o444)
        export = self.root / 'rubrics.json'
        result = self.run_script('--export-rubrics', str(export))
        self.assertIn('134 populated, 1 preserved', result.stdout)
        self.assertEqual(path.read_bytes(), sentinel)
        entry = next(e for e in json.loads(export.read_text())['benchmarks']
                     if e['path'] == 'coding/python-refactor.md')
        self.assertEqual(entry['status'], 'preserved-unrecognised')
        self.assertEqual(entry['reference'], [])
        self.assertEqual(entry['criteria'], [])
        self.assertIsNone(entry['max_score'])
        self.assertIsNone(entry['input_sha256'])

    def test_zero_byte_filled_but_whitespace_preserved(self):
        domain = self.prompts / 'reasoning'
        domain.mkdir(parents=True)
        empty = domain / 'scheduling.md'
        empty.touch()
        whitespace = domain / 'numerical-reasoning.md'
        whitespace.write_bytes(b' \n\t')
        self.run_script()
        self.assertTrue(empty.read_text().startswith('---\n'))
        self.assertEqual(whitespace.read_bytes(), b' \n\t')

    def test_validated_legacy_body_survives_migration_and_model_input(self):
        # This source is the original validated prompt, including its final newline.
        original = (
            'You are reviewing production Python code.\n\n'
            'Consider this function:\n\n'
            'def read_config(path):\n'
            '    with open(path) as f:\n'
            '        return json.load(f)\n\n'
            'Identify every issue you can find with this implementation for a production Linux service. '
            'Consider imports, encoding, error handling, security, observability, typing, testing, '
            'and operational behaviour.\n\n'
            'Then provide an improved implementation and explain each change.\n'
        ).encode()
        relative = 'coding/python-production-code-review.md'
        self.assertEqual(hashlib.sha256(original).hexdigest(), self.module.LEGACY_HASHES[relative])
        old_path = self.write_prompt(str(Path(relative).with_suffix('.txt')), original)
        export = self.root / 'rubrics.json'
        self.run_script('--migrate-txt', '--export-rubrics', str(export))
        path = self.prompts / relative
        self.assertFalse(old_path.exists())
        self.assertEqual(path.read_bytes().split(b'\n---\n', 1)[1], original)
        parsed = self.read_prompt(path)
        self.assertEqual(parsed['metadata']['version'], 0)
        self.assertEqual(parsed['prompt'].encode(), original.rstrip(b'\n'))
        self.assertEqual(parsed['input_sha256'],
                         hashlib.sha256(original.rstrip(b'\n')).hexdigest())
        entry = next(e for e in json.loads(export.read_text())['benchmarks'] if e['path'] == relative)
        self.assertEqual(entry['status'], 'validated-legacy')
        self.assertEqual(entry['version'], 0)
        self.assertEqual(entry['input_sha256'], parsed['input_sha256'])
        self.assertEqual(len(entry['criteria']), 5)

    def test_text_files_require_explicit_migration(self):
        path = self.write_prompt('coding/python-refactor.txt', b'Original text\n')
        result = self.run_script(success=False)
        self.assertIn('--migrate-txt', result.stderr)
        self.assertEqual(path.read_bytes(), b'Original text\n')
        self.assertEqual(list(self.prompts.rglob('*.md')), [])

    def test_migrate_catalogue_and_validated_prompts_then_repeat(self):
        for relative in self.module.FIXTURES:
            content = self.module.LEGACY_CONTENTS.get(relative)
            if content is None:
                content = self.module.render_legacy_fixture(relative)
            elif isinstance(content, str):
                content = content.encode('utf-8')
            self.write_prompt(str(Path(relative).with_suffix('.txt')), content)
        before = {path: path.read_bytes() for path in self.prompts.rglob('*.txt')}
        export = self.root / 'rubrics.json'
        self.run_script('--migrate-txt', '--dry-run', '--export-rubrics', str(export))
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        self.assertEqual(list(self.prompts.rglob('*.md')), [])
        self.assertFalse(export.exists())
        self.run_script('--migrate-txt', '--export-rubrics', str(export))
        self.assertEqual(len(list(self.prompts.rglob('*.md'))), 135)
        self.assertEqual(list(self.prompts.rglob('*.txt')), [])
        for entry in json.loads(export.read_text())['benchmarks']:
            relative = entry['path']
            if relative in self.module.LEGACY_CONTENTS:
                self.assertEqual(entry['status'], 'validated-legacy')
                self.assertEqual(entry['version'], 0)
            else:
                self.assertEqual(entry['status'], 'versioned')
                self.assertEqual(entry['version'], 2)
                self.assertEqual((self.prompts / relative).read_bytes(),
                                 self.module.render_fixture(relative))
        hashes = self.hashes()
        timestamps = {path: path.stat().st_mtime_ns for path in self.prompts.rglob('*.md')}
        self.run_script('--migrate-txt', '--export-rubrics', str(export))
        self.assertEqual(self.hashes(), hashes)
        self.assertEqual(timestamps, {path: path.stat().st_mtime_ns for path in timestamps})

    def test_custom_text_migration_preserves_exact_body_without_assigning_rubric(self):
        original = '\nCustom café prompt.\r\n---\nKeep this divider.\r\n\n'.encode('utf-8')
        source = self.write_prompt('coding/python-refactor.txt', original)
        empty = self.write_prompt('reasoning/scheduling.txt', b'')
        export = self.root / 'rubrics.json'
        self.run_script('--migrate-txt', '--export-rubrics', str(export))
        destination = source.with_suffix('.md')
        self.assertFalse(source.exists())
        self.assertFalse(empty.exists())
        self.assertEqual(destination.read_bytes().split(b'\n---\n', 1)[1], original)
        parsed = self.read_prompt(destination)
        self.assertEqual(parsed['prompt'].encode('utf-8'), original.rstrip(b'\n'))
        self.assertEqual(parsed['metadata']['version'], 0)
        entry = next(e for e in json.loads(export.read_text())['benchmarks']
                     if e['path'] == 'coding/python-refactor.md')
        self.assertEqual(entry['status'], 'preserved-unrecognised')
        self.assertEqual(entry['criteria'], [])
        self.assertEqual(entry['reference'], [])
        self.assertIsNone(entry['max_score'])
        self.assertEqual(entry['input_sha256'], parsed['input_sha256'])
        self.assertEqual(empty.with_suffix('.md').read_bytes(),
                         self.module.render_fixture('reasoning/scheduling.md'))

    def test_migration_conflict_and_invalid_utf8_fail_before_any_changes(self):
        for failure in ('conflict', 'utf8'):
            with self.subTest(failure=failure):
                self.prompts = self.root / failure
                first = self.write_prompt('adversarial/ambiguous-requirement.txt', b'Keep first\n')
                source = self.write_prompt('coding/python-refactor.txt',
                                           b'Keep source\n' if failure == 'conflict' else b'\xff')
                if failure == 'conflict':
                    self.write_prompt('coding/python-refactor.md', b'Keep destination\n')
                before = {path: path.read_bytes() for path in self.prompts.rglob('*.*')}
                export = self.root / (failure + '.json')
                self.run_script('--migrate-txt', '--export-rubrics', str(export), success=False)
                self.assertEqual(before,
                                 {path: path.read_bytes() for path in self.prompts.rglob('*.*')})
                self.assertTrue(first.exists())
                self.assertTrue(source.exists())
                self.assertFalse(export.exists())

    def test_migration_resumes_when_converted_destination_already_exists(self):
        relative = 'coding/python-refactor.md'
        source = self.write_prompt('coding/python-refactor.txt',
                                   self.module.render_legacy_fixture(relative))
        destination = self.write_prompt(relative, self.module.render_fixture(relative))
        before = destination.read_bytes(), destination.stat().st_mtime_ns
        self.run_script('--migrate-txt')
        self.assertFalse(source.exists())
        self.assertEqual(before, (destination.read_bytes(), destination.stat().st_mtime_ns))
        self.assertEqual(len(self.hashes()), 135)

    def test_read_prompt_returns_only_body_and_distinct_hashes(self):
        body = '\n# Task\nKeep café and CRLF.\r\n---\nBody divider.\n\n'
        content = (self.frontmatter() + body).encode('utf-8')
        path = self.root / 'input.md'
        path.write_bytes(content)
        parsed = self.read_prompt(path)
        self.assertEqual(parsed['metadata'], {
            'benchmark': 'coding--python-refactor', 'version': 2, 'domain': 'coding',
            'capability': 'refactoring', 'jurisdiction': 'UK',
            'expected_output': 'analysis-and-code', 'scoring': 'qualitative',
        })
        self.assertEqual(parsed['prompt'], body.rstrip('\n'))
        self.assertEqual(parsed['input_sha256'],
                         hashlib.sha256(body.rstrip('\n').encode('utf-8')).hexdigest())
        self.assertEqual(parsed['fixture_sha256'], hashlib.sha256(content).hexdigest())
        self.assertFalse(self.prompts.exists())

    def test_read_prompt_rejects_missing_required_fields(self):
        header = self.frontmatter()
        path = self.root / 'input.md'
        for field in ('benchmark', 'version', 'domain', 'capability', 'jurisdiction',
                      'expected_output', 'scoring'):
            with self.subTest(field=field):
                missing = ''.join(line for line in header.splitlines(keepends=True)
                                  if not line.startswith(field + ':'))
                path.write_text(missing + '# Task\nA task.\n')
                self.read_prompt(path, success=False)
        self.assertFalse(self.prompts.exists())

    def test_read_prompt_accepts_supported_yaml_quoting_and_comments(self):
        header = self.frontmatter().replace(
            'domain: coding\n', '# Metadata comment\n\ndomain: "coding"\n'
        ).replace('jurisdiction: UK\n', "jurisdiction: 'UK'\nnotes: 'Owner''s fixture'\n")
        body = '# Task\n\nKeep this body.\n---\nIncluding its horizontal rule.\n'
        path = self.root / 'quoted.md'
        path.write_text(header + body)
        payload = self.read_prompt(path)
        self.assertEqual(payload['metadata']['domain'], 'coding')
        self.assertEqual(payload['metadata']['jurisdiction'], 'UK')
        self.assertEqual(payload['metadata']['notes'], "Owner's fixture")
        self.assertEqual(payload['prompt'], body.rstrip('\n'))

    def test_read_prompt_rejects_bad_versions_duplicates_and_delimiters(self):
        header = self.frontmatter()
        invalid = {
            'no frontmatter': '# Task\nA task.\n',
            'noninitial frontmatter': '\n' + header,
            'unclosed frontmatter': header.rsplit('---\n', 1)[0],
            'duplicate field': header.replace('version: 2\n', 'version: 2\nversion: 0\n'),
            'text version': self.frontmatter(version='two'),
            'negative version': self.frontmatter(version='-1'),
            'boolean version': self.frontmatter(version='true'),
            'fractional version': self.frontmatter(version='1.5'),
            'hexadecimal scalar': header.replace('domain: coding', 'domain: 0xFF'),
            'exponent scalar': header.replace('domain: coding', 'domain: 1e3'),
            'collection scalar': header.replace('domain: coding', 'domain: [coding]'),
        }
        path = self.root / 'input.md'
        for case, content in invalid.items():
            with self.subTest(case=case):
                path.write_text(content + '# Task\nA non-empty task.\n')
                result = self.read_prompt(path, success=False)
                self.assertTrue(result.stderr)
        self.assertFalse(self.prompts.exists())

    def test_unknown_fixture_fails_before_writes(self):
        for suffix, arguments in (('.md', ()), ('.txt', ('--migrate-txt',))):
            with self.subTest(suffix=suffix):
                self.prompts = self.root / ('unknown-' + suffix[1:])
                unknown = self.write_prompt('coding/unknown' + suffix, b'custom fixture\n')
                result = self.run_script(*arguments, success=False)
                self.assertIn('No authored benchmark', result.stderr)
                self.assertEqual(list(self.prompts.rglob('*' + suffix)), [unknown])
                self.assertEqual(unknown.read_bytes(), b'custom fixture\n')
                self.assertEqual(len(list(self.prompts.rglob('*.*'))), 1)

    def test_symlink_file_is_rejected_without_touching_target(self):
        target = self.root / 'outside.md'
        target.write_bytes(b'protected')
        for suffix, arguments in (('.md', ()), ('.txt', ('--migrate-txt',))):
            with self.subTest(suffix=suffix):
                self.prompts = self.root / ('symlink-' + suffix[1:])
                domain = self.prompts / 'coding'
                domain.mkdir(parents=True)
                link = domain / ('python-refactor' + suffix)
                link.symlink_to(target)
                result = self.run_script(*arguments, success=False)
                self.assertIn('Refusing symlink', result.stderr)
                self.assertTrue(link.is_symlink())
                self.assertEqual(target.read_bytes(), b'protected')
                self.assertEqual(len(list(self.prompts.rglob('*.*'))), 1)

    def test_symlink_directory_is_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        self.prompts.mkdir()
        (self.prompts / 'coding').symlink_to(outside, target_is_directory=True)
        self.run_script(success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_conflicting_rubric_export_fails_before_population(self):
        export = self.root / 'rubrics.json'
        export.write_bytes(b'{"existing":"do not overwrite"}\n')
        before = export.read_bytes()
        self.run_script('--export-rubrics', str(export), success=False)
        self.assertEqual(export.read_bytes(), before)
        self.assertFalse(self.prompts.exists())
        source = self.write_prompt('coding/python-refactor.txt', b'Keep source\n')
        self.run_script('--migrate-txt', '--export-rubrics', str(export), success=False)
        self.assertEqual(export.read_bytes(), before)
        self.assertEqual(source.read_bytes(), b'Keep source\n')
        self.assertEqual(list(self.prompts.rglob('*.md')), [])

    def test_rubrics_cannot_be_exported_into_model_inputs(self):
        result = self.run_script('--export-rubrics', str(self.prompts / 'answers.json'), success=False)
        self.assertIn('outside the prompts tree', result.stderr)
        self.assertFalse(self.prompts.exists())

    def test_export_file_cannot_be_a_future_prompt_parent_directory(self):
        export = self.root / 'new' / 'rubrics.json'
        self.prompts = export / 'prompts'
        result = self.run_script('--export-rubrics', str(export), success=False)
        self.assertIn('parent directory', result.stderr)
        self.assertFalse(export.exists())

    def test_standalone_copy_uses_script_directory_from_unrelated_cwd(self):
        destination = self.root / 'standalone'
        destination.mkdir()
        script = destination / 'populate-benchmarks.py'
        shutil.copyfile(SCRIPT, script)
        result = subprocess.run([sys.executable, str(script)], cwd='/tmp',
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((destination / 'prompts').rglob('*.md'))), 135)
        self.assertFalse(self.prompts.exists())


if __name__ == '__main__':
    unittest.main()
