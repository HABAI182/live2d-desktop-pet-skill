# Changli engineering case study

This is a project-specific example, not a template for all characters.

The app uses React/TypeScript/Vite with Tauri/Rust native integration and a real Cubism runtime. Its desk-facing character has a keyboard hand, mouse hand, large head, ornaments and a small phoenix. Supplied art controls the character identity; creator references control desired liveliness without importing their models.

## Useful source boundaries

- `src/pet/presentation.ts`: semantic actions, state snapshots and the one-hand keyboard policy.
- `src/renderer/live2d/Live2DAdapter.ts`: semantic parameter mapping, per-event motion retriggering, expression resolution and renderer lifecycle.
- `src/renderer/live2d/CubismBackend.ts`: Core, native model parameters and custom runtime deformation.
- `HandDrawOrder.ts`: opt-in hands placed after torso anchors while unrelated drawables keep their relative order.
- `JawRepair.ts`: missing skin filled from the native face texture and bound to existing UV triangles; cached topology follows current deformation.
- `MouseMesh.ts`, `MouseRegionRenderer.ts`: mouse reconstruction and displacement shared with hand/cable.
- `FaceEffects.ts`: runtime expression/effect visuals separate from editable source rig.
- `src/overlay/keyOverlay.ts`: ephemeral physical labels, 680 ms lifetime, not saved input history.
- `src/settings/SettingsPanel.tsx` and `scalePreview.ts`: draft/coalesced continuous scale updates and final persistence.
- `src-tauri/src/input.rs`: privacy-preserving semantic conversion and transient physical labels.
- `src-tauri/src/pet_menu.rs`, `desktop.rs`, `windows.rs`: native windows, menu, desktop placement and lifecycle.

At the time this skill was made, the app version was 0.7.12, the current runtime was the v71 candidate, and the editable recovery file was `authoring/ChangliReferenceRepair-v71-verified.cmo3`. Verify these paths on every resumed task; version names are not evidence of visual acceptance.

## Lessons

1. All keyboard regions belong to the keyboard hand. Left/right keyboard zones do not mean anatomical left/right hand ownership; add depth and Space separately.
2. A moving mouse hand needs a complete mouse beneath it. Moving a keyboard hand needs continuous facial/torso underpaint. A neutral-pose cutout is insufficient.
3. Reset input residue and identify repeated actions by timestamp, not action ID alone. Restore default expressions when a requested face has no authored mapping.
4. Gaze and blink are coupled to expression openness; closed eyes for sleep are valid, closed eyes mislabeled as happy are a product mismatch.
5. The UI, native priorities and drag bounds are part of the pet experience. A pretty browser preview does not validate global input, focus or monitor placement.
6. Runtime patch meshes, masks, expressions and offsets do not prove the editable Cubism project contains those improvements. Save their separate provenance.
7. Keep app delivery version archives, save progress at material milestones and spend verification effort on the visible/native problem being changed.

Promotional videos and their production tools are intentionally excluded from this skill.
