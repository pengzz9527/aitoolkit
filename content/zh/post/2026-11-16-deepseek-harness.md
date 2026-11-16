---
title: 'DSH 评测：DeepSeek 官方 28 万星 Agent Harness，一切皆插件，npx 一条命令跑起 Web 编码智能体'
date: 2026-11-16
tags: ['DeepSeek', 'DeepSeek Harness', 'DSH', 'AI 编码 Agent', 'Agent Harness', 'Cordis', '插件架构', 'MCP', '开源工具']
categories: ['AI 工具评测']
description: 'DeepSeek Harness（dsh）是 DeepSeek 官方开源的 Agent Harness（MIT，28.1 万星，2026-08 创建）。它基于 Cordis 引擎实现了「一切皆插件」架构：Agent 循环、系统提示词、工具、沙箱、UI 面板全部是可组合的 YAML 插件补丁栈，npx @deepseek-ai/dsh web 一条命令即可在浏览器里跑编码 Agent，默认 DeepSeek-V4.1-Flash（1M 上下文），并可挂 42 家模型提供商、MCP 服务与 Skills 生态。'
---

# DSH 评测：DeepSeek 官方 28 万星 Agent Harness，一切皆插件，npx 一条命令跑起 Web 编码智能体

**DeepSeek Harness**（仓库名 `deepseek-harness`，命令名 `dsh`）是 DeepSeek 官方开源的 Agent Harness，仓库描述只有一句话：**"Everything is a Plugin."** 它是 Claude Code / Codex 这类「编码智能体外壳」（harness）的开源对标物——位于模型与终端之间，决定 Agent 怎么读文件、跑命令、和人对话的那一层软件。不同寻常的是，DSH 把**连 Agent 循环本身、系统提示词注册表、工具、上下文压缩、沙箱、UI 面板在内的一切**都做成了插件：一个 profile 就是一叠按顺序生效的 YAML 插件补丁，由 DeepSeek 自研的 **Cordis** 引擎（设计见论文 *A Programming Paradigm for Spatiotemporal Composability*）驱动。

它 2026 年 8 月中旬创建，三个月冲到 GitHub Trending 榜，总星标 **281,505**（Fork 34,803+），一周仍在涨 5,800+ 星，是本周 GitHub AI 工具区的头号项目。

- **GitHub 星标**：281,505+（周增 +5,800 星，Trending 前列）
- **GitHub 仓库**：https://github.com/deepseek-ai/deepseek-harness
- **官网**：https://deepseek.com/harness
- **文档站**：https://deepseek-harness.github.io/deepseek-harness/
- **许可证**：MIT
- **语言**：TypeScript（Node.js CLI/Web 端 + Python SDK）
- **创建时间**：2026-08-13，39 个 release
- **运行要求**：Node.js ^22.19 或 >= 24，pnpm 11
- **默认模型**：DeepSeek-V4.1-Flash（1M 上下文，支持文+图），API 走 Anthropic 兼容协议
- **状态**：官方标注 *developer preview*，**会有破坏性变更**

---

## 核心功能

### 1. 一切皆插件：Agent 循环本身也是插件

这是 DSH 与 Claude Code / Codex 最根本的架构差异。在 DSH 里，**没有一个行为是写死在核心里的**：

- `dsh-system-prompt` 是提示词注册表：各工具插件按数字序号向中央表注册段落，`renderPrompt()` 自动丢弃空段、拼接成最终 system prompt，插件还能挂部署人格前后缀；
- Agent 循环、上下文压缩（compaction）、沙箱、bash/read 等工具、Web UI 面板，全部是 Cordis 引擎上的「插件行」；
- 一个 **profile = 有序的插件包（bundle）列表 + 用户的 `cordis.patch.yml` + 命令行 `--patch` 覆盖层**。改行为不用改代码，加一层 YAML 补丁即可。

这意味着你可以只 fork 不装官方发行包，从最底层重建一个「只带自己想要的行为」的 Agent harness，而 Claude Code / Cursor CLI 这类闭源 harness 只开放到「插件市场」这一层。

### 2. 一条命令跑 Web UI，多入口模式统一

```bash
npx @deepseek-ai/dsh web
```

本地默认在 `http://127.0.0.1:3080` 启动 Web UI 并自动打开浏览器（`--no-open` 可只起服务；SSH 远程启动只打印主机 URL，由 SSH 客户端持有端口转发）。打开后在 **Settings → Models** 里填 DeepSeek API key，直接开 session。调用目录自动成为工作区，官方给的上手任务是 *"Summarize this repository and identify its main packages."*

同一命令族覆盖所有入口模式，profile 自动初始化：

| 命令 | 用途 |
|---|---|
| `dsh web` | 启动 Web UI（`standard` 预设，每会话独立装配 Agent） |
| `dsh headless "job"` | 无界面跑一次持久化会话，打印最终答案后退出（CI/脚本） |
| `dsh acp` | 以 ACP（Agent Client Protocol）stdio 服务自动化客户端 |
| `dsh sdk` / `dsh sdk-minimal` | JSON-RPC stdio 服务 Python/Node SDK 客户端 |

