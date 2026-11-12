# Offline validation

## Preconditions

Use the intended checkout with Git, Bash, and Python available. Review tracked changes without listing or opening private untracked vault content. Preserve concurrent edits. No credentials, integrations, onboarding, inference, or live updater execution are needed.

## Procedure

Run from the repository root:

```bash
for script in cog-update.sh .claude/lib/checkpoint.sh .claude/lib/lane-classify.sh scripts/build-agent-plugin.sh scripts/validate-agent-surface.sh; do bash -n "$script" || exit; done
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/doc_indexes.py --check
```

On a fresh CI checkout, also run `git diff --exit-code`. In a shared checkout, an existing task diff makes that command nonzero; compare before/after task-owned changes instead of discarding them to make the command pass. CI's check covers tracked changes, not an exhaustive secret or untracked-file scan.

## Verification

Each command must exit zero. Validator warnings require inspection: Kiro/Gemini subset count differences can warn without failing. The unit suite must report success, and index checking must report fresh maps. These observations establish helper/package checks, not live client or provider behavior.

If canonical skills changed, the responsible editor rebuilds `skills/` with `./scripts/build-agent-plugin.sh`, then repeats the validator. If paths changed, the delivery owner reviews/stages intended public paths, runs `python3 scripts/doc_indexes.py`, and repeats `--check`. Do not edit generated maps by hand.

## Escalation

For a failure, retain a sanitized command, exit code, and relevant output. Isolate the failing fixture or path. A lock requires owner review; do not remove an active writer's lock. A sensitive tracked path requires review before publication. Parent-owned source or index failures go to the responsible owner; do not run a live update, activate integrations, or replace unrelated work to repair validation.
