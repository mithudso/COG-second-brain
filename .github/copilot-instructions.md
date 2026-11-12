## Default Execution Strategy

- Read relevant local files and preserve concurrent work before editing.
- Run checks appropriate to each changed behavior and run the complete offline validation before delivery.
- Use actual repository commands and paths. Record unknowns and exceptions explicitly.
- Append sanitized request summaries to `prompts.md` and progress to `memory.md`; coordinate version changes with the release owner across all four version files.
- Keep work within the user's scope. Delegate only when authorized and useful. Do not invoke integrations, semantic indexing, or live updates as part of documentation validation.

## Orientation

Read `AGENTS.md` for commands, `CLAUDE.md` for shared conventions, `docs/wiki/index.md` for maintenance navigation, and `docs/ARCHITECTURE.md` / `docs/COMPONENTS.md` for actual boundaries. `WORKFLOW.md` governs opt-in verification harness runs.

## Build, Test, and Validation Commands

```bash
for script in cog-update.sh .claude/lib/checkpoint.sh .claude/lib/lane-classify.sh scripts/build-agent-plugin.sh scripts/validate-agent-surface.sh; do bash -n "$script" || exit; done
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/doc_indexes.py --check
```

There is no dependency install, server, Node build, configured type checker, or live app test. See `docs/DEVELOPMENT.md` for a single-file test command and controlled mirror/index regeneration. CI additionally runs `git diff --exit-code` on a fresh checkout.

## High-level Architecture

- Agent hosts interpret Markdown playbooks and work with user-owned vault files.
- `.claude/skills/` is canonical; `skills/` is generated; `.agents/` contains pointer stubs.
- Kiro and Gemini ship seven native core workflows each. The canonical set has 35 skills and 10 agents.
- Bash/Python helpers maintain local files and packaging. The updater alone fetches official upstream Git metadata.
- Optional services and MCP tools belong to the user's host; no server or datastore is bundled.

## Key Conventions

1. Edit canonical skills before derived copies and rebuild the mirror when needed.
2. Preserve Huy Tieu's MIT attribution and official upstream URLs. The personal fork is `mithudso/COG-second-brain`.
3. Stage only task-owned public files. Never inventory or publish private vault bodies or filenames.
4. Use synthetic test fixtures and local Git transport. Do not run the real updater for regression testing.
5. Treat `--check` and `--dry-run` updater modes as network operations with Git metadata effects.
6. Keep host integrations and credentials user-owned. No shared `.env`, MCP config, or automatic hooks are required.
7. Observe external results before claiming success. Static packaging validation does not certify live clients.
8. Keep generated maps path-only, offline, and derived from reviewed tracked/staged paths.
9. Record gaps without inventing runtime services, policies, compliance claims, or response SLAs.
