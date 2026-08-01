---
title: 'Page Agent: 纯前端 GUI 智能体，一行代码让网页听懂人话'
date: 2026-07-05
tags: ['GUI智能体', 'Web自动化', '前端AI', 'Alibaba', 'TypeScript', '开源工具']
categories: ['工具评测']
description: 'Page Agent 是阿里巴巴开源的纯前端 GUI 智能体，无需后端、浏览器插件或无头浏览器，只需一行 JS 代码即可让网页通过自然语言交互，GitHub 23K+ Star。'
---

想了解更多 AI 工具？浏览 [198007.xyz/tools](/tools/) 获取精选 AI 工具合集，或查看其他 [AI 工具评测](/reviews/)。

## 相关评测

- [**OmniRoute 评测**](/reviews/2026-07-02-OmniRoute/) — AI 路由优化工具
- [**Page Agent 评测**](/reviews/2026-07-05-page-agent/) — 自动化网页操作 Agent

> 一句话简介：Page Agent 是阿里巴巴开源的纯前端 GUI 智能体，无需后端、浏览器插件或无头浏览器，只需在网页中嵌入一行 JavaScript 代码，就能让用户通过自然语言操控 Web 界面，GitHub 星标已超 23,000。

在 AI Agent 蓬勃发展的当下，大多数网页自动化工具（如 Playwright、Selenium、browser-use）都依赖后端服务、无头浏览器或浏览器插件，部署复杂且资源开销大。**Page Agent** 另辟蹊径——它将整个 Agent 运行在浏览器页面内部，纯 JavaScript 实现，无需任何额外基础设施。

Page Agent 由阿里巴巴团队开源，于 2025 年 9 月发布，短短时间内就在 GitHub 上获得了 **23,284+ Star** 和 2,015+ Fork，成为目前最轻量的前端 GUI Agent 方案之一。如果你需要处理 Page Agent 输出的结构化数据（如 JSON 格式的 DOM 信息），本站的 [JSON 格式化工具](/tools/json-formatter/) 可以帮你快速查看和调试。

## 核心功能

### 1. 纯前端运行，零后端依赖

Page Agent 最大的亮点在于它的架构设计——它完全在浏览器页面内运行，不需要后端服务器、Python 环境或无头浏览器。你只需要在 HTML 中引入一个 `<script>` 标签，或者通过 npm 安装一个包，即可在网页中启动一个能理解自然语言的 AI 智能体。

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.11.0/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

### 2. 基于文本的 DOM 操作，无需截图

与传统的多模态 Agent 不同，Page Agent 不依赖截图或视觉模型来理解页面。它直接解析页面的 DOM 结构，以文本形式向 LLM 提供页面元素信息，从而做出决策。这种方式有几个显著优势：

- **无需多模态 LLM**：支持任何纯文本 LLM，包括 Qwen、GPT-4o-mini 等轻量级模型
- **Token 消耗更低**：避免了图片传输带来的高额 Token 成本
- **响应速度更快**：DOM 文本处理比图像识别快得多

### 3. 自备 LLM，灵活接入

Page Agent 采用 BYOLLM（Bring Your Own LLM）设计，你可以自由接入任意支持的 LLM 服务。例如接入阿里云通义千问：

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_API_KEY',
    language: 'zh-CN',
})

