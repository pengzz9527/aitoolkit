---
title: 'agent-desktop 评测：Vercel Labs 出品的 Rust 桌面操作 CLI，不看截图、不挪鼠标，让 Agent 直接读操作系统的无障碍树'
date: 2026-11-05
tags: ['AI工具', 'computer-use', '桌面自动化', '无障碍树', 'MCP', 'Rust', 'Vercel', 'CLI']
categories: ['AI 工具评测']
description: 'agent-desktop 是 Vercel Labs 开源的 computer use 工具，用 macOS AX API、Windows UI Automation、Linux AT-SPI 读取桌面应用的无障碍树并输出 JSON，每个可操作元素带一个 ref。默认 headless，不移动鼠标、不抢焦点；ref 绑定快照，UI 变了就返回 STALE_REF。v1.2.0 刚加入 MCP server。本文拆解它的四层架构、60 个命令、身份验证模型，以及和 browser-use、截图派 computer use 的真实分工。'
---

# agent-desktop 评测：Vercel Labs 出品的 Rust 桌面操作 CLI，不看截图、不挪鼠标，让 Agent 直接读操作系统的无障碍树

让 AI 去操作一个桌面软件，最常见的第一反应是「截图 + 让多模态模型看坐标 + 模拟点击」。这条路能跑通 demo，然后在真实工作里撞墙：分辨率变了坐标就偏，界面渲染慢一拍就点空，弹窗叠上来就直接失灵，而且每一步都要付一次视觉推理的钱。

Vercel Labs 的 **agent-desktop** 走了另一条路：**不问模型「屏幕上这是什么」，而是问操作系统「这个界面里有哪些控件」**。

一句话简介：**agent-desktop 是一个 Rust 写的跨平台 CLI + C 库，把桌面应用的无障碍树读成 JSON，给每个可操作元素分配 ref，Agent 通过 ref 点击和输入——没有截图，没有像素匹配，也不自带模型。**

- **GitHub**：https://github.com/vercel-labs/agent-desktop
- **文档**：https://agent-browser.dev/desktop
- **协议**：Apache 2.0
- **画像**：Star 15,618 / Fork 1,087 / 创建于 2026-02-19 / 最新版 v1.2.0（2026-11-05）
- **npm**：`agent-desktop`，月下载约 3.1 万次，已发 48 个版本
- **技术栈**：Rust（CLI + core + 三个平台 crate），发布物同时包含 C 库 `libagent_desktop_ffi`

---

## 核心功能

### 1. 用无障碍树代替截图：每个控件一个 ref

`snapshot` 读取目标应用的整棵无障碍树，把它序列化成 JSON，每个「可操作或可下钻」的节点带一个 ref：

```bash
agent-desktop snapshot --app Finder -i
```

返回的骨架大致是这样：

```json
{
  "version": "2.6",
  "ok": true,
  "command": "snapshot",
  "data": {
    "app": "Finder",
    "snapshot_id": "s8f3k2p9",
    "ref_count": 59,
    "complete": true,
    "tree": {
      "role": "window",
      "name": "Downloads",
      "children": [
        { "role": "treeitem", "name": "Documents", "ref_id": "@s8f3k2p9:e8", "available_actions": ["Click"] }
      ]
    }
  }
}
```

这里有几个设计细节值得注意：

- **ref 是「快照限定」的。** 完整形式是 `@<snapshot_id>:eN`，裸写 `@e8` 会直接报 `INVALID_ARGS`。这是刻意的——不允许一个没有出处的 ref 被当成全局 ID 用。
- **不是所有节点都有 ref。** 只有角色属于那 18 种交互控件（button、textfield、checkbox、link、menuitem、tab、slider、combobox、treeitem、cell、radiobutton、incrementor、menubutton、switch、colorwell、dockitem、listbox、option），或者自己声明了主操作的元素才会拿到 ref。焦点、右键菜单、滚动到可见区这类「几乎所有节点都有的」能力不算数——否则 Web 套壳应用的每个 div 都会变成可点击目标。
- **给 Agent 的是语义，不是像素。** `{ "role": "treeitem", "name": "Documents" }` 对一个 LLM 来说比「坐标 (173, 412) 处有灰色图标」好理解得多，也便宜得多：一次 snapshot 是纯 CPU 的树遍历，不需要多模态推理。

### 2. 默认 headless：不挪鼠标、不抢焦点

