# Layering and rigging

## Inventory before edits

Find the active `.model3.json`, moc3, texture atlas, physics, expressions and motions. Validate every referenced file. Prefer `cli-anything-live2d inspect/validate/deps/manifest --json` if installed; use `--help` to confirm syntax. Its edit operations can adjust JSON references and parameter presets, but do not replace mesh/deformer authoring in Cubism Editor.

Create a dated candidate and checksum inventory. Keep the last working editable rig and its runtime export together. Record the Cubism/Core versions and required parameter IDs.

## 保留原像素与锁定局部

认可底稿后，先区分问题在源图、裁片、网格、运行时变换还是窗口裁切。画面变窄时，检查画布尺寸、非等比缩放和 object-fit，不能先把脸重画宽；饱和度漂移先查色彩配置与滤镜。补画只覆盖允许的隐藏区/修补区和必要接缝，其他区域保留原像素。

同尺寸对齐基准图，记录本轮允许改动的遮罩与保护区差分。抗锯齿、重采样或色彩转换也可能引入差异，需要说明来源，不能口头宣称“完全没动”。用户只允许极少量修剪发尖时，不扩展到整头发量、脸宽或其他饰品。

## Separate complete objects

Start from a stable base and an occlusion map. A white-background illustration is not a transparent asset, and isolated visible fragments are not complete layers. Keep layer IDs, parent/side/driver, hidden-art coverage, blend/mask and version in an asset contract so the exporter and renderer agree. Adapt [layer-contract.json](../templates/layer-contract.json); this is a planning template, not an official Cubism format.

Typical desk-facing layers, back to front:

1. Rear hair, tails, accessories and body underpaint.
2. Face/skin, ears, eyes, brows and mouth.
3. Clothing, front hair and ornaments.
4. Complete keyboard and complete mouse/cable, placed according to reference perspective.
5. Hands/cuffs above the keyboard/mouse and torso occlusion anchors.
6. Phoenix and foreground effects as appropriate for the original composition.

Ordering is reference-dependent. Preserve unrelated drawables and mask relationships when moving a hand ahead of the torso.

## 常规角色的可动分层

生图或绘制前按动作选择下列结构；左右以角色自身为准，并与画面方向对应。独立变形、遮挡或物理摆动的对象分开，同步且不需独立控制的细节可以合并，不强给 Q 版添加长臂或过多碎层。

| 部位 | 常见拆法与完整性 |
| --- | --- |
| 头发与头部 | 后发、侧发、刘海、需要独立摆动的发束；脸底、耳、颈按转头和遮挡需要分开，发下皮肤补完整 |
| 每只眼睛 | 左右眼分别管理；上/下睫毛、完整眼白、虹膜/瞳孔、眼睑按开合与视线方案拆开；高光需要独立运动时另层，眉毛独立；眼白不能只剩虹膜外的可见环 |
| 嘴 | 按口形需求拆上下唇线、口腔；需要露出的牙/舌另层。简单闭口桌宠可简化，但脸底不保留重影嘴线 |
| 身体、衣服与手 | 按关节与遮挡拆躯干、前后衣片、上臂/前臂、手掌、袖口/后袖；手移开后身体与袖根仍完整，按动作决定是否细拆手指 |
| 饰品与配角 | 发饰主体与摆动挂件、缎带分开；鸟/凤凰按实际动作拆身体、翅、尾等，根部有连接余量 |
| 输入设备 | 键盘、完整鼠标、线缆与手分开；设备不带手掌残片，接触阴影按所属对象或独立层处理 |

具体闭眼几何和遮罩策略见 [eye-and-expression.md](eye-and-expression.md)，不要为追求层数拆出没有绘制完整的碎片。

## 从部件到可导入 PSD

保留便于修改的分层美术源，再另存导入用 PSD：每个可动部件占独立层，把该部件内部的线稿、填色、效果和图层蒙版按需要合并或应用，保留部件之间的分离。名称唯一，组装时使用统一画布与原始坐标，不整体合并角色。

