---
title: 'Firecrawl 评测：给 AI Agent 装一个「世界知识接口」——搜索、抓取、交互一个 API，外加 550+ 数据源'
date: 2026-11-25
tags: ['firecrawl', 'Web Scraping', 'AI Agent', 'MCP', 'RAG', '结构化数据', '开源工具', '数据提供商']
categories: ['AI 工具评测']
description: 'Firecrawl 是开源 Web 数据 API（约 20 万星，AGPL-3.0）：Search/Scrape/Crawl/Map/Parse/Interact 六个核心端点 + 自主 /agent 研究 + 550+ 数据源 Alexandria，输出干净 Markdown 与 schema 化 JSON；云、本地单二进制、自托管三种部署形态，AI Agent 经 MCP、CLI、SDK 任选接入。'
---

# Firecrawl 评测：给 AI Agent 装一个「世界知识接口」——搜索、抓取、交互一个 API，外加 550+ 数据源

**Firecrawl** 的官方定位一句话：**「让 Agent 更聪明的知识基础设施」（context API for AI agents）**。它把 AI Agent 拿真实世界数据要过的五道关——搜、抓、爬、交互、自主研究——打包成一套 API，输出 LLM 直接可吃的**干净 Markdown** 或**按你 schema 填好的 JSON**，把 JS 渲染、动态内容、PDF 这些脏活全替你干完。2026 年 9 月又上线 **Alexandria**：550+ 个数据提供商（政府、证券、电商、论文）接进同一个 API，Agent 搜的时候顺带就能「发现并运行」这些数据工具。

它 2024 年 4 月开源，两年冲到 **约 20.6 万星标**（2026-11-25 当日在 GitHub Trending 在榜），主仓 AGPL-3.0、SDK 为 MIT，是目前 Agent 数据接入赛道体量最大的开源项目之一。

- **GitHub 星标**：≈206,000（Trending 在榜）；MCP 服务器子仓 7.9K 星
- **GitHub 仓库**：https://github.com/firecrawl/firecrawl
- **官网 / 文档**：https://firecrawl.dev · https://docs.firecrawl.dev
- **许可证**：AGPL-3.0（主仓），SDK 与 MCP 服务器为 MIT
- **三种形态**：Firecrawl Cloud（firecrawl.dev 托管）/ Firecrawl Local（单二进制跑本机，自带 MCP 服务器）/ 自托管完整服务端（apps/api）
- **免费额度**：每月 1,000 credits（约 1,000 页），无需信用卡；付费 $19/月起
- **接入方式**：REST API、Python/Node SDK、官方 MCP 服务器、官方 CLI、Claude Code/Cursor 插件、ChatGPT 插件

---

## 核心功能

### 1. 六个核心端点，一条流水线打包

| 端点 | 干什么 | 计费（credits） |
|---|---|---|
| **Search** | 全网找新鲜来源，一次调用连结果全文一起拿回 | 2 / 10 条结果 |
| **Scrape** | 单 URL → 干净 Markdown / JSON / HTML / 截图，JS 渲染、缓存（最长 2 天）自动处理 | 1 / 页 |
| **Crawl** | 从起点 URL 跟链接爬整站 | 1 / 页 |
| **Map** | 不抓内容，只列出站里全部 URL（先探路再精抓） | 1 / 次调用 |
| **Parse** | PDF、文档 → 干净可用文本 | +1 / PDF 页 |
| **Interact** | 开一个真实浏览器会话：点击、填表、滚动、跨动态页面操作 | 2 / 浏览器分钟（带 prompt 的会话 7 / 分钟） |

再加 **Monitor**（定时检查最多 50 个目标，页面变了推 webhook/邮件，可写「降价到 $150 以下才提醒」这种自然语言目标，7 credits/页/次检查）和 **Agent**（见下）。生产工作流通常是 Search 找源 → Scrape 取文 → Interact 补动态交互，两三个端点串起来。

### 2. LLM-ready 输出：不写 CSS 选择器，不猜页面结构

Scrape 的 JSON 格式让你传 **JSON schema 或一句自然语言 prompt**，模型读渲染后的页面内容来填字段，站点 HTML 改版也不影响字段稳定。SDK 支持 Pydantic（Python）/ Zod（Node）做类型安全定义。一个 URL 同时出 Markdown + JSON 截图的写法（官方 Firecrawl 101 示例）：

```python
result = app.scrape(
    "https://example.com/pricing",
    formats=["markdown", {"type": "json", "prompt": "Extract all plan names and monthly prices"}]
)
print(result.markdown)   # 整页干净 Markdown
print(result.json)       # {"plans": [{"name": "Starter", "price": "$19/mo"}, ...]}
```

JSON / question（就页面提问）/ highlights（挑相关段落）/ PII 脱敏 等高级格式各 +4 credits/页，按需开。

### 3. /agent：不给你 URL，描述要什么它自己去找

这是 2026 年的主打能力：**只传 `prompt` 一个必填参数**，Agent 自主搜索、导航、跨站深挖，几分钟干完人工数小时的端到端数据采集。官方定位是「数据界的 deep research」。