这是 agent-desktop 和大多数 computer use 工具最实用的差别。

ref 动作走的是**无障碍 API 的语义调用**（macOS 的 `AXAction`、Windows 的 UIA pattern、Linux 的 AT-SPI Action），不是合成鼠标事件。也就是说：

- 光标不动，你可以同时用这台机器干别的；
- 目标窗口不需要被切到前台，后台窗口照样能操作；
- 多窗口并排时不会因为「点谁谁置顶」而互相打架。

需要真实输入时（比如某些只认物理事件的控件、或者要在 Wayland 下驱动指针），加全局 `--headed` 才会走物理输入，并且会先拿一个全局的**交互租约（interaction lease）**——机器范围内同一时刻只允许一个进程派发合成输入，避免两个并行 Agent 的点击交织成灾难。

### 3. ref 身份验证：UI 变了就拒绝，而不是点错地方

这是整套设计里最「工程」、也最容易被低估的部分。

每个 ref 在快照时都会记录一份**捕获证据**：角色 + 所有稳定字段（原生 id、稳定的 name 和 description）。真正执行动作前，工具会在当前活的窗口上重新统计这个谓词，必须**恰好命中唯一一个元素**才放行：

| 命中情况 | 返回 |
| --- | --- |
| 恰好 1 个 | 执行 |
| 0 个 | `STALE_REF`，去重新 snapshot |
| ≥ 2 个 | `AMBIGUOUS_TARGET`，带上候选窗口 id |
| 快照时就不唯一 | 读取都不读，直接拒绝 |
| 字段读不出来 | 记为 Unknown，**不当作匹配** |

规则里有两条很硬的约束：

- **值和位置永远不算身份。** 输入框里的文本是会变的，你不能因为文本框内容一样就认为还是那个控件。
- **读不完整的窗口证明不了任何东西。** 如果一个窗口没能被完整读取（比如滚出可视区的列表、超时的部分快照），它产出的 ref 会被拒绝，而不是拿去和一个更窄的树做比对。

这一层的意思很明确：**宁可失败，不要点错。** 对一个要替你点「删除」「确认转账」「发送邮件」的 Agent 来说，返回一个可恢复的 `STALE_REF` 远比点错按钮便宜。

### 4. 60 个命令，覆盖真干活的场景

不只是「点一下」。命令分十组：

| 分组 | 命令 |
| --- | --- |
| 观察 | `snapshot`、`find`、`get`、`is`、`screenshot`、`list-surfaces` |
| 操作 ref | `click`、`double-click`、`right-click`、`type`、`set-value`、`clear`、`focus`、`select`、`toggle`、`check`、`expand`、`scroll`、`scroll-to` |
| 键盘鼠标 | `press`、`hover`、`drag`、`mouse-move`、`mouse-click`、`mouse-wheel` |
| 应用与窗口 | `launch`、`close-app`、`list-apps`、`list-windows`、`focus-window`、`resize-window`、`move-window`、`minimize`、`maximize` |
| 通知 | `list-notifications`、`dismiss-notification`、`notification-action` |
| 剪贴板 | `clipboard-get`、`clipboard-set`、`clipboard-clear` |
| 等待 | `wait` |
| 会话 | `session`、`trace`、`cursor-overlay` |
| 系统 | `status`、`permissions`、`version`、`batch`、`skills` |

其中几个不是「凑数」的：

- **`--stdin`**：`type`、`set-value`、`clipboard-set` 可以从管道读文本，敏感内容不会出现在进程参数里。文档明确建议把含密码的步骤拆成独立命令，别放进 batch。
- **`close-app` 有保护名单**：会拒绝关闭操作系统会话关键进程（例如 Windows 的 `explorer.exe`），匹配是精确的进程名/包名，不是子串，避免关掉一个名字里恰好含 `explorer` 的应用。
- **`trace`**：会话里每个进程写一个 append-only JSONL，`trace show` / `trace export` 能合并成一条时间线，用来复盘「Agent 到底干了什么」。注意 trace 可以带截图和 refmap 副本，属于未脱敏证据。
- **`skills get desktop` / `skills get platform`**：二进制里直接内嵌了「教 Agent 怎么用我」的指南，按当前版本和当前操作系统生成。这个思路很聪明——工具自己带说明书，不怕模型知识过时。

