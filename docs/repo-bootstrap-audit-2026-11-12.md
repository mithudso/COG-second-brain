# Repository bootstrap audit, 2026-11-12

## Scope and evidence

This records the full repository maintenance bootstrap, including the bounded documentation producer and subsequent source, metadata and index verification. It applies repo-bootstrapper's standard file manifest and audit checklist to a Markdown/agent framework. The local bootstrap prompt was consulted. Explicit scope restrictions take precedence over server-specific scaffolding, global skill installation, semantic indexing, blanket staging, and shipping steps.

Evidence: local canonical helpers, packaging manifests, tracked framework paths, existing top-level docs, LICENSE, and local origin URL. No web research, user-memory lookup, integration probe, personal onboarding, real upstream update, inference, semantic indexing, Git commit, or lifecycle tool ran in this documentation subtask. Private vault bodies and untracked-path inventories are excluded.

The canonical inventory is 35 skills and 10 agents; Kiro/Gemini each ship seven core workflows. `.agents/` are pointer stubs; `skills/` is generated. Original author/license/URLs remain Huy Tieu/MIT/official upstream. Personal fork: `mithudso/COG-second-brain`.

**PRESENT** means a pre-existing applicable artifact was retained or linked. **ADDED** means an artifact was created in this maintenance batch, including explicitly identified parent-owned tooling. **EXCEPTION** means intentionally inapplicable or excluded by scope. **GAP** means unimplemented or awaiting its named owner. These labels do not mean all checks or delivery have completed.

## Standard file manifest

