# Workflow log archive

`memory.md` and `prompts.md` are append-only, sanitized maintenance logs. They currently start as small files. Review their sizes before either approaches 200 KB.

Automatic rotation is a known gap. No `scripts/rotate-workflow-logs.mjs`, Node dependency, scheduled job, or rotation guarantee is introduced for this text framework.

Before a manual rotation, confirm no editor has either log open and check for live swap/lock files. Coordinate with any active writer. Copy complete older version sections into a dated archive file here, retain the latest active section in each root log, and add a link to the archive. Review the diff to ensure no section was lost. Do not archive credentials, private user prompts, or customer material into public Git.

A future rotation helper should refuse live editor swap files and verify preservation before replacing a log. Its implementation remains separate work.
