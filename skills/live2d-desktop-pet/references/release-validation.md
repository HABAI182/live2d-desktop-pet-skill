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

Keep source commit, editable rig, runtime export, executable/installer, notices and SHA256 recoverable together. Use Release metadata and private archives for detailed records; avoid duplicate handoff and delivery reports in source Git. A source model and a runtime repaired model may have separate provenance.

Keep at least the current and previous recoverable versions. Never overwrite historical executables, move tags or delete old Releases as routine cleanup. When the user explicitly authorizes Git history cleanup, verify a full private mirror before rewriting the authorized branches. Target OS/architecture must be explicit in filenames and release notes; separate Windows and macOS builds.

## 原生验证与用户偏好

输入变更应明确精确构建、测试者、游戏模式与阶段。合成IPC事件可以核对真实EXE/模型参数，但不证明物理输入能穿过游戏或系统权限；菜单/登录界面测试不代表角色控制阶段。

需要用户实测时，先启动确认可见的同一构建与足够长的监听窗口，记录开始/结束时段、进程和聚合事件。收到反馈后先核对是否落在有效时段；过期空日志不是输入失败证据。已记录成功的步骤不让用户无故重做，聚合数据不含原始按键文本。

设置验证不能只看源码默认值。记录测试前偏好，在成功与失败路径恢复；核对持久化及当前窗口。用户新要求优先于保存的旧基线，不能将测试误关值恢复成“用户偏好”。

## 安装包与目录校验

```sh
python scripts/verify_delivery.py /path/to/delivery /path/to/delivery/SHA256.json
```

脚本路径相对skill目录。只读支持顶层数组、`files`或`assets`数组，各项包含file、sha256和可选bytes；错误/不一致返回非零。不会生成证书、检查Apple公证或运行程序。SHA256确认文件一致性，不是无漏洞保证。

正式发布之前，对齐：应用/安装包版本、真实源码提交、运行模型入口、可编辑源及运行时补丁来源、许可证、校验清单和用户文档。Windows/macOS分别检查对应平台配置；软件版本与模型版本独立记录。

## 按用途拆版，避免只改菜单

先写最新功能矩阵：哪些状态和动作属于哪版、允许哪些设置、入口资源、标识、配置和启动项。取消的 VTS/工程商品等不因旧报告仍写着就继续构建；不宣称没验收的面捕能力。免费/付费、数量和价格按当前项目决定。

| 版本方向 | 能力边界与相关验证 |
| --- | --- |
| 静态桌面版 | 固定中性图；独立轻量入口。若承诺无动画/键盘监听，检查未加载 Core/模型、无连续动画循环、原生无全局键盘钩子；桌面拖拽/命中所需鼠标处理可保留 |
| 基础互动版 | 只保留功能矩阵承诺的键鼠、视线与桌面能力；前端隐藏入口和原生拒绝越权动作/偏好同时检查 |
| 表情完整版 | 逐项列清情绪、动作、台词、快捷键；确认可执行及切换，不沿用其他产品数量宣传 |

这是一种用途拆分案例，不要求所有项目都有三版；静态产品明确标注静态，不能包装成正式可动 Live2D。各版需要独立配置/启动项时，确保互不覆盖；卸载或退出也不影响其他版。客户端分版不是在线授权/防破解系统，不夸大保护能力。

每版只打入实际运行资源，用明确清单排除旧模型、PSD/CMO3、开发日志和个人设置。静态包不能因共用 public 目录而顺带携带整套模型和 Core。检查构建输出及实际加载资源，不只看 edition 标记；HTML 入口替换若依赖 Vite，在解析模块前执行，可参照 [transformIndexHtml 的 pre 顺序](https://vite.dev/guide/api-plugin.html#transformindexhtml)。

## 便携 EXE 的实际验证

Tauri 的 `frontendDist` 可以表示目录或 URL：目录相对配置文件解析并嵌入资源，URL 模式不嵌入前端，见 [官方配置](https://v2.tauri.app/reference/config/#frontenddist)。秧秧构建曾把 Windows 绝对路径误解析成 URL；修为相对目录并确认 release 使用内置资源/custom-protocol 后，独立 EXE 才实际显示。不能把这解释成所有绝对路径都必然失败。

停止开发服务器，从独立 EXE 打开，检查页面来源、本地模型/图片、菜单和设置；构建成功而窗口隐身仍是失败。安装程序的 setup.exe 与无需安装的应用 EXE 分开命名；依赖外置目录的程序不能称单文件便携。Windows 的 WebView2 等系统依赖仍需在说明中列出。

版本号对齐 package/lock、Cargo/lock、Tauri 配置、界面及 PE 产品版本中实际使用的字段；模型与补片另外记。已有互动版未变化时不为新增静态版重打旧包，优先保留原字节及校验值。

Windows PowerShell 5.1 运行含中文路径的脚本注意编码；用兼容编码或可靠参数传入路径，发现文件时限定到目标版本/版别且要求唯一结果，不能用“第一个 EXE”启动未知包。临时本地诊断端口、测试配置和用户偏好须在退出时恢复，正常启动确认端口关闭。

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

用户要求 EXE 入口时，每次交付直接链接到经存在性核验的本地 EXE 和对应 GitHub EXE 附件，ZIP 可另给备份。文件名标明版本、版别与平台，不能只给文件夹或让用户从一堆附件猜；发布后核对附件原字节/哈希和标签对应的真实提交。私有仓库链接注明访问条件，不能冒称所有人都可下载。

作者的私有 GitHub 备份与买家领取是不同渠道。私有附件不对普通买家可达时，按当前平台能力配置交付入口，不公开仓库令牌或把私有素材搬到公共技能库。用户账号授权、平台认证、原画改编权和角色/IP 发行权分别判断；遇到售卖/申报问题查当时的官方规则，不在技能里固化价格、粉丝数、销量门槛或法律结论。只在已授权范围执行外部发布，结果不明先回查状态。

Before cleaning a repository, inspect references and package scripts. Archive unused candidates/media locally, confirm hashes, then remove only the authorized tracked content with an ordinary commit. Exclude credentials, caches, dependency runtimes, private databases, logs and generated deliveries from source Git.

Final delivery must give actual local artifact links, a concise implemented/verified/pending account and the exact remaining risk. Save a project checkpoint before long builds or usage boundaries.