### 5. v1.2.0 刚加的 MCP server

今天的这个版本最大的变化是 `agent-desktop mcp`：

```bash
agent-desktop mcp   # 以 stdio 暴露 MCP，每个 CLI 命令对应一个工具
```

CLI 的每个叶子命令都变成一个 MCP 工具（`desktop_snapshot`、`desktop_click`、`desktop_session_start`……），参数 schema 直接来自命令定义，返回值就是那个 JSON envelope。接进任何 MCP 客户端：

```json
{
  "mcpServers": {
    "agent-desktop": { "command": "agent-desktop", "args": ["mcp"] }
  }
}
```

这意味着在此之前你需要自己写一层「让 Claude Code / Cursor 会调这个 CLI」的胶水，现在一行配置就够。考虑到这是它今天冲上 trending 的直接原因，这个功能的实际价值可能比参数列表看起来更大。

---

## 它是怎么实现的

四层，边界很干净：

```text
你的 Agent
   │  CLI 调用（每命令一个 JSON envelope）  或  C 库（进程内）
   ▼
agent-desktop-core   ← 平台无关：快照、refmap、身份复核、命令语义
   │  PlatformAdapter trait
   ▼
平台 crate（编译期三选一）
   ├─ macOS   → AX API
   ├─ Windows → UI Automation
   └─ Linux   → AT-SPI
```

**核心层不认识任何操作系统**，平台适配器只负责把各自的 UI 分类体系映射到一套核心拥有的封闭词汇表（role、state、capability）。比如 UIA 的 `Tab` 是容器、`TabItem` 才是页签，正好和 ARIA 的命名相反——这类坑被收在适配器里，core 不用管。

还有一个细节能看出作者的较真程度：**证据是三态的**（`Known` / `Absent` / `Unknown`），而且永远不塌缩成两态。

> `Absent` 是一个答案：问过了，平台确实没有这个属性。`Unknown` 是没有答案：读取失败，或者读回来的值不可信。

`Absent` 可以满足「完整性」门槛，`Unknown` 绝对不能。反过来，角色、状态、可用操作只有在平台**正面声明**时才授予。所以「读失败」不会被误当成「不支持」，也不会被当成「支持」。

---

## 三平台支持与权限

| 平台 | 最低要求 | 无障碍 API | 主要门槛 |
| --- | --- | --- | --- |
| macOS | macOS 13+，Intel / Apple Silicon | AX API | 辅助功能权限；截图另需屏幕录制 |
| Windows | Windows 10 1809+，x64 / ARM64 | UI Automation | 无需授权；但二进制未签名，Smart App Control 会拦 |
| Linux | Ubuntu 24.04+，glibc 2.35+，X11 / Wayland | AT-SPI | 必须在用户的图形会话里跑，TTY / SSH / 容器里看不到任何应用 |

几个必须提前知道的坑：

- **macOS**：`agent-desktop permissions --guide` 会打开系统设置并给出图文指引，比自己在设置里翻三层快得多。
- **Windows**：干净安装的 Windows 11 上 **Smart App Control 会直接拦截**，官方说法很坦白——「没有任何下载方式或启动方式能绕过」，只能关掉。通过 npm 安装不会触发 SmartScreen。
- **Linux**：需要 `at-spi2-core`；X11 下键盘输入要 XTEST，Wayland 下要 GNOME Mutter RemoteDesktop，剪贴板要 `wl-clipboard`。Wayland 下应用指针输入会返回 `ACTION_NOT_SUPPORTED`，原生窗口的窗口控制会被拒绝。**Linux 支持是 1.0.0（10 月 27 日）才加的**，比 macOS / Windows 年轻得多，预期它最先出问题。

`agent-desktop status` 可以一次性告诉你：当前平台、权限状态、以及这个系统上支持哪些 surface。**如果 `supported_surfaces` 是空列表，说明无障碍总线没应答**，先把会话环境搞对再排查别的。

---

## 和同类工具对比

先划清赛道，因为这个领域经常被混为一谈。

