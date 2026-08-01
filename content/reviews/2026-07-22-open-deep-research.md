---
title: 'Open Deep Research 评测：LangChain 出品的开源深度研究 Agent，性价比碾压闭源方案'
date: 2026-07-22T08:00:00+08:00
description: 'Open Deep Research 是 LangChain 团队开源的深度研究 Agent，支持多种 LLM 提供商和搜索工具，在 Deep Research Bench 排行榜上 RACE 得分达 0.4344，默认配置成本仅 $45.98。'
tags:
  - AI工具
  - 深度研究
  - Agent
  - 开源项目
  - LangChain
  - 工具评测
  - GitHub Trending
categories:
  - 工具评测
---

## 工具简介

**Open Deep Research**（仓库名 `langchain-ai/open_deep_research`）是由 LangChain 团队开发的开源深度研究 Agent，基于 LangGraph 构建。该项目目前在 GitHub Trending 持续霸榜，截至 2026 年 7 月已获得 **12,300+ Stars**、1,700+ Forks，采用 Apache 2.0 开源许可证。

Open Deep Research 是一个简单但高度可配置的深度研究 Agent，支持多种 LLM 提供商（OpenAI、Anthropic、Ollama 等）、多种搜索工具（Tavily、MCP 服务器等），并且能在 Deep Research Bench 排行榜上取得 RACE 得分 0.4344（综合排名 #6），与闭源的 Perplexity Pro、Google Deep Research 等产品性能相当。

一句话总结：**Open Deep Research 是一个零门槛部署的开源深度研究 Agent——用你喜欢的模型和搜索工具，生成高质量研究报告，成本可控、完全私有。**

## 核心功能

### 1. 多 LLM 提供商灵活切换

Open Deep Research 内部使用多个 LLM 承担不同任务：摘要模型（Summarization）、研究模型（Research）、压缩模型（Compression）和报告撰写模型（Final Report）。每个角色都可以独立指定模型，支持 OpenAI（GPT-4.1、GPT-5）、Anthropic（Claude Sonnet 4）、OpenRouter 以及本地 Ollama 模型。这意味着你可以为每个环节选择性价比最优的模型组合——比如摘要用小模型省钱，研究用大模型保证质量。

### 2. 多搜索工具集成

默认使用 Tavily 搜索 API，同时支持完整的 MCP（Model Context Protocol）兼容性，以及 Anthropic 和 OpenAI 的原生网络搜索。你可以根据需要接入 Google Search、Bing、Brave 等多种搜索引擎，甚至通过 MCP 连接自定义的数据源。

### 3. 结构化研究流程

Open Deep Research 采用经典的"计划-执行-反思"工作流：
- **规划阶段**：Agent 先理解你的研究问题，制定搜索策略
- **信息收集**：通过搜索工具获取大量相关资料
- **摘要压缩**：对搜索结果进行智能摘要，避免上下文溢出
- **报告生成**：综合所有信息，生成结构化的最终研究报告

### 4. 交互式 LangGraph Studio UI

启动后会自动打开 LangGraph Studio 可视化界面，你可以在浏览器中直接输入研究问题、查看 Agent 的思考过程、调整配置参数。这种交互式体验让你能实时监控研究进度，随时干预和调整研究方向。

### 5. 标准化评估体系

项目内置了 Deep Research Bench 评估框架，包含 100 个 PhD 级别的研究任务（50 个英文、50 个中文），覆盖科学、技术、商业、金融等 22 个领域。你可以用它来量化对比不同模型组合的效果，找到最适合自己场景的配置。

## 适用人群

- **研究人员/分析师**：需要快速完成文献综述、行业分析、竞品调研的深度工作者
- **开发者**：希望在自己的应用中集成深度研究能力的 AI 工程师
- **学生/学术工作者**：需要自动化文献检索和资料整理功能的研究生、博士生
- **企业团队**：需要定制化研究报告生成的市场、战略部门

## 与同类工具对比

| 特性 | Open Deep Research | Perplexity Pro | Google Deep Research | Claude Computer Use |
|------|-------------------|----------------|---------------------|--------------------|
| 开源 | ✅ 完全开源 | ❌ 闭源 | ❌ 闭源 | ❌ 闭源 |
| 部署方式 | 本地/API | SaaS | SaaS | SaaS |
| 模型灵活性 | 支持多提供商 | 仅限自有模型 | 仅限自有模型 | 仅限 Claude |
| 单次研究成本 | ~$0.5-$2 | 订阅制 $20/月 | 订阅制 $20/月 | 按 token 计费 |
| 数据隐私 | 完全私有 | 数据上传云端 | 数据上传云端 | 数据上传云端 |
| 自定义程度 | 极高 | 低 | 低 | 低 |
| 排行榜得分 | RACE 0.4344 | 未公开 | 未公开 | 未公开 |