await agent.execute('点击登录按钮')
```

也支持 OpenAI、Anthropic 等主流 API。

### 4. Chrome 扩展 + MCP Server 双模式

对于更复杂的跨页面任务，Page Agent 提供了两个可选扩展：

- **Chrome 扩展**：支持跨标签页操作，适合需要同时在多个页面间协作的场景
- **MCP Server（Beta）**：允许外部 Agent 通过 Model Context Protocol 协议控制浏览器，为已有的 AI Agent 体系注入浏览器操控能力

### 5. 丰富的应用场景

Page Agent 定位清晰，主要面向以下场景：

- **SaaS AI Copilot**：在你的产品中嵌入 AI 副驾驶，用户只需说话即可完成操作
- **智能表单填写**：将繁琐的 ERP/CRM 表单填写流程简化为一句话
- **无障碍增强**：让视障用户通过语音或自然语言操控任何 Web 应用
- **跨页面 Agent**：结合 Chrome 扩展实现多页面协同任务

## 适用人群

| 人群 | 匹配度 | 说明 |
|------|--------|------|
| SaaS 产品经理 | ⭐⭐⭐⭐⭐ | 几行代码即可为产品增加 AI 交互能力 |
| 前端开发者 | ⭐⭐⭐⭐⭐ | 纯 TypeScript 实现，天然契合前端技术栈 |
| 企业 IT 管理员 | ⭐⭐⭐⭐ | 大幅简化内部系统（ERP/CRM）的操作门槛 |
| 无障碍开发 | ⭐⭐⭐⭐⭐ | 为 Web 应用提供全新的自然语言交互层 |
| AI Agent 开发者 | ⭐⭐⭐⭐ | 通过 MCP 协议为你的 Agent 增加浏览器操控能力 |

## 与同类工具对比

| 特性 | Page Agent | browser-use | Playwright + LLM | Selenium |
|------|-----------|-------------|-----------------|----------|
| 部署方式 | 纯前端 JS | Python 后端 | Python 后端 | Python 后端 |
| 是否需要后端 | 否 | 是 | 是 | 否 |
| 是否需要浏览器插件 | 否 | 否 | 否 | 否 |
| 是否需要无头浏览器 | 否 | 否 | 是 | 是 |
| 操作方式 | DOM 文本 | DOM 文本 + 截图 | 截图 + DOM | 选择器 |
| 多模态需求 | 否 | 可选 | 推荐 | 否 |
| Token 成本 | 低 | 中高 | 高 | 无 |
| 跨页面支持 | Chrome 扩展 | 需自行实现 | 需配置 | 需配置 |
| 上手难度 | 极低 | 中等 | 较高 | 中等 |
| GitHub Stars | 23K+ | 30K+ | 35K+ | 25K+ |

Page Agent 的核心差异化在于**极致的轻量化**——它把整个 Agent 塞进了一个前端 JS 库中，部署复杂度远低于其他方案。如果你只是想给现有 Web 应用加一个 AI 助手，Page Agent 几乎是零成本的选择。

## 如何使用

### 方法一：Demo 模式（最快体验）

1. 打开任意网页
2. 在浏览器控制台粘贴以下代码：

```html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.11.0/dist/iife/page-agent.demo.js" crossorigin="true"></script>
```

3. 对网页说："点击登录按钮"或"填写用户名"，Agent 会自动执行

> 注意：Demo 模式使用阿里提供的免费测试 LLM API，仅限技术评估使用。

### 方法二：NPM 安装（生产环境）

1. 安装依赖：

```bash
npm install page-agent
```

2. 在你的前端项目中引入并配置：

```javascript
import { PageAgent } from 'page-agent'

const agent = new PageAgent({
    model: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    apiKey: 'YOUR_DASHSCOPE_API_KEY',
    language: 'zh-CN',
})

// 监听用户输入
agent.onMessage((message) => {
    const result = await agent.execute(message)
    console.log(result)
})
```

3. 启动你的应用，即可通过自然语言操控页面

### 方法三：Chrome 扩展模式（跨页面）

1. 从 [Page Agent Chrome 扩展页面](https://alibaba.github.io/page-agent/docs/features/chrome-extension) 获取扩展
2. 安装到 Chrome 浏览器
3. 扩展支持在多个标签页之间进行协同操作

### 方法四：MCP Server 模式（对接已有 Agent）

1. 启动 Page Agent 的 MCP Server（Beta）
2. 在你的 AI Agent 框架中配置 MCP 客户端
3. 通过标准 MCP 协议发送浏览器操控指令

## 总结

Page Agent 是一个设计理念非常清晰的项目——**让每个网页都能听懂人话**。它避开了传统 Web 自动化方案对后端和无头浏览器的依赖，用纯前端 JavaScript 实现了完整的 GUI Agent 能力。

**优点：**
- 部署极简，一行代码即可上手
- 纯前端架构，无需额外基础设施
- 基于 DOM 文本而非截图，Token 成本低
- 支持任意 LLM，灵活性极高
- Chrome 扩展和 MCP Server 为进阶场景提供可能

**局限：**
- 目前主要面向单页面应用，复杂 SPA 的支持仍在完善中
- Demo LLM 仅限评估使用，生产环境需要自备 API Key
- Chrome 扩展和 MCP Server 仍处于 Beta 阶段

**推荐指数：⭐⭐⭐⭐⭐（5/5）**

对于任何希望为 Web 应用增加 AI 自然语言交互能力的团队来说，Page Agent 都是目前最值得关注的开源方案之一。尤其是它的纯前端架构，让部署成本降到了几乎为零的水平。如果你正在寻找一种轻量级的 AI Agent 方案来增强你的 Web 产品，Page Agent 绝对值得一试。

**项目地址：** https://github.com/alibaba/page-agent
**文档：** https://alibaba.github.io/page-agent/docs/introduction/overview
