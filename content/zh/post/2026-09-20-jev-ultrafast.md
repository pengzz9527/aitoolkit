---
title: 'Jev Ultrafast：浏览器自动化新速度标杆，7秒完成航班搜索'
date: 2026-09-20
tags: ['Jev Ultrafast', 'Browser Agent', 'AI 自动化', 'TypeSafe', '开源工具', 'LLM', '浏览器操作']
categories: ['AI 工具评测']
description: 'Jev Ultrafast 是 browser-use 团队开源的极速浏览器代理，结合 TypeSafe Jev 模型实现结构化决策，7秒完成 Google Flights 搜索，GitHub 星标 9,300+。'
---

# Jev Ultrafast：浏览器自动化新速度标杆，7秒完成航班搜索

**Jev Ultrafast**（browser-use/jev-ultrafast）是一款由 [browser-use](https://github.com/browser-use) 团队于 2026 年 9 月 16 日开源的极速浏览器自动化代理。它将 TypeSafe 的 **Jev** 结构化决策模型与浏览器操作深度融合，在保持自然语言目标驱动的同时，实现了远超传统方案的执行速度——Google Flights 航班搜索任务仅需约 7 秒即可完成。

目前 Jev Ultrafast 在 GitHub 上已获得 **9,360+ 星标**，使用 Python 编写，采用 MIT 许可证开源。

- **GitHub 星标**：9,360+
- **GitHub 仓库**：https://github.com/browser-use/jev-ultrafast
- **官方主页**：https://browser-use.com
- **文档中心**：https://docs.typesafe.ai/introduction
- **许可证**：MIT
- **语言**：Python
- **生态**：配合 Browser Harness 实现 Chrome 远程调试连接

---

## 核心功能

### 1. 动态索引动作空间

与传统浏览器代理每次返回完整页面截图或 DOM 不同，Jev Ultrafast 将页面元素组织为带编号的索引表：

```
[1] button    Change ticket type · Round trip
[2] combobox  Where from?        · San Francisco
[3] combobox  Where to?          · empty
[4] textbox   Departure          · empty
...
```

每个操作（CLICK、TYPE_TEXT、SELECT、SCROLL_UP、SCROLL_DOWN、WAIT、DONE、BLOCKED）只针对兼容元素类型，从源头上减少了模型推理的错误空间。

### 2. 单次请求双决策，一次网络往返

Jev 的核心创新在于将"选操作"和"选目标"合并到同一次 TypeSafe API 调用中：

```
page → element table → operation (click_target / type_text_target / select_target)
                                  ↓
                         匹配对应目标
                                  ↓
                         CLICK [7] ──→ 浏览器
                         TYPE_TEXT [3] ──→ 小 LLM 生成文本 → 浏览器
```

这一设计使浏览器代理的平均请求数从传统方案的 22 次降至 17 次，浏览器协议调用从 1,092 次骤降至 101 次，**整体速度提升约 25%**。

### 3. 文本生成仅在小模型中完成

Jev 本身负责结构化决策（选哪个操作、点哪个元素），而真正的文本输入（如城市名称）则由小型 LLM（如 inception/mercury-2.5）完成，且仅在 `TYPE_TEXT` 操作时触发。这大幅降低了 token 消耗——一次航班搜索任务文本部分仅花费约 $0.00006272。

### 4. 无截图默认循环

与大多数依赖屏幕截图的浏览器代理不同，Jev Ultrafast 的默认循环不传截图给模型，而是直接提供结构化的元素表。截图仅在 Inspector 调试界面中可选启用，通过独立录屏流实现可视化。

### 5. 丰富的验证与故障处理

系统内置了完善的点击守卫机制：检查文档状态、表单值、目标节点和周边上下文；对动画导致的误判自动过滤；对原生下拉选择器的中断进行特殊处理。任务结束后还会进行独立的结果验证。

---

## 适用人群

- **AI Agent 开发者**：需要高并发、低延迟的浏览器自动化能力来构建可靠的工作流
- **RPA 工程师**：希望用自然语言替代传统录制回放，实现更灵活的业务流程自动化
- **研究人员**：对 Agent 决策效率和结构化输出感兴趣，探索 LLM + 结构化模型的新范式
- **效率工具爱好者**：想体验"一句话完成航班搜索"这类炫技但实用的场景

---

## 与同类工具对比

| 维度 | Jev Ultrafast | browser-use 原版 | Selenium | Puppeteer |
|------|-------------|----------------|----------|-----------|
| 开源程度 | ✅ MIT 完全开源 | ✅ MIT 完全开源 | ✅ 开源 | ✅ 开源 |
| 自托管 | ✅ 本地运行 | ✅ 本地运行 | ✅ | ✅ |
| 自然语言目标 | ✅ 一句话驱动 | ✅ 一句话驱动 | ❌ 需写脚本 | ❌ 需写脚本 |
| 执行速度 | ⭐ 7s（航班搜索） | ~9.5s（同任务） | 不适用 | 不适用 |
| 无需截图 | ✅ 结构化元素 | ⚠️ 可选 | N/A | N/A |
| 结构化输出 | ✅ TypeSafe 原生 | ⚠️ 部分支持 | ❌ | ❌ |
| 学习曲线 | 中等 | 中等 | 较高 | 中等 |
| 适用场景 | 高速自动化、Agent | 通用浏览器自动化 | 传统测试 | 爬虫、测试 |

Jev Ultrafast 的独特价值在于**速度 + 结构化决策**的组合：它不是简单地让大模型看图打字，而是通过类型化提问让模型在有限动作空间内做选择，从而大幅降低推理延迟和错误率。

---

## 如何使用

### 方式一：快速上手（CLI 交互模式）

```bash
# 克隆仓库
git clone https://github.com/browser-use/jev-ultrafast.git
cd jev-ultrafast

# 安装依赖（需要 uv）
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入以下密钥：
# TYPESAFE_API_KEY=your-typesafe-key
# TEXT_MODEL_API_KEY=your-openrouter-key

# 启动交互界面
uv run jev
```

打开 http://127.0.0.1:8766，点击 **"Start demo → Run automatically"** 即可观看自动化演示。Inspector 面板会显示每个元素的编号、操作概率、目标概率和执行动作。

### 方式二：Python 编程调用

```python
from jev_ultrafast import Agent

with Agent(
    "https://www.google.com/travel/flights?hl=en",
    "Find one-way flights from Zurich to London on September 20, 2026, "
    "for one adult in economy. Stop when matching flight options are visible.",
) as agent:
    for state in agent.run():
        print(state["elapsed_ms"], state["status"])
```

保存为 `search_flights.py`，然后运行：

```bash
uv run --env-file .env python search_flights.py
```

### 方式三：命令行示例任务

仓库内置了多个示例，可直接运行：

```bash
# 航班搜索（完成后保持浏览器打开）
uv run --env-file .env python examples/flights.py --keep-open

# Wikipedia 文章查找
uv run --env-file .env python examples/run.py \
    --url https://en.wikipedia.org/wiki/Main_Page \
    --goal 'Find and open the Wikipedia article about Gödel'\''s incompleteness theorems.'
```

### 前置准备

- **Chrome 浏览器**：需允许远程调试，运行 `uv run browser-harness --doctor` 诊断连接
- **TypeSafe API Key**：在 https://console.typesafe.ai 申请
- **文本模型 Key**：推荐使用 OpenRouter，也可配置 Gemini、GLM、DeepSeek 等 OpenAI 兼容端点

---

## 总结

Jev Ultrafast 代表了浏览器自动化 Agent 的一个新方向：**用结构化决策替代纯视觉理解，用类型化提问替代自由生成**。它并非追求功能全覆盖，而是在特定场景（表单填写、链接导航、列表筛选）下做到了极致速度。

对于需要高速、低成本执行浏览器任务的开发者来说，Jev Ultrafast 是一个极具吸引力的选择。如果你正在构建需要频繁操作网页的 AI Agent，或者单纯对"一句话搜索航班"这类实用场景感兴趣，都值得试一试。

**推荐指数：★★★★☆**

- 优点：开源免费、执行速度极快、结构化决策降低错误率、成本极低
- 不足：功能相对聚焦（暂不支持 Canvas、上传、新标签页等复杂场景）；需要 TypeSafe API Key 才能完整使用；文档和示例相对较新，社区资源有限

---

喜欢这篇评测？浏览 [198007.xyz 工具集](/tools/) 发现更多 AI 自动化与浏览器操作工具。
