# Live2D Desktop Pet Skill

一份从实际桌宠工程总结出的 Codex / AI 编程助手技能：从接手现有项目、原画分层和 Cubism 绑定，到键鼠反馈、原生桌面窗口、设置、验收与版本发布。

目标是制作能日常使用、动作有回应、角色像原图的桌宠，同时明确区分占位素材、可编辑模型、运行时修复、浏览器验证与真正原生验收。

## 内容

技能入口：[SKILL.md](skills/live2d-desktop-pet/SKILL.md)。按任务需要加载下列详解：

| 文档 | 内容 |
| --- | --- |
| [完整施工流程](skills/live2d-desktop-pet/references/workflow-playbook.md) | 接手、垂直切片、原画、绑定、反馈系统、原生窗口、设置、发布与高效推进 |
| [工具与方法](skills/live2d-desktop-pet/references/tools-methods.md) | rg/Git、模型 CLI、Core、Cubism、浏览器、原生 API、电脑操作、权限与磁盘 |
| [分层与绑定](skills/live2d-desktop-pet/references/layering-rigging.md) | 完整遮挡物体、抠图边缘、underpaint、UV 绑定、网格/物理与导出来源 |
| [输入与桌面行为](skills/live2d-desktop-pet/references/runtime-native.md) | 同一手覆盖键盘各区、按压/伸手、眨眼/表情、鼠标联动、窗口焦点/拖拽、连续缩放 |
| [踩坑与高效修正](skills/live2d-desktop-pet/references/mistakes-repairs.md) | 15 类实际问题：身份跑偏、缺角、双手误触发、斗鸡眼、菜单消失、没保存、验收混淆等 |
| [审美指南](skills/live2d-desktop-pet/references/aesthetic-guide.md) | 辨识度、结构、软弹节奏、次级运动、表情语义、iOS/Win11 式秩序和图标 |
| [验收与交付](skills/live2d-desktop-pet/references/release-validation.md) | 证据层级、少而必要的验证、不同 OS、版本留档与清理规则 |
| [长离工程案例](skills/live2d-desktop-pet/references/changli-case-study.md) | 可迁移的模块边界与项目经验；不把角色特定映射当作万能模板 |

附带 [只读工程盘点脚本](skills/live2d-desktop-pet/scripts/inspect_pet.py)，使用 Python 3.9+ 与 Git，无第三方 Python 依赖。脚本只报告文件与 Git，不声称完成视觉或原生验收。

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
```

## 范围与边界

本仓库只含原创工程说明与只读脚本，没有角色贴图、模型、Cubism Core、SDK、程序安装包、收款码、个人机密或宣传视频工具。

技能不会从一张图片自动生成正式 Cubism 绑定。精细原画与网格关键形仍需可编辑源稿、编辑器和实际视觉检查；运行时补丁不能冒称为新的 CMO3 导出。

案例来自 [离火长明](https://github.com/HABAI182/changli-companion)。技术与审美判断按目标项目调整，不保证一套参数适合所有角色，也不复制参考作者素材。

## 许可与版本

MIT，见 [LICENSE](LICENSE)。首版 `v0.1.0`；变更见 [CHANGELOG.md](CHANGELOG.md)。
