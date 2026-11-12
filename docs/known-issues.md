# Known issues and limits

This is a maintenance scope record. It does not certify a live agent app or announce completion of the parent optimizer assessment.

| Symptom or limit | Cause | Workaround / affected surface |
|---|---|---|
| Optional integrations may be unavailable or unauthorized | Host/user owns setup and credentials | Use only active, authorized connections; no live provider checks were run |
| Static validation can pass while a host behaves differently | Packaging checks inspect files, not agent interpretation | Validate the requested workflow in its actual host before claiming live support |
| An update may stop after replacing earlier files | Per-file replacement is atomic; the whole allowlist is not transactional | Review diff and backups in an isolated checkout; see update runbook |
| Upstream replacement can overwrite fork customizations | The updater extracts listed official framework files | Review per-file decisions; inspect local maintenance links after an update |
| Kiro/Gemini expose fewer workflows | Seven native core workflows are shipped for each | Use canonical playbooks or universal documentation where the host supports them |
| Lock blocks mirror rebuild, checkpoint recording or updates after an interrupted owner | Lock recovery requires owner judgment | Confirm no writer is active before removing only a stale task lock |
| Five-standard external-call coverage is partial | No central error sink, remediation registry, dashboard, or application datastore exists | See external-calls inventory; do not report full operations compliance |
| Workflow logs can eventually grow | No automatic rotation helper exists | Review near 200 KB; archive append-only sections with editor-swap checks |
| No adopted code of conduct or security response SLA | These are maintainer policy choices | Do not invent commitments; maintainers decide separately |
| Agent inventory is documented manually | No generated agent-frontmatter table/check exists | Compare canonical frontmatter after role changes; component inventory links all 10 roles |
| Indexes cannot hide sensitive tracked names | Indexer uses Git paths, even if bodies stay unread | Review staged path set; do not track private vault filenames |

No new live bug claim is inferred from a placeholder alone. TODO/customization markers in playbooks require user-specific setup. Source fixes and the independent optimizer outcome belong to the parent maintenance task; see [bootstrap audit](repo-bootstrap-audit-2026-11-12.md) for the exact standards status.