| 工具 | 操作对象 | 感知方式 | 是否内置模型 | 形态 |
| --- | --- | --- | --- | --- |
| **agent-desktop** | **桌面应用** | **OS 无障碍树** | **无** | CLI / C 库 / MCP |
| browser-use（120k Stars，MIT） | 网页 | 浏览器 DOM + 可选截图 | 有（Python 库） | Python 库 |
| agent-browser（Vercel，同门） | 网页 | 浏览器 DOM | 无 | CLI |
| browser-tools-mcp（7.3k Stars） | 浏览器日志 / 调试 | DevTools 协议 | 无 | MCP server |
| 截图派 computer use（各家 GUI Agent） | 整屏像素 | 截图 + 坐标回归 | 有（多模态） | 各家的端到端 Agent |

**和 browser-use 的关系是互补，不是竞争。** browser-use 解决的是「让 Agent 上网操作」，它有自己的一套浏览器和模型接入；agent-desktop 明确说「它不自动化网页，网页请用 agent-browser」。你要做的是把 Gmail 网页版里的一封邮件另存到本地的 Keynote 里——这两件事正好需要两把不同的工具。

**和截图派的根本差别在「失败模式」。** 截图派的失败是**静默的**：坐标偏 8 个像素，点到了隔壁按钮，模型看到画面变了还以为成功了。agent-desktop 的失败是**显式的**：元素不在了就 `STALE_REF`，匹配到两个就 `AMBIGUOUS_TARGET`，每个错误都带 `disposition.retry` 告诉你重试是否安全。对一个要跑在别人电脑上的自动化流程，这个差别比「准确率 92% vs 88%」重要得多。

**它的代价也很清楚**：应用如果根本没实现无障碍，agent-desktop 就**看不见它**。自绘 UI 的软件、游戏、部分 Electron 应用（虽然有 Web Wrapper 跳过逻辑，能过滤掉一层层匿名容器）都会退化。截图派在这种场景下至少还能「看着点」。

---

## 如何使用

### 第一步：安装

```bash
npm install -g agent-desktop
agent-desktop version
```

需要 Node 18+。npm 包内置了 macOS / Windows / Linux、x64 / ARM64 的原生二进制和平台 helper。macOS 和 Linux 也可以用 Homebrew：

```bash
brew install agent-desktop
```

> **注意 npm 12 默认会拦截 install scripts。** 被拦下时每次调用会多走一层 Node launcher，额外约 125 ms，终端会打一次提示。要恢复原生性能：
> ```bash
> npm install -g agent-desktop --allow-scripts=agent-desktop
> ```

### 第二步：检查环境与授权

```bash
agent-desktop status              # 平台、权限、支持的 surface
agent-desktop permissions --guide # macOS：带你走一遍辅助功能授权
```

macOS 上第一次用一定要跑 `--guide`，否则你会得到一堆权限报错而不知道去哪点。

### 第三步：跑通「观察 → 操作 → 再观察」的闭环

```bash
agent-desktop snapshot --app Finder -i      # 只看可交互元素，每个带 ref
agent-desktop click @s8f3k2p9:e8            # 用刚才快照里的 ref 点击
agent-desktop snapshot --app Finder -i      # 重新观察，确认结果
```

这三行就是全部的心智模型：**工具不替你决定下一步，循环在你的 Agent 里。**

### 第四步：把 ref 交给你的 Agent

两种方式，按你的技术栈选：

**方式 A：MCP（推荐，v1.2.0+）**

```json
{
  "mcpServers": {
    "agent-desktop": { "command": "agent-desktop", "args": ["mcp"] }
  }
}
```

**方式 B：Skill / AGENTS.md**

```bash
npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop
```

或在 `AGENTS.md` 里加一句：

```markdown
Use `agent-desktop` to see and operate desktop apps. Before the first use, run
`agent-desktop skills get desktop` and `agent-desktop skills get platform`, and follow them.
```

**方式 C：C 库（进程内，零启动开销）**

每次 release 都附带 `libagent_desktop_ffi`，Python 用 `ctypes` 就能加载：

```python
import ctypes
lib = ctypes.CDLL("./lib/libagent_desktop_ffi.dylib")
lib.ad_adapter_create.restype = ctypes.c_void_p
assert lib.ad_init(7) == 0   # 主版本号要和 header 里的 AD_ABI_VERSION_MAJOR 对上
```

> 注意 1.1.0 起 C ABI 主版本是 7，而且 `ad_resolve_element_exact` 这类直接传元素句柄的入口被永久禁用了——**C 调用方无法提供 ref 所需的捕获证据**，只能走快照 ref。这是安全模型的必然结果，不是 bug。

### 第五步：处理密集界面