```bash
curl -X POST 'https://api.firecrawl.dev/v2/agent' \
-H 'Authorization: Bearer ***' \
-H 'Content-Type: application/json' \
-d '{ "prompt": "Find the pricing plans for Notion" }'
```

- 跑在 **Spark 2** 模型上（比上一代更快更便宜，精度相当），可传 `effort: low/medium/high` 控制思考深度；
- **动态计费**：简单单页提取几十 credits，复杂跨域研究几百 credits；单次默认 `maxCredits` 上限 2,500，触顶返回 `stopReason: "credit_limit_reached"` 且**失败不扣费**；
- 每天 **5 次免费运行**（playground 和 API 通用），官方建议大批量任务按类目/地区拆成每次 3–5 个 URL 分批跑。

### 4. Alexandria：550+ 数据提供商，「搜索即发现」

2026 年 9 月上线的数据库：2.5 亿+ 人物、7,500 万+ 公司、4,100 万+ 研究论文，外加 SAM.gov、SEC EDGAR、Grants.gov、各州企业注册库，以及 Shopify、Walmart、Best Buy、Target、Home Depot、IKEA 等零售商。Agent 在 `/search` 结果里**顺带看到可用的数据工具**（输入参数、价格都可见），免费发现，运行才扣该工具的 credits——把「找数据」从人肉翻 550 个站点变成一次搜索。

### 5. 云 / 本地 / 自托管三种形态，接入面全

- **Cloud**（默认）：什么机器都不用管，速率限制 `/scrape`、`/map`、`/search` 各 10 req/min，`/crawl`、`/agent`、`/interact` 各 2 req/min；
- **Firecrawl Local**：一个二进制跑在本机，网页转 Markdown + 本地 API + MCP 服务器，隐私敏感场景不上云；
- **自托管**：`apps/api` 完整服务端（队列、worker、数据库），数据全量自控；
- **接入**：官方 MCP 服务器（`https://mcp.firecrawl.dev/v2/mcp` 托管端点，**无 key 也能免费跑 scrape/search/parse**，OAuth 或 API key 解锁全量 34 个工具）、官方 CLI、Python/Node SDK、Claude Code / Cursor / ChatGPT 插件。Agent 自己也能读 `firecrawl.dev/agent-onboarding/SKILL.md` 完成自助接入。

---

## 适用人群

- **做 RAG / 知识库 / Agent 的团队**：网页、PDF、论文、政府数据一个 API 进上下文，Markdown 直喂 LLM 不用自己写解析管线；
- **用 Claude Code / Cursor 的开发者**：MCP / CLI 一键接入，Agent 直接「上网调研」，连 `SKILL.md` 自助引导都有；
- **电商与价格监控**：Monitor + `product` 格式 + Alexandria 零售商源，黑五价格追踪、竞品价格告警是官方主打 recipe；
- **市场 / 竞争情报**：`/agent` 描述一句「找头部 5 家 CRM 的定价」即可跨站采集，配 Alexandria 的公司库做线索挖掘；
- **隐私合规团队**：自托管 + 零数据保留（ZDR）选项，数据不落第三方（ZDR 请求有附加 credits）。

**不太适合：**

- **纯本地零云且要全功能**：Firecrawl Local 单二进制没有 Search / Alexandria，完整能力在 Cloud；自托管全服务端又偏重；
- **非开发者**：API / CLI / MCP 全要技术栈，没有图形界面；
- **一次性抓个网页**：注册、装 SDK、扣额度，不如直接 curl 一条；
- **AGPL 敏感场景**：自托管完整服务端是 AGPL-3.0，商业内嵌要法务过一下。

---

## 与同类工具对比

| 维度 | Firecrawl | Crawl4AI（本栏目评测过） | Apify | Jina Reader |
|---|---|---|---|---|
| 形态 | 云 API + 本地单二进制 + 自托管 | 开源库，纯本地 | Actor 市场平台（Crawlee 开源、平台闭源） | 单用途 URL→文本 API |
| Agent 友好 | **MCP/CLI/插件全，prompt 式 /agent 自主取数** | 库形态，代码调用 | 需挑 Actor、管资源 | 一行 curl 出文本 |
| 结构化提取 | **schema/prompt 填 JSON，不依赖选择器** | LLM/规则提取 | AI Web Scraper（含 LLM tokens） | 无 |
| 数据源广度 | **550+ 提供商 Alexandria（政府/证券/电商/论文）** | 只有公开网页 | 数千个 Actor 各付各费 | 只有网页 |
| 动态交互 | **Interact 浏览器会话（点击/填表/滚动）** | 无内置浏览器 | 部分 Actor 有 | 无 |
| 计费 | **统一 credit 池，价格可预测**（1 credit≈1 页） | 免费 | 计算单元 + 按事件 + 存储，各 Actor 不同 | 免费额度 + 按量 |
| 隐私 | 自托管 / ZDR / Local 三选一 | 全本地 | 平台托管 | 平台托管 |

