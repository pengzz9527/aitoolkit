---
title: AI Job Search 评测：把 Claude Code 变成你的全职求职助理，简历、求职信、面试一站生成
date: 2026-10-19
tags: [AI工具, 智能体, 求职工具, 效率工具, 开源, Claude Code]
categories: [AI工具评测]
description: AI Job Search 是构建在 Claude Code 上的开源求职工作流，fork 下来填入个人档案后，自动评估岗位匹配度、定向改写 LaTeX 简历、撰写求职信、批量排岗并准备面试。作者亲自用这套流程 69 份投递换来 1 份签约。
---

# AI Job Search 评测：把 Claude Code 变成你的全职求职助理，简历、求职信、面试一站生成

海投岗位最耗时间的从来不是「投」，而是每一份都要把简历从头到尾改一遍、把求职信写得既贴岗位又不夸张。**AI Job Search** 就是把这件事整个交给 Claude Code 干：fork 一个仓库，把你的简历、LinkedIn 导出、学历文件丢进去，然后一条 `/scrape` 跨多个招聘网站抓岗位，`/apply` 对单条岗位自动「评估匹配度 → 起草定向简历 + 求职信 → 第二个 agent 复核 → 修订 → 输出 LaTeX PDF」。作者 Mads Lorentzen 本人是个地质物理学家，2025 年底被裁员后就是靠这套流程自己找工作的——69 份定制投递、20 个一面、1 份签约，2026 年 6 月入职 AI 工程师。项目 2026 年 3 月开源，半年内星标已冲到 **5.4 万**，MIT 协议，迭代非常勤。

## 工具简介

**AI Job Search** 是一个跑在本机的 AI 求职框架，核心是把 Claude Code 训练成「懂你、懂岗位、懂写作」的整套投递流水线：

- **GitHub**: https://github.com/MadsLorentzen/ai-job-search
- **语言**: Python 3.10+（工作流骨架）+ LaTeX（CV / 求职信编译）+ Bun（岗位搜索 CLI）
- **开源协议**: MIT
- **依赖**: Claude Code CLI（Pro/Max/Team 订阅或 Anthropic API 按量计费）
- **定位**: 求职工作流 + agent 编排，不是聊天机器人；核心「self-profiling / fit evaluation / drafter-reviewer」三段与语言、国家无关，岗位搜索 skill 默认配了丹麦市场（Jobindex、Jobnet、Akademikernes Jobbank），社区在 Discussions 里为其他地区提供 fork

## 核心功能

1. **/setup 三条入库路径**：指向 `documents/` 目录（CV PDF、LinkedIn 导出、学历、推荐信、过往投递）自动识别；或者直接在对话里贴一份 CV；或者交互式 interview 提问。档案越详细，后续定制越精准，这是官方反复强调的一点。
2. **/scrape + /rank 批量抓岗**：`/scrape` 跨多个招聘网站去重抓取匹配岗位；岗位多时跑 `/rank`，用并行 agent 按 5 个维度批量评分，输出带「真实强弱项 + 截止提醒 + 失效标记」的排序短名单。Deal-breaker 项（如「不要倒班」「最低薪资必须 ≥ X」）会直接一票否决。
3. **/apply 定向申请流水线**：给定 URL 或粘贴 JD，自动走「匹配度评估 → LaTeX 简历 + 求职信草稿 → reviewer agent 复核挑刺 → 修订」四步，产物是编译好的 PDF。`cover.cls` 用 `xelatex` 编译（需要 fontspec），CV 用 `lualatex`（现代 MiKTeX 的 pdflatex 常因 fontawesome5 报错）。
4. **/interview 面试准备包**：针对已 track 的 application，调出原始 JD + 你实际投出的 CV/求职信 + 之前轮次反馈，研究公司和面试官（verify-before-use 规则），把高频问题映射到你自己的 STAR 例子；缺的部分会给你「诚实的过渡答案」，不会给你编造经历；最后附一个 mock interview。
5. **/outcome + /gmail-sync + /notion-sync 收口**：记录每个 application 的最终结果，把投出去的物料归档到 `documents/applications/<company>_<role>/`；`/outcome followup` 在 10 天没回音时自动起草「只使用已投递材料里出现过的事实」的跟进邮件，一次最多两次，只给草稿不代发；`/gmail-sync` 从 Gmail 读面试邀请/offer/拒绝等信号，批量给你确认后才落库；`/notion-sync` 通过官方 Notion MCP（OAuth 无 API key）单向同步到 Notion 数据库，纯只读，仓库文件始终是 source of record。

