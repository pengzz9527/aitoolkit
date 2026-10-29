---
title: 'JetBrains ThinkRail 评测：把 pi 编码 Agent 装进真 IDE，SPEC.md 活文档让意图活过会话'
date: 2026-10-29
tags: ['AI工具', '编码Agent', 'IDE', 'JetBrains', '开源', 'TypeScript', 'Spec', 'MCP']
categories: ['AI 工具评测']
description: 'JetBrains 开源的 agentic IDE ThinkRail 今天登上 GitHub Trending：它把 pi 编码 Agent 包进 Monaco 编辑器、终端和 git worktree 隔离工作区里，SPEC.md 活规格 + 可移植 Agent Skills 让项目知识跨会话存活。本文拆解架构、安装路径、与 Claude Code / Cursor 等同类工具的真实差异。'
---

# JetBrains ThinkRail 评测：把 pi 编码 Agent 装进真 IDE，SPEC.md 活文档让意图活过会话

编码 Agent 的下一轮竞争，不在「谁的回答更好」，而在**Agent 工作完之后，项目里留下了什么**。

单轮聊天工具里，Agent 关掉窗口就失忆：上周的决定、没写完的架构、临时约定，全得从头再说一遍。JetBrains 的 **ThinkRail**（Apache 2.0，5.3k Star，2026-10-29 登上 GitHub Trending 榜首）把赌注押在这个问题上：它不是一个「更花哨的对话框」，而是围绕 [`pi`](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) 编码 Agent 做的一个**轻量真 IDE**——Monaco 编辑器、终端、git 变更标记、worktree 隔离工作区，再加一层被官方称为「living specs」的 `SPEC.md` 规格图，让意图比会话活得久。

## 工具简介

**ThinkRail** 是 JetBrains 孵化器（incubator）项目的 agentic IDE：你在 JetBrains AI 或任意 `pi` 支持的 provider 上跑编码 Agent，但 Agent 不是裸跑在终端里，而是跑在一个「真实 IDE 外壳」里，并且**每次使用都在学习你的项目**。

- **GitHub**：https://github.com/JetBrains/thinkrail
- **官网**：https://thinkrail.ai
- **发布方**：JetBrains（incubator 项目，Apache 2.0）
- **Star**：约 5,336（2026-10-29），当日 GitHub Trending 第 1
- **主语言**：TypeScript（Bun 运行时 + React 19）
- **两种形态**：原生桌面应用（Electrobun）或自包含 `thinkrail` CLI（在浏览器里打开同一套应用），应用状态都在 `~/.thinkrail`
- **引擎**：进程内跑 `pi`——模型、skills、压缩、成本、会话状态全由 `pi` 负责；ThinkRail 自己只管工作区、编辑器和通信协议
- **语言**：内置英文、日语、简中、西语，可放 `en.json` 翻译文件进 `~/.thinkrail/locales` 加语言
- **依赖**：`git` 必须在 PATH；模型走 JetBrains AI 登录或 `pi` 自带认证，**ThinkRail 自己没有账号体系**

## 核心功能

### 1. 隔离工作区：git worktree 当「沙箱单元」

打开任意 git 仓库就是一个 project；从 project 切出来的 workspace 就是标准 `git worktree`，各占一个分支和独立目录。多个 Agent 可以**并行**在不同 worktree 里干活，互不碰你的主 checkout，最后合掉好的分支、删掉其余的。

细节值得注意：

- 已完成或休眠的 workspace 会**自动沉到「shelf」**——对应的 PR 合了/关了，或者一周没动，就会自己收起来，你一回它又复活
- 顶栏实时显示当前分支相对 `origin` 和它那个 PR 的状态，下一步一键完成：push、按 plan / commits / PR 模板 / Agent 草稿开 PR
- PR 开了之后能看到 CI 检查和 review 状态；失败的 check 或 diverged 分支可以直接**交给 Agent 处理**，合并时沿用该仓库上次用过的 merge 方式

