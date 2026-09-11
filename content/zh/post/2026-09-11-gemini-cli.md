---
title: 'Gemini CLI — Google 官方开源终端 AI 助手，10 万+ Stars 的命令行智能体'
date: 2026-09-11
tags: ['AI Agent', 'CLI', 'Gemini', '开源工具', '终端工具']
categories: ['AI 工具评测']
description: 'Gemini CLI 是 Google 官方开源的终端 AI Agent，将 Gemini 3 模型的强大能力直接带入你的命令行，支持自然语言编程、文件操作、Shell 命令、Google Search Grounding 等功能，个人账号享免费额度。'
---

# Gemini CLI — Google 官方开源终端 AI 助手，10 万+ Stars 的命令行智能体

![Gemini CLI](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/assets/gemini-screenshot.png)

**Gemini CLI** 是 Google Gemini 团队官方开源的终端 AI Agent 工具，Stars 数已超过 106,900。它将 Gemini 3 模型的强大能力直接带入命令行，让你用自然语言与代码库对话、执行文件操作、运行 Shell 命令、查询实时信息，甚至通过 GitHub Action 集成到 CI/CD 流程中。项目采用 Apache 2.0 许可证，完全开源免费。

- **GitHub 星标**：106,910+
- **语言**：TypeScript
- **许可证**：Apache 2.0
- **官网**：https://geminicli.com
- **文档**：https://geminicli.com/docs/
- **仓库**：https://github.com/google-gemini/gemini-cli

---

## 核心功能

### 1. 免费额度友好的个人使用

使用个人 Google 账号登录即可免费使用：**每分钟 60 次请求、每天 1,000 次请求**，无需配置 API Key。对于日常编程辅助、代码阅读和理解任务来说，这个额度非常宽裕。

### 2. Gemini 3 模型 + 100 万 Token 上下文窗口

内置对 Gemini 3 系列模型的支持，包括改进的推理能力和 100 万 Token 的超长上下文窗口。这意味着你可以将整个大型代码库一次性加载进对话中，让 AI 全面理解你的项目结构后再给出建议。

### 3. 内置工具链：搜索、文件操作、Shell 命令、网页抓取

Gemini CLI 不只是聊天机器人，它配备了实用的内置工具：
- **Google Search Grounding**：查询时自动联网获取最新信息，避免模型幻觉
- **文件读写操作**：直接读取、创建、编辑项目中的文件
- **Shell 命令执行**：在受控环境中运行终端命令
- **网页抓取**：获取网页内容作为上下文

### 4. MCP 扩展生态

支持 Model Context Protocol（MCP），可以通过 MCP Server 扩展更多能力。已有社区开发的插件支持 Imagen 图像生成、Veo 视频生成、Lyria 音频生成等媒体创作能力，也可以连接内部工具和数据库。

### 5. GitHub 深度集成

