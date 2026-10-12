# Input, rendering and native behavior

## State architecture

Normalize input to semantic actions in the native layer. Send transient physical key labels only when the user enables a key overlay. Do not reconstruct typed text, retain key history, intercept input or transmit it.

Keep presentation state independent from React component lifetimes: action start/expiry, expression, gaze, physics and bubbles. The renderer consumes a snapshot; user interface updates should not recreate the Cubism instance.

Each repeated input needs a new start timestamp even when its action ID is unchanged. Use channels for keyboard press/reach/depth, mouse press/displacement, head response and expressions so one action does not freeze the others.

## Per-frame composition

1. Restore/reset ephemeral parameters to their base values.
2. Update authored motions and expressions according to explicit priorities.
3. Apply coherent blink, gaze, breath and physical secondary motion.
4. Apply semantic input overrides in a defined order, especially hand ownership and release.
5. Update Core and draw the current state with stable clipping/order.

Check the SDK's required load/save/update order. Do not assume a generic ordering fits every renderer. Stop or release a conflicting authored motion when direct input takes ownership.

Keep keyboard reach after key release long enough to look natural, while releasing the press immediately. A spring with velocity and damping yields better rebound than restarting the same CSS animation on every key.

Use the same gaze target for both eyes and verify sign conventions on the actual rig. Limit pupil motion so the eyes do not converge at neutral. Blend expression openness with blink closure, rather than overwriting each other frame by frame.

## One-hand keyboard example

Map all physical keys by region, not just Q/A/U/H examples. Separate left/right and front/back coordinates plus the Space landing point. Then map the entire keyboard to the designated hand. Mouse actions use the other hand. Anatomical left/right and the screen drawing order may be opposite.

Inspect reach extremes: the keyboard hand must remain above the torso; the mouse hand must not expose a permanent hole. Keep complete underpaint underneath.

## Windows integration

Native responsibilities include transparent/frameless windows, show/hide, tray, global input, click-through, monitor placement, settings/menu priority and lifecycle. Use the existing framework's APIs and Win32 flags deliberately.

- Startup: initialize listeners independently of foreground focus and send a readiness handshake after WebView/model initialization.
- Pet: avoid stealing foreground focus on routine reactions.
- Menu/settings: raise and focus the intended UI when requested. A menu drag must not be dismissed by transient blur/lost-focus events; track drag state and delay dismissal until release.
- Placement: compute space beside the visible character. Use monitor work areas, common coordinate units and scale-aware visible bounds.
- Drag/edge snap: place the handle inside a usable corner; account for transparent margins so the pet can reach the screen bottom.
- Fullscreen behavior: identify the pet's monitor and avoid hiding for unrelated monitors; manual hide remains authoritative.
- Shutdown: dispose hooks, timers, Core resources and tray state.

Browser callbacks are a preview fallback, not proof of global hooks or desktop transparency. Native verification must launch the built EXE/app in its target OS.

## Continuous settings

Use an in-memory draft while dragging. Coalesce updates to avoid dozens of overlapping native resizes. Flush pending work before persisting the final value, guard stale completions with revisions, and roll back failed saves.

Scale pet overlays with a common container unit, such as cqw, rather than unrelated fixed pixel values. Clamp bubbles to remain readable while adapting to model size. Physical window dimensions must also follow the scale; adjusting only CSS can clip the character.

Use a few well-defined categories and consistent rows. Place related expression controls in symmetric groups. Keep dangerous/debug-only commands out of ordinary settings; do not display implementation labels in the everyday product UI.
