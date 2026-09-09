---
title: 'Browser Use：用自然语言指挥 AI 操控浏览器，自动化办公从此简单'
date: 2026-09-09
tags: ['AI Agent', '浏览器自动化', 'Python', '开源工具']
categories: ['AI 工具评测']
description: 'Browser Use 是一个让 AI Agent 像人一样使用浏览器的开源框架，支持填写表单、抓取数据、自动登录等复杂操作，基于 Playwright + LLM，GitHub 星标超 11 万。'
---

# Browser Use：用自然语言指挥 AI 操控浏览器，自动化办公从此简单

## 一句话简介

**Browser Use** 是一个开源 Python 框架，让 AI Agent 像人类一样使用网页浏览器——打开页面、点击按钮、填写表单、提取数据，全部用自然语言描述即可。

- **GitHub 星标**：113,700+
- **语言**：Python
- **许可证**：MIT
- **最新稳定版**：0.13.10
- **官网**：https://browser-use.com
- **文档**：https://docs.browser-use.com

---

## 核心功能

### 1. 自然语言驱动浏览器操作

只需描述你想做什么，Browser Use 的 AI Agent 会自动完成。比如"填写这份求职申请表"、"抓取 Hacker News 首页标题"、"登录我的邮箱检查新邮件"——它都能办到。

### 2. 基于 Playwright 的真实浏览器渲染

与传统的 HTTP 请求爬虫不同，Browser Use 使用 Playwright 驱动真实浏览器，能够处理 JavaScript 渲染的单页应用（SPA）、需要登录才能访问的页面、以及复杂的交互式表单。

### 3. 支持多种 LLM 后端

兼容主流大模型，包括 OpenAI GPT-4o、Anthropic Claude、Google Gemini 等。你也可以使用 Browser Use Cloud 提供的托管模型服务，新用户可获得 15 美元免费额度。

### 4. MCP 协议支持

Browser Use 已集成 Model Context Protocol (MCP)，可以无缝接入 Claude Code、Cursor、Codex、Hermes 等 AI 编程助手，让你直接在编辑器里用自然语言调用浏览器自动化能力。

### 5. 云端托管与本地部署双模式

- **Browser Use Cloud**：托管式 Agent，无需配置本地环境，API 调用即可
- **本地库**：完全本地运行，数据不出本地，适合对隐私要求高的场景

---

## 适用人群

- **职场人士**：自动化填写重复性表单、批量处理网页数据
- **开发者**：构建需要浏览器操作的 AI Agent 应用
- **数据分析师**：从需要登录的网站抓取结构化数据
- **RPA 替代者**：寻找传统 RPA 工具现代化替代方案的用户
- **AI 爱好者**：探索 Agentic AI 在真实场景中的应用

---

## 与同类工具对比

| 特性 | Browser Use | Selenium | Playwright (原生) | Web Scraping Robot |
|------|------------|----------|-------------------|-------------------|
| 自然语言驱动 | ✅ | ❌ | ❌ | ❌ |
| 真实浏览器渲染 | ✅ | ✅ | ✅ | ✅ |
| 自动填写表单 | ✅ | 需手动编写 | 需手动编写 | 有限 |
| LLM 集成 | 内置 | 需自行对接 | 需自行对接 | 有限 |
| MCP 支持 | ✅ | ❌ | ❌ | ❌ |
| 上手难度 | 低（几行代码） | 中高 | 中 | 低 |
| 社区活跃度 | 极高（11万+ stars） | 高 | 高 | 中 |

**总结**：Browser Use 最大的差异化在于"用自然语言描述任务，AI 自动完成浏览器操作"，大幅降低了浏览器自动化的门槛。

---

## 如何使用

### 第一步：安装

```bash
# 使用 uv（推荐）
uv venv --python 3.12
source .venv/bin/activate
uv pip install browser-use
uvx browser-use install  # 安装 Chromium 浏览器
```

或使用 pip：

```bash
pip install browser-use
```

### 第二步：配置 API Key

创建 `.env` 文件：

```bash
# 方式一：使用 Browser Use Cloud（推荐新手）
BROWSER_USE_API_KEY=your_api_key_here

# 方式二：自带 LLM Provider
ANTHROPIC_API_KEY=your_anthropic_key
# 或
GOOGLE_API_KEY=your_google_key
# 或
OPENAI_API_KEY=your_openai_key
```

### 第三步：写一个简单脚本

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model='gpt-4o')

agent = Agent(
    task='访问 Hacker News 首页，找到当前排名第一的故事标题和链接',
    llm=llm
)

result = await agent.run()
print(result)
```

### 第四步：运行

```bash
python your_script.py
```

Agent 会自动启动浏览器，完成你描述的任务，并返回结果。

### 第五步：在 AI 编程助手中使用（MCP 模式）

如果你使用 Claude Code、Cursor 等工具，只需一条指令即可安装：

```
Install or upgrade browser-use to the latest stable version with uv using Python 3.12, run `browser-use skill install` to register the skill, and connect it to my browser.
```

然后直接告诉 AI 你要做什么，比如"帮我去 GitHub 上找最新的 AI Agent 框架并列出 TOP 5"。

---

## 局限性

1. **依赖 LLM 稳定性**：复杂任务可能需要多次重试，费用随任务复杂度上升
2. **浏览器渲染开销**：相比纯 API 调用，浏览器自动化速度较慢
3. **反爬虫风险**：频繁操作可能触发目标网站的反爬机制
4. **Cloud 服务限制**：免费额度仅 15 美元，重度使用需付费

---

## 总结

Browser Use 是目前最易上手的 AI 浏览器自动化工具之一，GitHub 11 万+ 星充分说明了其受欢迎程度。它将复杂的浏览器自动化操作抽象为简单的自然语言描述，无论是填写求职表、批量抓取数据，还是构建智能体应用，都能大幅降低开发成本。

对于已经使用 Claude Code、Cursor 等 AI 编程助手的开发者来说，Browser Use 的 MCP 集成更是锦上添花——让 AI 拥有了"眼睛和手"，可以真正在网页上完成实际工作。

**推荐指数**：⭐⭐⭐⭐⭐（5/5）

如果你是 AI 爱好者或需要浏览器自动化能力的开发者，Browser Use 绝对值得尝试。从安装到第一个 Agent 运行，通常不超过 5 分钟。

---

> 📎 **相关链接**
> - [GitHub 仓库](https://github.com/browser-use/browser-use)
> - [官方文档](https://docs.browser-use.com)
> - [Browser Use Cloud](https://cloud.browser-use.com)
> - [示例代码](https://github.com/browser-use/browser-use/tree/main/examples)
