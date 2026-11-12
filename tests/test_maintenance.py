"""Offline regression checks using synthetic text, isolated vaults and local Git."""
from pathlib import Path
import contextlib
import io
import re
import select
import signal
import time
import shlex
from unittest.mock import patch
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASH = '/bin/bash' if Path('/bin/bash').exists() else 'bash'


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    original = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = original
    return module


def read_fixture_marker(stream, expected, timeout=5):
    """Read one controlled subprocess barrier without an unbounded readline."""
    deadline, data = time.monotonic() + timeout, bytearray()
    while b'\n' not in data:
        remaining = deadline - time.monotonic()
        if remaining <= 0 or not select.select([stream], [], [], remaining)[0]:
            raise TimeoutError('Fixture did not complete its barrier marker')
        chunk = os.read(stream.fileno(), 4096)
        if not chunk:
            raise EOFError('Fixture closed before its barrier marker')
        data.extend(chunk)
        if len(data) > 4096:
            raise ValueError('Fixture barrier marker exceeds its bound')
    if bytes(data).splitlines()[0].decode('utf-8') != expected:
        raise ValueError('Unexpected fixture barrier marker')


def finish_fixture(process, input='release\n', timeout=10):
    """Reap the fixture's dedicated process group even if its writer stalls."""
    try:
        return process.communicate(input=input, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate(timeout=5)
        raise TimeoutError('Fixture process group exceeded its cleanup deadline') from error
    finally:
        for pipe in (process.stdin, process.stdout, process.stderr):
            if pipe is not None:
                pipe.close()


class IsolatedTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT='0', PYTHONDONTWRITEBYTECODE='1')
        self.real_git = shutil.which('git')
        self.empty_template = self.base / 'empty-template'
        self.empty_template.mkdir()

    def command(self, args, cwd=None, input=None, env=None):
        return subprocess.run(args, cwd=cwd, input=input, env=env or self.env,
                              text=True, capture_output=True, check=False, timeout=40)

    def git(self, directory, *args):
        result = self.command([self.real_git, '-C', str(directory), *args])
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def initialize(self, directory):
        directory.mkdir()
        self.git(directory, 'init', '--template=' + str(self.empty_template), '-b', 'main')
        self.git(directory, 'config', 'user.name', 'Fixture')
        self.git(directory, 'config', 'user.email', 'fixture@example.invalid')

    def write(self, directory, relative, text, executable=False):
        path = directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        if executable:
            path.chmod(0o755)
        return path

    def updater_fixture(self, validator_exit=0, full_table=False):
        upstream, vault = self.base / 'upstream', self.base / 'vault'
        for directory, label, version in [(upstream, 'new', '3.13.1'), (vault, 'old', '3.13.0')]:
            self.initialize(directory)
            self.write(directory, 'README.md', label + ' readme\n')
            self.write(directory, 'AGENTS.md', label + ' agents\n')
            self.write(directory, 'COG-VERSION', version + '\n')
            self.write(directory, '.claude-plugin/plugin.json', json.dumps({'name': 'cog-second-brain', 'version': version}))
            validator = '#!/bin/sh\nprintf "VALIDATOR_SEEN\\n"\nexit ' + str(validator_exit) + '\n'
            self.write(directory, 'scripts/validate-agent-surface.sh', validator, executable=True)
            self.write(directory, '.gitignore', (ROOT / '.gitignore').read_text())
            self.git(directory, 'add', '.')
            self.git(directory, 'commit', '-m', 'Synthetic fixture')
        source = (ROOT / 'cog-update.sh').read_text()
        if not full_table:
            # Absent upstream files have no effect on these fixtures. Keep one
            # full-table integration case; trim only fixture configuration here.
            fixture_files = ['README.md', 'AGENTS.md', 'COG-VERSION', '.claude-plugin/plugin.json',
                             'scripts/validate-agent-surface.sh', 'scripts/build-agent-plugin.sh', '.gitignore']
            table = 'FRAMEWORK_FILES=(\n' + ''.join('  "' + name + '"\n' for name in fixture_files) + ')'
            source, changed = re.subn(r'(?ms)^FRAMEWORK_FILES=\(\n.*?^\)', lambda _: table, source, count=1)
            self.assertEqual(changed, 1)
        self.write(vault, 'cog-update.sh', source, executable=True)
        self.write(vault, '00-inbox/MY-PROFILE.md', 'Synthetic private profile.\n')
        self.git(vault, 'remote', 'add', 'cog-upstream', 'https://github.com/huytieu/COG-second-brain.git')
        transport = self.base / 'transport-bin'
        transport.mkdir()
        # Preserve the advertised URL while replacing fetch transport with a
        # local fixture. No subprocess can contact a real upstream here.
        wrapper = ('#!/bin/sh\nif [ "$1" = fetch ]; then\n'
                   ' remote_url=$(' + shlex.quote(self.real_git) + ' remote get-url "$2") || exit\n'
                   ' exec ' + shlex.quote(self.real_git) + ' -c "url.file://' + str(upstream)
                   + '.insteadOf=$remote_url" -c protocol.file.allow=always "$@"\nfi\nexec '
                   + shlex.quote(self.real_git) + ' "$@"\n')
        self.fixture_git = self.write(transport, 'git', wrapper, executable=True)
        self.env['PATH'] = str(transport) + os.pathsep + self.env['PATH']
        return vault

    def update(self, vault, *args, input=None, env=None):
        return self.command([BASH, str(vault / 'cog-update.sh'), *args], cwd=vault, input=input, env=env)

    def checkpoint_fixture(self):
        vault = self.base / 'checkpoint-vault'
        vault.mkdir()
        script = self.write(vault, '.claude/lib/checkpoint.sh', (ROOT / '.claude/lib/checkpoint.sh').read_text(), executable=True)
        return vault, script

    def test_fixture_initialization_ignores_ambient_hook_sources(self):
        hooks = self.base / 'hostile-hooks'
        template = self.base / 'hostile-template'
        marker = self.base / 'hook-executed'
        hook = '#!/bin/sh\n: > ' + shlex.quote(str(marker)) + '\n'
        self.write(hooks, 'post-commit', hook, executable=True)
        self.write(template, 'hooks/post-commit', hook, executable=True)
        global_config = self.write(self.base, 'hostile-global-config', '[core]\n hooksPath = ' + json.dumps(str(hooks)) + '\n')
        ambient = {'GIT_TEMPLATE_DIR': str(template), 'GIT_CONFIG_GLOBAL': str(global_config),
                   'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.hooksPath',
                   'GIT_CONFIG_VALUE_0': str(hooks)}
        probe = IsolatedTests('test_fixture_initialization_ignores_ambient_hook_sources')
        try:
            with patch.dict(os.environ, ambient):
                probe.setUp()
                repo = probe.base / 'isolated-repository'
                probe.initialize(repo)
                # Refuse to make even a synthetic commit unless the actual
                # effective hook configuration and template output are empty.
                config = probe.command([probe.real_git, '-C', str(repo), 'config', '--get', 'core.hooksPath'])
                self.assertEqual(config.returncode, 1)
                self.assertFalse(any(path.is_file() and os.access(path, os.X_OK)
                                     for path in (repo / '.git/hooks').glob('*')))
                probe.git(repo, 'commit', '--allow-empty', '-m', 'Controlled hook-isolation fixture')
            self.assertFalse(marker.exists())
        finally:
            probe.doCleanups()

    def test_force_updates_every_file_and_preserves_vault(self):
        vault = self.updater_fixture(full_table=True)
        result = self.update(vault, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'new readme\n')
        self.assertEqual((vault / 'AGENTS.md').read_text(), 'new agents\n')
        self.assertEqual((vault / 'COG-VERSION').read_text(), '3.13.1\n')
        self.assertEqual((vault / '00-inbox/MY-PROFILE.md').read_text(), 'Synthetic private profile.\n')
        self.assertIn('VALIDATOR_SEEN', result.stdout)

    def test_interactive_no_preserves_framework_edits(self):
        vault = self.updater_fixture()
        result = self.update(vault, input='no\n' * 10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')
        self.assertEqual((vault / 'AGENTS.md').read_text(), 'old agents\n')

    def test_updater_refuses_directory_destination(self):
        vault = self.updater_fixture()
        (vault / 'README.md').unlink()
        (vault / 'README.md').mkdir()
        result = self.update(vault, '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('non-regular', result.stderr)
        self.assertEqual(list((vault / 'README.md').iterdir()), [])

    def test_validate_mode_refuses_linked_validator(self):
        vault = self.updater_fixture()
        sentinel = self.base / 'outside-executed'
        outside = self.write(self.base, 'outside-validator.sh', '#!/bin/sh\ntouch ' + shlex.quote(str(sentinel)) + '\n', executable=True)
        validator = vault / 'scripts/validate-agent-surface.sh'
        validator.unlink()
        validator.symlink_to(outside)
        result = self.update(vault, '--validate')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(sentinel.exists())

    def test_updater_comparison_failure_cannot_report_current(self):
        vault = self.updater_fixture()
        fake = self.base / 'bad-show'
        fake.mkdir()
        wrapper = '#!/bin/sh\nif [ "$1" = show ]; then case "$2" in *:README.md) exit 19;; esac; fi\nexec ' + shlex.quote(str(self.fixture_git)) + ' "$@"\n'
        self.write(fake, 'git', wrapper, executable=True)
        result = self.update(vault, '--force', env=dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH']))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Cannot compare', result.stderr)
        self.assertNotIn('Everything is up to date', result.stdout)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')

    def test_updater_busy_lock_preserves_framework(self):
        vault = self.updater_fixture()
        (vault / '.cog-update.lock').mkdir()
        result = self.update(vault, '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Another updater', result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')

    def test_interactive_skip_does_not_abort_after_first_item(self):
        vault = self.updater_fixture()
        result = self.update(vault, input='n\n' * 10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')
        self.assertEqual((vault / 'AGENTS.md').read_text(), 'old agents\n')
        self.assertIn('4 file(s) skipped', result.stdout)

    def test_packaging_failure_propagates_after_updates(self):
        vault = self.updater_fixture(validator_exit=7)
        result = self.update(vault, '--force')
        self.assertIn('VALIDATOR_SEEN', result.stdout)
        self.assertNotEqual(result.returncode, 0)

    def test_failed_git_show_cannot_truncate_live_framework(self):
        vault = self.updater_fixture()
        fake_bin = self.base / 'fake-bin'
        fake_bin.mkdir()
        counter = self.base / 'show-count'
        wrapper = ('#!/bin/sh\nif [ "$1" = show ]; then\n case "$2" in *:README.md)\n'
                   ' n=0\n [ ! -f ' + shlex.quote(str(counter)) + ' ] || n=$(cat ' + shlex.quote(str(counter)) + ')\n'
                   ' n=$((n+1))\n printf "%s\\n" "$n" > ' + shlex.quote(str(counter)) + '\n'
                   ' for stage in ./.cog-update.*; do if [ -f "$stage" ]; then printf partial-broken-content; exit 19; fi; done\n esac\nfi\nexec '
                   + shlex.quote(str(self.fixture_git)) + ' "$@"\n')
        self.write(fake_bin, 'git', wrapper, executable=True)
        env = dict(self.env, PATH=str(fake_bin) + os.pathsep + self.env['PATH'])
        result = self.update(vault, '--force', env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')

    def test_update_rejects_symlinked_framework_without_touching_target(self):
        vault = self.updater_fixture()
        outside = self.write(self.base, 'outside-note.md', 'Outside fixture must survive.\n')
        (vault / 'README.md').unlink()
        (vault / 'README.md').symlink_to(outside)
        result = self.update(vault, '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(), 'Outside fixture must survive.\n')

    def test_update_backups_are_ignored(self):
        vault = self.updater_fixture()
        self.update(vault, '--force')
        backups = list(vault.glob('README.md.backup-*'))
        self.assertTrue(backups)
        result = self.command([self.real_git, '-C', str(vault), 'check-ignore', '--no-index', '--', backups[0].name])
        self.assertEqual(result.returncode, 0, 'Updater backups must not become publishable files.')

    def test_checkpoint_cdpath_does_not_change_ledger_root(self):
        vault, script = self.checkpoint_fixture()
        relative = script.relative_to(vault)
        result = self.command([BASH, str(relative), 'record', str(vault / 'run'), 'CP-1', 'PASS', 'literal'],
                              cwd=vault, env=dict(self.env, CDPATH='.'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((vault / '.claude/logs/checkpoint-ledger.tsv').is_file())
        self.assertFalse(any('\n' in p.name for p in vault.iterdir()))

    def test_checkpoint_busy_ledger_fails_without_partial_record(self):
        vault, script = self.checkpoint_fixture()
        lock = vault / '.claude/logs/checkpoint-ledger.lock'
        lock.mkdir(parents=True)
        result = self.command([BASH, str(script), 'record', str(vault / 'run'), 'CP-1', 'PASS', 'literal'])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('busy', result.stderr)
        self.assertFalse((vault / 'run/evidence/checkpoints.tsv').exists())
        self.assertFalse((vault / '.claude/logs/checkpoint-ledger.tsv').exists())

    def test_lane_typography_cannot_trigger_tiny_override(self):
        script = ROOT / '.claude/lib/lane-classify.sh'
        result = self.command([BASH, str(script), 'classify', 'implement typography across all screens and ship'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'full')

    def test_lane_matcher_failure_cannot_return_low_risk(self):
        fake = self.base / 'bad-grep'
        fake.mkdir()
        self.write(fake, 'grep', '#!/bin/sh\nexit 2\n', executable=True)
        result = self.command([BASH, str(ROOT / '.claude/lib/lane-classify.sh'), 'classify', 'security'],
                              env=dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH']))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('match', result.stderr)
        self.assertNotIn(result.stdout.strip(), ['normal', 'tiny'])

    def test_checkpoint_invalid_outcome_writes_no_record(self):
        vault, script = self.checkpoint_fixture()
        run = vault / 'run'
        result = self.command([BASH, str(script), 'record', str(run), 'CP-1', 'TYPO', 'synthetic'])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((run / 'evidence/checkpoints.tsv').exists())

    def test_checkpoint_preserves_note_as_one_literal_record(self):
        vault, script = self.checkpoint_fixture()
        run = vault / 'run'
        note = 'path C:\\new\\test\nFAKE\tPASS'
        result = self.command([BASH, str(script), 'record', str(run), 'CP-1', 'PASS', note])
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = (run / 'evidence/checkpoints.tsv').read_text().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(len(lines[0].split('\t')), 4)
        self.assertIn('\\nFAKE\\tPASS', lines[0])
        self.assertIn('C:\\\\new\\\\test', lines[0])

    def test_checkpoint_status_does_not_create_log_directory(self):
        vault, script = self.checkpoint_fixture()
        result = self.command([BASH, str(script), 'status', str(vault / 'run')])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((vault / '.claude/logs').exists())

    def test_census_excludes_its_previous_output(self):
        corpus = self.base / 'corpus'
        corpus.mkdir()
        self.write(corpus, 'author.md', '# Author\nA real sentence. Another sentence.\n')
        output = corpus / 'baseline.md'
        script = ROOT / '.claude/skills/voice-baseline/scripts/census.py'
        args = ['python3', str(script), str(corpus), '--out', str(output)]
        first = self.command(args)
        self.assertEqual(first.returncode, 0, first.stderr)
        before = output.read_text()
        second = self.command(args)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(output.read_text(), before)

    def test_markdown_fences_support_tildes_indent_and_long_markers(self):
        scanner = load_module('scan_fences', '.claude/skills/slop-gate/scripts/scan.py')
        census = load_module('census_fences', '.claude/skills/voice-baseline/scripts/census.py')
        samples = ['~~~text\nHonestly really really —\n~~~\nOrdinary prose.\n',
                   '   ```text\nHonestly really really —\n   ```\nOrdinary prose.\n',
                   '````text\n```\nHonestly really really —\n```\n````\nOrdinary prose.\n']
        for text in samples:
            with self.subTest(text=text):
                self.assertEqual(scanner.scan(text), [])
                self.assertNotIn('really', census.strip_fences(text))

    def test_scanner_edit_removing_exemption_scans_result(self):
        target = self.write(self.base, 'draft.md', 'slop-ok: exhibit\nHonestly this is a test.\n')
        payload = {'tool_name': 'Edit', 'tool_input': {'file_path': str(target),
                   'old_string': 'slop-ok: exhibit\n', 'new_string': ''}}
        result = self.command(['python3', str(ROOT / '.claude/skills/slop-gate/scripts/scan.py'), '--hook'], input=json.dumps(payload))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'], 'deny')

    def test_scanner_exempt_binary_does_not_abort_batch(self):
        binary = self.base / 'image.png'
        binary.write_bytes(b'\xff\x00')
        prose = self.write(self.base, 'draft.md', 'Honestly this is a test.\n')
        result = self.command(['python3', str(ROOT / '.claude/skills/slop-gate/scripts/scan.py'), str(binary), str(prose)])
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('image.png: exempt', result.stdout)
        self.assertIn('tell(s)', result.stdout)

    def test_scanner_normalizes_parent_components_before_exemption(self):
        module = load_module('scan_paths', '.claude/skills/slop-gate/scripts/scan.py')
        self.assertFalse(module.exempt('build/../draft.md', 'Honestly this is a test.'))
        self.assertTrue(module.exempt('build/draft.md', 'Honestly this is a test.'))

    def test_scanner_unreadable_file_does_not_abort_remaining_checks(self):
        prose = self.write(self.base, 'draft.md', 'Honestly this is a test.\n')
        result = self.command(['python3', str(ROOT / '.claude/skills/slop-gate/scripts/scan.py'), str(self.base / 'missing.md'), str(prose)])
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn('cannot read', result.stderr)
        self.assertIn('tell(s)', result.stdout)

    def test_heading_blank_lines_have_bounded_runtime_in_both_scanners(self):
        code = ('import importlib.util; '
                's=importlib.util.spec_from_file_location("fixture", __import__("sys").argv[1]); '
                'm=importlib.util.module_from_spec(s); s.loader.exec_module(m); '
                'text="\\n"*32000+"# The System"; '
                'm.scan(text) if hasattr(m,"scan") else m.HEADING.findall(text); '
                'm.scan("# The Point"+" "*32000+"x") if hasattr(m,"scan") else m.HEADING.findall("# A"+" "*32000+"x\\n")')
        for relative in ['.claude/skills/slop-gate/scripts/scan.py', '.claude/skills/voice-baseline/scripts/census.py']:
            result = subprocess.run(['python3', '-B', '-c', code, str(ROOT / relative)],
                                    env=self.env, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_census_verdict_sentence_boundaries_include_questions(self):
        module = load_module('census_boundaries', '.claude/skills/voice-baseline/scripts/census.py')
        text = 'Why? The system works.\n\nWhy! The widget breaks.\n'
        self.assertEqual(len(module.VERDICT.findall(text)), 2)
        self.assertEqual(len(module.VERDICT.findall('Why?\tThe system works.\n')), 1)

    def test_scanner_ignores_fenced_exhibits(self):
        scanner = load_module('cog_scanner', '.claude/skills/slop-gate/scripts/scan.py')
        self.assertEqual(scanner.scan('An exhibit:\n```text\n—\n```\n'), [])

    def test_scanner_hook_handles_non_object_json(self):
        script = ROOT / '.claude/skills/slop-gate/scripts/scan.py'
        for payload in ['[]', '{"tool_name":"Write","tool_input":[1]}']:
            with self.subTest(payload=payload):
                result = self.command(['python3', str(script), '--hook'], input=payload)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), {})

    def test_builder_keeps_previous_mirror_if_copy_fails(self):
        vault = self.base / 'builder-vault'
        vault.mkdir()
        self.write(vault, '.claude/skills/one/SKILL.md', 'new canonical\n')
        old = self.write(vault, 'skills/one/SKILL.md', 'old valid mirror\n')
        script = self.write(vault, 'scripts/build-agent-plugin.sh', (ROOT / 'scripts/build-agent-plugin.sh').read_text(), executable=True)
        fake = self.base / 'failing-cp'
        fake.mkdir()
        self.write(fake, 'cp', '#!/bin/sh\nexit 29\n', executable=True)
        env = dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH'])
        result = self.command([BASH, str(script)], env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(old.exists())
        self.assertEqual(old.read_text(), 'old valid mirror\n')

    def test_lane_hard_gate_survives_large_multiline_summary(self):
        script = ROOT / '.claude/lib/lane-classify.sh'
        summary = 'security\n' + 'x' * 100000
        for _ in range(5):
            result = self.command([BASH, str(script), 'classify', summary])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'full')

    def test_lane_treats_backslashes_literally_and_explains_hard_gates(self):
        script = ROOT / '.claude/lib/lane-classify.sh'
        result = self.command([BASH, '-O', 'xpg_echo', str(script), 'classify', r'routine\c security'])
        self.assertEqual(result.stdout.strip(), 'full')
        for text, lane in [('security', 'full'), ('broken', 'bug'), ('audit only', 'backfill'), ('typo', 'tiny')]:
            result = self.command([BASH, str(script), 'explain', text])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('lane=' + lane, result.stdout)
            self.assertIn('reasons=', result.stdout)

    def test_census_checks_unseen_watchwords_and_phrase_boundaries(self):
        module = load_module('cog_census', '.claude/skills/voice-baseline/scripts/census.py')
        author = self.write(self.base, 'author.md', 'An ordinary sentence.\n')
        draft = self.write(self.base, 'draft.md', 'Really really really really.\n')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.check(module.census([author]), draft), 1)
        self.assertEqual(module.count_phrase("The reality. Where's the rest?", 'the real'), 0)
        self.assertEqual(module.count_phrase("Where's the rest?", "here's"), 0)
        self.assertEqual(module.count_phrase("The real issue: here's a fact.", 'the real'), 1)

    def test_census_contractions_and_paragraph_endings(self):
        module = load_module('cog_census_shapes', '.claude/skills/voice-baseline/scripts/census.py')
        author = self.write(self.base, 'author.md', 'An ordinary sentence.\n')
        baseline = module.census([author])
        cases = [("That's the point.\n", 1), ("That’s the point.\n", 1),
                 ('The system works.\nThe widget breaks.\nAn ordinary continuation.\n', 0),
                 ('The system works.\n\nThe widget breaks.\n', 1)]
        for text, expected in cases:
            draft = self.write(self.base, 'draft.md', text)
            with self.subTest(text=text), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(module.check(baseline, draft), expected)

    def test_census_rejects_incomplete_traversal(self):
        module = load_module('cog_census_walk', '.claude/skills/voice-baseline/scripts/census.py')
        corpus = self.base / 'corpus'
        corpus.mkdir()
        self.write(corpus, 'author.md', 'An ordinary sentence.\n')

        def interrupted_walk(*args, **kwargs):
            yield str(corpus), [], ['author.md']
            callback = kwargs.get('onerror')
            if callback:
                callback(PermissionError('synthetic traversal denied'))

        error = io.StringIO()
        with patch.object(module.os, 'walk', interrupted_walk), patch.object(module.sys, 'argv', ['census.py', str(corpus)]), contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(), 2)
        self.assertIn('synthetic traversal denied', error.getvalue())

    def test_scanner_edit_checks_the_complete_candidate(self):
        draft = self.write(self.base, 'draft.md', 'simple clean.\n')
        payload = {'tool_name': 'Edit', 'tool_input': {'file_path': str(draft), 'old_string': 'clean', 'new_string': 'clean elegant'}}
        result = self.command(['python3', str(ROOT / '.claude/skills/slop-gate/scripts/scan.py'), '--hook'], input=json.dumps(payload))
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(decision['permissionDecision'], 'deny')
        self.assertEqual(draft.read_text(), 'simple clean.\n')

    def test_scanner_exemptions_match_path_components(self):
        scanner = load_module('cog_scanner_paths', '.claude/skills/slop-gate/scripts/scan.py')
        self.assertFalse(scanner.exempt('node_modules-migration.md', 'Great question.'))
        for path in ['node_modules/post.md', 'build/guide.md', './build/guide.md']:
            self.assertTrue(scanner.exempt(path, 'Great question.'))

    def test_scanner_whitespace_prefix_has_bounded_runtime(self):
        script = ROOT / '.claude/skills/slop-gate/scripts/scan.py'
        result = subprocess.run(['python3', str(script), '-'], input='\n' * 16000 + 'Neutral sentence.',
                                text=True, capture_output=True, env=self.env, timeout=5, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('stdin: clear', result.stdout)

    def test_updater_rejects_foreign_remote_without_framework_writes(self):
        vault = self.updater_fixture()
        self.git(vault, 'remote', 'set-url', 'cog-upstream', 'https://example.invalid/foreign.git')
        result = self.update(vault, '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((vault / 'README.md').read_text(), 'old readme\n')

    def test_updater_uses_script_checkout_from_personal_subdirectory(self):
        vault = self.updater_fixture()
        result = self.command([BASH, str(vault / 'cog-update.sh'), '--force'], cwd=vault / '00-inbox')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'new readme\n')
        self.assertFalse((vault / '00-inbox/README.md').exists())

    def test_updater_repairs_mode_only_missing_executable_bit(self):
        vault = self.updater_fixture()
        for name in ['README.md', 'AGENTS.md', 'COG-VERSION', '.claude-plugin/plugin.json']:
            (vault / name).write_bytes((self.base / 'upstream' / name).read_bytes())
        target = vault / 'scripts/validate-agent-surface.sh'
        before = target.read_bytes()
        target.chmod(0o644)
        self.git(vault, 'config', 'core.filemode', 'false')
        result = self.update(vault, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(target.stat().st_mode & 0o111)
        self.assertEqual(target.read_bytes(), before)
        self.assertIn('VALIDATOR_SEEN', result.stdout)

    def test_updater_repairs_mode_only_unexpected_executable_bit(self):
        vault = self.updater_fixture()
        for name in ['README.md', 'AGENTS.md', 'COG-VERSION', '.claude-plugin/plugin.json']:
            (vault / name).write_bytes((self.base / 'upstream' / name).read_bytes())
        target = vault / 'README.md'
        before = target.read_bytes()
        target.chmod(0o755)
        result = self.update(vault, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(target.stat().st_mode & 0o111)
        self.assertEqual(target.read_bytes(), before)

    def test_updater_preserves_upstream_executable_bit(self):
        vault = self.updater_fixture()
        upstream = self.base / 'upstream'
        self.write(upstream, 'scripts/build-agent-plugin.sh', '#!/bin/sh\nexit 0\n', executable=True)
        self.git(upstream, 'add', '.')
        self.git(upstream, 'update-index', '--chmod=+x', 'scripts/build-agent-plugin.sh')
        self.git(upstream, 'commit', '-m', 'Add executable fixture')
        result = self.update(vault, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((vault / 'scripts/build-agent-plugin.sh').stat().st_mode & 0o111)

    def test_updater_handles_only_new_files_on_system_bash(self):
        vault = self.updater_fixture()
        for name in ['README.md', 'AGENTS.md', 'COG-VERSION', '.claude-plugin/plugin.json']:
            (vault / name).write_bytes((self.base / 'upstream' / name).read_bytes())
        (vault / 'README.md').unlink()
        result = self.update(vault, '--force')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((vault / 'README.md').read_text(), 'new readme\n')

    def test_validate_mode_fails_when_validator_is_absent(self):
        vault = self.updater_fixture()
        (vault / 'scripts/validate-agent-surface.sh').unlink()
        result = self.update(vault, '--validate')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('no validation was performed', result.stderr)

    @unittest.skipUnless(os.name == 'posix', 'Fixture pipe deadlines use POSIX select')
    def test_partial_fixture_marker_expires_without_waiting_for_newline(self):
        reader, writer = os.pipe()
        try:
            with os.fdopen(reader, 'rb') as stream:
                os.write(writer, b'COPY_')
                with self.assertRaises(TimeoutError):
                    read_fixture_marker(stream, 'COPY_READY', timeout=0.05)
        finally:
            os.close(writer)

    @unittest.skipUnless(os.name == 'posix', 'Fixture termination uses POSIX process groups')
    def test_fixture_timeout_kills_and_reaps_owned_group(self):
        from unittest.mock import Mock
        process = Mock(pid=12345)
        process.communicate.side_effect = [subprocess.TimeoutExpired('synthetic', 10), ('', '')]
        with patch.object(os, 'killpg') as kill_group:
            with self.assertRaises(TimeoutError):
                finish_fixture(process)
        kill_group.assert_called_once_with(12345, signal.SIGKILL)
        self.assertEqual(process.communicate.call_count, 2)
        for pipe in (process.stdin, process.stdout, process.stderr):
            pipe.close.assert_called_once()

    def test_builder_excludes_generated_metadata_without_touching_canonical_files(self):
        vault = self.base / 'builder-vault'
        vault.mkdir()
        self.write(vault, '.claude/skills/one/SKILL.md', 'canonical\n')
        metadata = ['.DS_Store', 'one/.DS_Store', 'one/scripts/__pycache__/fixture.pyc', 'one/scripts/standalone.pyc', 'one/scripts/old.pyo']
        for relative in metadata:
            self.write(vault, '.claude/skills/' + relative, 'synthetic generated artifact\n')
        script = self.write(vault, 'scripts/build-agent-plugin.sh', (ROOT / 'scripts/build-agent-plugin.sh').read_text(), executable=True)
        result = self.command([BASH, str(script)])
        self.assertEqual(result.returncode, 0, result.stderr)
        for relative in metadata:
            with self.subTest(path=relative):
                self.assertFalse((vault / 'skills' / relative).exists())
                self.assertEqual((vault / '.claude/skills' / relative).read_text(), 'synthetic generated artifact\n')
        self.assertFalse((vault / 'skills/one/scripts/__pycache__').exists())
        self.assertEqual((vault / 'skills/one/SKILL.md').read_text(), 'canonical\n')

    def test_builder_releases_lock_when_old_stage_cleanup_fails(self):
        vault = self.base / 'builder-vault'
        vault.mkdir()
        canonical = self.write(vault, '.claude/skills/one/SKILL.md', 'canonical\n')
        self.write(vault, 'skills/one/SKILL.md', 'old\n')
        script = self.write(vault, 'scripts/build-agent-plugin.sh', (ROOT / 'scripts/build-agent-plugin.sh').read_text(), executable=True)
        fake = self.base / 'bad-rm'
        fake.mkdir()
        self.write(fake, 'rm', '#!/bin/sh\nif [ "$1" = -rf ]; then exit 41; fi\nexec ' + shlex.quote(shutil.which('rm')) + ' "$@"\n', executable=True)
        result = self.command([BASH, str(script)], env=dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH']))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((vault / '.claude/.build-agent-plugin.lock').exists())
        self.assertEqual((vault / 'skills/one/SKILL.md').read_bytes(), canonical.read_bytes())
        self.assertIn('cleanup failed', result.stderr)
        retry = self.command([BASH, str(script)])
        self.assertEqual(retry.returncode, 0, retry.stderr)

    @unittest.skipUnless(os.name == 'posix', 'Pipe-select concurrency fixture uses POSIX process pipes')
    def test_builder_serializes_competing_writers(self):
        vault = self.base / 'builder-vault'
        vault.mkdir()
        canonical = self.write(vault, '.claude/skills/one/SKILL.md', 'canonical\n')
        self.write(vault, 'skills/one/SKILL.md', 'old\n')
        script = self.write(vault, 'scripts/build-agent-plugin.sh', (ROOT / 'scripts/build-agent-plugin.sh').read_text(), executable=True)
        fake = self.base / 'blocking-cp'
        fake.mkdir()
        self.write(fake, 'cp', '#!/bin/sh\nprintf "COPY_READY\\n"\nIFS= read -r release\nexec ' + shlex.quote(shutil.which('cp')) + ' "$@"\n', executable=True)
        env = dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH'])
        first = subprocess.Popen([BASH, str(script)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, env=env, start_new_session=True)
        try:
            read_fixture_marker(first.stdout, 'COPY_READY')
            second = self.command([BASH, str(script)], input='release\n', env=env)
            self.assertNotEqual(second.returncode, 0)
        finally:
            output, error = finish_fixture(first)
            self.assertEqual(first.returncode, 0, output + error)
        self.assertEqual((vault / 'skills/one/SKILL.md').read_bytes(), canonical.read_bytes())
        self.assertFalse((vault / 'skills/skills').exists())

    def validator_fixture(self):
        vault = self.base / 'validator-vault'
        vault.mkdir()
        entries = []
        for name in ['alpha', 'beta']:
            body = f'---\nname: {name}\ndescription: Synthetic skill\n---\n'
            self.write(vault, f'.claude/skills/{name}/SKILL.md', body)
            self.write(vault, f'skills/{name}/SKILL.md', body)
            self.write(vault, f'.agents/skills/{name}/SKILL.md', body + f'.claude/skills/{name}/SKILL.md\n')
            entries.append({'name': name, 'path': f'.claude/skills/{name}/SKILL.md'})
        self.write(vault, '.claude-plugin/plugin.json', json.dumps({'version': '3.13.0', 'skills': entries}))
        self.write(vault, 'plugin.json', json.dumps({'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'name': 'cog-second-brain', 'version': '3.13.0'}))
        self.write(vault, 'marketplace-entry.json', '{"version":"3.13.0"}')
        self.write(vault, '.claude/agents/worker.md', 'Synthetic agent.\n')
        cursor = {'version': '3.13.0', 'skills': entries, 'agents': ['worker']}
        self.write(vault, '.cursor-plugin/plugin.json', json.dumps(cursor))
        self.write(vault, 'COG-VERSION', '3.13.0\n')
        self.write(vault, 'AGENTS.md', '### /alpha\n### /beta\n')
        for name in ['README.md', 'SETUP.md', 'CONTRIBUTING.md', '.github/MARKETPLACE.md', 'docs/AGENT-SUPPORT.md']:
            self.write(vault, name, 'AGENTS.md\n')
        for number in range(7):
            self.write(vault, f'.kiro/powers/{number}/POWER.md', 'fixture\n')
            self.write(vault, f'.gemini/commands/{number}.toml', 'fixture=1\n')
            self.write(vault, f'.gemini/skills/{number}.md', 'fixture\n')
        script = self.write(vault, 'scripts/validate-agent-surface.sh', (ROOT / 'scripts/validate-agent-surface.sh').read_text(), executable=True)
        return vault, script

    def test_validator_ignores_only_known_generated_mirror_artifacts(self):
        vault, script = self.validator_fixture()
        self.write(vault, 'skills/.DS_Store', 'synthetic Finder metadata\n')
        self.write(vault, '.claude/skills/alpha/scripts/__pycache__/fixture.pyc', 'synthetic cache\n')
        self.write(vault, 'skills/alpha/scripts/old.pyo', 'synthetic cache\n')
        self.write(vault, 'skills/alpha/scripts/standalone.pyc', 'synthetic cache\n')
        result = self.command([BASH, str(script)])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_still_rejects_unexpected_source_mirror_files(self):
        vault, script = self.validator_fixture()
        self.write(vault, 'skills/alpha/unexpected.md', 'This is an unexpected source file.\n')
        result = self.command([BASH, str(script)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mirror is missing or drifted', result.stdout + result.stderr)

    def test_validator_rejects_unquoted_colon_in_skill_description(self):
        vault, script = self.validator_fixture()
        target = vault / '.agents/skills/alpha/SKILL.md'
        target.write_text(target.read_text().replace('description: Synthetic skill', 'description: Synthetic: skill'))
        result = self.command([BASH, str(script)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unquoted colon in skill description', result.stdout + result.stderr)

    def test_validator_mandatory_checks_survive_python_optimization(self):
        vault, script = self.validator_fixture()
        plugin = json.loads((vault / 'plugin.json').read_text())
        plugin['name'] = 'wrong-plugin'
        (vault / 'plugin.json').write_text(json.dumps(plugin))
        result = self.command([BASH, str(script)], env=dict(self.env, PYTHONOPTIMIZE='1'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing $schema/name', result.stdout + result.stderr)

    def test_validator_command_heading_is_not_a_prefix_match(self):
        vault, script = self.validator_fixture()
        (vault / 'AGENTS.md').write_text('### /alpha-beta\n### /beta\n')
        result = self.command([BASH, str(script)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing /alpha', result.stdout + result.stderr)

    def test_validator_rejects_stale_cursor_package(self):
        vault, script = self.validator_fixture()
        cursor = json.loads((vault / '.cursor-plugin/plugin.json').read_text())
        cursor['version'] = '3.12.0'
        (vault / '.cursor-plugin/plugin.json').write_text(json.dumps(cursor))
        result = self.command([BASH, str(script)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Cursor packaging differs', result.stdout + result.stderr)

    def test_validator_rejects_duplicate_manifest_coverage(self):
        vault, script = self.validator_fixture()
        manifest = json.loads((vault / '.claude-plugin/plugin.json').read_text())
        manifest['skills'][1] = dict(manifest['skills'][0])
        (vault / '.claude-plugin/plugin.json').write_text(json.dumps(manifest))
        result = self.command([BASH, str(script)])
        self.assertNotEqual(result.returncode, 0)

    def test_validator_search_errors_cannot_report_success(self):
        vault, script = self.validator_fixture()
        fake = self.base / 'bad-search'
        fake.mkdir()
        for name in ['grep', 'rg']:
            self.write(fake, name, '#!/bin/sh\nexit 2\n', executable=True)
        result = self.command([BASH, str(script)], env=dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH']))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Could not inspect', result.stdout + result.stderr)

    def test_validator_cleans_temporary_manifest_on_parse_error(self):
        vault, script = self.validator_fixture()
        (vault / '.claude-plugin/plugin.json').write_text('{')
        fake = self.base / 'known-temp'
        fake.mkdir()
        manifest_temp = self.base / 'temporary-manifest'
        self.write(fake, 'mktemp', '#!/bin/sh\n: > ' + shlex.quote(str(manifest_temp)) + '\nprintf "%s\\n" ' + shlex.quote(str(manifest_temp)) + '\n', executable=True)
        result = self.command([BASH, str(script)], env=dict(self.env, PATH=str(fake) + os.pathsep + self.env['PATH']))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(manifest_temp.exists())

    def test_validator_missing_optional_surface_warns_without_aborting(self):
        vault, script = self.validator_fixture()
        shutil.rmtree(vault / '.kiro/powers')
        result = self.command([BASH, str(script)])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('found 0', result.stdout)


    def test_indexes_ignore_untracked_private_files_and_sort_paths(self):
        module = load_module('doc_indexes', 'scripts/doc_indexes.py')
        repo = self.base / 'index-repo'
        self.initialize(repo)
        self.write(repo, 'tracked.md', 'Public reference.\n')
        self.write(repo, 'private-note.md', 'Synthetic private note.\n')
        self.git(repo, 'add', 'tracked.md')
        paths = module.inventory(repo)
        self.assertIn('tracked.md', paths)
        self.assertNotIn('private-note.md', paths)
        self.assertEqual(paths, sorted(paths))
        outputs = module.render(paths)
        self.assertNotIn('Synthetic private note', ''.join(outputs.values()))
        self.assertEqual({r['path'] for r in json.loads(outputs[module.OUTPUTS[0]])['files']}, set(paths))

    def test_indexes_reject_missing_or_symlinked_tracked_paths(self):
        module = load_module('doc_indexes', 'scripts/doc_indexes.py')
        repo = self.base / 'index-repo'
        self.initialize(repo)
        target = self.write(repo, 'tracked.md', 'Public reference.\n')
        self.git(repo, 'add', 'tracked.md')
        target.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing tracked file'):
            module.inventory(repo)
        target.symlink_to(self.write(self.base, 'outside.md', 'Synthetic outside.\n'))
        with self.assertRaisesRegex(ValueError, 'Linked tracked path'):
            module.inventory(repo)

    def test_index_render_escapes_markdown_links(self):
        module = load_module('doc_indexes', 'scripts/doc_indexes.py')
        overview = module.render(['notes/a [b](c).md'])['docs/codebase-overview.md']
        self.assertIn('a \\[b\\](c).md', overview)
        self.assertIn('../notes/a%20%5Bb%5D%28c%29.md', overview)


if __name__ == '__main__':
    unittest.main()