| Manifest row | Status | Evidence or disposition |
|---|---|---|
| `.github/copilot-instructions.md` | ADDED | Default strategy, exact offline commands, conventions, and shared log rule. |
| `CLAUDE.md` | PRESENT | Existing playbook retained; count corrected and local maintenance/log links appended. Detailed commands live in DEVELOPMENT.md. |
| `AGENTS.md` | PRESENT | Existing command catalog and 10-agent tables retained; local component/agent inventory linked. Generated agent inventory remains a gap below. |
| `GEMINI.md` | PRESENT | Existing playbook retained; shared conventions and seven-workflow boundary appended. |
| `memory.md` | ADDED | Sanitized versioned progress log; parent delivery is explicitly pending. Release owner coordinates final version heading. |
| `prompts.md` | ADDED | Append-only sanitized request summary; no private prompt transcript. |
| `docs/archive/` | ADDED | Archive README explains size review and preservation procedure. |
| `scripts/rotate-workflow-logs.mjs` | GAP | No automatic rotation helper; logs are tiny. Review near 200 KB and check editor swap/locks before manual rotation. No Node dependency introduced. |
| `.editorconfig` | ADDED | UTF-8/LF/final newline, indentation, Markdown trailing-space exception. |
| `.gitignore` | PRESENT | Existing vault/backup/log/cache protections are parent-owned. Ignore rules cannot protect already tracked sensitive content. |
| `.gitattributes` | ADDED | Text LF normalization and binary markers. |
| `.nvmrc or .node-version` | EXCEPTION | No mandatory Node runtime or package manifest. Optional npx installation is user-owned. |
| `.tool-versions` | EXCEPTION | Optional tool manager; CI declares Python 3.11/3.13 without imposing a local manager. |
| `.env.example` | EXCEPTION | No mandatory service environment variables or shared credentials; supported environment assumptions are documented. |
| `.vscode/settings.json` | EXCEPTION | No mandatory editor, formatter service, or application runtime. |
| `.vscode/extensions.json` | EXCEPTION | Editor choices remain user-owned. |
| `.vscode/launch.json` | EXCEPTION | No application server/debug launch target to configure. |
| `.vscode/mcp.json` | EXCEPTION | No bundled MCP server; optional host connections remain user-owned. |
| `.mcp.json` | EXCEPTION | No mandatory repository MCP service or shared authentication. |
| `.github/workflows/ci.yml` | ADDED | Four Ubuntu/macOS x Python 3.11/3.13 jobs; syntax, packaging, synthetic unit tests, index freshness, tracked diff check. Remote CI outcome is parent-owned. |
| `.github/dependabot.yml` | ADDED | Monthly GitHub Actions updates; no npm/pip runtime ecosystem exists. |
| `.github/CODEOWNERS` | ADDED | Personal-fork reviewer @mithudso; local origin URL matches fork. This does not assert review rules are enabled. |
| `.github/PULL_REQUEST_TEMPLATE.md` | ADDED | Change, reason, tests, risk, rollback. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | ADDED | Synthetic reproduction and privacy guidance. |
| `.github/ISSUE_TEMPLATE/feature_request.md` | ADDED | Observable behavior, validation, boundaries. |
| `.github/SECURITY.md` | ADDED | Conditional private reporting guidance and threat-model link; no invented mailbox, support window, or response SLA. |
| `LICENSE` | PRESENT | MIT, copyright 2025 Huy Tieu; unchanged. |
| `CONTRIBUTING.md` | PRESENT | Existing contribution playbook retained; development/testing/security/audit links appended. |
| `CODE_OF_CONDUCT.md` | GAP | Adoption and enforcement are maintainer choices. No policy invented. |
| `docs/ARCHITECTURE.md` | ADDED | Context, local containers, component flows, decisions, quality boundaries. |
| `docs/DEVELOPMENT.md` | ADDED | Actual prerequisites, commands, environments, focused workflow, troubleshooting. |
| `docs/COMPONENTS.md` | ADDED | 35 canonical skills, 10 linked agents, derived surfaces, seven maintained helpers, separate indexer/test tooling. |
| `docs/SECURITY.md` | ADDED | STRIDE threats, host/user boundaries, secret handling, reporting limits. |
| `docs/MCP.md` | ADDED | No shipped server or tool inventory; optional host MCP scope explained. |
| `docs/TESTING.md` | ADDED | Behavioral suite, exact commands, real CI gates, no numeric coverage threshold or live-app claim. |
| `README.md` | PRESENT | Existing product entry retained; stale 33 counts corrected to locally counted 35; local fork and maintenance docs linked. |
| `docs/codebase-overview.md` | ADDED | Complete tracked/staged path map generated after explicit public-path staging; freshness check passes. |
| `docs/high_signal_file_index.json` | ADDED | All tracked/staged paths represented with classification; no document bodies or embeddings; freshness check passes. |
| `scripts/semantic_indexer.py` | EXCEPTION | Intentionally absent. Inference, embeddings, and semantic ingestion are outside this maintenance scope. |
| `scripts/watch_and_index.sh` | EXCEPTION | Intentionally absent; no background watcher or semantic indexing activation. |
| `scripts/check-doc-indexes.mjs or equivalent` | ADDED | Parent implements Python stdlib equivalent scripts/doc_indexes.py --check; no Node runtime needed. |
| `docs/integrations-and-assumptions.md` | ADDED | Actual Git source identity, optional provider boundary, environment assumptions. |
| `docs/known-issues.md` | ADDED | Limits, preservation concerns, remaining policy/automation gaps; no optimizer completion claim. |
| `docs/onboarding.md` | ADDED | Contributor walkthrough distinct from optional personal onboarding. |
| `docs/INSTALLATION.md` | ADDED | Fork installation, verification, update/uninstall boundaries. |
| `docs/requirements.md` | ADDED | Functional/quality requirements, system tools, no fabricated package pins or hardware targets. |
| `docs/logging.md` | ADDED | Actual console/TSV outputs, sensitive text limits, missing central logger and rotation. |
| `docs/caching-and-optimization.md` | ADDED | Derived mirrors/maps, Git state, measured-performance limits; parent assessment pending. |
| `docs/runbooks/*.md` | ADDED | validation.md and framework-update.md use preconditions, actions, verification, escalation. |
| `docs/external-calls.md` | ADDED | Literal updater call sites distinguish local Git operations from fetch; per-call logging/test/retry gaps are explicit. |
| `server/src/lib/operations-registry.js or mcp-server equivalent` | EXCEPTION | No application server, MCP service, or datastore exists; do not create an unrelated operations runtime. |
| `scripts/generate-ops-registry-doc.mjs` | EXCEPTION | No operations runtime to generate from; manual scoped external-call inventory is explicit. |
| `docs/operations-registry.json` | EXCEPTION | No executable operations registry; five-standard coverage remains partial; no pass is claimed. |
| `docs/tool-inventory.json` | EXCEPTION | No registered server tools/routes; local agent inventory is in COMPONENTS.md. |

## Additional audit checklist items

