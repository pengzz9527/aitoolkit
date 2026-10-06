---
title: 'Claude-Mem：让 AI 编程助手跨会话记住一切，再也不怕断片'
date: 2026-10-06
tags: [AI工具, AI记忆, Claude Code, 开源, 开发者工具]
categories: [AI 工具评测]
description: 一款 96k+ Star 的开源持久记忆系统，自动捕获 AI 编程助手的会话过程，用 AI 压缩后注入未来会话，支持 Claude Code、OpenClaw、Codex、Gemini 等 10+ 种工具。
---

# Claude-Mem：让 AI 编程助手跨会话记住一切，再也不怕断片

用过 Claude Code 或其他 AI 编程助手的人都有这个痛点：会话一断，AI 就"失忆"了。项目背景、之前的决策、踩过的坑，全都要从头再说一遍。

**[Claude-Mem](https://github.com/thedotmack/claude-mem)**（⭐ 96,700+）就是为了解决这个问题而生的。它自动捕获 AI 助手在会话中的一切操作，用 AI 生成语义摘要压缩存储，并在未来会话开始时自动注入相关上下文，让 AI 真正实现"记得住、接得上"。

## 核心功能

### 1. 多 Agent 工具支持

Claude-Mem 不局限于 Claude Code，支持 **10+ 种 AI 编程助手**：

- Claude Code（插件市场安装）
- OpenClaw（一键脚本安装）
- Codex、Gemini CLI、Hermes、Copilot、OpenCode
- T3 Code、Antigravity CLI、OMP（Oh My Pi）、Grok Bot

每种工具都有对应的安装方式，覆盖主流的 AI 编程工作流。

### 2. 自动捕获 + AI 压缩

通过 5 个生命周期钩子（SessionStart、UserPromptSubmit、PostToolUse、Stop、SessionEnd）自动捕获工具调用、代码变更、决策过程等"观察"（Observation），再用 AI 生成紧凑的语义摘要。无需任何手动操作，全程自动化。

### 3. 渐进式披露检索

采用 **3 层检索工作流**，大幅节省 Token 消耗：

| 步骤 | 工具 | Token 成本 |
|------|------|-----------|
| 第 1 层 | `search` — 获取带 ID 的紧凑索引 | ~50-100 tokens/条 |
| 第 2 层 | `timeline` — 查看时间线上下文 | ~50-100 tokens/条 |
| 第 3 层 | `get_observations` — 按需拉取完整细节 | ~500-1000 tokens/条 |

相比直接全量注入，Token 节省可达 **10 倍**，既省钱又不浪费上下文窗口。

### 4. 混合检索：SQLite + Chroma 向量库

底层存储使用 SQLite（FTS5 全文搜索）+ Chroma 向量数据库（语义搜索），支持按类型（decision、bugfix、security_alert 等）、时间、项目多维度过滤，检索精度和速度都有保障。

### 5. 隐私控制

支持 `<private>` 标签，标记的内容不会进入记忆存储。敏感信息（密钥、内部数据等）可以被排除在记忆系统之外，数据始终保存在本地 SQLite 中。

## 适用人群

- **Claude Code / Codex / Gemini CLI 重度用户**：每天多个会话，项目背景反复丢失，最需要持久记忆
- **长期项目维护者**：跨周、跨月维护同一个项目，需要 AI 记住历史决策
- **团队协作场景**：将观察记忆通过 Web Viewer 共享，降低新成员上手成本
- **AI Agent 开发者**：Claude-Mem 本身就是一个高质量的 Agent 记忆架构参考
- **中文开发者**：内置 `code--zh` 模式，生成的观察摘要直接是中文

## 与同类工具对比

| 特性 | Claude-Mem | 手动 CLAUDE.md | Mem0 | Supermemory |
|------|-----------|---------------|------|-------------|
| 自动捕获 | ✅ 钩子自动 | ❌ 手动 | ✅ | ✅ |
| 支持工具数 | 10+ | 1（Claude Code） | 多 | 多 |
| AI 压缩 | ✅ 语义摘要 | ❌ | ✅ | ✅ |
| 向量检索 | ✅ Chroma | ❌ | ✅ | ✅ |
| Token 节省 | ✅ 3 层渐进 | ❌ | 部分 | 部分 |
| 本地存储 | ✅ SQLite | ✅ 文件 | 云端 | 云端 |
| 中文模式 | ✅ 内置 | ❌ | ❌ | ❌ |
| 开源协议 | Apache 2.0 | — | 部分开源 | 闭源 |

与其他记忆工具相比，Claude-Mem 的独特优势在于：**多工具覆盖最广（10+ 种）、纯本地存储、渐进式 Token 节省设计**，以及内置的中文支持，对中文开发者友好度最高。

## 如何使用

### 安装（Claude Code）

```bash
# 方式一：npx 一键安装
npx claude-mem install

# 方式二：Claude Code 插件市场
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```

安装后重启 Claude Code，系统会自动配置所有钩子和 Worker 服务。

### 安装（OpenClaw）

```bash
curl -fsSL https://install.cmem.ai/openclaw.sh | bash
```

### 安装（其他工具）

```bash
# OpenCode
npx claude-mem install --ide opencode

# T3 Code
npx claude-mem install --ide t3code

# Grok Bot
npx claude-mem install --ide grok-bot
```

### 启用中文模式

编辑 `~/.claude-mem/settings.json`：

```json
{
  "CLAUDE_MEM_MODE": "code--zh"
}
```

重启 Claude Code 后，所有生成的观察摘要将使用中文。

### 搜索历史记忆

在 Claude Code 中直接用自然语言提问，Claude-Mem 的 MCP 工具会自动介入：

```
# 示例对话
你：我们上周决定用 SQLite 替代 MySQL，原因是什么？
Claude（自动调用 mem-search）：根据 #247 号观察（2026-09-28），团队决定迁移到 SQLite，
原因是部署简化、无外部依赖，预计减少 40% 基础设施成本...
```

### 系统要求

- Node.js ≥ 20.0.0
- Bun（自动安装）
- SQLite 3（内置）
- uv（向量搜索用，自动安装）

## 注意事项

1. **不要 `npm install -g claude-mem`**：全局安装只装 SDK 库，不会注册钩子和 Worker 服务，务必用 `npx claude-mem install`
2. **登录问题**：安装时会提示登录 claude-mem 账户（免费试用 14 天），不想要可加 `--provider` 参数跳过，或直接使用自己的 API Key
3. **数据管理**：观察数据存在本地 SQLite，定期备份 `~/.claude-mem/` 目录；Web Viewer 提供实时查看界面
4. **隐私敏感场景**：在涉及商业秘密的项目中，善用 `<private>` 标签排除敏感内容

## 总结

**Claude-Mem** 是目前最完整的 AI Agent 持久记忆系统，96k+ Star 的数据印证了它的实际价值。它把"AI 失忆"这个最恼人的问题，用自动钩子 + AI 压缩 + 渐进检索的组合方案彻底解决，而且覆盖工具广、纯本地运行、还有中文模式。

### 推荐指数：⭐⭐⭐⭐⭐（5/5）

**优点：**
- 支持 10+ 种 AI 编程助手，覆盖面行业最广
- 纯本地存储（SQLite + Chroma），数据不出门
- 3 层渐进检索，Token 节省最高 10 倍
- 内置中文模式，中文开发者零门槛
- Apache 2.0 开源，可自由商用和嵌入
- 自动运行，无需手动干预

**缺点：**
- 安装流程略复杂（多 IDE 多入口，文档分散）
- 免费试用期过后需订阅或自带 API Key
- 大项目长期运行后 SQLite 文件会越来越大，需关注磁盘

如果你每天用 Claude Code 或其他 AI 编程助手做开发，Claude-Mem 是必须装的"记忆增强插件"——让 AI 真正拥有持续的项目记忆，开发体验会有质的飞跃。

---

*项目地址：https://github.com/thedotmack/claude-mem*
*文档：https://docs.claude-mem.ai/*
*官网：https://claude-mem.ai*

---

喜欢这篇评测？浏览 [198007.xyz 工具集](/tools/) 发现更多 AI 编程辅助工具。
