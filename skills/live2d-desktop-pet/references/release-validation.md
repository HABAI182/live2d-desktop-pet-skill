# Verification and delivery

## Evidence ladder

Record each level separately:

| Level | Evidence | What it cannot establish |
| --- | --- | --- |
| Files | Model references, JSON schema, checksums, compiled source | Appearance or behavior |
| Unit/Core | Semantic mappings, blink curves, parameter behavior | Visible WebGL quality or OS windows |
| Browser | Real WebGL/model rendered and input/extreme poses inspected | Global input, tray, click-through or native placement |
| Native | Packaged target-OS application exercised | Other OS/DPI/monitor cases not exercised |

Do not mark `webglRendered:false`, `windowsDesktopVerified:false` or "saved; verification pending" as complete. If a user tested a target device, attribute that evidence to the user rather than claiming your own test.

## Small meaningful checks

- Input change: separate mouse, keyboard, rapid repeated keyboard and mouse→keyboard transitions.
- Blink/gaze: neutral, eyes closed by expression, blink midpoint and reopen, fast mouse extremes.
- Art: source-reference overlay/crops, all relevant hand extremes, alpha edge on contrasting backgrounds.
- Native UI: startup without desktop click; open/drag menu; settings above pet; bottom/side placement where changed.
- Packaging: build the changed target, inspect version/resources and smoke-launch if the host supports it.

Run broader tests only for new failures, code changes or unresolved risks. Documentation cleanup needs a path/reference check, not a full native rebuild.

On Windows temp-directory ENOENT, use a verified project-local TEMP/TMP for that command. Do not repurpose HOME/CODEX_HOME or disable checks merely because temporary storage failed.

## Version preservation

Keep source commit, editable rig, runtime export, executable/installer, notices and SHA256 together in immutable per-version delivery records. A source model and a runtime repaired model may have separate provenance.

Keep at least the current and previous recoverable versions. Never overwrite historical executables, move tags, force-push or delete old Releases as routine cleanup. Target OS/architecture must be explicit in filenames and release notes; separate Windows and macOS builds.

Before cleaning a repository, inspect references and package scripts. Archive unused candidates/media locally, confirm hashes, then remove only the authorized tracked content with an ordinary commit. Exclude credentials, caches, dependency runtimes, private databases, logs and generated deliveries from source Git.

Final delivery must give actual local artifact links, a concise implemented/verified/pending account and the exact remaining risk. Save a project checkpoint before long builds or usage boundaries.
