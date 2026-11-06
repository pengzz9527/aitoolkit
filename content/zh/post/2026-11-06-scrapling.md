---
title: 'Scrapling 评测：98K Star 的 Python 爬虫框架，从单页请求到大规模爬取一气呵成'
date: 2026-11-06
tags: ['爬虫', 'Web Scraping', 'Python', '开源', '数据提取', '反爬', 'AI Agent', 'MCP']
categories: ['AI 工具评测']
description: 'Scrapling 把快速 HTTP 请求、隐身浏览器、强解析和并发爬虫塞进同一个 Python 包：能扛 Cloudflare 验证、能抓后台 API 流量、能把整个站点导出成干净 Markdown，还内置 MCP 服务器和 CLI 让 AI Agent 直接调用。本文拆解它的四大能力、与 Crawl4AI / Playwright 的分工，以及从入门到上线的完整路径。'
---

# Scrapling 评测：98K Star 的 Python 爬虫框架，从单页请求到大规模爬取一气呵成

**一句话简介**：Scrapling 是一个 Python 爬虫框架——单个 HTTP 请求、JS 渲染、反爬对抗、并发爬取、数据导出，全部装在一个包里，还内置 MCP 服务器和 CLI，让 AI Agent 也能直接上手。

## 工具概览

| 属性 | 信息 |
| --- | --- |
| 仓库地址 | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |
| GitHub 星标 | ⭐ 98,261 |
| Fork 数 | 10,292 |
| 创建时间 | 2024-10-13 |
| 最近更新 | 2026-11-05 |
| 许可证 | BSD 3-Clause |
| 最新版 | v0.5.1（2026-11-04 发布） |
| Python 要求 | ≥ 3.10 |
| 文档 | https://scrapling.readthedocs.io |
| 社区 | Discord / X @Scrapling_dev，文档提供简中、日、阿语等 10 种语言版本 |

Scrapling 从 2024 年 10 月创建，两年冲到 98K Star 并登上榜首，v0.5 大版本（2026-10-17）带来了 Spider 架构和 MCP 服务器——它已经不只是一个「requests 加强版」，而是把从抓取到导出的整条链路都收编了。

---

## 核心功能

### 1. 三档 Fetcher：按需求选难度

Scrapling 最核心的设计是**分层抓取**，不是所有页面都需要浏览器：

| Fetcher | 用途 | 成本 |
| --- | --- | --- |
| `Fetcher`（HTTP） | 静态页、API，纯 HTTP 请求 | 最低 |
| `DynamicFetcher` | 需要 JS 渲染、登录态、点击交互 | 中（起浏览器） |
| `StealthyFetcher` | 对抗 Cloudflare Turnstile / 反爬盾 | 最高（隐身浏览器） |

大部分任务用 HTTP 档就够了；只有页面是 SPA 或带人机验证时，才升级到 Dynamic / Stealthy。这比「全场景开浏览器」省得多资源。

### 2. 反爬对抗：不止浏览器伪装

Stealthy 档能处理 Cloudflare Turnstile 和 Interstitial 拦截，加上**持久会话**（登录态复用）和**后台 API 流量捕获**——后者是亮点：很多 SPA 的真正数据来自 XHR 请求，Scrapling 可以直接监听网络层拿到原始 JSON，跳过 DOM 解析。

### 3. 解析能力：CSS / XPath / 自适应元素追踪

- 支持 CSS 选择器、XPath、正则、纯文本搜索；
- **自适应元素追踪**：页面改版后元素挪个位置，选择器还能跟着找到；
- **相似元素匹配**：「找出所有长得像卡片的块」这类模糊需求能直接写；
- **干净 Markdown 输出**：整页转成给 LLM / RAG 用的结构化 Markdown，去噪后直接入库。

### 4. Spider：并发爬虫骨架

内置 `Spider` 类，写起来像 Scrapy，但更轻：

