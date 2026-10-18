# Live2D Desktop Pet Skill

一份从真实项目总结出的 Codex / AI 助手技能：从角色参考、Q版底稿生图、定稿后的局部修补，到分层补绘、Cubism绑定、键鼠动作、原生窗口、设置与分平台发行。

目标是制作能日常使用、动作有回应、角色像原图的桌宠，同时明确区分占位素材、可编辑模型、运行时修复、浏览器验证与真正原生验收。

当前版本 **v3.2.0**：在长离经验上加入秧秧从单图拆层到独立桌面版本的制作与纠错复盘，重点细化双眼、闭眼与情绪、手袖与白边、透明命中和 EXE 交付。调用名仍为 `$live2d-desktop-pet`。先按任务选择阶段，不在每次小修时加载整套文档。

## 内容

技能入口：[SKILL.md](skills/live2d-desktop-pet/SKILL.md)。按任务需要加载下列详解：

| 文档 | 内容 |
| --- | --- |
| [底稿与精准修图](skills/live2d-desktop-pet/references/image-direction.md) | 不够Q时换结构，认可后保护底图；身份/构图/编辑契约分离 |
| [键盘空间与配列](skills/live2d-desktop-pet/references/keyboard-space.md) | 物理与屏幕镜像、空格方向、完整分区、单手/双手选择 |
| [完整施工流程](skills/live2d-desktop-pet/references/workflow-playbook.md) | 接手、垂直切片、原画、绑定、反馈系统、原生窗口、设置、发布与高效推进 |
| [工具与方法](skills/live2d-desktop-pet/references/tools-methods.md) | rg/Git、模型 CLI、Core、Cubism、浏览器、原生 API、电脑操作、权限与磁盘 |
| [分层与绑定](skills/live2d-desktop-pet/references/layering-rigging.md) | 完整遮挡物体、抠图边缘、underpaint、UV 绑定、网格/物理与导出来源 |
| [双眼与表情专项](skills/live2d-desktop-pet/references/eye-and-expression.md) | 旧眼清理、双眼遮罩、闭眼残框、困倦/脸红语义、瞳色与视线 |
| [输入与动作架构](skills/live2d-desktop-pet/references/runtime-native.md) | 独立通道、冲突motion、眨眼/表情、鼠标联动和手部归属 |
| [长按与游戏排错](skills/live2d-desktop-pet/references/input-and-game.md) | down/repeat/up、同手多键、聚合诊断、鸣潮权限与Mac授权 |
| [窗口与设置](skills/live2d-desktop-pet/references/windows-settings.md) | 原生菜单外点/拖动、冷启动、透明留白、连续缩放与偏好恢复 |
| [踩坑与高效修正](skills/live2d-desktop-pet/references/mistakes-repairs.md) | 28 类问题及最短修正路线，包含原像素保护、眼袖夹带、透明挡点击与分版加载失败 |
| [审美指南](skills/live2d-desktop-pet/references/aesthetic-guide.md) | 辨识度、结构、软弹节奏、次级运动、表情语义、iOS/Win11 式秩序和图标 |
| [验收与交付](skills/live2d-desktop-pet/references/release-validation.md) | 证据层级、少而必要的验证、不同 OS、版本留档与清理规则 |
| [参考图与来源](skills/live2d-desktop-pet/references/source-provenance.md) | 长离起源文字、后续可见样张、玄翎修图经验和缺失像素边界 |
| [秧秧制作与纠错案例](skills/live2d-desktop-pet/references/yangyang-case-study.md) | 阶段顺序、反馈到机制、修复证据与未验收范围，具体偏好不泛化为全角色默认 |

附带3个Python 3.9+助手，无第三方Python依赖：[只读工程盘点](skills/live2d-desktop-pet/scripts/inspect_pet.py)、[键盘SVG/JSON示意](skills/live2d-desktop-pet/scripts/keyboard_layout.py)、[只读发行校验](skills/live2d-desktop-pet/scripts/verify_delivery.py)。盘点有Git时读取跟踪文件，没有Git时可明确指定模型。

