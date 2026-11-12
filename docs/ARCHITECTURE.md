# Architecture

COG stores knowledge as Markdown in an Obsidian-compatible Git checkout. A user-selected agent interprets playbooks and edits files. COG ships no application server, database, listening port, background watcher, or model runtime.

## Context and containers

```text
User -> installed agent -> canonical playbooks (.claude/skills/)
                          -> Markdown vault (user-owned content)
                          -> optional user-configured integrations
Maintainer -> Bash/Python helpers -> framework files and packaging checks
                               -> Git metadata -> official upstream (fetch only)
Obsidian -> the same Markdown files (optional editor)
```

The agent host, Git hosting, Obsidian, and integration providers are outside the framework boundary. The checkout runs locally. CI runs synthetic checks on GitHub-hosted Ubuntu and macOS runners.

## Components and flows

- `.claude/skills/` holds 35 canonical skills. `.claude/agents/` holds 10 agent roles. `.claude/roles/` supplies role recommendations.
- `.agents/` contains pointer stubs; `skills/` is a generated copy of canonical skills. Kiro and Gemini each ship seven core workflows. Cursor uses manifests and rules. See [components](COMPONENTS.md).
- The user invokes a skill; the host reads the playbook; the agent reads authorized inputs, writes Markdown, and observes any external result. Skill instructions require their own approval and evidence rules.
- `cog-update.sh` checks an allowlist of framework paths against a fetched upstream commit. It replaces individual files, rebuilds the skill mirror, and validates packaging. This is not a transaction across the whole update.
- `scripts/doc_indexes.py` builds path-only retrieval maps from Git's tracked/staged path set. It reads no document bodies and performs no inference or embedding.

## Architectural decisions

1. **Markdown and Git are the persistence model.** Users can inspect and edit files without a running service. Sync and backup remain user choices.
2. **Canonical playbooks have derived surfaces.** Contributors edit `.claude/skills/` and regenerate `skills/`; pointer stubs do not duplicate the full playbook.
3. **Maintenance checks stay offline.** Tests use synthetic content and local Git fixtures. Semantic indexing and live integration checks require separate authorization.
4. **Integrations belong to the user.** No shared credentials or mandatory MCP configuration ships with this maintenance baseline.

## Constraints

Packaging parity proves static consistency. It does not certify live agent clients or integration permissions. No latency, throughput, availability, or compliance guarantee is established. Private vault content must stay outside public commits and retrieval maps. See [security](SECURITY.md) and [testing](TESTING.md).
