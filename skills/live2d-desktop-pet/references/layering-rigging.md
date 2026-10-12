# Layering and rigging

## Inventory before edits

Find the active `.model3.json`, moc3, texture atlas, physics, expressions and motions. Validate every referenced file. Prefer `cli-anything-live2d inspect/validate/deps/manifest --json` if installed; use `--help` to confirm syntax. Its edit operations can adjust JSON references and parameter presets, but do not replace mesh/deformer authoring in Cubism Editor.

Create a dated candidate and checksum inventory. Keep the last working editable rig and its runtime export together. Record the Cubism/Core versions and required parameter IDs.

## Separate complete objects

Typical desk-facing layers, back to front:

1. Rear hair, tails, accessories and body underpaint.
2. Face/skin, ears, eyes, brows and mouth.
3. Clothing, front hair and ornaments.
4. Complete keyboard and complete mouse/cable, placed according to reference perspective.
5. Hands/cuffs above the keyboard/mouse and torso occlusion anchors.
6. Phoenix and foreground effects as appropriate for the original composition.

Ordering is reference-dependent. Preserve unrelated drawables and mask relationships when moving a hand ahead of the torso.

## Reconstruct hidden areas

A flattened reference does not contain art behind a hand. Removing the hand alone reveals missing material.

- Complete the mouse body under the hand and move mouse/hand/cable coherently.
- Fill facial/torso areas using matching source skin or fabric, not a flat patch that creates a visible seam.
- Feather internal joins while keeping external contours opaque.
- Inspect alpha halos, stray fragments and missing tail corners at extreme poses, not only neutral.
- Preserve outlines at consistent thickness and color. Avoid unnecessary silhouette expansion; compare against the supplied reference.

For runtime underpaint, bind patch vertices to the native mesh (e.g. barycentric coordinates in UV triangles) so the patch follows head turns and spring deformation. Cache static topology instead of re-searching triangles every frame.

## Rig

Separate front/back hair, ornament pendants, tails/wings, hand presses/reaches, eye openness/gaze, head angle/shape and body breath. Give deformations enough art beneath them to remain filled.

Use small parameter ranges initially, then inspect combined extremes. Test keyboard reach + depth + head bounce + eye gaze together; independent single-parameter checks can miss tears.

Attach physical secondary motion to stable drivers and tune damping, gravity and delay. The character should settle after input rather than oscillate forever.

## Source truth

A repaired atlas, custom renderer mesh or runtime draw-order override is a runtime repair. It is not a new Cubism Editor export unless the editable project was changed, saved and re-exported successfully. Keep the distinction in the handoff and public delivery notes.

Do not binary-edit proprietary rig formats speculatively. Use the editor/export tools and documented SDK. Preserve provided licenses and third-party notices when packaging Core/runtime libraries.
