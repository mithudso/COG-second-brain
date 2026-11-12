# Requirements

## Functional requirements

1. Store knowledge in user-editable Markdown, using the documented vault layout.
2. Supply canonical skills, role guidance, and agent definitions with derived host surfaces.
3. Preserve user content during framework maintenance; updater writes are restricted to its explicit framework allowlist, which includes some public templates inside vault directories.
4. Validate manifest skill coverage, mirror parity, command headings, and release version agreement.
5. Provide opt-in evidence checkpoints and heuristic risk lanes for harness workflows.
6. Generate deterministic offline maps from tracked/staged file paths without reading vault bodies or creating embeddings.
7. Respect user integration choices and observe external mutations before reporting success.

## Compatibility and quality

The helper CI matrix is Ubuntu and macOS, Python 3.11 and 3.13. Shell helpers use Bash, including accommodations for macOS system Bash 3.2. Git must support the commands used by the tests, including `git init -b`; a minimum Git release is not pinned. Windows and live host compatibility need separate verification.

Preserve filenames, executable modes, personal content, and unrelated concurrent work. Tests must be repeatable with synthetic input and local Git. No measured latency, throughput, vault-size ceiling, uptime target, or numeric coverage threshold is established.

## Dependencies

| Requirement | Purpose | Pin policy |
|---|---|---|
| Git | Tracked paths, local fixtures, optional upstream fetch | System/user supplied; no exact version pin |
| Bash and Unix tools | Maintenance helpers | OS supplied; checked in Ubuntu/macOS CI |
| Python 3 stdlib | Scanners, tests, offline indexes, JSON validation | CI selects 3.11 and 3.13; patch releases float |
| Agent host | Interprets skills | User selected; outside helper runtime |
| Obsidian | Optional Markdown editor | User supplied |
| Integration tools/accounts | Optional skill capabilities | User-owned configuration and credentials |
| GitHub Actions | Repository CI | Tagged action refs; Dependabot tracks updates |

There are no mandatory npm/pip runtime dependencies or lockfiles to pin. Node is unnecessary for maintained helpers; the optional `npx skills` installation route in existing docs uses a separate user-provided toolchain. No `.env`, MCP, or editor scaffolding is required. Semantic indexing scripts are intentionally absent.
