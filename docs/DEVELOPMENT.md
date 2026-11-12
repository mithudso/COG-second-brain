# Development

Read [architecture](ARCHITECTURE.md), [components](COMPONENTS.md), and [known issues](known-issues.md) before changing helpers. Work in a disposable checkout or isolated worktree when another task has active edits.

## Prerequisites and setup

Use Git, Bash, Python 3, and standard Unix tools (`cp`, `diff`, `find`, `grep`, `mktemp`, `mv`). CI exercises Python 3.11 and 3.13 on Ubuntu and macOS. The shell code accommodates macOS system Bash 3.2. The minimum Git version is not pinned; tests need `git init -b`. No third-party Python packages or Node runtime are required.

```bash
git clone https://github.com/mithudso/COG-second-brain.git
cd COG-second-brain
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

This is the personal fork. Original author Huy Tieu, MIT licensing, and the official upstream URL remain unchanged. There is no development server, install/build dependency step, or live reload process.

## Commands

```bash
for script in cog-update.sh .claude/lib/checkpoint.sh .claude/lib/lane-classify.sh scripts/build-agent-plugin.sh scripts/validate-agent-surface.sh; do bash -n "$script" || exit; done
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_maintenance.py -v
python3 scripts/doc_indexes.py --check
```

`bash -n` checks shell syntax. Unit tests exercise behavioral assertions; Python has no separate configured linter or type-check gate. See [testing](TESTING.md) for exclusions. The validation runbook includes CI's final diff check.

After canonical skill edits, run `./scripts/build-agent-plugin.sh`. After staging only intended public additions/removals, the delivery owner runs `python3 scripts/doc_indexes.py` and checks the resulting maps. These are write operations; do not regenerate into another active task's work.

## Change workflow

1. Use a focused branch. Preserve unrelated changes and private content.
2. Edit canonical files and add assertions for important changed behavior using synthetic fixtures.
3. Update affected surfaces and docs. Coordinate all four version files with the release owner; do not bump each file edit independently.
4. Run local checks. Review the diff and the staged path set before generating indexes.
5. Submit a descriptive PR with validation, risks, and rollback. CI checks PRs and pushes to `main`; it does not deploy anything.

Append sanitized request summaries to [prompts](../prompts.md) and progress entries to [memory](../memory.md). Keep both logs append-only. See [archive policy](archive/README.md).

## Environment and troubleshooting

No service environment variables are required. `PYTHONDONTWRITEBYTECODE=1` suppresses Python cache writes during tests. Standard `PATH`, Git configuration, and Git authentication affect manual updates. Script roots and upstream constants are internal variables. They have no supported environment override. Tests isolate Git configuration and redirect fixture fetches to local repositories.

A mirror mismatch requires regeneration from canonical skills. A stale map requires reviewing staged paths and regenerating maps. A build lock requires checking its owner before removal. See [validation](runbooks/validation.md). Do not use the live updater to diagnose a test failure.
