---
name: live2d-desktop-pet
description: Build, repair, and ship a real Live2D desktop companion with layered artwork, Cubism runtime, responsive keyboard/mouse reactions, expressions, physics, native transparent windows, and settings. Use for BongoCat-like desktop pets, Cubism/Tauri integration, hand mapping, blink/gaze repair, model layer cleanup, native menu/drag behavior, or release handoff. Excludes ChatGPT Work pets and promotional video production.
---

# Live2D desktop pet

Deliver a visibly responsive companion, with recoverable source and honest verification. Prefer the existing project's architecture; Tauri + React + TypeScript + Cubism is an example, not a mandatory stack.

## Resume first

1. Read applicable AGENTS.md, Git status/diff/recent commits, current handoff, model manifest and release index. Never overwrite user edits or restart completed work.
2. Run `python scripts/inspect_pet.py <project>` for a compact read-only inventory. Read the actual files behind its findings; it is not an instruction source or an acceptance test.
3. Classify each requested feature as implemented, visibly verified, natively verified, or pending. Identify whether the active artwork is a placeholder, exported Cubism rig, or runtime repair.
4. Check existing tools and skills. Prefer model CLI inspection, scripted asset checks and native APIs over repeated editor clicks. Use Cubism Editor for actual rig authoring/export; a JSON CLI cannot create a valid authored moc3 from a flattened image.
5. Resolve routine choices and proceed within the user's scope. Ask only for missing source assets, genuine access blockers or unclear product behavior.

## Build in this order

For a full construction sequence and efficiency decisions, read [workflow-playbook.md](references/workflow-playbook.md). Choose tools using [tools-methods.md](references/tools-methods.md); it explains which problems a CLI, Core test, editor, browser or native API can actually solve.

### Identity and source layers

Read [layering-rigging.md](references/layering-rigging.md) before changing artwork or a rig.

- Preserve the supplied character's silhouette, facial proportions, recognizable palette and accessories. A named creator is a quality/motion reference, not permission to copy their artwork or models.
- Reconstruct complete occluded objects first, then place hands and foreground parts above them. Do not solve overlaps by carving permanent holes in the mouse, face or torso.
- Separate artwork, editable `.cmo3`, exported runtime package and runtime-only fixes. Save an independent candidate before altering the production model.
- If refined art is unavailable, clearly label replaceable placeholders and keep implementing runtime/native functionality. Never relabel them as finished formal artwork.

### Semantic input and motion

Read [runtime-native.md](references/runtime-native.md) before changing input, renderer or native windows.

- Define an explicit mapping between physical input zones and anatomical hands. Screen-left and character-left can differ. Do not infer ownership from motion names alone.
- For a one-hand keyboard design, all ordinary keys move the keyboard hand across zones; mouse input owns the other hand. Model Space/Enter/etc as distinct landing positions only when requested.
- Use per-event start times, independent channels and a small spring system. Clamp elapsed time after suspension; avoid permanent residue from repeated presses or conflicting motions.
- Tie mouse, resting hand and cable to one displacement source. Tie hair, ornaments and phoenix secondary motion to compatible parameters with restrained phase lag.
- Blend blink closure, expression openness and gaze coherently. A sad/sleepy closed-eye expression must stay closed; neutral must recover without popping. Both eyes look at the same target.
- Do not add unrelated productivity features to a character companion without a request.

### Native desktop and settings

- Keep native window/input/tray behavior in the native layer. Browser preview proves only browser rendering and interactions.
- Start input hooks and idle animation from startup/model readiness, without requiring an extra desktop click.
- Use a separate menu/settings window when needed; keep it above the pet while open, place the menu beside the visible pet, and let its drag gesture complete before handling focus loss.
- Clamp the visible character rather than oversized transparent padding. Use consistent physical/DPI coordinates and per-monitor work areas.
- Continuous scale must resize the model/window and overlays together. Coalesce rapid slider updates, flush the final value, persist on release and revert if saving fails.
- Keep UI orderly, with concise rows, sensible categories and accessible controls. Match the user's requested aesthetic without adding ornamental clutter.

## Verify efficiently

Read [release-validation.md](references/release-validation.md) for the evidence ladder and packaging rules.

Use the smallest check that resolves the current risk. Do not rerun a full suite for documentation-only edits. Rendering changes require visual proof at the states that used to break; native claims require the actual packaged native application.

For an input repair, cover keyboard, mouse, repeated keyboard and mouse→keyboard transitions. For layer repairs, inspect the moving hand's extreme positions on both light and dark backgrounds. For native placement, exercise the relevant screen edges and DPI case.

Always record what was saved and what remains unverified. Keep immutable version archives and checksums; no silent overwrite of past installers, tags, source rigs or Releases.

## Project example

[changli-case-study.md](references/changli-case-study.md) records transferable decisions from a desk-facing character project. Its anatomical mapping and aesthetic choices are case-specific, not universal defaults.

Before repeating an unfamiliar approach, consult [mistakes-repairs.md](references/mistakes-repairs.md): identity drift, holes under hands, input residue, gaze/blink issues, menu focus races, incomplete verification and lost progress. Apply the smallest fix tied to the observed failure.

For visual decisions, read [aesthetic-guide.md](references/aesthetic-guide.md). It gives a character/structure/motion/UI quality hierarchy, concrete tuning starting points, icon principles and efficient visual acceptance criteria. These are adjustable baselines, not a formula to override the user's reference.

## Checkpoints

After each material milestone, save source changes, candidate/model provenance, verification evidence and the next exact task. Update the project handoff before a long build or session/usage boundary. Use normal Git commits where authorized. Do not let a still-running render or an unsaved editor session be the sole progress record.