## 适用人群

- 正在海投、简历/求职信写不过来、且愿意用 Claude Code 的重度求职者
- 换赛道（如从传统行业转 AI）想快速验证自己在某类岗位上的匹配度的人——`/upskill` 会给你一张按优先级排好的技能缺口热图 + 学习路径
- 求职过程中希望全程留痕、可复盘的人（`job_search_tracker.csv` + `/html-report` 生成本地离线 HTML 漏斗仪表盘）
- **不适合**：完全不想付费跑 Claude Code 的人（无免费额度）、不想 fork 到私有仓库而只想「克隆即用」的人（fork 默认公开，`/setup` 会把姓名、联系方式、薪资期望写进 tracked 文件，官方强烈建议改用「私有仓库 + upstream」配方）

## 与同类工具对比

| 工具 | 定位 | 优势 | 局限 |
| --- | --- | --- | --- |
| **AI Job Search** | 本地 agent 化求职流水线 | 定向简历/求职信、drafter-reviewer 双 agent、面试 prep 包、结果归档、Notion/Gmail 同步、可自定义模板与岗位搜索 | 依赖 Claude Code 订阅；岗位搜索默认北欧市场，其他地区要装社区 fork |
| **LinkedIn AutoApply** | 平台内一键海投 | 无需外部工具、覆盖岗位多 | 不可定制内容，简历只有一份，容易误投 |
| **Teal / Rezi** | SaaS 简历生成器 | 上手快、模板多、ATS 检查 | 订阅制、数据在云端、缺乏面试准备与结果追踪 |
| **Handshake / JobBank 原生** | 平台招聘工具 | 免费、合规 | 单岗位视角、无「匹配度批量评分」、无归档 |
| **纯 Claude Chat 提问** | 一次性求职问答 | 灵活 | 无结构、无记忆、无 LaTeX 编译、无漏斗管理 |

一句话：**只要投过 10 份以上简历，且愿意付一份 Claude Code 订阅，这套工具能省掉 80% 的定制写作时间，还能把面试准备也自动化掉；只是想省事海投，LinkedIn AutoApply 更轻。**

## 如何使用（具体步骤）

**1. 准备前置工具**（一次性）：

```bash
# Claude Code CLI（订阅或 API）
npm install -g @anthropic-ai/claude-code
# Python 3.10+（大多数发行版已带）
python3 --version
# Bun（岗位搜索 CLI 运行时）
curl -fsSL https://bun.sh/install | bash
# LaTeX 发行版任选其一：TeX Live / MacTeX / TinyTeX / MiKTeX
# 需要 lualatex + xelatex 两条编译链
# 可选：pip install pypdf（ATS 可解析性检查）
```

**2. Fork 并克隆到私有仓库**（强烈建议，避免简历入库后被公开看到）：

```bash
# 官方 SETUP.md 第 8 节的配方：私有仓库 + upstream
git clone https://github.com/MadsLorentzen/ai-job-search.git my-job-search
cd my-job-search
# 在 GitHub 上新建同名私有仓库，改 remote 指向私有库
git remote set-url origin https://github.com/<you>/my-job-search
git push -u origin main
# 之后每周 upstream 更新用官方脚本预览再合：
python3 tools/check_upstream_updates.py
python3 tools/upstream_triage.py
```

**3. 安装岗位搜索 CLI**：

```bash
python3 tools/install_portal_clis.py   # Windows: python tools\install_portal_clis.py
# 会 bunt install 到 .agents/skills/*/cli/ 每个发现的岗位搜索工具
# 带 install-time lifecycle script 的会被跳过并报告
# --dry-run 先看看它会装什么
```

