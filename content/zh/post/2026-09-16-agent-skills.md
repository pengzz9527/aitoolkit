---
title: 'Agent Skills：Addy Osmani 开源的 AI 编程 Agent 工程技能库，9.5 万 Star 的 Agent 进化指南'
date: 2026-09-16
tags: ['Agent Skills', 'AI Agent', '编程助手', '工程规范', '开源工具', 'Claude Code', 'Cursor', 'Codex']
categories: ['AI 工具评测']
description: 'Agent Skills 是 Addy Osmani 开源的 AI 编程 Agent 工程技能库，包含 25 个覆盖完整开发生命周期的结构化工作流技能，支持 Claude Code、Cursor、Codex 等 70+ Agent 工具，GitHub 星标近 9.5 万。'
---

# Agent Skills：Addy Osmani 开源的 AI 编程 Agent 工程技能库，9.5 万 Star 的 Agent 进化指南

**Agent Skills** 是由 Google 前端工程师 Addy Osmani 于 2026 年 2 月开源的 AI 编程 Agent 工程技能库。它的核心理念很直接：AI Agent 默认倾向于走最短路径——而这往往意味着跳过规范文档、测试、安全审查和那些让软件真正可靠的最佳实践。Agent Skills 通过 25 个结构化工作流技能，为 Claude Code、Cursor、Codex 等主流 AI 编程 Agent 注入了资深工程师的工程纪律。

- **GitHub 星标**：94,956+
- **GitHub 仓库**：https://github.com/addyosmani/agent-skills
- **许可证**：MIT
- **语言**：JavaScript（Markdown 技能文件）
- **作者**：Addy Osmani（Google 前端工程师，Chrome DevTools 核心贡献者）
- **官方文档**：https://github.com/addyosmani/agent-skills

---

## 核心功能

### 1. 覆盖完整开发生命周期的 25 个技能

Agent Skills 将软件开发流程拆解为六个阶段，每个阶段配备若干结构化技能：

| 阶段 | 代表技能 |
|------|---------|
| Define（定义） | `interview-me`、`idea-refine`、`spec-driven-development`、`constraint-driven-development` |
| Plan（规划） | `planning-and-task-breakdown` |
| Build（构建） | `incremental-implementation`、`test-driven-development`、`context-engineering`、`frontend-ui-engineering`、`api-and-interface-design` |
| Verify（验证） | `browser-testing-with-devtools`、`debugging-and-error-recovery` |
| Review（审查） | `code-review-and-quality`、`code-simplification`、`security-and-hardening`、`performance-optimization` |
| Ship（交付） | `git-workflow-and-versioning`、`ci-cd-and-automation`、`deprecation-and-migration`、`documentation-and-adrs` |

每个技能都是结构化的工作流，包含明确的步骤、验证门控和质量标准，而非泛泛的建议。

### 2. Slash 命令驱动，开箱即用

Agent Skills 提供了 9 个核心斜杠命令，直接映射到开发生命周期：

| 命令 | 功能 | 核心原则 |
|------|------|---------|
| `/spec` | 在写代码前先写好需求文档 | Spec before code |
| `/plan` | 将需求拆解为可执行的小任务 | Small, atomic tasks |
| `/build` | 增量式实现，一次一个切片 | One slice at a time |
| `/test` | 测试即证明 | Tests are proof |
| `/constraints` | 设定质量门槛并统一执行 | Decide it once, enforce it everywhere |
| `/review` | 合并前的质量审查 | Improve code health |
| `/webperf` | Web 性能审计 | Measure before you optimize |
| `/code-simplify` | 代码简化 | Clarity over cleverness |
| `/ship` | 安全上线 | Faster is safer |

更贴心的是，`/build auto` 命令可以在你批准计划后自动执行所有任务，无需人工逐阶段介入——但每个任务仍会独立测试和提交，失败时会自动暂停。

### 3. 按需自动激活技能

Agent Skills 能根据当前任务自动激活相关技能：编写 API 时自动触发 `api-and-interface-design`，构建前端界面时自动触发 `frontend-ui-engineering`，让你无需手动记忆和调用每个技能。

### 4. 兼容 70+ AI Agent 工具

这是 Agent Skills 最强大的特性之一。它通过统一的 skills CLI 可以安装到超过 70 个 AI 编程 Agent 中，包括：

- **Claude Code**（推荐，支持 marketplace 一键安装）
- **Cursor**
- **Codex**（OpenAI）
- **GitHub Copilot**
- **Gemini CLI**（Google）
- **Cline**
- **Windsurf**
- **Antigravity CLI**
- **Command Code**
- **Kiro IDE & CLI**
- **OpenCode**

