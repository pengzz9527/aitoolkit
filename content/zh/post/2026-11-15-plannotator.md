---
title: 'Plannotator 评测：11.3k 星「人回环」审查台，Agent 的计划与代码在浏览器里可视化批注，一键回传'
date: 2026-11-15
tags: ['Plannotator', 'AI 编码 Agent', 'Claude Code', 'Codex', 'Gemini CLI', '计划评审', '代码评审', 'Human-in-the-loop', 'MCP', '开源工具']
categories: ['AI 工具评测']
description: 'Plannotator 是 backnotprop 开源的本地、浏览器端 AI 编码 Agent 审查工作台（Apache-2.0/MIT 双协议，11,300+ 星，GitHub 今日趋势第一）。它通过 hooks 与 plugins 直连 Claude Code、Codex、Gemini CLI 等 Agent：Agent 出计划自动弹出浏览器批注审批，diff 与 GitHub/GitLab PR 可视化评审，还能批注任意 URL/HTML、端到端加密分享、用 Inbox 管多 Agent 任务，并集成 VS Code/Obsidian/Notion。'
---

# Plannotator 评测：11.3k 星「人回环」审查台，Agent 的计划与代码在浏览器里可视化批注，一键回传

**Plannotator**（backnotprop/plannotator）是 2025 年 12 月底开源的一个「人回环」（human-in-the-loop）审查工作台，仓库描述一句话：**"The workspace to stay in the loop and on top of agents - shape, decide, plan, annotate, review code, share with team, and send all feedback to agents with one click."** 它把自己定位成**本地、浏览器端的 Agent 审查界面**——Agent 出计划、出代码、出文档时，自动在你的浏览器里打开一个可视化评审页，你删、插、改、批注，然后一键把结构化反馈发回给 Agent，让它继续干活。

它最近一天涨了 **408 星**，登上 GitHub Trending 榜首，总星标已破 **11,300**（Fork 965+）。这个热度的背后是一个很实际的痛点：Agent 跑得越来越长、越来越「无人驾驶」，人怎么低成本地留在回路里？Plannotator 的答案是——**别在终端里盯着滚字，把评审搬进浏览器，像批 PR 一样批 Agent 的工作。**

- **GitHub 星标**：11,300+（今日 +408，Trending 第一）
- **GitHub 仓库**：https://github.com/backnotprop/plannotator
- **官网**：https://plannotator.ai
- **许可证**：Apache-2.0 / MIT 双协议任选
- **语言**：TypeScript（本地服务 + 浏览器 UI，单文件 HTML hook 产物）
- **支持的 Agent**：Claude Code、Codex、Copilot CLI、Gemini CLI、OpenCode、Kiro、Droid、Amp、DeepSeek Harness、Pi；Inbox 另接 Grok Bot、Muse、Hermes、OpenClaw 等个人助理
- **代码托管**：Git、GitHub、GitLab，另支持 GitButler、Jujutsu（jj）、Perforce（p4）
- **桌面/终端变体**：Plannotator TUI（`brew install plannotator/tap/plannotator-tui`）、Herdr Annotate
- **集成**：VS Code 扩展、Obsidian、Bear、Notion

---

## 核心功能

### 1. 计划评审：Agent 出方案，浏览器批注，批准/驳回结构化回传

这是 Plannotator 的「钩子」所在。Agent 的 plan mode 通过 harness 的 hooks 接好之后，**不需要敲任何命令**：Agent 每产出一个计划，本地服务就读取计划内容并在浏览器里打开评审 UI。你在页面上做四类操作——删除、插入、替换、批注，然后二选一：

- **Approve**：Agent 直接继续实现；
- **Request changes**：你的批注被打包成结构化反馈发回 Agent，Agent 修订后你会看到 **plan diff**（计划改了什么一目了然）。

在 Claude Code 2.1.287+ 上这个流程还不阻塞：Claude 结束当轮，你的决定稍后作为一条消息到达，评审节奏完全由你定。

### 2. 代码评审：本地 diff 和远程 PR 都能批，批完回给 Agent

`/plannotator-review` 打开 diff 视图（文件树 + 并排对比），支持：

```
/plannotator-review                    # 评审未提交的本地改动
/plannotator-review <github-pr-url>    # 评审 GitHub PR
/plannotator-review <gitlab-mr-url>    # 评审 GitLab MR
plannotator review --gitbutler         # 评审 GitButler 工作区
plannotator review --patch-file x.diff # 评审静态 diff 文件
```

你像在 GitHub 上一样给具体代码行留评论、建议改法，评论最终**发回发起评审的 Agent 会话**，让 Agent 自己按你的意见改——评审和修复在同一个回环里完成，而不是「人看完再口头转述给 Agent」。

### 3. 批注万物：文件、文件夹、URL、HTML、Agent 的最后一条回复

