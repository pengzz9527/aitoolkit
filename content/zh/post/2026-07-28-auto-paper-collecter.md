---
title: 'auto-paper-collecter 评测：你的私人学术雷达，让 AI 替你读论文'
date: 2026-07-28T08:00:00+08:00
description: 'auto-paper-collecter 是一款由 OvOhao 开源的 LLM 驱动的学术文献自动聚合工具，支持多源检索、智能摘要和个性化推送，已在 GitHub 上收获 54+ Star，并上架 SkillHub 平台。'
tags:
  - AI工具
  - 科研辅助
  - 开源项目
  - Hugging Face
  - GitHub Trending
  - 自然语言处理
categories:
  - 工具评测
---

## 一句话介绍

**auto-paper-collecter** 是由开发者 OvOhao 打造的一款轻量级、自托管的学术文献自动聚合工具，主打"私人学术雷达"概念——通过 LLM 联想扩展和多源检索，每天自动帮你从 arXiv、Crossref、Semantic Scholar 等平台抓取最新论文，并用中文生成简洁摘要，让你的研究前沿跟踪从此不再费力。目前已上架 **SkillHub** 平台，获得社区关注 ⭐ **54+ Star**。

## 它是什么？

在快节奏的科研工作中，跟踪最新文献是一件令人头疼的任务：arXiv 每天新上百篇论文，关键词搜索容易漏掉同义表达，更别提还要过滤掉跨领域的噪声结果。**auto-paper-collecter** 正是为了解决这个问题而生——它是一个用 Python 编写的单页 Web 应用，前后端同源，无需构建即可开箱使用。

该工具采用 **"LLM + 多源检索"** 的核心架构：你先输入关心的几个关键词，程序会用 LLM 进行联想式扩展搜索（例如搜"C2Rust"时也会匹配"C-to-Rust translation"），然后从多个学术数据源并行抓取相关论文，再用 LLM 过滤掉不相关的结果、生成中文摘要，最终呈现在一个漂亮的网页仪表盘中。