```python
class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    async def parse(self, response):
        for q in response.css('.quote'):
            yield {"text": q.css('.text::text').get(),
                   "author": q.css('.author::text').get()}

result = QuotesSpider().start()
result.items.to_json("quotes.json")
```

自带**并发、代理轮换、自动重试、AutoThrottle（自动限速）、暂停/续跑（pause/resume）、流式处理**，导出 JSON / JSONL / CSV / XML 一行搞定。有现成模板可套用。

### 5. MCP 服务器 + CLI + Agent Skill：给 AI 用

这是 Scrapling 和传统爬虫框架最大的差异：

- **MCP 服务器**：让 Claude Code / Cursor / Hermes 这类 AI Agent 直接「浏览网页 + 提取数据」，Agent 说人话就能抓数据；
- **CLI 与交互 shell**：`scrapling fetch` 一行命令在终端抓页面，不用写 Python；
- **Agent Skill**：官方发布了 Clawhub 上的 Skill 包，Agent 开箱即用。

爬虫能力第一次成了 LLM 的一等公民工具。

---

## 适合谁用

**适合：**

- **Python 爬虫开发者**：需要比 requests 多一点（反爬、JS、会话），又不想上 Scrapy 那么重的工程，Scrapling 的甜蜜点就在这里；
- **AI 数据管道 / RAG 团队**：要批量抓网页转 Markdown 喂给模型，干净 Markdown 输出 + 并发 Spider 是现成的；
- **AI Agent 开发者**：给 Agent 接网页抓取能力，MCP 服务器直接配进 Claude Code / Codex，不用写胶水代码；
- **终端重度用户**：偶尔抓个页面，`scrapling` CLI 比打开 IDE 快。

**不适合：**

- **要跑分布式集群的超大规模采集**：Scrapy 的分布式生态（Scrapy-Redis 等）仍然更成熟，Scrapling 的 Spider 是单机并发为主；
- **纯浏览器自动化**：如果你的核心需求是「自动点按钮填表」，Playwright 本身更直接，Scrapling 是「抓取数据」而非「操作浏览器」；
- **Node.js 技术栈**：Scrapling 是纯 Python 项目。

---

## 与同类工具对比

| 维度 | Scrapling | Crawl4AI | Playwright | Scrapy |
| --- | --- | --- | --- | --- |
| **定位** | 全链路抓取（请求→解析→爬取→导出） | LLM 友好型网页转 Markdown | 浏览器自动化框架 | 工业级分布式爬虫 |
| **JS 渲染** | ✅ 内置浏览器 | ✅ 内置 | ✅ 核心能力 | ❌ 需插件 |
| **反爬对抗** | ✅ 隐身浏览器 + Cloudflare 处理 | ✅ 隐身浏览器 | ⚠️ 需自己做指纹 | ❌ 靠中间件 |
| **后台 API 流量捕获** | ✅ 这是独有卖点 | ⚠️ 部分支持 | ⚠️ 需手动监听 | ❌ |
| **并发爬虫** | ✅ 内置 Spider + 代理轮换 | ⚠️ 基础 | ❌ | ✅ 最成熟 |
| **暂停/续跑** | ✅ | ⚠️ | ❌ | ✅ |
| **数据导出** | ✅ JSON/JSONL/CSV/XML 一行 | ⚠️ 主要输出 Markdown | ⚠️ 自己写 | ⚠️ 需 pipeline |
| **MCP / AI Agent 集成** | ✅ 官方 MCP 服务器 | ✅ 自带 MCP | ⚠️ 社区方案 | ❌ |
| **工程重量** | 中（单包安装） | 中 | 轻 | 重 |
| **典型用户** | 想一套工具干完事的人 | RAG / LLM 数据管道 | 自动化测试 / 填表 | 大规模采集团队 |

一句话分工：**只是操作浏览器 → Playwright；喂 LLM 的干净数据 → Crawl4AI；大规模分布式采集 → Scrapy；从抓一个页面到铺一个站全都要、还顺手给 AI Agent 用 → Scrapling。**