这是「多 Agent 并行干活」在开源工具里少数把**收尾流程**（PR、CI、merge、cleanup）闭环做掉的设计。本站评测过的 [Orca](https://198007.xyz/post/2026-10-21-orca/) 也是「多 Agent 同 worktree 编排」路线，但 ThinkRail 把编排收在 JetBrains 官方手里、且 PR 生命周期是一等公民。

### 2. 真 IDE 外壳，不是「聊天窗 + 文件树」

可拆分工作台：Monaco 编辑器多 tab、带实时 git 变更标记和 Changed 视图的文件树、终端、文档，全部限定在激活 workspace 范围内。你可以**锚定在文件和 diff 上写 review 评论，作为结构化上下文送进对话**——等于把「人工 review 意见」变成 Agent 可读的输入。也支持把工作区用你本机已安装的 IDE 打开（ThinkRail 管 Agent，IDE 管编辑，互不替代）。

### 3. Specs as ground truth：`SPEC.md` 活规格图

这是 ThinkRail 名字里「gets better every time you use it」的技术底：代码旁边有一张相互链接的 `SPEC.md` 文件图，Agent 通过专用 `spec_*` 工具读它、搜它、**自己维护它**。意图（intention）于是活过了会话——下个 Agent 会话开场先读 spec 图，而不是靠上下文里塞的聊天记录。

官方自己也是这么开发 ThinkRail 的：`goal-and-requirements.md` 和 `architecture.md` 是 canonical 规格，每个模块旁边挂着 `SPEC.md`，「改到边界、契约或决策，spec 在同一笔变更里同步更新」。Spec-first 不是口号，是它自己写的工程纪律。

### 4. Agent 不止 shell：提问、可视化、MCP 三条外延

- **结构化提问**：Agent 在聊天里发多选/单选题问你，而不是猜。该工具同时以裸 `pi` 包发布：`pi install npm:@thinkrail/pi-ask-user-question`
- **内联可视化**：图表、方案对比、文件预览直接渲染在聊天里；Agent 提 UI 改动时会出 **before/after mockup，可以像 diff 一样逐条评论**。同样有裸包：`pi install npm:@thinkrail/pi-visualize`
- **MCP 服务器**：接 `pi` 的 `mcp.json`（Settings 里可加、可预设）。非只读调用**先在聊天里问你再执行**；仓库自己声明的服务器默认关着，要你批准；OAuth 服务器从 Settings 里登录。信任的工具可以按项目放行

### 5. 模型和凭据全是你自己的

登录 JetBrains AI，或走 `pi` 原生认证接任意 provider；ThinkRail 没有自己的账号。它还会读你已有的 `~/.pi/agent` 配置（skills、mcp.json），想换一份（比如个人版 `~/.pi/agent-personal`）在 Settings → Environment 里指过去即可。

## 适用人群

- **已经在用 `pi` 或 Claude Code / Cursor 编码 Agent、但嫌「裸终端 + 网页 diff」糙的人**：ThinkRail 补的是 IDE 层，Agent 引擎还是 `pi`，你已有的 `~/.pi/agent` 配置直接能用
- **多 Agent 并行改同一仓库的人**：worktree 隔离 + 自动 shelf + PR 生命周期管理，是目前开源工具里闭环最完整的「Agent 工厂」形态之一
- **团队 lead / 架构师**：`SPEC.md` 活规格图是给人看的文档资产，review 评论能当结构化上下文喂 Agent——规格既是给 Agent 的指令，也是给人的真相来源
- **JetBrains 生态重度用户**：官方孵化器项目，Windows 构建有 JetBrains 签名；不过它不是 IntelliJ 插件，是独立应用
- **想给终端版 `pi` 加装备的人**：两个工具包（question / visualize）对裸 `pi` 也可安装使用，不用整个换 IDE

**不太适合**：想要「IDE 全家桶」（重构、调试器、数据库工具那种 JetBrains 全家桶手感）的人——它是轻量 workbench，不替代 IntelliJ 产品线；想「一个界面跑所有 Agent 引擎（Codex、Claude、Grok）」的人——本站的 [OpenBot](https://github.com/nightly-labs/openbot)（同 Trending）路线更宽，ThinkRail 是单引擎深壳。

## 与同类工具对比

| 维度 | ThinkRail | Claude Code / Codex CLI | Cursor / Windsurf | Orca（本站 10-21） |
|------|-----------|-------------------------|-------------------|--------------------|
| 出品 | JetBrains（incubator，Apache 2.0） | Anthropic / OpenAI | 商业 | 商业/开源 |
| Agent 引擎 | `pi`（固定） | 自研 | 自研（内嵌多模型） | 多 Agent 统一编排 |
| IDE 形态 | **真 workbench（Monaco + 终端 + git）** | 纯终端 | 全功能 IDE | 编排层（非完整 IDE） |
| 隔离 | **git worktree workspace + 自动 shelf** | git worktree（手动） | 分支 | worktree 编排 |
| 跨会话记忆 | **SPEC.md 活规格图 + Agent Skills** | CLAUDE.md / AGENTS.md 静态文件 | 代码库索引 | 任务队列 |
| MCP | 支持，按项目信任模型 | 支持 | 支持 | 支持 |
| PR 生命周期 | **CI 状态 + review + Agent 处理失败 check + 一键 merge** | 弱 | 弱 | 弱 |
| 多 Agent 并行 | 每 workspace 多 `pi` 会话 | 手动多开 | 手动多开 | 核心卖点 |
| 凭据 | 你的 provider，无自家账号 | 订阅 | 订阅 | 订阅 |
| 适合 | 想要「Agent + IDE + 规格」闭环的个人和团队 | 终端工作流信徒 | 全功能 IDE 用户 | 多 Agent 编排重用户 |

**怎么选**：已经深度用 Claude Code / Codex CLI，终端工作流够用，不用换；想要「Agent 干活时旁边有真的编辑器、diff 和终端」，ThinkRail 是目前开源里完成度最高的选项；想要多引擎（Codex + Claude + Grok 同屏），看 OpenBot；把 Orca 的编排、ThinkRail 的规格、Claude Code 的终端手感叠起来用，也是真实可行的组合。

## 如何使用

### 第 1 步：安装 CLI（macOS / Linux / Git Bash）

```bash
curl -fsSL https://raw.githubusercontent.com/JetBrains/thinkrail/main/install.sh | bash
```

Windows（cmd / PowerShell）：

```powershell
powershell -c "irm https://raw.githubusercontent.com/JetBrains/thinkrail/main/install.ps1 | iex"
```

桌面版则去 [releases 页](https://github.com/JetBrains/thinkrail/releases) 下 `thinkrail-desktop-*` 资产。Linux 桌面构建需要 glibc 2.38+ 和 GTK3/WebKit：

```bash
sudo apt install libgtk-3-0 libwebkit2gtk-4.1-0 libayatana-appindicator3-1 librsvg2-2
```

### 第 2 步：跑起来，选项目

```bash
thinkrail ~/code/my-repo
```

首次启动会引导你连 provider（JetBrains AI 登录或 `pi` 自带认证）并选项目；没有现成仓库可以点「Start a new project」在 `~/thinkrail` 下建一个，或「Add project → Clone repository…」直接 clone。需要 `git` 在 PATH。

### 第 3 步：开 workspace，让 Agent 并行干活

1. 从 project 切一个 worktree workspace（每个 workspace 独立分支 + 目录）
2. 在 workspace 里开多个 `pi` 会话，各配各的模型，实时 token 和成本读数可见
3. 中途可以转向当前 turn、排队后续指令、委派给 subagent；共享的 plan 由 Agent 更新、你来编辑，每步完成可单独 commit review
4. 在 diff 上锚定写 review 评论 → 一键送进对话当结构化上下文

### 第 4 步：维护规格，让意图存活

1. 在 project 里建 `SPEC.md` 图（官方开发自己的 ThinkRail 也是这么做的）
2. Agent 通过 `spec_*` 工具读写，你随时可在 Specs 面板看整张图渲染成的树
3. 纪律：**改边界/契约/决策时，spec 和代码在同一笔变更里一起改**——这是它「越用越懂你项目」的前提

### 第 5 步：接上 MCP 和外挂

- `pi` 的 `mcp.json` 直接生效；Settings 里可加服务器或预设
- 非只读 MCP 调用会在聊天里先问你；仓库自带的服务器默认关闭，批准后才开
- 终端版 `pi` 想加同款装备：

```bash
pi install npm:@thinkrail/pi-ask-user-question
pi install npm:@thinkrail/pi-visualize
```

### 第 6 步：PR 收尾

顶栏看分支相对 `origin` 和 PR 的状态 → 一键 push / 开 PR（用 plan、commits、你的 PR 模板或 Agent 草稿写描述）→ PR 里看 CI 和 review → 失败的 check 或 diverged 分支**直接交给 Agent** → 按仓库上次方式 merge，或重开 / 删远程分支。

## 局限与注意事项

1. **JetBrains incubator 项目，不是正式产品线**：孵化器徽章意味着它可能改名字、改方向甚至砍掉，关键流程别全押在上面；桌面构建更新机制也只在携带有效 HTTPS feed identity 的包上出现
2. **Linux 构建无签名**：Windows CLI / 桌面可执行是 JetBrains 签名的，macOS CLI 签名但未公证，Linux 全部无签名——企业环境要自己过签名策略
3. **引擎单一**：只跑 `pi`。你习惯的 Claude Code / Codex CLI 会话不能直接搬过来（共享的是 `~/.pi/agent` 配置，不是各自的历史会话）
4. **有使用分析**：基础事件（启动、建会话、发消息、连 provider）绑定随机安装 ID，明确不含 prompt / 代码 / 文件 / 凭据；「Share additional usage data」默认是引导你开的，不需要就在 Settings → Privacy 关掉，CLI 也能 `thinkrail --no-analytics`
5. **规格的价值取决于纪律**：`SPEC.md` 是活文档，没有「改了代码忘了改 spec」的自动护栏——这是它最容易被团队用成「又一份过期文档」的点
6. **桌面应用依赖重**：Linux 要装一堆 GTK/WebKit 库，且是 setup tarball 手动装法，和 `thinkrail` CLI 的轻不是一回事

## 总结

**推荐指数：★★★★☆（4/5）**

ThinkRail 的判断很清晰：编码 Agent 的竞争下半场是「**Agent 干完活，项目里留下什么**」。它的答案是三层——worktree 隔离工作区（干的活可控可并行）、SPEC.md 活规格（意图比会话长命）、可移植 Agent Skills（经验跨 Agent 复用）。这三层在开源编码工具里，目前没有同代竞品做得这么完整：Orca 管编排、Claude Code 管终端、Cursor 管全功能 IDE，ThinkRail 管的是「**IDE + 规格 + 规格纪律**」这个组合。

扣的那颗星：incubator 身份（可能变、可能停）、单一 `pi` 引擎（没有多引擎切换）、规格维护靠人肉纪律（没有自动护栏）。

**适合谁**：想要「Agent 干活时手边有真编辑器 + 规格文档」的个人开发者和小团队、已经用 `pi` 且想让它住进 IDE 的人、以及被「CLAUDE.md 写一次就过期」坑过、想建一套跨会话规格体系的人。装之前把「incubator」三个字的含义想清楚再上车。
