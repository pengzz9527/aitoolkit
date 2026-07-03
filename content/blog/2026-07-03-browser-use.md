---
title: 'Browser Use 评测：让 AI 代理操控浏览器，自动化一切网页操作'
date: 2026-07-03T08:00:00+08:00
description: 'Browser Use 是一个开源 AI 浏览器自动化框架，支持使用 GPT、Claude 等大语言模型驱动浏览器完成网页操作任务，GitHub 星标超 10 万，是目前最流行的 AI Agent 工具之一。'
tags:
  - AI
  - 浏览器自动化
  - AI Agent
  - 工具评测
  - 开源
  - Python
categories:
  - AI 工具评测
---

## 一句话介绍

**Browser Use** 是一个开源的 AI 浏览器自动化框架，允许开发者使用 GPT、Claude 等大语言模型驱动浏览器，自动完成网页上的各种操作任务——从数据抓取、表单填写到复杂的跨页面工作流。GitHub 星标超过 10 万，是目前最热门且最成熟的 AI Agent 工具之一。

---

## 核心功能

### 1. 自然语言驱动的浏览器操作

Browser Use 的核心卖点是用自然语言描述你想让 AI 代理做的事情，它就能自动完成。比如你说"帮我查找 GitHub 上 browser-use 项目的星标数"，它会自动打开浏览器、搜索、点击、截图分析，最终返回结果。整个过程完全由大语言模型驱动，无需编写任何选择器或脚本。

### 2. 支持多种大语言模型

Browser Use 兼容主流 LLM 后端，包括 OpenAI（GPT-4/GPT-5）、Anthropic（Claude）、Google Gemini 以及 Browser Use 自研的优化模型。这种灵活性意味着用户可以根据预算和需求自由选择模型，同时也支持通过自有 API Key 接入任意兼容 OpenAI 接口的模型。

### 3. 灵活的浏览器配置

内置 Playwright 引擎，支持有头（headed）和无头（headless）两种模式运行。可以精确控制允许的域名范围、浏览器窗口大小、视口设置等。对于需要登录的场景，还支持连接本地已登录的浏览器实例，避免重复认证。

### 4. 结构化输出与任务历史

每次 Agent 运行都会完整记录操作历史——包括每一步的思考过程、执行的 DOM 操作、截图和最终结果。这些历史记录可以导出查看，也可以用于调试和优化 Agent 的行为。最终结果可以以结构化格式返回，方便后续程序处理。

### 5. 云端部署选项

除了本地部署，Browser Use 还提供了云服务（Browser Use Cloud），免去了环境配置的麻烦。云服务自带反检测能力，适合大规模自动化任务。同时支持 CLI 模式，可以直接在 Claude Code、Cursor 等编码工具中使用。

---

## 适用人群

- **开发者**：需要自动化网页操作流程的后端和全栈工程师
- **数据分析师**：需要从网页批量采集数据但缺乏专业爬虫经验的人员
- **产品经理**：需要快速验证网站交互流程或竞品功能的产品人员
- **普通用户**：希望用自然语言完成重复性网页操作的非技术人员
- **AI 研究者**：研究多模态 Agent 行为和安全边界的学术人员

---

## 与同类工具对比

| 特性 | Browser Use | AutoGPT | Playwright + LLM | Dify |
|------|-------------|---------|-------------------|------|
| 上手难度 | 低（几行代码即可运行） | 中高（需要大量调优） | 高（需自行编写所有逻辑） | 中（可视化编排） |
| 浏览器控制 | 原生支持 Playwright | 需集成 | 直接封装 | 需集成插件 |
| LLM 兼容性 | 支持多种模型 | 主要 OpenAI | 取决于实现 | 支持多种 |
| 开源协议 | MIT | Apache 2.0 | 开源 | AGPL |
| 社区活跃度 | 极高（10 万+ ⭐） | 高 | 中 | 高 |
| 生产就绪度 | 高（已广泛用于生产） | 中 | 取决于实现 | 高 |

Browser Use 的优势在于它专注于"浏览器自动化"这一垂直场景，做得比通用 AI Agent 框架更精细。相比 AutoGPT 的泛化能力，Browser Use 在网页交互的准确性和稳定性上表现更好；相比直接写 Playwright 脚本，它省去了繁琐的元素定位和状态管理。

---

## 如何使用

### 方法一：本地安装（推荐）

**1. 安装依赖**

```bash
# 使用 uv（推荐）
uv add browser-use

# 或使用 pip
pip install browser-use
```

**2. 配置环境变量**

在项目根目录创建 `.env` 文件：

```
GOOGLE_API_KEY=your_google_key
# 或者使用其他模型
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

**3. 编写第一个 Agent**

```python
import asyncio
from browser_use import Agent, BrowserProfile, ChatBrowserUse

async def main():
    agent = Agent(
        task="查找 GitHub 上 browser-use 项目的星标数",
        llm=ChatBrowserUse(model='openai/gpt-5.5'),
        browser_profile=BrowserProfile(
            headless=True,
            allowed_domains=["*.github.com"],
        ),
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### 方法二：使用云服务

如果不想配置本地环境，可以直接使用 Browser Use Cloud：

1. 访问 https://cloud.browser-use.com 注册账号
2. 获取 API Key
3. 在 `.env` 中添加 `BROWSER_USE_API_KEY=your_key`
4. 使用相同的 Python SDK 调用，但模型选择 `bu-2-0`（Browser Use 自研模型）

### 方法三：在 Claude Code 中使用

Browser Use 3.0 引入了 CLI 技能模式，可以直接嵌入编码代理：

```
# 在 Claude Code 中输入：
Install or upgrade browser-use to the latest stable version with uv using Python 3.12,
register the skill from browser-use skill, and connect it to my browser.
```

---

## 总结与推荐

**推荐指数：⭐⭐⭐⭐⭐（5/5）**

Browser Use 是目前将大语言模型与浏览器自动化结合得最好的开源项目之一。它的 API 设计简洁直观，几行代码就能启动一个能自主操控浏览器的 AI Agent。10 万+ 的 GitHub 星标和活跃的社区生态证明了其可靠性和实用性。

**值得推荐的理由：**
1. 上手极快，几行 Python 代码即可开始使用
2. 支持多种 LLM 后端，灵活适配不同预算和场景
3. Playwright 原生集成，浏览器操作稳定可靠
4. MIT 开源协议，可自由商用
5. 提供云服务和 CLI 技能模式，满足从个人到企业的需求

**需要注意的地方：**
1. 使用外部 LLM API 会产生调用费用，复杂任务可能消耗较多 token
2. 部分网站有反自动化机制，可能需要额外配置绕过
3. 无头模式下对复杂 JavaScript 渲染页面的处理能力有限
4. 自研模型 `bu-2-0` 仅在使用云服务时可用

**最佳适用场景：** 需要自动化执行网页操作流程的任务，如竞品监控、数据采集、表单自动填写、网站测试等。特别适合那些需要"让 AI 像人一样操作浏览器"的场景。

**项目地址：** https://github.com/browser-use/browser-use
**官方网站：** https://browser-use.com
**文档：** https://docs.browser-use.com
**云服务：** https://cloud.browser-use.com
