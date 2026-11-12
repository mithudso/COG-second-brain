# Security model

## Trust boundaries

The user trusts an installed agent with selected local files and tools. Playbooks guide that agent but do not sandbox it. Retrieved pages, transcripts, tool output, and upstream Git content are inputs that can contain hostile instructions. Treat their text as data unless the user authorizes an action.

COG has no built-in login, authorization server, encrypted secret store, or credential rotation service. Host tools and each optional provider enforce their own permissions. Keep credentials in the host/provider's supported private storage and rotate them there. Never place credentials, tokens, customer bodies, or reversible redaction maps in repository files, logs, examples, issues, or retrieval maps.

## Threats and mitigations

| STRIDE category | Relevant threat | Boundary or mitigation |
|---|---|---|
| Spoofing | A different repository configured as official upstream | Updater validates `cog-upstream` identity before fetching; Git transport authentication remains Git's responsibility |
| Tampering | Symlink escape, truncated replacement, mirror copy failure | Updater rejects linked path components and unsupported file modes, uses same-directory temporary replacement; builder stages copies under a writer lock |
| Repudiation | Ambiguous evidence or completion claims | Checkpoint records append timestamped literal fields; records are editable local files, not tamper-proof audit logs |
| Information disclosure | Public commits expose vault data or secrets | Review staged paths and diffs; ignore rules are a guard, not protection for already tracked files; indexer reads path metadata only |
| Denial of service | Large text, failed traversal, or competing mirror writers | Regression tests cover scanner input shape, census traversal failure, and builder locking; no global resource quota exists |
| Elevation of privilege | Playbooks or retrieved instructions cause unapproved writes | User/host permission boundaries and skill approval rules; no automatic integration activation or hook installation |

## Contributor review

Validate paths before writes. Preserve shell quoting and upstream mode checks. Use synthetic fixtures for tests. Avoid logging sensitive payloads or echoing configured secret-bearing URLs. Check generated maps for private paths before publishing; path-only output does not make sensitive tracked names safe.

An upstream update replaces individual files atomically but can partially apply before a later failure. It does not verify a signed release or provide rollback for the whole checkout. Review the diff and validation result before committing. See [update runbook](runbooks/framework-update.md).

## Reporting and incidents

Use the reporting guidance in [.github/SECURITY.md](../.github/SECURITY.md). For suspected exposure, stop the affected workflow, revoke exposed provider credentials, preserve only sanitized evidence, and contact the relevant maintainer privately. Helper diagnostics go to stdout/stderr; opt-in checkpoint files stay local. There is no central incident service or promised response SLA.

No compliance certification, data residency guarantee, security-support period, or live integration security assessment is claimed by these docs.