| Check | Status | Disposition |
|---|---|---|
| `docs/wiki/index.md`, `docs/wiki/maintenance.md` | ADDED | Offline navigation only; no remote wiki integration or publication. |
| `SETUP.md`, `WORKFLOW.md` maintenance links | PRESENT | Existing playbooks retained; appended network/validation boundaries. Harness remains opt-in. |
| `docs/llm-repo-index.json` | EXCEPTION | Parent path-only indexer instead emits high_signal_file_index.json, codebase-overview.md, and llms.txt. No semantic or content index. |
| Context-file global skill installation and skillfish metadata | EXCEPTION | No docs/*-context.md files or global skill installation requested. No user-environment mutations. |
| Legacy support counts and agent roles | PRESENT | Refreshed support matrix and manifest metadata to35skills/commands and10agents. fix-agent remains writable;3verification roles are read-only. Five versions align at3.13.1. |
| Generated agent-frontmatter table and drift check | GAP | All 10 roles linked in COMPONENTS.md; AGENTS.md remains a hand-maintained catalog. No claim that its table is generated. |
| Concept-tree registration/refresh | EXCEPTION | No repository concept-tree runtime; external registries/knowledge lifecycle belong to parent. |
| MCP boot/self-test/tool count | EXCEPTION | Repository ships no MCP server. User connections are not probed. |
| npm/pip audit, lockfiles, engines parity | EXCEPTION | No mandatory third-party runtime dependencies; system tool versions and CI patch releases float. Optional host tools are outside scope. |
| Native host and MV3 offscreen audits | EXCEPTION | No browser-extension/native-host application runtime in this framework. |
| Authentication health checks | EXCEPTION | Optional providers and Git authentication are user-owned; no live credential probe authorized. |
| Customer data and index privacy | GAP | This bounded subtask does not certify all tracked content. Parent must review staged paths and generated maps; no private names/bodies may enter public output. |
| Action SHA pinning | ADDED | Official GitHub tag commits resolved on2026-11-12 and SHA pinned; monthly Dependabot configured. No latest-major claim. |
| Five-standard external-call contract | GAP | CLI exists; console diagnostics/manual recovery are partial; no central log/automatic remediation. Dashboard/datastore are architectural exceptions. See external-calls.md. |
| Log rotation near 200 KB | GAP | Manual archive guidance exists; no automated swap-aware rotation helper. |
| Security response-time SLA | GAP | Maintainer choice; no commitment invented. |
| Full optimizer assessment/report | ADDED | Detailed structural findings,59 synthetic regression tests, full path coverage, snapshots/rollback and qualified independent gate result in code-deep-optimizer-2026-11-12.md. |

## Validation contract and exact limits

The proposed CI matrix has four jobs: Ubuntu/macOS with Python 3.11/3.13. Each job runs:

```bash
for script in cog-update.sh .claude/lib/checkpoint.sh .claude/lib/lane-classify.sh scripts/build-agent-plugin.sh scripts/validate-agent-surface.sh; do bash -n "$script" || exit; done
./scripts/validate-agent-surface.sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/doc_indexes.py --check
git diff --exit-code HEAD
```

Tests use synthetic stdlib fixtures and local Git, including redirected updater fetches. No live updater or provider certification is implied. No numeric line-coverage target is enforced. Packaging subset counts can warn without failure. The final diff check is for a fresh CI checkout; existing shared-checkout changes require preservation and scoped before/after review.

Parent owns final source/test execution, generated-map freshness after staging, version alignment, optimizer conclusion, remote CI observation, commits, and delivery. This audit is an honest partial standards baseline, with explicit gaps and architectural exceptions. It is not a zero-findings report.

## Documentation subtask observations

Local review resolved all relative links in 27 new Markdown docs/metadata/log files, verified 35 canonical skills and 10 agents against local paths, matched all 15 updater command anchors to source, parsed CI/Dependabot YAML, and checked the four-job/seven-step CI shape. The new prose passed the local scanner after three wording fixes. Scoped tracked-diff whitespace checking passed. No parent-owned source/test suite, index generation, live updater, remote CI, or delivery step was run by this documentation producer.

## Final maintenance verification

The full run repairs one High and54Medium findings across four structural iterations (including two directed blind-gate repairs), including later metadata/CI/test defects. All 59 synthetic tests, packaging, shell syntax,4 JSON manifests,17 TOML configs,35 pointer identities,90 frontmatters and3YAML metadata files pass locally. The narrow dependency-free skill-frontmatter guard covers required fields and the observed bare-colon failure; it is not a complete YAML parser. All 18 tracked vault-layout/template files remain byte-identical. No untracked private primary-vault paths were inventoried.

The source-only independent gate and final delivery are recorded in the optimizer report and external batch receipt. Four remote CI combinations must pass on the final pushed head before merge. The delivery receipt records observed check IDs, merged PR/content verification, and safe primary synchronization; this document does not claim a merge in advance. Remaining manifest gaps above are intentional explicit limits, including workflow-log rotation, generated frontmatter table, full operations coverage, and maintainer policy choices.

The optimizer exit remains **BLIND-AUDIT-DISSENT** after both allowed independent gates found subsequently repaired defects. All 59 tests and the final conventional checks pass, but no third blind audit of the final directed repair is claimed.