Slack、Figma 这类界面，一次全量 snapshot 会非常大。文档给的路子是**先看骨架，再下钻**：

```bash
agent-desktop snapshot --skeleton --app Slack -i --compact
agent-desktop snapshot --root @s8f3k2p9:e3 -i --compact
```

`--skeleton` 只给结构，`--root` 从某个 ref 往下读。这样做还有一个额外好处：下钻得到的 ref 仍然是按**整个窗口**计数和验证的，不会因为「只看了局部」而放松身份复核。

### 第六步：上生产前

```bash
agent-desktop session start --name "daily-report"
# 之后每条命令带 --session，或设 AGENT_DESKTOP_SESSION
agent-desktop trace show
```

会话把 refmap、trace、manifest 收在 `~/.agent-desktop/sessions/<id>/` 下，出了问题能回放时间线。**但记住 trace 里可能有截图和剪贴板内容**，别把 `~/.agent-desktop/` 打进公开日志、CI artifact 或者 issue 附件。

---

## 几个需要留意的地方

**它不是一个 Agent，是一个 Agent 的手。** README 写得很清楚：「没有模型在里面，循环在你的 Agent 里」。这意味着**能力上限取决于调用它的模型**——模型不会用 ref、不会读错误码、不会在 `STALE_REF` 之后重新快照，工具再好也没用。好在 `skills get` 内嵌指南和结构化的错误码已经把这部分门槛压得很低了。

**版本号小，但语义变更不少。** 0.10.0 移除裸 `@eN`，1.1.0 把 C ABI 推到 7 并收紧 `AMBIGUOUS_TARGET` 的判定，envelope 升到 2.6。**这些都不是「修 bug」，是会让你现有脚本行为变化的变更。** 绑定版本，读 CHANGELOG 再升级。

**166 个 open issue。** 对一个今年 2 月才建、四个月发到 1.2.0 的项目来说很正常，但也说明边界情况还在收口——尤其是三个平台各自的无障碍实现差异巨大，某个具体应用的某个具体控件出问题，是大概率会遇到的。

**隐私面的风险是真实的。** snapshot 会读到你整个窗口的界面文本，包括不该出现的东西。README 第一段就在提醒这件事。我的建议：在专用用户账号或虚拟机里跑，别在存着客户数据的日常账号上直接放开。

**网页场景它不管。** 想用它点网页是走错门了，去用 agent-browser 或 browser-use。

---

## 总结

| 维度 | 评价 |
| --- | --- |
| **创新性** | ★★★★☆ 无障碍树做 computer use 不是首创，但把身份验证做到这个严谨程度的不多见 |
| **实用性** | ★★★★☆ 桌面重复劳动、后台批处理、跨应用搬运，正好是截图派最难受的场景 |
| **工程质量** | ★★★★★ 三态证据模型、快照限定 ref、交互租约、C ABI 版本化，看得出是大厂 lab 的底子 |
| **文档** | ★★★★★ CONCEPTS.md 写得像论文，FAQ / install / json-output 覆盖到权限和坑位 |
| **上手难度** | ★★★☆☆ 装和跑三分钟，调权限和调 Agent 的循环要半天 |
| **推荐指数** | **★★★★☆（4.5/5）** |

`agent-desktop` 最聪明的地方，是它承认了「操作电脑」这件事真正的难点不在识别，而在**确认**。多模态模型已经能看懂屏幕了，但它们不知道自己点的是不是想点的那个东西。agent-desktop 把「我看到的这个元素，现在还是那个元素吗」变成了每一步都要回答的问题，答不出来就拒绝执行。

这份克制让它的功能和同类看起来偏少——没有内置 Agent、没有模型、不碰网页、Wayland 下能力还打折。但换来的是一个可以放心交给 Agent 去点的桌面：它要么做对，要么明确告诉你它做不到。

如果你正在给团队搭「AI 帮我处理这些重复的桌面流程」的东西，而这条路你已经用截图 + 坐标试过一轮并放弃了，那 agent-desktop 值得一个下午。如果你只是想让 AI 帮你点一下网页上的按钮——出门左转，这不是你要的工具。

- **GitHub**：https://github.com/vercel-labs/agent-desktop
- **文档**：https://agent-browser.dev/desktop
- **最快上手**：`npm i -g agent-desktop && agent-desktop status`
- **给 Agent 装 Skill**：`npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop`