按官方[PSD 注意事项](https://docs.live2d.com/en/cubism-editor-manual/precautions-for-psd-data/)使用 RGB、8 bit/channel、sRGB，并核对目标 Cubism 支持的混合模式。导入后检查各部件是否形成独立对象、位置与叠放是否一致；只有重组预览正确不代表已经完成网格、参数或物理绑定。

## Reconstruct hidden areas

A flattened reference does not contain art behind a hand. Removing the hand alone reveals missing material.

- Complete the mouse body under the hand and move mouse/hand/cable coherently.
- Fill facial/torso areas using matching source skin or fabric, not a flat patch that creates a visible seam.
- Feather internal joins while keeping external contours opaque.
- Inspect alpha halos, stray fragments and missing tail corners at extreme poses, not only neutral.
- Preserve outlines at consistent thickness and color. Avoid unnecessary silhouette expansion; compare against the supplied reference.

For runtime underpaint, bind patch vertices to the native mesh (e.g. barycentric coordinates in UV triangles) so the patch follows head turns and spring deformation. Cache static topology instead of re-searching triangles every frame.

Keep each hand's palm, cuff and rear sleeve separable where motion exposes their joint. Repair the sleeve/torso underneath rather than cutting it out. A long tail or hair repair needs a plausible continuous contour and thickness, not a stretched cropped edge. Inspect clean alpha on both dark and light backgrounds; do not erase the original outline as if it were residue.

## 白边、缺角与手袖的定位顺序

| 检查层 | 典型线索 | 对应处理 |
| --- | --- | --- |
| 原画/裁片 RGBA | 黑底下有白晕，原文件也缺一角 | 区分白底混色与原有白色高光；局部去污染/补轮廓 |
| Atlas/UV/网格 | 原裁片完整，导出后少一角或邻图串色 | 检查裁切、透明留边、UV、网格覆盖与纹理采样 |
| 剪贴/混合 | 只在眼白遮罩边或特定渲染器露色 | 核对 mask、半透明轮廓与 straight/premultiplied-alpha 约定 |
| 运行时/窗口 | 动时缺角、缩放后裁边，源图中性正常 | 查累积形变、组合极值、canvas 与窗口尺寸/布局 |

把可疑区域合成到黑、白、中灰和棋盘格，并看常用桌面尺寸与局部放大。Alpha 灰度图能看透明残片，但不能区分正确的浅色发丝和污染；不要按“接近白色”全图删像素，或统一腐蚀所有边缘。透明像素的颜色、边缘 Alpha 与混合配置要一起检查。

手部裁片先单独显示：掌缘之外是否带着脸、头发、另一只手、长袖外沿或底稿阴影？只让应共同运动的掌部与末端袖口随手；后袖/袖根固定或渐变衔接。先补齐手移开后露出的对象，再检查四区、Space、鼠标 XY 和最大允许弹性叠加；一侧修好不代表另一侧也合格。

缺角先找来源，不能用放大整块头发遮住它。新补发束应接得上原描边、方向与厚度；必要时只做用户允许的极小修剪。眼睛的旧眼清理、遮罩与闭眼结构另见 [eye-and-expression.md](eye-and-expression.md)。

## Rig

Separate front/back hair, ornament pendants, tails/wings, hand presses/reaches, eye openness/gaze, head angle/shape and body breath. Give deformations enough art beneath them to remain filled.

Use small parameter ranges initially, then inspect combined extremes. Test keyboard reach + depth + head bounce + eye gaze together; independent single-parameter checks can miss tears.

Suggested control coverage, adapted to the rig: head angle/translation/soft compression; independent eye openness and shared-target gaze; mouth openness/form; hand press plus lateral/depth reach; hair roots/tips; pendant swing; companion body/wing/tail/flame channels. Put pivots near attachment roots. Mesh density follows deforming boundaries, not a uniform high-poly goal.

Export a real runtime package: model3 points to its actual moc3, textures and optional physics/motions/expressions. Check group/parameter IDs, mask relationships, straight/premultiplied-alpha expectations, drawable ordering and resource disposal in the actual renderer. A manifest that resolves every file still does not prove the model looks correct.

Attach physical secondary motion to stable drivers and tune damping, gravity and delay. The character should settle after input rather than oscillate forever.

## Source truth

A repaired atlas, custom renderer mesh or runtime draw-order override is a runtime repair. It is not a new Cubism Editor export unless the editable project was changed, saved and re-exported successfully. Keep the distinction in the handoff and public delivery notes.

Do not binary-edit proprietary rig formats speculatively. Use the editor/export tools and documented SDK. Preserve provided licenses and third-party notices when packaging Core/runtime libraries.
