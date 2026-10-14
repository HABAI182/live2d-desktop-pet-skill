---
name: live2d-desktop-pet
description: 从参考图与 Q 版底稿设计、局部修图、遮挡补全和 Cubism 绑定，到键鼠动作、原生桌面窗口、设置、排错与分平台交付，制作或修复真正的 Live2D 桌宠。适用于 BongoCat 式桌宠和现有 Cubism/Tauri 工程；单张立绘任务只执行图像阶段。排除 ChatGPT Work 宠物和宣传视频制作。
metadata:
  version: "3.1.0"
---

# Q 版 Live2D 桌宠：从底稿到可用软件

先让角色像、结构完整、输入有回应，再增加动态和界面。沿用用户的技术栈和已认可资产；这是一套决策与修复方法，不是强制新建工程的模板。

## 接手与选择当前阶段

读取 AGENTS、Git status/diff、最近提交、进度、实际模型入口及发行索引。建立“需求—现状—证据—下一步”，不重复已完成工作。可运行 `python scripts/inspect_pet.py PROJECT` 做只读盘点；非 Git 工程用 `--model` 明确入口。命令中的脚本路径以本 skill 目录为基准。

| 用户任务 | 先读 | 本轮产物 |
| --- | --- | --- |
| 没有底稿、还不够 Q、像普通半身插画 | [生图与局部编辑](references/image-direction.md) | 候选底稿、身份卡、结构对照 |
| 已认可画面，只修键盘/眼睛/头发/袖口 | [生图与局部编辑](references/image-direction.md)、[参考与来源](references/source-provenance.md) | 指定区域修正、锁区对照 |
| 键盘方向、空格、键区与手的落点 | [键盘空间](references/keyboard-space.md) | 几何与输入映射，可生成 SVG/JSON 示意 |
| 抠图、缺角、移动后露洞、Cubism 建模 | [分层与绑定](references/layering-rigging.md) | 补全图层、可编辑源、真实导出 |
| 长按抖动、两手混用、眨眼/视线异常 | [动作架构](references/runtime-native.md)、[输入与游戏排错](references/input-and-game.md) | 正确状态、参数与相关场景证据 |
| 菜单、拖拽、缩放、设置、启动不动 | [原生窗口与设置](references/windows-settings.md) | 打包程序中的真实行为 |
| 新工程全流程或阶段安排 | [施工流程](references/workflow-playbook.md) | 最短可运行切片及分阶段交付 |
| 美术、软弹感、UI 与图标不好看 | [审美指南](references/aesthetic-guide.md) | 可指出变化原因的视觉对照 |
| 打包、GitHub、Mac 移植附件合入 | [验收与发布](references/release-validation.md) | 独立版本、真实来源、校验及恢复记录 |

只加载当前任务需要的文档。工具选择见 [tools-methods.md](references/tools-methods.md)，实际失败和修法见 [mistakes-repairs.md](references/mistakes-repairs.md)。

## 不可混淆的边界

1. 用户最新要求决定范围。探索期可以改变构图；底稿认可后的局部修复保护未授权改变的区域。这不是让每个常规实现选择都再次等批准。
2. 分开记录角色身份参考、构图/动态风格参考和当前编辑底图。案例图不自动成为新项目底稿，更不能把新角色生成成长离或玄翎。
3. 平面图、透明裁片、可编辑分层、CMO3、MOC3 导出、运行时补丁是不同产物。图像或 JSON 工具不能凭空完成真实 Cubism 网格绑定。
4. 手、脸、衣服和鼠标先作为完整对象补齐，再处理遮挡。不要挖掉底层来伪造图层优先级。
5. 先定义物理键区、角色左右手、屏幕左右、导出参数的映射。单手键盘与双手键盘均可，以当前用户指定的归属为准。
6. 真正重新按下可以重新触发弹动；操作系统 autorepeat 只维持长按，不重启头部弹簧、按压周期和 authored motion。浮显重复是独立偏好。
7. 全局输入属于原生层，浏览器事件只做预览。注册成功不等于游戏中仍有事件。OS 权限、工具应用权限、文件权限和 SDK 许可分别诊断。
8. 文件、Core、浏览器、目标系统实机分别验收。不能将参数注入、ZIP 检查或 Windows 上的 Mac 包检查称为真实键鼠/Mac 验收。
9. 少做重复测试，只覆盖变化触及的风险；脚本改过用户开关，结束时恢复并核对持久化和实际可见状态。
10. 每个实质里程碑保存进度、源码/模型来源、证据和下一步。发布对应真实源码并保留旧版；仅向用户授权的目标仓库发布，不上传原始聊天、机密或无关材料。

## 最小执行契约

按需填写 [character-contract.json](templates/character-contract.json) 和 [image-request.md](templates/image-request.md)：角色、操作系统、朝向、身份锚点、底图及参考职责、允许改/保留区、手部归属和具体验收结果。

底稿未齐时，程序可用明确标注的占位资产先跑通加载、一次键盘/鼠标、空闲动作和设置；正式图层和模型必须另过美术与绑定验收门，不要把占位图变成“已完成 Live2D”。

[长离案例](references/changli-case-study.md)包含起稿、单手到双手需求演进、0.7.15 长按与游戏兼容、Mac 收录，以及精细原生美术的未完成边界。[来源说明](references/source-provenance.md)区分原始文字、后续样张与缺失的最早三张图。

结束时给出可打开的本地产物、实现与验证范围、仍有的限制，并保存 [handoff.json](templates/handoff.json) 所示的恢复信息。用户要求完整桌宠时持续推进可做的阶段，不用一张静态图或一个单测代替交付。