Open Deep Research 的最大优势在于**完全开源 + 模型自由 + 成本可控**。如果你只需要偶尔做做研究，Perplexity Pro 的订阅制可能更省心；但如果你需要频繁研究、关注数据隐私、或者想深度定制研究流程，Open Deep Research 是更好的选择。

## 如何使用

### 步骤一：安装依赖

```bash
git clone https://github.com/langchain-ai/open_deep_research.git
cd open_deep_research
uv venv
source .venv/bin/activate
uv sync
```

> 推荐使用 `uv` 作为包管理器（比 pip 快 10-100 倍），如果没有安装可以先运行 `pip install uv`。

### 步骤二：配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你需要的 API Key：

```bash
# 模型配置（以 OpenAI 为例）
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# 搜索 API（默认使用 Tavily）
TAVILY_API_KEY=tvly-xxxxxxxxxxxx

# 可选：使用其他模型提供商
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
# OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxx
```

### 步骤三：启动 LangGraph Server

```bash
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

启动成功后会显示三个地址：
- API：http://127.0.0.1:2024
- Studio UI：https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- API Docs：http://127.0.0.1:2024/docs

### 步骤四：开始研究

在浏览器中打开 LangGraph Studio UI，在 `messages` 输入框中输入你的研究问题，点击 `Submit`。例如：

> "请帮我调研 2026 年 AI Agent 领域的最新进展，包括主要技术路线、代表性产品和未来趋势。"

Agent 会自动进行搜索、摘要、分析和报告生成，完成后会输出一份结构化的研究报告。

### 步骤五：自定义配置

在 Studio UI 的 "Manage Assistants" 标签页中，你可以调整各个角色的模型选择、搜索工具、最大迭代次数等参数，找到最适合自己需求的配置。

## 常见问题

**Q: 需要 GPU 吗？**
A: 不需要。Open Deep Research 本身是 Python 脚本，LLM 推理通过 API 调用完成。如果你想使用本地 Ollama 模型，则需要 GPU。

**Q: 一次研究大概花多少钱？**
A: 根据 Deep Research Bench 的测试数据，默认配置（GPT-4.1-mini + GPT-4.1）每次研究约花费 $0.5-$2，具体取决于研究问题的复杂度和搜索结果数量。

**Q: 支持中文研究吗？**
A: 支持。Deep Research Bench 专门包含 50 个中文研究任务，且模型本身支持多语言。

**Q: 可以部署到服务器上供团队使用吗？**
A: 可以。项目支持 LangGraph Platform 托管部署，也可以自行搭建 OAP（Open Agent Platform）实例。

## 总结推荐

Open Deep Research 是目前开源社区中**最成熟的深度研究 Agent 实现之一**。它由 LangChain 团队维护，代码质量高、文档完善、生态丰富。最大的亮点在于：

1. **模型无关**——不绑定任何特定 LLM 提供商，自由选择性价比最优的方案
2. **搜索灵活**——支持 Tavily、MCP、原生搜索等多种数据源
3. **成本透明**——没有订阅费，按 token 计费，单次研究成本可控
4. **评估完备**——内置标准化 benchmark，方便量化对比和优化

**推荐指数：⭐⭐⭐⭐⭐（5/5）**

对于需要深度研究能力的个人和企业来说，Open Deep Research 是目前开源方案中的首选。无论你是想自己做研究、开发研究类应用，还是仅仅好奇 AI Agent 能做到什么程度，都值得试一试。

---

- **GitHub**: https://github.com/langchain-ai/open_deep_research
- **在线 Demo**: https://oap.langchain.com
- **官方教程**: https://academy.langchain.com/courses/deep-research-with-langgraph
- **排行榜**: https://huggingface.co/spaces/Ayanami0730/DeepResearch-Leaderboard

---

想了解更多 AI 工具？浏览 [198007.xyz/tools](/tools/) 获取精选 AI 工具合集，或查看其他 [AI 工具评测](/reviews/)。

## 相关评测

- [**Palmier Pro 评测**](/reviews/2026-07-26-palmier-pro/) — YC 支持的 AI 原生视频编辑器，支持 MCP Agent 集成
- [**Nativ 评测**](/reviews/2026-07-25-nativ/) — macOS 原生本地 AI 运行环境
