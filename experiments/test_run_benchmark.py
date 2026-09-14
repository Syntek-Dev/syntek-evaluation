"""Exercise the Markdown runner with a real fixture reader and mocked runtime.

Run: python3 -m unittest discover -s experiments -p 'test_run_benchmark.py'
No model calls, network access or GPU hardware are required.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


EXPERIMENTS = Path(__file__).resolve().parent


@unittest.skipUnless(shutil.which('jq') and shutil.which('bash'), 'requires jq and bash')
class RunBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        # A space also checks that the runner handles its own location safely.
        self.experiments = self.root / 'model lab'
        self.experiments.mkdir()
        for name in ('run-benchmark.sh', 'populate-benchmarks.py'):
            shutil.copy2(EXPERIMENTS / name, self.experiments / name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.runtime_log = self.root / 'runtime.log'
        self.request = self.root / 'request.json'
        self.environment = {
            **os.environ,
            'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
            'BENCHMARK_TEST_RUNTIME_LOG': str(self.runtime_log),
            'BENCHMARK_TEST_REQUEST': str(self.request),
        }
        self.mock_command('curl', '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

with open(os.environ['BENCHMARK_TEST_RUNTIME_LOG'], 'a') as log:
    log.write('curl\\n')
arguments = sys.argv[1:]
if 'http://127.0.0.1:11434/api/version' in arguments:
    print(json.dumps({'version': 'test-runtime'}))
elif 'http://127.0.0.1:11434/api/generate' in arguments:
    payload = arguments[arguments.index('-d') + 1]
    json.loads(payload)
    Path(os.environ['BENCHMARK_TEST_REQUEST']).write_text(payload)
    print(json.dumps({
        'response': 'Mock answer', 'done': True,
        'prompt_eval_count': 11, 'eval_count': 7,
        'prompt_eval_duration': 100000000, 'eval_duration': 200000000,
        'total_duration': 400000000, 'load_duration': 100000000,
    }))
else:
    sys.exit('Unexpected curl invocation: ' + repr(arguments))
''')
        self.mock_command('ollama', '''#!/usr/bin/env bash
printf 'ollama\\n' >> "$BENCHMARK_TEST_RUNTIME_LOG"
[[ "$1" == ps ]] || exit 1
printf 'NAME ID SIZE PROCESSOR CONTEXT UNTIL\\n'
printf 'test:model abc 1 GB 100%% GPU 8192 5 minutes from now\\n'
''')
        self.mock_command('nvidia-smi', '''#!/usr/bin/env bash
printf 'nvidia-smi\\n' >> "$BENCHMARK_TEST_RUNTIME_LOG"
printf 'Mock GPU, 16384, 2048, 0, 42, 50.0\\n'
''')
        self.mock_command('free', '''#!/usr/bin/env bash
printf 'free\\n' >> "$BENCHMARK_TEST_RUNTIME_LOG"
printf '              total used free shared buff/cache available\\n'
printf 'Mem: 32000000000 8000000000 16000000000 0 8000000000 24000000000\\n'
''')
        self.mock_command('lscpu', '''#!/usr/bin/env bash
printf 'lscpu\\n' >> "$BENCHMARK_TEST_RUNTIME_LOG"
printf 'Model name: Mock CPU\\nCore(s) per socket: 4\\nCPU(s): 8\\n'
''')

    def mock_command(self, name, content):
        path = self.bin / name
        path.write_text(content)
        path.chmod(0o755)

    def run_benchmark(self, name):
        return subprocess.run(
            ['bash', str(self.experiments / 'run-benchmark.sh'), 'test:model', name],
            cwd=self.root, env=self.environment, capture_output=True, text=True,
            timeout=20,
        )

    def write_fixture(self, body, version=2):
        metadata = {
            'benchmark': 'coding--python-production-code-review',
            'version': version,
            'domain': 'coding',
            'capability': 'code-review',
            'jurisdiction': 'UK',
            'expected_output': 'analysis-and-code',
            'scoring': 'qualitative',
        }
        header = '---\n' + ''.join(f'{key}: {value}\n' for key, value in metadata.items()) + '---\n'
        content = header.encode() + body
        path = self.experiments / 'prompts/coding/python-production-code-review.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return metadata, content

    def test_only_body_is_sent_and_metadata_and_hashes_are_recorded(self):
        cases = (
            (2, '# Task\n\nReview "quotes", \\slashes, $(literal), `code`, £5 and\t tabs.\n\n'.encode()),
            (0, b'You are reviewing production Python code.\n\n'
             b'Consider this function:\n\n'
             b'def read_config(path):\n'
             b'    with open(path) as f:\n'
             b'        return json.load(f)\n\n'
             b'Identify every issue you can find with this implementation for a production Linux service. '
             b'Consider imports, encoding, error handling, security, observability, typing, testing, '
             b'and operational behaviour.\n\n'
             b'Then provide an improved implementation and explain each change.\n'),
            (2, b'\n# Task\r\n\r\nKeep the body line endings and trailing space. \r\n'),
        )
        for index, (version, body) in enumerate(cases, start=1):
            with self.subTest(version=version):
                metadata, content = self.write_fixture(body, version)
                result = self.run_benchmark('coding/python-production-code-review')
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                request = json.loads(self.request.read_text())
                expected_input = body.rstrip(b'\n')
                self.assertEqual(request, {
                    'model': 'test:model', 'prompt': expected_input.decode(),
                    'stream': False, 'keep_alive': '5m',
                })
                # The runner's existing log is a sequence of JSON objects.
                records = subprocess.run(
                    ['jq', '-s', '.', str(self.experiments / 'results/benchmarks.jsonl')],
                    capture_output=True, text=True, check=True, timeout=5,
                )
                record = json.loads(records.stdout)[-1]
                self.assertEqual(record['id'], f'AI01-{index:04d}')
                self.assertEqual(record['prompt'], 'coding/python-production-code-review')
                self.assertEqual(record['fixture_metadata'], metadata)
                self.assertEqual(record['input_sha256'], hashlib.sha256(expected_input).hexdigest())
                self.assertEqual(record['fixture_sha256'], hashlib.sha256(content).hexdigest())
                self.assertEqual(record['runtime_version'], 'test-runtime')
                self.assertEqual(record['prompt_tokens'], 11)
                self.assertEqual(record['output_tokens'], 7)

    def test_malformed_frontmatter_fails_before_runtime_or_results(self):
        self.write_fixture(b'# Task\nTest\n')
        path = self.experiments / 'prompts/coding/python-production-code-review.md'
        path.write_text('---\nversion: not-an-integer\n---\n# Task\nTest\n')
        result = self.run_benchmark('coding/python-production-code-review')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ERROR:', result.stdout + result.stderr)
        self.assertFalse(self.runtime_log.exists())
        self.assertFalse((self.experiments / 'results').exists())

    def test_txt_file_requires_migration_before_running(self):
        self.write_fixture(b'# Task\nTest\n')
        path = self.experiments / 'prompts/coding/python-production-code-review.md'
        path.rename(path.with_suffix('.txt'))
        result = self.run_benchmark('coding/python-production-code-review')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('python-production-code-review.md', result.stdout)
        self.assertFalse(self.runtime_log.exists())
        self.assertFalse((self.experiments / 'results').exists())


if __name__ == '__main__':
    unittest.main()