```
/plannotator-annotate README.md            # 批注本地 markdown
/plannotator-annotate src/                # 浏览并批注整个文件夹
/plannotator-annotate https://docs.rs/…    # 抓取任意 URL 再批注
/plannotator-annotate report.html --render-html  # 原样渲染 HTML 再批注
/plannotator-last                          # 批注 Agent 上一条回复
```

这意味着它不只是一个「代码工具」：**spec、PRD、竞品页面、Agent 产出的 HTML 原型**都可以拿来批。官方甚至提供了 PRD 模板让你开箱就有一个真实文档可练。

### 4. 端到端加密分享 + 团队工作区

分享计划给同事批注，再导入反馈直接发回你的 Agent：

- **小计划**：全部内容编码进 URL hash，不经过任何服务器；
- **大计划**：走短链服务，但内容是 **AES-256-GCM 在浏览器里先加密**，服务器只存解不开的密文，解密钥匙只存在于分享链接里，7 天后自动删除。

团队协作的主方向是 **Plannotator Workspaces**（托管产品），开源侧的链接分享正在向 Workspaces 迁移（尚未宣布移除时间）。

### 5. Plannotator Inbox：多 Agent 时代的「收件箱」

这是新增的杀手特性，官方称之为**「多 Agent 工作之间缺失的评审层」**：多个 Agent 在后台持续干活，把决定、问题、原型、计划、文件丢进同一个本地收件箱窗口（`plannotator inbox`），你随时打开、点选作答、批注文件、按下发送——回复自动发回**发起询问的那个会话**，不占用任何 Agent 会话的等待时间。对同时挂着几个 Agent 干活的人来说，这等于给「人」配了一个统一任务台。

另外内置 **Ask AI**：评审任何内容时可以把选区丢给配置的模型提问，或发起一次 AI 评审，让 AI 的评论直接贴到 diff 上。

---

## 适用人群

- **重度使用 Claude Code / Codex / Gemini CLI 的工程师**：任务跑长之后最缺的就是「低成本回环」。Plannotator 把「批准计划 / 验收代码 / 纠偏」从终端滚屏里解放出来，浏览器里批注比打字高效得多。
- **带团队评审 Agent 产出的人**：分享 + 批注 + 导入反馈的流程，让非技术同事也能参与「Agent 做了什么、该不该做」的决策，而不必看懂终端输出。
- **同时跑多个 Agent 的人**：Inbox 把散在各会话里的待答问题聚成一处，是名副其实的「多 Agent 前台」。
- **知识工作者**：Obsidian / Notion / Bear 集成 + URL 批注，把它当「带 AI 回传能力的批注器」用也很顺手。
- **GitButler / jj 用户**：这类工具生态里缺的正是配套的评审界面，Plannotator 支持得比较完整。

**不太适合：**

- **只跑短任务、从不进入 plan mode 的用户**：没有计划可批，核心卖点就用不上。
- **不装 Agent 的纯手工开发者**：它的回传机制依赖 hooks/plugins，脱离 Agent 生态只是一个 markdown 批注器。
- **对本地服务有洁癖、零网络容忍的团队**：它默认本地存储、无遥测，但每个评审界面加载时会向 GitHub 检查新版本（不发送任何内容，且暂无关闭开关），`git ls-remote` 远端检查可用 `PLANNOTATOR_GIT_REMOTE_CHECK=0` 关闭。

---

## 与同类工具对比

| 维度 | Plannotator | Claude Code 内置 plan mode | GitHub PR 评审 | open-code-review |
|------|-------------|---------------------------|----------------|------------------|
| 形态 | **浏览器可视化批注台** | 终端内批准/修改 | Web 平台 | LLM 自动评审工具 |
| 谁产出意见 | 人（可叠加 Ask AI） | 人 | 人 | 模型 |
| 意见回传方式 | **结构化反馈直接进 Agent 会话** | 终端确认 | 评论后靠人肉转述 | 评论贴到 diff |
| 覆盖对象 | 计划、diff、PR、URL、HTML、Agent 消息 | 仅计划 | 仅代码变更 | 仅代码变更 |
| 多 Agent 管理 | ✅ Inbox | ❌ | ❌ | ❌ |
| 分享/协作 | ✅ 加密短链 + Workspaces | ❌ | ✅ | 部分 |
| 支持 Agent 数 | **10+ 家** | 仅 Claude Code | 无 | 通用 |
| 部署 | 本地服务，零账号 | 内置 | SaaS | 本地/云 |
| 上手成本 | 低（插件安装即用） | 零 | 零 | 中 |

结论很清晰：**Plannotator 填的是「人 → Agent」这一段空白**。内置 plan mode 只能「同意/打回」，GitHub 评审产出的意见要人肉喂回 Agent，LLM 评审（如 open-code-review）是「机审机」。只有 Plannotator 把**人的视觉批注**变成了 Agent 能直接消费的**结构化指令**，并且横跨十多家 Agent harness——这是它 11k 星的根本原因。

