# Testing

## Strategy and suites

Maintenance validation emphasizes behavior on important changed paths. `tests/test_maintenance.py` uses Python stdlib `unittest`, synthetic text, temporary checkouts, and local Git repositories. Its helper regression cases cover:

- Updater multi-file progress, interactive skips, failure propagation, atomic replacement, path/symlink refusal, official remote identity, checkout location, executable modes, and ignored backups.
- Literal checkpoint TSV escaping, invalid outcomes, read-only status, CDPATH and busy-writer behavior.
- Lane hard-risk detection, multiline input, literal backslashes, substring collisions and matcher failures.
- Scanner fenced exhibits, malformed hook JSON, reconstructed Edit candidates, path-component exemptions, and a bounded-runtime case.
- Census word/phrase boundaries, unseen watchwords, self-output exclusion, and traversal failures.
- Mirror copy failure recovery and competing writers.
- Validator duplicate manifest coverage, search errors, temporary cleanup, exact headings, optimized Python, Cursor parity, malformed description scalars and optional-surface warnings.

Additional indexer cases check sorted tracked-only paths, untracked-body exclusion, missing/symlinked paths, and Markdown link escaping. Updater tests rewrite fixture fetch transport to local Git. They do not fetch the real upstream or modify the user's vault.

## Commands

Run from the repository root:

```bash
for script in cog-update.sh .claude/lib/checkpoint.sh .claude/lib/lane-classify.sh scripts/build-agent-plugin.sh scripts/validate-agent-surface.sh; do bash -n "$script" || exit; done
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_maintenance.py -v
python3 scripts/doc_indexes.py --check
```

The fourth command selects the single maintenance test file. A focused test may also be run from `tests/` with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_maintenance.IsolatedTests.test_checkpoint_preserves_note_as_one_literal_record -v`.

## CI gates and coverage

[CI](../.github/workflows/ci.yml) runs Ubuntu and macOS with Python 3.11 and 3.13, for four jobs. Each job runs shell syntax checks, packaging validation, all unit tests, path-map freshness, and `git diff --exit-code`. Every invoked check must exit zero. Tests isolate their fixtures; they must not change tracked framework files.

There is no enforced numeric line-coverage threshold or coverage tool. The target is meaningful assertions for important and changed/risky paths. The gate is all collected tests passing, plus the static checks above. There is no percentage claim or blanket 100% line mandate.

## Writing tests and limits

Use `test_<behavior>` methods, temporary directories with cleanup, synthetic input, and explicit assertions on exit codes, output, file bytes, and preservation. Stub failure boundaries deliberately. Do not use production credentials, raw customer content, real upstream fetches, or live publishing.

These checks do not certify agent interpretation, Obsidian UI, live onboarding, provider authentication, actual publishing, model output quality, or end-to-end application behavior. The scanner runtime case is a regression bound, not a performance SLA. The validation runbook explains failure triage.

The current maintenance suite collects 63 tests. Controlled child-process barriers have overall deadlines, and timeout cleanup kills/reaps only the fixture-owned process group. CI also compares the worktree/index against HEAD so staged mutations fail validation.

Source-parity regressions distinguish maintained files from ignored Finder/Python artifacts. Builder tests preserve canonical artifact bytes while checking that only the staged copy excludes them. Unexpected source-file differences still fail validation.

Git fixtures strip inherited `GIT_*`, disable system/global Git configuration and use an explicitly owned empty template. The hostile-hook regression inspects the actual hook inventory before making a synthetic commit. Local final verification additionally uses an external task-scoped process-tree egress guard; no network exception is needed. That workstation guard is not a shipped runtime dependency and does not retroactively verify earlier runs.

A controlled maintenance mutation check independently removed each of the four artifact exclusions from disposable helper copies; the preservation/parity tests detected every removal with assertion failures.
