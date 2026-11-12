# Framework update

## Preconditions

An upstream update is an explicit maintenance operation. Use an isolated checkout when local framework customizations or concurrent edits exist. Back up user content separately. Confirm the intended official source is Huy Tieu's COG; the personal fork remains `mithudso/COG-second-brain`.

The updater writes only its `FRAMEWORK_FILES` allowlist. The list includes public README/template files within vault directories. It does not mean every path under a vault directory is excluded. Private user content must remain outside that allowlist.

## Procedure

The following commands are documented for a separately authorized update; documentation production and CI do not run them:

```bash
./cog-update.sh --check
./cog-update.sh --dry-run
./cog-update.sh
```

Both preview modes add `cog-upstream` if absent and fetch `main`; they change Git metadata even though they do not replace framework files. An existing foreign `cog-upstream` URL is refused. The updater then pins the fetched commit for local object reads.

Review changed files individually in interactive mode. Choose skip for customizations you want to keep. Choose backup plus update when appropriate. Interactive accept without backup can replace a local file. `--force` skips per-file decisions and makes unique backups of existing files; reserve it for an explicitly approved replacement scope.

Updates use same-directory temporary files, preserve supported upstream modes, and reject linked path components. The script rebuilds the root skill mirror after changes and runs packaging validation. It does not automatically commit changes. New fork-only maintenance files are not automatically added to the upstream allowlist.

## Verification and recovery

Review the diff, attribution, local maintenance links, mirror, and version alignment. Run the [offline validation suite](validation.md). Check that intended private content was preserved without exposing its names or bodies in public output.

If a later step fails, earlier file replacements may remain. Stop and inspect the diff and any ignored `*.backup-*` files. Restore only the intended file from its reviewed backup or a known Git version. Never use blanket reset, checkout, or stash operations on shared work. A mirror recovery failure prints a staging location to preserve for inspection.

## Escalation

For source identity, permission, fetch, path validation, mirror, or packaging errors, keep sanitized diagnostics and resolve the specific failure before committing. Do not override the official-remote identity guard or retry unknown authentication failures automatically. There is no central remediation service, all-files rollback transaction, or security response SLA.