结论：Crawl4AI 赢在纯本地零成本，Apify 赢在长尾站点 Actor 覆盖，Jina 赢在极简。Firecrawl 切的是**「Agent 要一个接口拿全部数据」**的地：credit 池计费可预测、prompt 式提取不依赖选择器、Alexandria 把政府/证券/电商数据并进同一个入口，这三点是同类里独有的组合。短板：非本地全功能需上云，credit 计费对高频 JSON 提取/浏览器分钟数要盯着。

> ⚠️ 三个要留意的点：
> 1. **成本结构**：JSON/question/highlights 各 +4 credits/页、Interact 带 prompt 会话 7 credits/分钟、Agent 单次动辄几百 credits——用 `maxCredits` 封顶，大批量任务拆 3–5 URL 一批；
> 2. **速率限制**：`/crawl`、`/agent`、`/interact` 只有 2 req/min，突发批量要用 batch scrape 而不是循环单发；
> 3. **MCP 无 key 端点能力有限**：`mcp.firecrawl.dev/v2/mcp` 免 key 只有 scrape/search/parse 三件套且限速，crawl/map/agent 必须配 key。

---

## 如何使用

### 第一步：注册拿 API Key（免费 1,000 credits/月，无需信用卡）

firecrawl.dev 注册 → 控制台复制 `fc-` 开头的 key。每月 1,000 credits ≈ 1,000 页基础抓取，个人试用完全够。

### 第二步：Python SDK 三行上手

```python
pip install firecrawl-py

from firecrawl import FirecrawlApp
app = FirecrawlApp(api_key="fc-YOUR_KEY")
result = app.scrape("https://docs.firecrawl.dev", formats=["markdown"])
print(result.markdown[:500])
```

### 第三步：接入 MCP（Claude Code / Cursor / 任意 MCP 客户端）

托管端点，免 key 三件套也能先用：

```json
{
  "mcpServers": {
    "firecrawl": {
      "url": "https://mcp.firecrawl.dev/v2/mcp",
      "headers": { "Authorization": "Bearer fc-YOUR_KEY" }
    }
  }
}
```

不配 key 也能跑 scrape/search/parse（限速）；配了 key（或走 `/v2/mcp-oauth` 登录）解锁 crawl、map、interact、agent、monitor 全量 34 个工具。也可以自托管 `firecrawl/firecrawl-mcp-server`。

### 第四步：让 Agent 自主研究（/agent）

对话里一句话即可，Agent 自己决定搜什么、抓什么：

> 「找头部 5 家 CRM 的定价页，按公司、起步价、企业版价格、试用政策整理成表格。」

内部就是 `/agent`：prompt 必填、schema 可选、`effort` 控制思考深度、`maxCredits` 封顶。每天 5 次免费。

### 第五步：CLI + 官方 skills（终端党）

```bash
npm install -g firecrawl-cli
npx -y firecrawl-cli@latest init -y --browser   # 装 CLI + 认证 + 给检测到的 coding agent 装 skills
firecrawl search "firecrawl pricing"
firecrawl scrape https://example.com
firecrawl x download https://docs.firecrawl.dev --limit 20 -y   # 整站落本地
```

`firecrawl setup workflows` 还能装官方预置 recipe（lead gen、deep research、SEO audit、知识库构建）。

### 第六步（可选）：本地 / 自托管

隐私敏感就装 **Firecrawl Local** 单二进制：本机出 Markdown + 本地 API + MCP，不碰网络。数据全自控则从 `apps/api` 部署完整服务端（含队列、worker、数据库，AGPL-3.0）。

---

## 总结

Firecrawl 回答的问题是：**Agent 要真实世界的数据，凭什么要自己拼五个工具？** 它的方案是「六个端点 + 自主 /agent + 550+ 数据源 Alexandria + 统一 credit 池 + 云/本地/自托管三形态」，把搜索、渲染、结构化提取、动态交互、监控全部收进一个 API，且对 Agent 生态（MCP、CLI、插件、SKILL.md 自助接入）铺得比同类全。2026 年 20 万星、当日 Trending 在榜，是这个赛道事实上的标准件。对个人和团队，免费 1,000 credits/月足够把 RAG 管线的「取数」环节直接外包给它；对 Agent 开发者，prompt 式 JSON 提取 + /agent + Alexandria 的组合目前没有全功能替代品。

**扣分点：**

- **全功能离不开云**：Search / Alexandria 只在 Cloud，Local 单二进制是阉割版，自托管全服务端偏重；
- **credit 计费要盯着**：高级格式 +4/页、Interact 7/分钟、Agent 动态几百/次，不设 `maxCredits` 容易超预算；
- **限速偏低**：crawl/agent/interact 各 2 req/min，重批量场景需要排批；
- **AGPL-3.0**：商业内嵌自托管版本需要法务评估。

**推荐指数：⭐⭐⭐⭐☆（4/5）**

- **做 RAG / Agent 的开发者** → **直接换掉手写抓取管线**，MCP 或 SDK 二选一接入；
- **Claude Code / Cursor 用户** → `init` 一条命令装 CLI + skills，Agent 调研类任务全交给它；
- **电商 / 竞情团队** → Monitor + Alexandria 零售商源，价格告警与线索挖掘开箱即用；
- **纯本地零云且要全功能** → 选 Crawl4AI 自组管线，Firecrawl 不是给这个场景的。