**4. 建立个人档案**：

```bash
claude
# 在 Claude Code 里执行：
/setup
# 三选一：扫 documents/ 目录 / 直接贴一份 CV / 走 interview
```

**5. 抓岗 + 批量排岗**：

```bash
/scrape
# 跨多个岗位站去重抓取，按匹配度排序
/rank
# 岗位太多时：并行 agent 批量评分 5 维，出带缺口标注的短名单
```

**6. 定向投递**：

```bash
/apply https://jobindex.dk/job/1234567
# 岗位 URL 拉不到的话：
/apply <把 JD 全文贴进来>
# 流程：匹配度评估 → LaTeX 简历 + 求职信草稿 → reviewer agent 挑刺 → 修订 → 输出 PDF
# 注意：JD 被当作「不可信输入」处理，agent 不会执行 JD 里嵌的任何指令
```

**7. 面试准备**：

```bash
/interview
# 调出该岗位的完整档案：JD、你实际投出的 CV、之前轮次反馈
# 生成 STAR 映射、mock interview、诚实的过渡答案
```

**8. 结果归档与同步**：

```bash
/outcome
# 记录结果、归档材料到 documents/applications/<company>_<role>/
/outcome followup
# 10 天没回音时起草跟进邮件（只用你已投递材料里出现过的事实），草稿不发
/gmail-sync
# 从 Gmail 读面试邀请/offer 信号，批量确认后落库
/notion-sync
# 官方 Notion MCP（OAuth，无 API key）单向同步到 Notion，纯只读
/html-report
# 生成本地离线 HTML 漏斗仪表盘
```

**小贴士**：
- 换自定义模板：`/add-template` 注册任何能命令行编译到 PDF 的 CV/求职信工具链（LaTeX、Typst 都可以），注册时会强制跑一次试编译
- 换市场：`/add-portal` 自动生成你本地岗位站的搜索 skill，也可以从 Discussions 里的 portal index（#78）抄别人的——但**必须读完代码**：官方故意不做「一键装第三方 skill」，因为你的 `.claude/settings.json` 已经白名单了这些 CLI
- 重置：`/reset profile` / `/reset documents` / `/reset all`，会明确告知会删什么、要你打 `RESET` 才真的删
- 安全提示：官方在 SECURITY.md 里写得很清楚——岗位 URL 内容是不可信输入，agent 是「指令层」而非「沙箱层」，第一次接触不熟悉的岗位站先扫一眼它 fetch 了什么、写了什么再点发送

## 总结与推荐指数

AI Job Search 把「求职」这件事重新拆成了 agent 能干的颗粒度：档案是结构化数据、岗位匹配是评分函数、简历/求职信是编译产物、面试准备是可复现的 prep 包、投递结果是可归档的档案。它不是又一个「帮我写求职信」的 SaaS，而是一套能留痕、能复盘、能换市场、能换模板的工作流。作者本人 69 份投递换 1 个 offer 的案例，加上 5.4 万星标 + 每周 CHANGELOG + 官方向社区开放的 portal/skill 贡献通道，让它成为 Claude Code 生态里最「生产级」的垂直用例之一。对正在换工作、且能接受 Claude Code 订阅成本的人来说，这套工具链几乎是「必装」。

- 适合：重度海投、想系统留痕、愿意为 Claude Code 付费的求职者
- 不适合：只想一键海投、不愿私有化归档、或没订阅 Claude Code 的人

**推荐指数：⭐⭐⭐⭐（4.0 / 5）**

> 如果你已经投了 10 份以上简历，且愿意 fork 到私有仓库认真填一次 `/setup`，AI Job Search 能把你「改简历 + 写求职信 + 准备面试」这三件事压缩到每份岗位 20 分钟内，且每一笔都能追溯。

📌 想了解更多 AI 工具与智能体推荐？浏览本站 [全部 88 款在线 AI 工具 →](/tools/)