> ⚠️ 三个要留意的点：
> 1. **开源侧的链接分享在弃用边缘**，官方把团队协作用力点放在托管的 Workspaces 上，强依赖「加密短链分享」的团队要留意。
> 2. **Ask AI / URL 抓取会把相关内容发给你在设置里配置的模型提供商**，隐私敏感内容评审前先确认 provider 是本地还是云端。
> 3. **它不替你判断，只替你传话**：批注质量取决于人，Agent 也只是照单执行反馈，别把它当成质量守门员。

---

## 如何使用

### 第一步：安装（按你用的 Agent 选一条）

**Claude Code**（插件市场安装，装完必须重启 Claude Code）：

```
/plugin marketplace add backnotprop/plannotator
/plugin install plannotator@plannotator
```

**Gemini CLI**（要求 0.36.0+；安装器自动检测 `~/.gemini` 并配好 hook）：

```powershell
# Windows PowerShell
irm https://plannotator.ai/install.ps1 | iex
```

macOS/Linux 从 release 下载 `plannotator` 二进制放入 PATH 即可（仓库 227 个 release，更新非常勤）。

**Codex** 无需装斜杠命令，用 `!` 前缀或 skills：`!plannotator review`、`!plannotator last`。

### 第二步：等计划自动弹出

装好后什么都不用做。下次 Agent 进入 plan mode 并产出计划时，Plannotator UI 会自动在浏览器里打开。你批注完毕，**Approve** 让 Agent 继续实现，或 **Request changes** 把意见打回去。Agent 修订后，页面上直接显示 plan diff。

### 第三步：手动触发评审与批注

```
/plannotator-last                 # 批注 Agent 上一条回复（最快的上手方式）
/plannotator-review               # 评审当前未提交改动
/plannotator-review https://github.com/xxx/pull/123   # 评审远端 PR
/plannotator-annotate spec.md     # 批注文档并把反馈发回 Agent
```

### 第四步：团队场景用分享或 Inbox

- 单人/小团队：评审界面点分享，大计划走 AES-256-GCM 加密短链，同事批完后你把他们的反馈导入并发回自己的 Agent；
- 多 Agent 并行：`plannotator inbox` 打开统一收件箱，Agent 通过插件（Claude Code / Pi / OpenCode）或 MCP（`plannotator inbox mcp`）把问题丢进来，你作答后回复自动回到原会话。

### 第五步：把成果沉淀进知识库（可选）

在 Settings 面板配置 Obsidian / Notion / Bear，批准的计划会自动存为带 YAML frontmatter 和反向链接的笔记；VS Code 用户装 `backnotprop.plannotator-webview` 扩展，计划直接开在编辑器 tab 里、diff 可内联查看、批注可从编辑器侧边栏添加。

### 常用 CLI

```bash
plannotator sessions                # 查看当前 Plannotator 会话
plannotator sessions --open 1       # 在浏览器重开第 1 个会话
plannotator archive                 # 只读浏览已保存的计划决定
```

---

## 总结

Plannotator 抓准了 Agent 工作流里最容易被忽略的一环：**「人」正在变成瓶颈**。Agent 的产速远超人的阅读速度，终端里逐字滚屏批准计划、人肉转述评审意见，这套姿势撑不了多久的多 Agent 时代。Plannotator 给出的解法很聪明——不改造 Agent，只在 Agent 和人之间插一个**浏览器批注层**：hooks 负责自动拦截，结构化反馈负责自动回传，Inbox 负责聚合多 Agent，加密分享负责团队协作。11.3k 星、单日 +408、227 个 release 的迭代速度，说明它确实是被需要的那块拼图。

**扣分点：**

- **不替你做判断**：它是传送带不是守门员，批注质量全在你；
- **团队协作用力点在托管 Workspaces**，开源链接分享已标记弃用，强依赖该功能要盯紧路线图；
- **Ask AI / URL 抓取涉及内容外发**，敏感代码要配本地模型 provider；
- **对不用 Agent 的人没有独立价值**；
- 版本迭代极快（227 个 release），API 与配置项可能有滞后。

**推荐指数：⭐⭐⭐⭐☆（4.5/5）**

- **每天用 Claude Code / Codex / Gemini CLI 跑长任务的人** → **强烈建议装**，计划评审是「一次安装永久回环」的投入；
- **带多个 Agent 并行干活的人** → **Inbox 值得一试**，这是目前少见的「多 Agent 前台」；
- **团队需要评审 Agent 产出** → 装起来配合分享/Workspaces 用，但注意开源侧链接分享在弃用；
- **不碰 AI 编码 Agent 的用户** → 不用试，它是回环组件不是独立工具。
