# Components

## Framework surfaces

| Path | Responsibility | Inputs and effects |
|---|---|---|
| `.claude/skills/` | 35 canonical playbooks and bundled references | Agent reads instructions; invoked skills may write vault content or call authorized integrations |
| `.claude/agents/` | 10 specialized roles, listed below | Host supplies tools and permissions; these are instructions, not a running agent service |
| `.claude/roles/` | Six role packs and a template | Profile role guides skill recommendations |
| `.agents/skills/`, `.agents/agents/` | Pointer stubs for Antigravity | Delegate to canonical `.claude/` files |
| `skills/`, `plugin.json` | Generated skill mirror and Agent Plugins manifest | Mirror build copies canonical skills; manifest declares spec 1.0.0 |
| `.claude-plugin/`, `.cursor-plugin/`, `.cursorrules`, `marketplace-entry.json` | Host packaging metadata | Host-specific discovery; version fields require coordinated changes |
| `.kiro/powers/` | Seven native core powers | Partial surface |
| `.gemini/commands/`, `.gemini/skills/`, `GEMINI.md` | Seven native commands and skill files | Partial surface; advanced playbooks remain in `.claude/skills/` |
| `AGENTS.md`, `CLAUDE.md` | Universal catalog and host conventions | Read-only orientation until an agent invokes work |
| `00-inbox/` through `06-templates/` | Vault layout and templates | User-owned content; no maintenance inventory of private files |
| `docs/`, `docs/wiki/` | Maintainer reference and offline navigation | No wiki publishing or hosting step |

## Maintained helpers

| Canonical path | Public command/API | Dependencies and effects |
|---|---|---|
| `.claude/lib/checkpoint.sh` | `init`, `record`, `status` with a run directory | Bash, date, filesystem; init creates evidence scaffolding; record appends escaped literal TSV under a single-writer lock (busy means retry); status reads records |
| `.claude/lib/lane-classify.sh` | `classify` or `explain` with a summary | Bash and text tools; writes lane/reasons to stdout; classification is heuristic; matcher errors fail and tiny keywords use word boundaries |
| `.claude/skills/slop-gate/scripts/scan.py` | Files, `-` for stdin, or `--hook`; `scan(text)` | Python stdlib; reports tells or host hook decisions; Edit checks reconstructable file candidates; no hook is installed automatically |
| `.claude/skills/voice-baseline/scripts/census.py` | Corpus directory, `--ext`, `--out`, `--check` | Python stdlib; counts words/shapes; optional output write; excludes its output and checked draft; traversal failures are errors |
| `cog-update.sh` | Interactive, `--check`, `--dry-run`, `--force`, `--validate`, `--help` | Git and Unix tools; upstream fetch, allowlisted replacements, optional backups, mirror rebuild and validator |
| `scripts/build-agent-plugin.sh` | No arguments | Bash and copy/move tools; single-writer lock, staged copy excluding generated Finder/Python artifacts, replacement of `skills/`, recovery on failed replacement |
| `scripts/validate-agent-surface.sh` | No arguments | Bash, Python, Git-independent file checks; validates manifests, exact skill set, maintained-source mirror equality (known generated artifacts excluded), command headings, version parity, and subset counts |

The seven helpers above are the maintenance regression scope. `scripts/doc_indexes.py` is separate offline documentation tooling: `inventory(root)` obtains Git tracked/staged paths, `render(paths)` formats them, and `--check` compares three maps without writing. `tests/test_maintenance.py` uses `unittest` and temporary repositories.

## Agent inventory

All canonical roles declare `model: sonnet`. Their scope is the authorized task and vault, with no account selection or authentication built in. External access comes from the host and user-owned integration configuration. `.agents/` pointer metadata may map a role to another host model.

| Canonical role | When to use | Required tools/auth |
|---|---|---|
| [worker-data-collector](../.claude/agents/worker-data-collector.md) | Structured extraction | Files or source-specific GitHub/Slack/Jira/Linear access |
| [worker-researcher](../.claude/agents/worker-researcher.md) | Evidence gathering | Host web tools; source access where required |
| [worker-file-ops](../.claude/agents/worker-file-ops.md) | Vault file changes | Authorized local filesystem access |
| [worker-executor](../.claude/agents/worker-executor.md) | Pre-approved mutations | Target CLI/API credentials supplied by user |
| [worker-publisher](../.claude/agents/worker-publisher.md) | Approved publishing | Target publishing integration or webhook credentials |
| [brief-people-updater](../.claude/agents/brief-people-updater.md) | Profile updates from evidence | Local files and source access if needed |
| [task-verifier](../.claude/agents/task-verifier.md) | Read-only artifact acceptance | Read access to artifact and acceptance criteria |
| [integration-verifier](../.claude/agents/integration-verifier.md) | Read-only cross-task verification | Read access to connected artifacts |
| [fix-agent](../.claude/agents/fix-agent.md) | Targeted fixes after a fixable failure | Scoped write/test tools; this role can edit files |
| [harvest-curator](../.claude/agents/harvest-curator.md) | Propose adoption notes | Read staging; no durable knowledge promotion |

Dependency direction: canonical playbooks feed pointer stubs and generated packaging; builder feeds mirror; validator checks packaging; tests invoke isolated helper copies; indexer maps tracked paths. No component requires an application datastore.
