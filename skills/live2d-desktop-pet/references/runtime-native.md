# Input, rendering and native behavior

## State architecture

Normalize input to semantic actions in the native layer. Keep physical codes only as current held state; bounded display labels serve the optional overlay. Do not reconstruct typed text, retain key history, intercept input or transmit it. See [input-and-game.md](input-and-game.md) for edges, autorepeat, release and OS permissions.

Keep presentation state independent from React component lifetimes: action start/expiry, expression, gaze, physics and bubbles. The renderer consumes a snapshot; user interface updates should not recreate the Cubism instance.

Each distinct physical re-press needs a new start timestamp even when its action ID is unchanged. OS autorepeat is not a new press: it maintains the held pose without restarting head springs, the pressure cycle or authored motion. Use independent channels for keyboard press/reach/depth, mouse press/displacement, head response and expressions.

## Per-frame composition

1. Restore/reset ephemeral parameters to their base values.
2. Update authored motions and expressions according to explicit priorities.
3. Apply coherent blink, gaze, breath and physical secondary motion.
4. Apply semantic input overrides in a defined order, especially hand ownership and release.
5. Update Core and draw the current state with stable clipping/order.

Check the SDK's required load/save/update order. Do not assume a generic ordering fits every renderer. Stop or release a conflicting authored motion when direct input takes ownership.

On release, set the pressure target toward neutral and ease it out; reach may settle slightly later. If the same hand still owns another held key, preserve that key instead. A spring with velocity and damping yields a controlled rebound; do not restart a CSS animation on every autorepeat.

Use the same gaze target for both eyes and verify sign conventions on the actual rig. Limit pupil motion so the eyes do not converge at neutral. Blend expression openness with blink closure, rather than overwriting each other frame by frame.

## One-hand keyboard example

This is an optional ownership policy, not the current default for every project. A two-hand policy maps physical left/right zones to anatomical hands, with keyboard ownership overriding the mouse while the mouse hand is busy. Confirm screen mirroring and model parameter names; see [keyboard-space.md](keyboard-space.md).

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

Detailed window, startup, scaling and persisted-setting behavior is in [windows-settings.md](windows-settings.md). Do not copy a case project's default elevated launch or browser flags into an unrelated product without evidence and authorization.

## Continuous settings

Use an in-memory draft while dragging. Coalesce updates to avoid dozens of overlapping native resizes. Flush pending work before persisting the final value, guard stale completions with revisions, and roll back failed saves.

Scale pet overlays with a common container unit, such as cqw, rather than unrelated fixed pixel values. Clamp bubbles to remain readable while adapting to model size. Physical window dimensions must also follow the scale; adjusting only CSS can clip the character.

Use a few well-defined categories and consistent rows. Place related expression controls in symmetric groups. Keep dangerous/debug-only commands out of ordinary settings; do not display implementation labels in the everyday product UI.
