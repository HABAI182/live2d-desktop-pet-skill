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

Runtime vertex edits must start from a stable per-frame base, not the previous frame's deformed vertices; otherwise stretching accumulates. If editing a mask drawable outside Core, verify mask invalidation in that Framework version as well. Eye art, clipping and closed-eye semantics are covered in [eye-and-expression.md](eye-and-expression.md).

## 视线、鼠标手与弹性分别调

视线跟随、鼠标手平移和按压共享输入来源，但不是同一输出状态。视线空闲回正不能把手和鼠标拉回中点；手/鼠标共用位移驱动，手指按压另叠加，袖根使用连续权重衔接。

先定义屏幕坐标到角色空间的映射、最大位移和用户幅度乘数，再调大范围。在最大允许设置和斜向极值核对露底、线缆、袖口以及另一只手；不能只在默认滑杆下检查。秧秧的具体像素行程见 [案例](yangyang-case-study.md)，不可跨模型照抄。

视线空闲机可拆为 following → waiting → returning → centered。以真实指针位移更新时间，使用有意义的移动阈值抑制噪声；不要每次收到相同轮询数据都刷新计时。移动检测放在视线目标钳制之前或另存原始坐标，避免范围外移动被误判静止。延迟、幅度和回正开关可配置；重新移动平滑接回，关闭跟随时按产品定义归位。

弹性以短按压下、长按保持、释放回弹与次级余韵组合，冲量有上限、阻尼能收住。真实重按可叠加受控反馈，autorepeat 不新增冲量；帧间隔异常时限制积分步长，避免卡顿后一次飞出。头发、挂饰与鸟从各自根部受驱动，不让所有对象同步整块缩放。参数起调与观感检查见 [aesthetic-guide.md](aesthetic-guide.md)。

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