此外，技能文件本质上是 Markdown，任何支持系统提示或指令文件的 Agent 都可以直接使用。

### 5. 源自 Google 工程文化的最佳实践

技能中融入了大量来自 Google 工程实践的核心概念，包括：Hyrum 定律（API 设计）、Beyonce 规则（测试命名）、测试金字塔、Change Sizing（约 100 行变更）、Chesterton 栅栏（代码简化）、Trunk-based 开发、Shift Left 理念、Feature Flags 等。这些不是抽象理论，而是直接嵌入到每一步操作流程中。

---

## 适用人群

- **AI 编程 Agent 用户**：正在使用 Claude Code、Cursor、Codex 等工具，希望提升代码质量的开发者。
- **团队技术负责人**：希望将工程规范标准化并自动应用于团队所有开发者的技术 leader。
- **初级开发者**：希望通过 Agent 的学习和引导，快速掌握资深工程师的工作流程和规范。
- **开源项目维护者**：需要统一代码审查标准和开发流程的项目组织者。
- **工程文化移植者**：希望在自己的团队中引入 Google 级工程实践的个人或组织。

---

## 与同类工具对比

| 特性 | Agent Skills | obra/Superpowers | mattpocock/skills |
|------|-------------|------------------|-------------------|
| 技能数量 | 25 个 | 较少 | 较少 |
| Agent 兼容性 | 70+ 工具 | 有限 | 有限 |
| 安装方式 | CLI / 原生插件 / Markdown | 原生插件 | 原生插件 |
| 工程深度 | 覆盖完整生命周期 | 侧重构建 | 侧重单点能力 |
| 来源背景 | Google 工程实践 | 社区贡献 | 个人经验 |
| GitHub Stars | 94,956+ | ~20,000+ | ~10,000+ |

Agent Skills 在三个主流技能库中规模最大、兼容性最强，且背靠 Google 成熟的工程方法论，是目前 AI 编程 Agent 技能库中的旗舰级选择。

---

## 如何使用

### 方式一：通过 Skills CLI 安装（推荐，支持 70+ Agent）

```bash
# 安装全部 25 个技能
npx skills add addyosmani/agent-skills

# 先浏览再安装
npx skills add addyosmani/agent-skills --list

# 只安装某个特定技能
npx skills add addyosmani/agent-skills --skill test-driven-development

# 安装指定技能（如 interview-me）
npx skills add addyosmani/agent-skills --skill interview-me
```

### 方式二：Claude Code 原生安装

```bash
# Marketplace 安装
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills

# 或本地开发安装
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

### 方式三：Cursor 安装

将技能文件复制到项目的 `.cursor/skills/` 目录（从 `agent-skills/skills/` 同步），并将简短策略放在 `.cursor/rules/*.mdc` 中。详见项目文档 [docs/cursor-setup.md](https://github.com/addyosmani/agent-skills/blob/main/docs/cursor-setup.md)。

### 方式四：Codex CLI 安装（v0.122+）

```bash
codex plugin marketplace add addyosmani/agent-skills
codex plugin add agent-skills@agent-skills
```

安装后在对话中使用 `@` 引用技能，如 `@spec-driven-development`。

### 方式五：Gemini CLI 安装

```bash
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills
# 或本地安装
gemini skills install ./agent-skills/skills/
```

### 日常使用示例

```bash
# 开始一个新项目：先定义需求
/spec

# 拆解任务
/plan

# 增量构建
/build

# 测试驱动
/test

# 代码审查
/review

# 快速自动构建（批准计划后全自动）
/build auto
```

---

## 总结推荐指数

Agent Skills 是目前 AI 编程 Agent 生态中最成熟、最全面的工程技能库，9.5 万 Star 足以说明其受欢迎程度。它不仅仅是一套 prompt 模板，而是将 Google 级的工程实践转化为 Agent 可直接执行的structured workflows，真正填补了"AI 能写代码"和"AI 能写出生产级代码"之间的鸿沟。

如果你是重度 AI 编程 Agent 用户，或者希望团队所有开发都遵循统一的工程规范，Agent Skills 几乎是必装工具。它的 70+ Agent 兼容性更是业界罕见，无论你是 Claude Code、Cursor 还是 Codex 的用户，都能找到对应的安装方式。

**推荐指数：★★★★★**（5/5 — 当前 AI 编程 Agent 技能库中的标杆之作，强烈推荐给所有 Agent 用户）