通过官方的 [Gemini CLI GitHub Action](https://github.com/google-github-actions/run-gemini-cli)，可以将 AI 能力直接嵌入 GitHub 工作流：
- **Pull Request 自动审查**：AI 读取代码变更并给出上下文感知的反馈
- **Issue 智能分类**：根据内容自动标签和优先级排序
- **按需协助**：在 Issue 或 PR 中 @gemini-cli 请求帮助
- **自定义工作流**：构建自动化、定时和按需执行的 AI 工作流

### 6. 非交互式脚本模式

支持 `--output-format json` 和 `--output-format stream-json` 两种结构化输出模式，可以无缝集成到自动化脚本和 CI/CD 流水线中，实现真正的全自动 AI 驱动工作流。

### 7. 多模态代码生成

支持从 PDF、图片、设计稿甚至手绘草图中生成应用程序代码，让创意到代码的转化更加直接。

---

## 适用人群

- **开发者**：希望用自然语言快速理解代码库、调试问题、生成代码的工程师
- **DevOps 工程师**：需要将 AI 能力集成到 CI/CD 流程中的运维人员
- **技术负责人**：希望通过 AI 辅助代码审查和 Issue 管理的团队领导
- **终端爱好者**：喜欢在命令行环境中完成所有工作的效率追求者
- **Python/JS 开发者**：需要快速原型开发和自动化脚本编写的程序员

---

## 与同类工具对比

|| 特性 | Gemini CLI | Claude Code | Codex CLI | OpenClaw |
|------|----------|-------------|-----------|----------|
| 厂商背景 | Google | Anthropic | OpenAI | 社区开源 |
| 开源 | ✅ Apache 2.0 | ✅ AGPL-3.0 | ❌ 闭源 | ✅ MIT |
| 免费额度 | ✅ 60次/分，1000次/天 | ⚠️ 需付费订阅 | ⚠️ 按量计费 | ✅ 免费 |
| 上下文窗口 | 100 万 Token | 200 万 Token | 100 万 Token | 100 万 Token |
| MCP 支持 | ✅ | ✅ | ❌ | ✅ |
| GitHub 集成 | ✅ 官方 Action | ✅ | ⚠️ 有限 | ✅ |
| 非交互模式 | ✅ JSON/Stream | ✅ | ✅ | ✅ |
| 多模态输入 | ✅ 图片/PDF/草图 | ✅ | ✅ | ✅ |
| 上手难度 | 低（npm install） | 中 | 中 | 高 |

**总结**：Gemini CLI 的核心优势在于 Google 官方背书 + 免费额度友好 + Apache 2.0 开源许可证，对于个人开发者和小型团队来说是最容易上手且成本最低的终端 AI Agent 选择之一。

---

## 如何使用

### 第一步：安装

有三种推荐方式，选择最适合你的一种：

```bash
# 方式一：npx 一键运行（无需安装，最快体验）
npx @google/gemini-cli

# 方式二：npm 全局安装（推荐长期使用）
npm install -g @google/gemini-cli

# 方式三：Homebrew 安装（macOS/Linux）
brew install gemini-cli
```

### 第二步：认证登录

安装完成后运行：

```bash
gemini
```

首次启动会提示你选择认证方式：

- **Sign in with Google**（推荐）：用个人 Google 账号登录，享受免费额度，无需管理 API Key
- **Gemini API Key**：去 [AI Studio](https://aistudio.google.com/apikey) 获取 API Key，适合需要更高配额或专业模型控制的场景
- **Vertex AI**：适合企业用户，已接入 Google Cloud 基础设施的团队

### 第三步：基础使用

```bash
# 在当前目录启动（自动加载项目上下文）
gemini

# 指定模型
gemini -m gemini-2.5-flash

# 包含多个目录
gemini --include-directories ../lib,../docs

# 非交互模式获取文本回复
gemini -p "解释这个项目的架构"

# 获取结构化 JSON 输出
gemini -p "分析代码质量并列出问题" --output-format json
```

### 第四步：在项目中配置 GEMINI.md

在项目根目录创建 `GEMINI.md` 文件，可以定制 Gemini CLI 的行为：

```markdown
# 项目提示词

你是一个专业的 TypeScript 开发者。请遵循以下规范：
- 使用 ESLint 和 Prettier 格式化代码
- 写测试时优先使用 Vitest
- 提交信息遵循 Conventional Commits 规范
```

### 第五步：集成到 GitHub Actions

在 `.github/workflows/gemini.yml` 中添加：

```yaml
name: Gemini Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/run-gemini-cli@main
        with:
          code-assist-token: ${{ secrets.GEMINI_TOKEN }}
          prompt: "Review this PR and provide constructive feedback on code quality and potential bugs."
```

---

## 局限性

1. **Google 账号依赖**：免费额度需要个人 Google 账号，部分地区的用户可能受限
2. **网络环境要求**：Google 服务在国内访问可能需要代理，影响使用体验
3. **企业级功能需付费**：超出免费额度后需要购买 Code Assist License 或按 Vertex AI 计费
4. **生态相对年轻**：相比 Claude Code，MCP 插件生态和社区经验还在快速增长中

---

## 总结

Gemini CLI 是 Google 在终端 AI 助手赛道上的重磅之作。凭借 106,900+ Stars 和社区认可度，它已经证明了自身价值。对于个人开发者而言，免费额度 + 100 万 Token 上下文 + Google Search Grounding 的组合非常具有吸引力，让你能在日常编码中零成本地体验 AI 辅助。

如果你已经习惯在终端中工作，或者正在寻找一个可以集成到 GitHub 工作流中的 AI 代码助手，Gemini CLI 是目前最值得尝试的选择之一。

**推荐指数**：⭐⭐⭐⭐☆（4.5/5）

---

> 📎 **相关链接**
> - [GitHub 仓库](https://github.com/google-gemini/gemini-cli)
> - [官方文档](https://geminicli.com/docs/)
> - [在线演示](https://geminicli.com)
> - [GitHub Action](https://github.com/google-github-actions/run-gemini-cli)
> - [Changelog](https://www.geminicli.com/docs/changelogs)