### 3. 模型不锁定：42 家提供商 + 免费模型插件

默认走 `deepseek-official` 路由（DeepSeek-V4.1-Flash，另有 V4-Pro 可选），但基础包同时挂载了 `dsh-llm-pi-ai`，生成的模型目录覆盖 **42 家提供商**——Anthropic、OpenAI、OpenAI Codex、Google、Vertex、Bedrock、OpenRouter、GitHub Copilot、Hugging Face 以及自定义 OpenAI 兼容网关。在 Web UI 的 Models 页面写一段 `llm-pi-ai:` 设置即可切换路由，**harness 与模型彻底解耦**。

社区侧还有一个热插件 `dsh-our-free-model`（7.2 万星，一周 +8,900）：装上即免登录、免注册、免 API key，直接调 DeepSeek V4.1 Flash 和 Kimi K3 这类前沿模型。它由社区维护，使用前务必自行确认其连接方式与信任边界——这是「免费午餐」类插件的常规注意事项。

### 4. MCP、Skills、Hooks 全兼容，旧生态平滑迁移

- **MCP**：`dsh-mcp-client` 支持 stdio 与 Streamable HTTP，一个 server 一行配置，工具以 `mcp__<server>__<tool>` 命名挂载，默认不开启任何 server；
- **Skills**：识别 `SKILL.md` 束或扁平 `.md` 文件，从项目内 `.dsh/skills`、`.agents/skills` 和用户目录 `~/.dsh/skills`、`~/.agents/skills` 自动发现，通过 `skill` 工具加载——**与 Anthropic Skills 生态的目录约定直接互通**；
- **Hooks**：Cordis 事件监听器 + 瀑布流（`agent/pre-step`、`agent/request-error`、`tools/pre-execute` / `tools/post-execute`、`system-prompt/assemble`），实验性包还能直接跑现有的 **Claude Code / Codex 命令钩子**，存量 hook 资产可以平移。

### 5. 插件管理 = pnpm 直通

Profile 里的插件就是 pnpm 包，管理命令把参数原样转发给 pnpm：

```bash
npx -p @deepseek-ai/dsh dsh plugin --profile web add <package>
npx -p @deepseek-ai/dsh dsh plugin --profile web remove <package>
```

`add`、`remove`、`update`、`why` 全部照常工作，插件包在 `package.json` 里声明 `dsh.bundle` 即被收编进该 profile 的 bundle 列表。插件仓库加 `dsh-plugin` topic 即可获得可发现性。

---

## 适用人群

- **DeepSeek 生态的用户**：官方出品，默认路由就是 DeepSeek API，1M 上下文的 V4.1 Flash 开箱即用，比第三方 harness 少一层适配。
- **想「自己造 harness」的工程师**：连 Agent 循环、提示词注册表、沙箱都是插件行，fork 之后可以从任意层重建行为，这是闭源 harness 给不了的空间。
- **多模型 / 多提供商用户**：42 家提供商路由 + OpenAI 兼容自定义网关，harness 不锁模型，切换成本接近零。
- **存量 Claude Code / Codex 用户**：Skills 目录互通、命令钩子可跑，迁移是「加一层配置」而不是「重学一套体系」。
- **CI / 自动化团队**：`dsh headless` + `dsh acp` 提供脚本化与会话自动化入口，Python SDK（wheel 打包同一命令）适合做程序化集成。

**不太适合：**

- **求稳的生产环境用户**：官方明确标注 developer preview，「会有破坏性变更」写在 README 第一屏，生产依赖前先读 `SAFETY.md`；
- **只想要开箱即用、不想碰架构的人**：插件栈 + YAML 补丁的表达力是有学习成本的，「一行 npx」之后仍要理解 profile/patch 机制才能定制；
- **对模型有强制要求（必须 Claude / GPT）且不想配路由的团队**：虽然 42 家提供商都在，但默认体验和文档重心都在 DeepSeek 侧。

---

## 与同类工具对比

| 维度 | DSH (dsh) | Claude Code | Codex CLI | Orca |
|------|-----------|-------------|-----------|------|
| 出品方 | **DeepSeek 官方** | Anthropic（闭源） | OpenAI（闭源） | StablyAI（开源） |
| 形态 | Web UI / 终端 headless / SDK / ACP 多形态 | 终端交互 | 终端交互 | 多 Agent 车队调度 |
| 架构 | **一切皆插件，YAML 补丁栈（Cordis）** | 核心闭源 + 插件市场 | 核心闭源 | Agent 编排层 |
| 默认模型 | DeepSeek-V4.1-Flash（1M ctx） | Claude 系 | GPT 系 | 自带 |
| 换模型 | 42 家提供商一行配置 | 官方渠道 | 官方渠道 | 支持 |
| MCP / Skills / Hooks | **全兼容，可平移存量资产** | 原生 | 原生 | 部分 |
| 许可证 | **MIT** | 闭源 | 闭源 | MIT |
| 成熟度 | developer preview，破坏性变更 | 生产可用 | 生产可用 | 快速迭代 |
| 上手成本 | 中（需懂 profile/patch） | 低 | 低 | 中 |