项目于 2026年6月25日首次发布，2026年6月27日更新至 v1.1，增加了移动端适配、深色模式、反馈学习和多渠道推送等功能。目前已开源并采用 **MIT 许可证**，GitHub 仓库地址为 [https://github.com/OvOhao/auto-paper-collecter](https://github.com/OvOhao/auto-paper-collecter)，同时在 SkillHub 平台 ([https://skillhub.cn/skills/auto-paper-collecter](https://skillhub.cn/skills/auto-paper-collecter)) 上架，方便直接安装使用。

## 核心功能

### 1. 多源聚合检索

auto-paper-collecter 支持从 **7个数据源** 同时获取论文信息：

| 数据源 | 内容类型 | 说明 |
|--------|---------|------|
| arXiv | 预印本 | 计算机领域主力源 |
| Crossref | 期刊/会议元数据 | 含 IEEE·ACM，仅提供摘要 |
| Semantic Scholar | 综合学术检索 | 自带 TLDR，限定计算机领域 |
| GitHub | 代码仓库 | 追踪与主题相关的实现 |
| HuggingFace | 热门模型/论文 | 与 arXiv 互补 |
| Papers with Code | 论文 + 代码 | 公共 API 可用时生效 |
| RSS | 学术新闻博客 | 可自定义订阅源 |

所有来源的数据会自动去重合并，确保你不会重复看到同一篇论文。

### 2. LLM 智能抓取（联想扩展）

这是 auto-paper-collecter 最核心的亮点。传统检索只匹配字面关键词，而该工具利用 LLM 做"**联想扩展**"——当你在搜索框中输入 `C2Rust` 时，系统会自动联想到 `C-to-Rust translation`、`migrating legacy C to Rust` 等相关查询，大幅召回遗漏的论文。同时，LLM 还能理解跨领域的语义差异，自动过滤掉"医学中的 translation"或"金融中的 AI"这类噪声结果，只保留真正切题的计算机领域论文。

### 3. 中文摘要生成

每篇抓取到的论文，系统会用 LLM 自动生成一句**中文总结（TL;DR）**，包含方法说明和核心贡献。你不必再一篇篇打开英文阅读摘要，直接看中文提炼即可快速判断是否值得深入阅读全文。首次抓取 + 全文摘要生成约需 1-3 分钟，后台异步完成。

### 4. 领域热点分析

工具会基于抓取到的论文，使用 LLM **聚合成主流子领域**，统计近 7 天和 30 天的增量变化，并为 Top 3 热门方向给出详细总结和对应论文清单。这帮助你快速把握当前研究趋势，而不是被动地逐条浏览论文列表。

### 5. 个性化收藏与笔记管理

你可以对感兴趣的文章进行**一键收藏**、添加个人笔记、复制 BibTeX 条目方便引用。界面支持按已读/未读筛选，标记已读后会减少推送同类文章——这是一个简单的"👍/👎 反馈学习"机制，越用越懂你的需求。

### 6. 多渠道推送与定时报告

支持以下通知方式：
- **浏览器通知**：有新论文时即时提醒
- **SMTP 邮件摘要**：定时发送当日/每周汇总
- **微信推送**：可通过企业微信群机器人或 Server酱集成
- **Telegram / Slack**：团队协作场景可用

此外，每周精选论文会自动归档生成周报，方便你回顾本周的重要进展。

### 7. Skill Agent 集成

项目内置了 **Claude Code / Codex 通用的 Agent Skill**，只需对 AI 助手说一声*"运行我的文献雷达"* 或 *"今天有什么新论文"*，它就能跑完整条流水线并产出当日摘要——而且**不需要任何 AI API key**，因为 running skill 的模型本身就是那个 LLM。安装命令简单如一行：`/plugin marketplace add OvOhao/auto-paper-collecter` → `/plugin install auto-paper-collecter@auto-paper-collecter`。

## 适用人群

**- 科研人员**：研究生、博士后、教授等需要每天跟踪领域最新动态的研究者，可以用此工具节省大量文献筛选时间。

**- AI/ML 从业者**：持续关注大模型、NLP、CV 等技术进展的工程师，能快速获取最新的开源论文和实现代码。

**- 技术爱好者**：喜欢自学新技术、希望保持知识更新的开发者，可以作为个人知识管理的辅助工具。

**- 教育团队**：导师可以为学生定期推送领域综述材料，助教可整理最新参考文献供教学使用。

**- 自主研究者**：没有机构资源访问权限的独立研究者，可通过这个免费开源方案平等获取前沿信息。

## 与同类工具对比

| 特性 | auto-paper-collecter | Connected Papers | ResearchRabbit | arXiv Sanity | Feedly + arXiv |
|------|---------------------|------------------|----------------|--------------|----------------|
| 多源聚合 | ✅ 7个数据源 | ❌ 仅论文图谱 | ✅ 多库 | ❌ 仅 arXiv | ✅ 可配置 |
| LLM 摘要 | ✅ 自动生成中文 | ❌ 无 | ⚠️ 部分 | ❌ 无 | ❌ 无 |
| 联想扩展 | ✅ LLM 智能推理 | ❌ 基于引用图 | ❌ 基于相似性 | ❌ 基于向量 | ❌ 无 |
| 本地部署 | ✅ 自托管/本地 | ❌ 云端 SaaS | ❌ 云端 SaaS | ❌ 本地 script | ✅ 自建 |
| API Key 依赖 | ⚠️ 可选（LLM功能用） | ✅ 必需 | ✅ 必需 | ❌ 无 | ❌ 无 |
| 推送通知 | ✅ 邮件/TG/Slack/微信 | ❌ 弱 | ⚠️ 有限 | ❌ 无 | ✅ 强 |
| Agent Skill | ✅ Claude/Codex 原生 | ❌ 无 | ❌ 无 | ❌ 无 | ❌ 无 |
| 免费开源 | ✅ MIT 许可证 | ❌ Freemium | ❌ Freemium | ✅ 免费 | ✅ 免费 |

**auto-paper-collecter 的独特优势**在于其 **LLM 驱动的智能化流程**和**高度可配置的 Agent Skill 集成**。相比纯图形化工具（如 Connected Papers），它更适合自动化、批量的文献跟踪；相比简单的 RSS 聚合器（如 Feedly），它能主动理解和过滤内容，而非被动接收。最重要的是，它是完全**开源自托管**的，你的关键词、笔记和偏好都不会上传到第三方服务器，隐私更有保障。

## 如何使用

### 第一步：环境准备

确保已安装 **Python 3.10+** 和 pip。推荐使用虚拟环境隔离依赖：

```bash
git clone https://github.com/OvOhao/auto-paper-collecter.git
cd auto-paper-collecter
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

或者如果你熟悉 Docker，可以直接跳过依赖配置：

```bash
cp .env.example .env    # （可选，默认有合理配置）
docker compose -d up   # 数据库持久化到 ./data
```

### 第二步：配置 AI 网关（可选但推荐）

编辑 `.env` 文件，填入你的 OpenAI 兼容网关信息：

```env
AI_BASE_URL=https://your-api-endpoint.com
AI_API_KEY=sk-your-api-key
AI_MODEL=gpt-4o-mini      # 或 any compatible model
AI_ENABLED=true           # 设为 false 可退回到原始摘要（不耗 API）
```

其他可选配置包括：
- `SEMANTIC_SCHOLAR_KEY`：提高 Semantic Scholar 请求速率
- `GITHUB_TOKEN`：提升 GitHub API 配额上限
- `SMTP_*` 系列变量：配置邮件推送
- `REFRESH_TIMES`、`TIMEZONE`：每日抓取时间和时区设置

### 第三步：启动服务

```bash
python run.py
```

默认监听端口为 `http://localhost:8000`。打开浏览器进入仪表盘。

### 第四步：订阅关键词设置

在网页界面点击"订阅设置"，输入你关心的英文关键词（例如 `transformer attention mechanism`），然后点击"保存并拓取"。系统将立即触发一次抓取流程，LLM 会在后台进行联想扩展、多源检索、过滤和摘要生成。

### 第五步：查看日报

抓取完成后，页面会自动刷新显示"今日文献流"——按真实发表时间排序的论文列表，每篇都有中文 TL;DR 摘要、来源标签和快速操作按钮（收藏、笔记、标记已读）。顶部还有实时搜索框，可以在已有结果中快速筛选。

### 第六步（进阶）：配置 Agent Skill

如果你是 Claude Code 用户，安装 skill 后就可以直接用自然语言交互：

```
你：今天有什么新论文？
auto-paper-collecter Skill：正在运行文献雷达...获取最新摘要...
```

skill 目录位于 `skills/auto-paper-collecter/`，完全基于 Python 标准库，零外部依赖，可在任何支持 Claude/Codex 的环境中运行。

## 总结推荐指数

**auto-paper-collecter** 是一个设计精巧、功能完备的个人科研助手，它将 LLM 的智能能力与多源学术数据聚合完美结合，让文献跟踪变得像刷推送一样轻松。特别是对于需要每天保持知识更新的研究者和开发者来说，这个工具的省时效果非常显著。

**优点：**
- 🌟 **全链路 LLM 赋能**：从联想扩展、跨源过滤到中文摘要，每一步都用 AI 增效
- 🌟 **多源整合**：一次查询，7个数据源一网打尽，避免来回切换网站
- 🌟 **中文友好**：界面和摘要都针对中文使用者优化，降低阅读门槛
- 🌟 **灵活部署**：支持 Python 直接运行、Docker 容器、Agent Skill 多种模式
- 🌟 **开源免费**：MIT 许可证，可自由修改和二次分发
- 🌟 **隐私可控**：自托管方案，你的关键词和数据不会上传到第三方
- 🌟 **技能生态**：SkillHub 上架，可与 Claude/Codex 等 agent 无缝集成

**不足：**
- ⚠️ **首次设置有一定门槛**：需要配置 AI 网关和环境依赖，对新手不够友好
- ⚠️ **LLM 调用消耗成本**：如果开启 LLM 功能，需要消耗 API token（但可降级为免费模式）
- ⚠️ **依赖外部服务稳定性**：arXiv、Semantic Scholar 等源的可用性会影响整体抓取成功率
- ⚠️ **当前仅支持英语关键词**：虽然摘要为中文，但检索关键词目前需用英文，限制了部分用户的使用
- ⚠️ **单用户设计**：暂无多用户支持，团队共享协作功能较弱

**综合评分：8.2/10**

auto-paper-collecter 目前处于早期活跃开发阶段（上线不到2个月），已展现出相当成熟的功能水平和良好的用户体验。它特别适合那些想要**自动化文献跟踪**、又不想受制于商业云服务（如 Connected Papers 的订阅费用）的个人研究者和开发者。

虽然它在一些细节体验上还有优化空间（比如中文关键词支持、错误处理更友好），但其**核心理念和创新设计**已经证明了价值——让 AI 替你做那些重复性的搜索和归纳工作，把精力集中在更有价值的创造上。

如果你是一名科研工作者、技术爱好者或开源贡献者，值得把这个工具加入你的日常工作流。建议先试用免费模式（`AI_ENABLED=false` 使用基础摘要），满意后再配置自己的 LLM API 解锁完整智能功能。这个项目还在快速迭代中，后续加入的多用户支持和移动端体验值得期待。

---

*本文基于 2026 年 7 月 28 日的公开信息撰写，工具功能和性能可能随时更新，请以官方最新信息为准。GitHub 仓库：[https://github.com/OvOhao/auto-paper-collecter](https://github.com/OvOhao/auto-paper-collecter) · SkillHub：[https://skillhub.cn/skills/auto-paper-collecter](https://skillhub.cn/skills/auto-paper-collecter)*
