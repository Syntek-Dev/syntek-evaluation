"""Exercise the Markdown runner with a real fixture reader and a mocked llama-server.

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
            'BENCHMARK_TEST_SERVER_MODE': 'ok',
        }
        self.environment.pop('LLAMA_SERVER_URL', None)
        self.environment.pop('BENCHMARK_MACHINE_ID', None)
        # A mock llama-server: /health, /props and /v1/chat/completions.
        self.mock_command('curl', '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit

arguments = sys.argv[1:]
urls = [argument for argument in arguments if argument.startswith('http')]
if len(urls) != 1:
    sys.exit('Unexpected curl invocation: ' + repr(arguments))
url = urlsplit(urls[0])
with open(os.environ['BENCHMARK_TEST_RUNTIME_LOG'], 'a') as log:
    log.write('curl ' + urls[0] + '\\n')
mode = os.environ['BENCHMARK_TEST_SERVER_MODE']
if url.path == '/health':
    if mode == 'loading':
        print('curl: (22) The requested URL returned error: 503', file=sys.stderr)
        sys.exit(22)
    print(json.dumps({'status': 'ok'}))
elif url.path == '/props':
    print(json.dumps({
        'build_info': 'b9999-abc1234',
        'model_path': '/models/test-model-Q4_K_M.gguf',
        'total_slots': 1,
        'default_generation_settings': {'n_ctx': 8192},
    }))
elif url.path == '/v1/chat/completions':
    payload = arguments[arguments.index('-d') + 1]
    json.loads(payload)
    Path(os.environ['BENCHMARK_TEST_REQUEST']).write_text(payload)
    response = {
        'object': 'chat.completion',
        'model': 'test:model',
        'choices': [{
            'index': 0, 'finish_reason': 'stop',
            'message': {'role': 'assistant', 'content': 'Mock answer'},
        }],
        'usage': {'prompt_tokens': 11, 'completion_tokens': 7, 'total_tokens': 18},
    }
    if mode != 'no-timings':
        response['timings'] = {
            'cache_n': 0,
            'prompt_n': 11, 'prompt_ms': 100.0, 'prompt_per_second': 110.0,
            'predicted_n': 7, 'predicted_ms': 200.0, 'predicted_per_second': 35.0,
        }
    print(json.dumps(response))
else:
    sys.exit('Unexpected curl invocation: ' + repr(arguments))
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

    def records(self):
        # Every line of the results log must be one complete JSON object.
        lines = (self.experiments / 'results/benchmarks.jsonl').read_text().splitlines()
        return [json.loads(line) for line in lines]

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
                    'model': 'test:model',
                    'messages': [{'role': 'user', 'content': expected_input.decode()}],
                    'stream': False,
                })
                records = self.records()
                self.assertEqual(len(records), index)
                record = records[-1]
                self.assertEqual(record['id'], f'AI01-{index:04d}')
                self.assertEqual(record['prompt'], 'coding/python-production-code-review')
                self.assertEqual(record['fixture_metadata'], metadata)
                self.assertEqual(record['input_sha256'], hashlib.sha256(expected_input).hexdigest())
                self.assertEqual(record['fixture_sha256'], hashlib.sha256(content).hexdigest())
                self.assertEqual(record['runtime'], 'llama.cpp')
                self.assertEqual(record['runtime_version'], 'b9999-abc1234')
                self.assertEqual(record['prompt_tokens'], 11)
                self.assertEqual(record['prompt_processed_tokens'], 11)
                self.assertEqual(record['prompt_cached_tokens'], 0)
                self.assertEqual(record['output_tokens'], 7)
                self.assertEqual(record['prompt_duration_ns'], 100000000)
                self.assertEqual(record['output_duration_ns'], 200000000)
                self.assertEqual(record['total_duration_ns'], 300000000)
                self.assertEqual(record['prompt_tokens_per_second'], 110.0)
                self.assertEqual(record['generation_tokens_per_second'], 35.0)
                self.assertEqual(record['total_duration_seconds'], 0.3)
                self.assertEqual(record['llama_server'], {
                    'url': 'http://127.0.0.1:8080',
                    'model_path': '/models/test-model-Q4_K_M.gguf',
                    'served_model': 'test:model',
                    'context_tokens': 8192,
                    'slots': 1,
                })
                raw = json.loads((self.experiments / f'results/outputs/AI01-{index:04d}.json').read_text())
                self.assertEqual(raw['choices'][0]['message']['content'], 'Mock answer')

    def test_response_without_llama_timings_records_nulls_not_guesses(self):
        # Other OpenAI-compatible servers (vLLM) return usage but no timings.
        self.environment['BENCHMARK_TEST_SERVER_MODE'] = 'no-timings'
        self.write_fixture(b'# Task\nTest\n')
        result = self.run_benchmark('coding/python-production-code-review')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = self.records()[-1]
        self.assertEqual(record['prompt_tokens'], 11)
        self.assertEqual(record['output_tokens'], 7)
        for field in (
            'prompt_processed_tokens', 'prompt_cached_tokens', 'prompt_duration_ns',
            'output_duration_ns', 'total_duration_ns', 'prompt_tokens_per_second',
            'generation_tokens_per_second', 'total_duration_seconds',
        ):
            self.assertIsNone(record[field], field)
        self.assertIsInstance(record['wall_duration_seconds'], float)

    def test_server_url_and_machine_can_be_overridden(self):
        self.environment['LLAMA_SERVER_URL'] = 'http://127.0.0.1:9999/'
        self.environment['BENCHMARK_MACHINE_ID'] = 'AI02'
        self.write_fixture(b'# Task\nTest\n')
        result = self.run_benchmark('coding/python-production-code-review')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = self.records()[-1]
        self.assertEqual(record['id'], 'AI02-0001')
        self.assertEqual(record['machine'], 'AI02')
        self.assertEqual(record['llama_server']['url'], 'http://127.0.0.1:9999')
        called = [line for line in self.runtime_log.read_text().splitlines() if line.startswith('curl ')]
        self.assertTrue(called)
        self.assertTrue(all(line.startswith('curl http://127.0.0.1:9999/') for line in called), called)

    def test_server_not_ready_fails_before_results(self):
        self.environment['BENCHMARK_TEST_SERVER_MODE'] = 'loading'
        self.write_fixture(b'# Task\nTest\n')
        result = self.run_benchmark('coding/python-production-code-review')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ERROR: llama-server is not ready', result.stdout + result.stderr)
        self.assertFalse(self.request.exists())
        self.assertFalse((self.experiments / 'results').exists())

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