结论：**DSH 抢的是「harness 这一层」的开源定义权**。Claude Code / Codex 把外壳做成了产品，DSH 把外壳做成了**可拆解的插件系统**——你不仅能在上面装插件，连底座本身都是你的。配合 MIT 协议和官方维护，它等于给「不想被任何厂商的 harness 锁住、又要生产级默认体验」的用户留了一条正路。短板也很直白：developer preview + 破坏性变更，生产环境要盯紧 39 个 release 的迭代节奏。

> ⚠️ 三个要留意的点：
> 1. **官方标注 developer preview，THERE WILL BE COMPATIBILITY-BREAKING CHANGES**，自建插件/补丁层前先读 `SAFETY.md` 与 release notes；
> 2. **免费模型类插件（如 dsh-our-free-model）是社区产物**，免 key 的代价是信任边界不透明，敏感代码仓库里用之前确认其连接链路；
> 3. **默认走 DeepSeek API**，内容外发到 DeepSeek 侧，隐私敏感项目可改用 `dsh-llm-pi-ai` 路由挂本地/自建网关。

---

## 如何使用

### 第一步：环境准备

安装 Node.js（^22.19 或 >= 24）和 pnpm 11，无需克隆仓库。

### 第二步：一条命令启动 Web UI

```bash
npx @deepseek-ai/dsh web
```

浏览器自动打开 `http://127.0.0.1:3080`。SSH 远程场景加 `--no-open` 只起服务并打印主机 URL，端口由 SSH 客户端转发。

### 第三步：配置模型

在 **Settings → Models** 填入 DeepSeek API key（默认路由 `deepseek-flash` = DeepSeek-V4.1-Flash，1M 上下文、支持文+图），也可以在此页写 `llm-pi-ai:` 段切换其他 42 家提供商。

### 第四步：开 session，从仓库摘要开始

调用目录自动成为工作区。先试官方给的入门任务：

```
Summarize this repository and identify its main packages.
```

然后正常下编码任务即可，`standard` 预设每会话独立装配工具集。

### 第五步：按需扩展 profile 与插件

```bash
# 给 web profile 装一个插件包
npx -p @deepseek-ai/dsh dsh plugin --profile web add <package>

# 基于默认模板另起一个自定义 profile
dsh --profile myflow --from-default-profile web
```

MCP server 在设置里一行挂载（stdio 或 Streamable HTTP）；Skills 直接放进项目 `.dsh/skills` 或全局 `~/.dsh/skills`（`.agents/skills` 目录同样被识别，Claude Code 的 skill 资产可直接复用）。

### 第六步：脚本化与自动化

```bash
dsh headless "跑一遍测试并总结失败项"   # 一次性无头会话
dsh acp                                   # ACP stdio，接自动化客户端
```

Python 侧 `pip install` 官方 wheel 后用 SDK profile 做程序化集成，最小化配置用 `sdk-minimal`。

### 从源码运行（进阶）

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

`pnpm run dev:web` 可在一个终端里完成构建、服务、随源码改动重建前端 bundle。

---

## 总结

DSH 做了一件 Claude Code 和 Codex 都没做的事：**把 harness 本身开源并彻底插件化**。Cordis 引擎把 Agent 循环、提示词注册表、工具、压缩、沙箱、UI 全部变成 YAML 补丁栈里的插件行，MIT 协议 + 官方维护 + 28 万星的社区势能，让它既是「DeepSeek 用户的一等公民外壳」，也是「拒绝被厂商锁死外壳」的工程师的自留地。42 家提供商路由、MCP/Skills/Hooks 的存量兼容，又把迁移成本压得很低。

**扣分点：**

- **developer preview 且官方明示破坏性变更**，生产依赖需要跟 39 个 release 的节奏；
- **上手门槛高于「开箱即用」型 Agent**，profile / bundle / patch 三层概念要花时间消化；
- **默认与文档重心都在 DeepSeek**，非 DeepSeek 用户要自己配路由；
- **免费模型类社区插件信任边界需自行确认**。

**推荐指数：⭐⭐⭐⭐☆（4.5/5）**

- **DeepSeek API 用户** → **强烈建议试用**，这是目前能拿到的最完整的官方 harness；
- **想自建/魔改 Agent 外壳的工程师** → **最值得深挖的开源底座**，连循环本身都能换；
- **存量 Claude Code / Codex 重度用户** → 可以先装来跑 Skills 和命令钩子做对比，不必立刻迁移；
- **生产环境求稳的团队** → 观望一个稳定版，或用 `headless` 模式先在 CI 里试点。