两者（Scrapling 和 Crawl4AI）在「LLM 友好抓取」上有重叠，Scrapling 的优势在反爬对抗的深度和 API 流量捕获，Crawl4AI 的优势在 Markdown 处理策略的精细度（BM25 过滤等）。实际项目可以混用。

---

## 如何使用

### 第一步：安装

```bash
pip install scrapling
# 需要浏览器渲染/隐身模式时，安装浏览器组件：
scrapling install
```

### 第二步：抓一个静态页面（HTTP 档）

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
print(quotes)
```

### 第三步：需要 JS 渲染时切 Dynamic

```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.get('https://example.com/spa/')
data = page.css('.item .price::text').getall()
```

### 第四步：遇到 Cloudflare 验证上 Stealthy

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.get('https://protected-site.com/')
```

### 第五步：写 Spider 铺整站并导出

参考上面「核心功能」第 4 节的例子，`result.items.to_json()` / `.to_csv()` 直接落盘，支持代理列表、重试次数、AutoThrottle 参数。

### 第六步：让 AI Agent 直接用（MCP）

把 Scrapling 的 MCP 服务器加进你的 Agent（以 Claude Code 为例）：

```bash
claude mcp add scrapling -- scrapling mcp
```

之后 Agent 就能直接说「把这个页面的价格表抓成 JSON」，底层调用 Scrapling 完成抓取。终端党也可以直接 `scrapling fetch URL` 一行搞定。

---

## 几个需要留意的地方

**v0.x 阶段的 API 波动**：项目处于 0.5.x，大版本之间（0.4 → 0.5 跨度半年）接口有调整，升级前看一眼 changelog。好的一点是 open issue 只有 14 个，维护状态健康。

**隐身模式的重度依赖**：`scrapling install` 会装完整浏览器，体积不小；纯 HTTP 场景可以只装基础包。Stealthy 档对 Cloudflare 的对抗是「能过」但非「永远过」，对手更新防护后可能失效，生产环境建议配代理轮换。

**Spider 不是 Scrapy 的替代**：它的并发模型是单机 asyncio，没有分布式部署方案。几万个页面量级的任务用它完全没问题，上百万级还是 Scrapy 的领地。

**数据合规**：抓什么、怎么用，始终要过一遍目标站点的服务条款和本地法规。Scrapling 的 AutoThrottle 默认限速是好设计，但别为了产量关掉——被封 IP 是小事，合规问题是事故。

---

## 总结

| 维度 | 评价 |
| --- | --- |
| **创新性** | ★★★★★ API 流量捕获 + MCP 集成 + Agent Skill，把爬虫做成了 AI 时代的标准件 |
| **实用性** | ★★★★★ 从一行命令到整站管道都覆盖，分层设计不浪费资源 |
| **工程质量** | ★★★★☆ 两年 98K Star，issue 数极低，10 种语言文档，0.x 版本的迭代节奏可以接受 |
| **文档** | ★★★★☆ readthedocs 完整，简中 README 齐全；CLI / MCP 章节对新用户稍显进阶 |
| **上手难度** | ★★★★☆ `pip install` + 三行代码出结果，门槛极低 |
| **推荐指数** | **★★★★★（5/5）** |

Scrapling 的聪明之处在于**不逼你选**：一个包覆盖从「curl 替代品」到「整站爬虫」的全部档位，再顺手把 MCP 服务器和 CLI 塞进去——它既是你自己写爬虫的工具，也是你 AI Agent 的手和眼睛。爬虫这块，Python 生态过去十年没有过一个「一个包全干完」的项目，Scrapling 是第一个。

- **GitHub**：https://github.com/D4Vinci/Scrapling
- **文档**：https://scrapling.readthedocs.io
- **快速开始**：`pip install scrapling`，三行代码出第一份数据
