# Verification and delivery

## Evidence ladder

Record each level separately:

| Level | Evidence | What it cannot establish |
| --- | --- | --- |
| Files | Model references, JSON schema, checksums, compiled source | Appearance or behavior |
| Unit/Core | Semantic mappings, blink curves, parameter behavior | Visible WebGL quality or OS windows |
| Browser | Real WebGL/model rendered and input/extreme poses inspected | Global input, tray, click-through or native placement |
| Native | Packaged target-OS application exercised | Other OS/DPI/monitor cases not exercised |

Do not mark `webglRendered:false`, `windowsDesktopVerified:false` or "saved; verification pending" as complete. If a user tested a target device, attribute that evidence to the user rather than claiming your own test.

## Small meaningful checks

- Input change: separate mouse, keyboard, rapid repeated keyboard and mouse→keyboard transitions.
- Blink/gaze: neutral, eyes closed by expression, blink midpoint and reopen, fast mouse extremes.
- Art: source-reference overlay/crops, all relevant hand extremes, alpha edge on contrasting backgrounds.
- Native UI: startup without desktop click; open/drag menu; settings above pet; bottom/side placement where changed.
- Packaging: build the changed target, inspect version/resources and smoke-launch if the host supports it.

Run broader tests only for new failures, code changes or unresolved risks. Documentation cleanup needs a path/reference check, not a full native rebuild.

On Windows temp-directory ENOENT, use a verified project-local TEMP/TMP for that command. Do not repurpose HOME/CODEX_HOME or disable checks merely because temporary storage failed.

## Version preservation

Keep source commit, editable rig, runtime export, executable/installer, notices and SHA256 together in immutable per-version delivery records. A source model and a runtime repaired model may have separate provenance.

Keep at least the current and previous recoverable versions. Never overwrite historical executables, move tags, force-push or delete old Releases as routine cleanup. Target OS/architecture must be explicit in filenames and release notes; separate Windows and macOS builds.

## 原生验证与用户偏好

输入变更应明确精确构建、测试者、游戏模式与阶段。合成IPC事件可以核对真实EXE/模型参数，但不证明物理输入能穿过游戏或系统权限；菜单/登录界面测试不代表角色控制阶段。

设置验证不能只看源码默认值。记录测试前偏好，在成功与失败路径恢复；核对持久化及当前窗口。用户新要求优先于保存的旧基线，不能将测试误关值恢复成“用户偏好”。

## 安装包与目录校验

```sh
python scripts/verify_delivery.py /path/to/delivery /path/to/delivery/SHA256.json
```

脚本路径相对skill目录。只读支持顶层数组、`files`或`assets`数组，各项包含file、sha256和可选bytes；错误/不一致返回非零。不会生成证书、检查Apple公证或运行程序。SHA256确认文件一致性，不是无漏洞保证。

正式发布之前，对齐：应用/安装包版本、真实源码提交、运行模型入口、可编辑源及运行时补丁来源、许可证、校验清单和用户文档。Windows/macOS分别检查对应平台配置；软件版本与模型版本独立记录。

## 收录别人的平台发行版

1. 读取原Release和精确源码提交，检查目标仓库现状、同名tag/草稿和分支祖先关系。源码可能已通过PR合入，不为“再合并一次”强推远端。
2. 下载原始附件，按上游元数据和清单核对大小/SHA256；保留文件名与原字节。记录贡献者、上游URL、提交、架构、最低系统与签名声明来源。
3. 主机支持时做目标系统实机核验。否则只检查可证明的ZIP CRC、Mach-O/PE、plist/版本、引用和容器结构；明确不能验证新平台运行或签名可信度。
4. 仅在用户已授权发布的仓库创建独立平台Release。标签指向真实平台源码，不能指向Windows当前HEAD再称Mac源码。保留完整历史；分支已有更新先fetch检查，不移动旧tag。
5. 上传前先查现有资产；同名同哈希复用，缺失项续传，已发布附件不同则新版本。写请求超时先查远端状态，不能盲目重试创建。
6. 发布后核对远端资产ID/大小/哈希、公开URL与tag提交，更新版本索引、README、检查点和本地恢复记录。源码、安装包、证据分开保存，避免复制多份大模型。

读取元数据和大附件传输可能走不同的可用网络路径。依据实际错误诊断连接和代理，不将TLS超时归因于文件权限，也不要求用户重新授予已经存在的授权。凭据由gh/连接器管理，不输出到日志或manifest。

## 面向用户的交付

README列主要功能、分平台下载、上手、权限与常见问题，以及用户指定的GitHub/B站链接。源码/缓存/宣传材料和个人日志不混入客户安装包；公共仓库不自动附完整原始聊天或未确认可发布的素材。

最终回复给真实Release及本地文件入口，说明本轮已验证和未验证范围。检查点应写“完成到哪、证据在哪里、下一步是什么”，而不是只说“已保存”。

Before cleaning a repository, inspect references and package scripts. Archive unused candidates/media locally, confirm hashes, then remove only the authorized tracked content with an ordinary commit. Exclude credentials, caches, dependency runtimes, private databases, logs and generated deliveries from source Git.

Final delivery must give actual local artifact links, a concise implemented/verified/pending account and the exact remaining risk. Save a project checkpoint before long builds or usage boundaries.