提供可填写的[角色与范围契约](skills/live2d-desktop-pet/templates/character-contract.json)、[生图/修图请求](skills/live2d-desktop-pet/templates/image-request.md)、[图层遮挡契约](skills/live2d-desktop-pet/templates/layer-contract.json)。

新增[视觉纠错记录](skills/live2d-desktop-pet/templates/visual-review.md)：按本轮风险对齐修前/修后姿态、保护区、参数和画面证据，保留恢复信息，避免同一反馈反复返工。

## 从一张底稿开始，怎样推进

1. 建立角色身份、构图与当前底图的职责；不够Q时调整头身体量和桌宠形式
2. 确认方向后局部修补，检查键盘透视、手部、眼神和保护区；保存认可版本
3. 补全遮挡的脸、衣服、鼠标、尾羽，准备可动层，再做真实Cubism网格、参数、物理与导出
4. 用明确的手部归属与down/repeat/up驱动模型；程序骨架可在素材制作期间同步推进
5. 完成原生输入、菜单、拖动、设置与持久化；不要让浏览器预览代替系统行为
6. 只验证本轮风险，恢复测试偏好，保留源码/模型来源与分平台版本，持续保存进度

技能不再附带角色案例位图。请提供自己有权使用的底图；历史图片的来源与移出说明见[素材说明](skills/live2d-desktop-pet/assets/ASSET-NOTICE.md)。几何键盘 SVG/JSON 示例继续保留。

## 安装

在 Codex 中请求：

> 使用 skill-installer，从 HABAI182/live2d-desktop-pet-skill 安装 skills/live2d-desktop-pet

也可把 `skills/live2d-desktop-pet` 整个目录复制到 `~/.codex/skills/`；安装后重开会话以加载技能。

通用 skills CLI：

```sh
npx skills add HABAI182/live2d-desktop-pet-skill --skill live2d-desktop-pet
```

## 使用

```text
使用 $live2d-desktop-pet，先读当前工程、AGENTS、Git diff 和最近进度。
不要重复已经完成的工作，继续完成键鼠动作与原生桌面功能。
按用户原图保留角色辨识度，保存候选模型和可恢复检查点。
交付时分别说明文件/Core、浏览器和原生实际验证的范围。
```

```sh
python skills/live2d-desktop-pet/scripts/inspect_pet.py /path/to/project
python skills/live2d-desktop-pet/scripts/inspect_pet.py /path/to/project --model public/models/pet/pet.model3.json
python skills/live2d-desktop-pet/scripts/keyboard_layout.py --view front-facing-pet --output-dir /path/to/new-keyboard-reference
python skills/live2d-desktop-pet/scripts/verify_delivery.py /path/to/delivery /path/to/delivery/SHA256.json
```

查看[脚本生成的正面对坐键盘示例](examples/keyboard-front-facing/keyboard.svg)及其[坐标数据](examples/keyboard-front-facing/keyboard.json)。它是几何参照，不是已画好角色风格的成品贴图。

## 范围与边界

本仓库包含原创工作流说明、3个辅助脚本、模板和键盘几何示例。不包含角色运行贴图包、Cubism模型/Core/SDK、桌宠安装包、收款码、个人机密或宣传视频工具；不把完整原始聊天和未筛选资料直接公开。

技能不会从一张图片自动生成正式 Cubism 绑定。精细原画与网格关键形仍需可编辑源稿、编辑器和实际视觉检查；运行时补丁不能冒称为新的 CMO3 导出。

案例来自 [离火长明](https://github.com/HABAI182/changli-companion)及秧秧玄翎制作过程。技术与审美判断按目标项目调整，不保证一套参数适合所有角色，也不复制参考作者素材。秧秧案例只公开方法；其私有素材与工程不随技能提供。

## 许可与版本

原创代码与说明采用MIT，见[LICENSE](LICENSE)；不附带角色图像或授予角色的额外权利。当前版本 `v3.2.0`，已有标签与发行附件保留。变更见[CHANGELOG.md](CHANGELOG.md)。

脚本检查：`python -m unittest discover -s tests -v` 和 `python tools/check_package.py`。
