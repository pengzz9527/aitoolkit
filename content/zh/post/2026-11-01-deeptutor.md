---
title: 'DeepTutor 评测：港大 53k Star 的终身个性化家教，把「辅导—出题—生成教材—复习」串成一台机器'
date: 2026-11-01
tags: ['AI工具', 'AI教育', '个性化学习', '多智能体', 'RAG', '开源', 'Python', '港大HKUDS']
categories: ['AI 工具评测']
description: '港大 HKUDS 的 DeepTutor 用一套 agent 运行时把聊天辅导、难度校准出题、生成式教材、沉浸式阅读、遗忘曲线复习串成闭环，L1/L2/L3 三层可审计记忆让「越教越懂你」不再是黑箱。本文拆解它的六层架构、四种安装路径、与 Khanmigo / NotebookLM / ChatGPT 学习模式的真实差异，以及 TutorBench 论文数据背后的边界。'
---

# DeepTutor 评测：港大 53k Star 的终身个性化家教，把「辅导—出题—生成教材—复习」串成一台机器

问 ChatGPT 一道题，它会答。第二天再问，它不记得你上次卡在哪。第三周你发现：错过的知识点没人回头找，做对的题没人帮你安排复习，攒下的 40 份 PDF 讲义躺在文件夹里没人整合成一本书。

**DeepTutor** 要解决的就是这条断裂的链路。它由香港大学数据智能实验室（HKUDS，就是 LightRAG、nanobot、AI-Researcher 那一批）开发，Apache 2.0 开源。最新 **v1.7.1 发布于 2026-11-01**，仓库已有 **53,052 Star、6,495 Fork**，PyPI 上迭代了 53 个版本。它的定位不是「又一个 AI 聊天框」，而是**agent 原生的学习工作区**：聊天、出题、研究、可视化、生成教材、沉浸式阅读、复习调度共享同一个会话上下文与同一套学习者记忆。

一句话简介：**DeepTutor 是一个开源的、本地优先的终身个性化辅导系统——它把「家教」拆成可组合的 agent 能力，并用一套你能打开文件读的记忆系统把它们粘起来。**

- **GitHub**：https://github.com/HKUDS/DeepTutor
- **官网/文档**：https://deeptutor.info（有简中、繁中、日、西、法、阿、俄等 12 种 README）
- **论文**：arXiv 2604.26962《DeepTutor: Towards Agentic Personalized Tutoring》
- **协议**：Apache 2.0，**官方明确说明目前没有任何付费在线产品**（纯开源，没有 SaaS 版）
- **技术栈**：Python 3.11–3.14 + Next.js 16 / React 19；核心包 PyPI `deeptutor` 当前 1.7.1，历史可查 53 个版本
- **画像**：Star 53,052 / Fork 6,495 / 创建于 2025-12-28 / 最近推送 2026-10-31

---

## 核心功能

### 1. 一个运行时，八种学习模式共享上下文

多数「AI 学习工具」的每个功能都是一个孤岛：聊天里讲完的概念，到了测验页面就没了。DeepTutor 的做法是**所有能力跑在同一个 agent loop 上**，只是换了 workflow：

| 模式 | 干的事 | 你留下的东西 |
| --- | --- | --- |
| **Chat** | 带工具、带知识库、带子 agent 的辅导对话 | 会话 + 记忆 |
| **Ask Questions / Quiz** | 难度校准的提问与作答 | 题目 + 错因进 Question Bank |
| **Research** | 带引用的深度研究报告 | 报告 + 引用 |
| **Solve** | 分步解题推理 | 解题轨迹 |
| **Visualize / Math Animator** | Chart.js / Manim 动画 | 图与动画 |
| **Mastery Path** | 把学习目标拆成知识点地图 | 掌握度证据 |
| **Immersive Reading** | 在文档/网页/视频/音频旁学习 | 逐页引用 + 高亮笔记 |
| **Book** | 把素材编译成可交互教材 | 可编辑章节块 |

关键是这些模式**共享 sticky session context**——工作区、知识库、人格、模型、Reading/Mastery 状态跨轮保留。你在 Chat 里问的问题，和 Quiz 里出的题、Book 里编的章节，读的是同一份资料、同一个「你是谁」。

### 2. 六种检索引擎任选，还能用 recall 指标帮你选

Knowledge Center 是它最能拉开差距的地方。一个知识库绑定一种引擎，官方支持：

- **LlamaIndex**（默认，向量 + BM25 混合，可选 cross-encoder 重排、FAISS 精确/HNSW 索引）
- **PageIndex**（推理式检索、页级引用，可托管或自托管 OSS）
- **GraphRAG / LightRAG**（知识图谱检索，LightRAG 是 HKUDS 自己的项目）
- **LightRAG Server**（检索外包给你自己的 HTTP 实例）
- **WeKnora / 腾讯 IMA / MarginNote 4 / Kiwix / Obsidian 库**

更狠的是它给了**评测命令**。写一份 QA 集（JSONL，每行 `query` + `gold` 段落），然后：

```bash
deeptutor kb eval my-kb --dataset qa.jsonl --top-k 5 --mode hybrid --save baseline.json
deeptutor kb eval-diff baseline.json candidate.json
```

输出 Recall@k / Precision@k / nDCG@k / MRR / MAP / Hit@k 六项指标，**纯函数计算、没有 LLM 当裁判**，还能对比不同索引参数、不同 query rewrite 策略的差异。这个设计值得所有做 RAG 的人抄：与其猜哪个引擎好，不如拿你自己的问答集打分。

### 3. 可审计的三层记忆，而不是黑箱向量库

个性化最怕「不知道为什么它这么看我」。DeepTutor 的记忆是**文件化的三层金字塔**：

- **L1**：工作区镜像 + 追加写入的事件流（`trace/<surface>/<date>.jsonl`）
- **L2**：按面（chat / notebook / quiz / kb / book / partner / cowriter）整理的事实（`L2/<surface>.md`），带指回 L1 实体的引用
- **L3**：跨面综合（`L3/<profile|recent|scope|preferences>.md`），记录它综合了哪些 L2

Memory Graph 用一圈一圈的节点把 L3—L2—L1 的**证据边**画出来，你能点进去看「它认为我擅长 X」是从哪几条对话哪里推断出来的。不满意就直接改 Markdown 文件。这是我在开源学习工具里见过最诚实的「个性化」实现。

### 4. Partners：一个带手机号的 AI 家教

每个 Partner 有自己的 `SOUL.md`（人格与教学风格）、模型策略、工具策略、私有记忆，还有**自己的 IM 渠道**：飞书、Telegram、Slack、Discord、钉钉、QQ/NapCat、企业微信、WhatsApp、Zulip、Mattermost、Matrix、Teams。官方的一句话定义很精准——「**一个 Partner 就是有性格、有手机号的聊天**」。

每个入站消息都变成一次正常的 ChatOrchestrator 轮次。多个 Partner 还能组成 Partner Group 开一场有席位、有共享记忆模式的多方讨论。对自学者来说，这意味着「随时能发消息问」的家教，而不是「必须打开网页」的工具。

Partners 之外还能挂 **My Agents**：直接调用本机的 Claude Code、Codex、Grok CLI、Antigravity、Kimi、opencode、MiMo Code、Hermes Agent、OpenClaw，把它们的输出流进 Activity 面板——相当于让编码 agent 当你的助教。

### 5. 不是摘要，是「活的教材」

Book 不是把 PDF 摘要成一篇长文。它先给你一个**章节大纲让你审**，你确认后才开始编译。每一章编译成**可编辑的类型化块**：文本、callout、测验、闪卡、时间线、代码、图表、交互 HTML、动画、概念图、深挖、你的批注，每章自带 Page Chat。你可以插入、移动、重生成、改写、甚至**切换块类型**。

它还有两个务实到近乎可爱的运维命令：

```bash
deeptutor book health                # 检测源文档漂移（教材基于的 PDF 改了没）
deeptutor book refresh-fingerprints  # 刷新源基线
```

以及闪卡**导出到 Anki**（`DeepTutor::<笔记标题>` 牌组，重导入更新而非重复）、日历事件导出 `.ics`。它不试图把你锁在自己的复习系统里。

---

## 适用人群

**非常适合**：

- **自学者 / 终身学习者**：你要读 20 篇论文搞懂一个新领域，需要有人陪你读、给你出题、把知识编成教材。DeepTutor 的 Reading + Book + Mastery Path 正好是一条流水线
- **考研 / 考公 / 考证党**：Question Bank + 错题 + Practice 复习调度 + Anki 导出，把「刷题—错题—复习」闭环做完了
- **老师与教研**：Book 能从自己的讲义生成可交互教材，Partner 可以接到班级的飞书/企微群
- **家庭场景**：v1.6.3 起有 learner/guardian 账号模型——学习者账号锁能力与素材政策，监护人可看报告、批素材、重置凭证
- **想自己跑在本地、不愿把学习数据交给 SaaS 的人**：Docker 一条命令、数据在一个卷里、记忆是你能读的 Markdown

**不太适合**：

- **只想问一句话就走的用户**：启动一个 Web 服务 + 配 provider，对「今天数学作业第三题」来说太重，ChatGPT 就够了
- **完全不想折腾配置的人**：虽然是 Docker 一条命令，但之后要在 Settings 里配 Provider、模型、嵌入、搜索、语音、解析引擎，**配置面非常宽**
- **需要合规审计的企业采购**：它是自托管项目，不是有 SLA 的商业产品，没有官方付费支持

---

## 与同类工具对比

| 维度 | **DeepTutor** | Khanmigo | NotebookLM | ChatGPT 学习模式 | Gemini Guided Learning |
| --- | --- | --- | --- | --- | --- |
| 开源 / 自托管 | ✅ Apache 2.0，Docker 一条命令 | ❌ | ❌ | ❌ | ❌ |
| 数据位置 | 你自己的 `data/` 目录 | 厂商云 | Google 云 | OpenAI 云 | Google 云 |
| 学习记忆 | **L1/L2/L3 可审计 Markdown** | 有学习档案（不可见） | 无跨会话记忆 | 有记忆（不可查/不可编辑） | 有（黑箱） |
| 教材生成 | Book Engine（类型化块 + 大纲先审） | 无 | Audio/Video Overview + 报告 | 无 | 无 |
| 题库与复习 | Question Bank + Practice + Anki 导出 | 有练习 | 无 | 无 | 有练习 |
| RAG 引擎选择 | **6 种，可评测对比** | 内部 | 内部 | 内部 | 内部 |
| IM 触达 | 13 种渠道 | 网页/App | 无 | App | App |
| 成本 | 自付 API 费 / 本地模型 | 订阅 | 订阅 | 订阅 | 订阅 |
| 上手成本 | 高（配置面宽） | 低 | 低 | 低 | 低 |

说白了，这三类工具不在同一个坐标里：

- **Khanmigo / ChatGPT / Gemini** 卖的是「零配置的教育体验」，你付出的是订阅费和**数据可见性**
- **NotebookLM** 卖的是「把资料读懂」，但它不追踪你学没学会
- **DeepTutor** 卖的是「**这套家教是你自己的**」——数据在你机器上，记忆是你能改的文件，检索引擎是你能评测替换的，模型是你能换的

代价也很直白：它把配置复杂度还给了你。

---

## 如何使用（具体步骤）

### 路径 A：Docker，最快看到完整界面

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

打开 `http://127.0.0.1:3782`。命名卷 `deeptutor-data` 保存所有设置与数据；只需要暴露 3782 一个端口。

### 路径 B：PyPI，Web 应用 + CLI

要求 **Python 3.11–3.14** 和 **Node.js 20.9+**。

```bash
mkdir -p my-deeptutor && cd my-deeptutor
python -m pip install -U "deeptutor[full]"
deeptutor init      # 交互式：端口 + LLM provider + 可选 embedding/search
deeptutor start     # 同时起后端与前端
```

`deeptutor[full]` 装 Web 应用 + CLI；裸 `deeptutor` 只装核心聊天与 SDK。`Ctrl+C` 同时停两个服务。

**从 1.6.15 或更早升级要注意**：先停服务、备份运行时目录、**卸载旧的 `deeptutor-cli` 包**，再装新包族，保持同一个 `DEEPTUTOR_HOME`，然后跑 `python -m pip check` 和 `deeptutor module list` 验证。

### 路径 C：CLI 极简版（不装 Node.js）

```bash
mkdir -p my-deeptutor && cd my-deeptutor
python -m pip install -U deeptutor
deeptutor init --cli
deeptutor chat
```

核心包只有 Chat、Ask Questions、CLI 和 SDK；Research、Solve、Book、Knowledge 等能力需要装对应模块（`deeptutor module install research`）。

### 路径 D：桌面预览版

`dev` 分支的 `Desktop Release` workflow 会产出 macOS（arm64 / x64 DMG）与 Windows x64（Setup / 便携 ZIP）安装包，捆绑了 Python、Node.js 和完整工作区，**不需要终端**。注意两点：**v1.7.0/v1.7.1 的正式 Release 不含桌面安装包**，得去 workflow 的 Artifacts 里下（需登录 GitHub，7 天后过期）；Windows 预览版未签名，会弹 SmartScreen。

### 第一次使用的推荐流程

1. **Settings → Providers** 配一个 provider（OpenAI 兼容端点都行，也可以 `deeptutor provider login openai-codex` 用你自己的 ChatGPT 套餐走 OAuth，凭据只落在 `data/system/user-secrets/` 下，沙箱够不到）
2. **Settings → Language models** 选模型，顺便配 **Task models**（给起标题、写起始提示这类杂活指定一个便宜的小模型）
3. **建一个工作区**：一门课 / 一个项目一个 workspace，别把所有东西堆一个屋
4. **Resources → Knowledge Center** 建知识库，上传讲义，选解析引擎（PDF 复杂就上 MinerU 或 Docling，纯文本直接用 Text-only 最快）
5. **Learning → New learning → Book**，选这个知识库生成一本可交互教材，**先审大纲**
6. **Learning → Mastery Path** 定学习目标，让它拆知识点地图
7. **Practice** 里做错题 → 自动进 Question Bank → 定期复习，需要就导出 Anki
8. 配一个 **Partner** 接到你自己的飞书/Telegram，通勤路上也能问

### 想让别的 agent 来驱动它

```bash
# 单次、机器可读（NDJSON，一行一个事件）
deeptutor run deep_solve "求 d/dx[sin(x^2)]" --tool reason --format json

# 跨轮保持同一个 session
SID=$(deeptutor run deep_research "Survey 2026 papers on RAG" \
  --config mode=report --config depth=standard --format json \
  | jq -r 'select(.type=="done").session_id')
deeptutor run deep_question "Quiz me on that survey" --session "$SID" --format json
```

仓库根目录有 `SKILL.md`，专门给 agent 读的交接文档；`ask_user` 在没有 TTY 时会自动空回复而不是挂死，headless 友好。

---

## 局限与注意事项

1. **配置面是真的宽**。Provider、语言模型、任务模型、嵌入、搜索、语音、图像/视频生成、解析引擎、MCP、CLI Apps、模块、记忆预算……每一项都有合理的默认值，但**想用好必须逐项过一遍**。这是「自托管能力」的必然代价，不是 bug
2. **论文数据要看清楚口径**。arXiv 摘要说「个性化指标平均提升 10.8%，在五种骨架上增强通用 agentic 推理 29.4%」，但这是它**自建的 TutorBench**（基于大学课程、用 LLM 模拟学生做第一人称交互评测）上的结果，不是 K-12 实测、也不是真人学习效果。方向可信，绝对数字要打折
3. **模块化带来的版本风险**。1.7.0 起拆成「核心包 + 功能模块」，模块必须与核心版本一致，混装会炸。升级前**务必先 `deeptutor module list` + 备份运行时目录**
4. **多用户是可选能力，不是默认**。认证默认关闭（单用户模式）。开多人要先改 `auth.json`、重启、注册第一个管理员，再在 `/admin/users` 分配权限。**PocketBase 在多用户部署下应保持空值**，官方明说了它只是单用户集成
5. **知识库索引与嵌入强绑定**。原生 LightRAG 查询要求当前 embed 配置（模型、维度、端点）与索引发布时一致，换了嵌入就得重建。好消息是它有 `version-N` 目录保留旧索引，重建期间旧索引不会中途被毁
6. **技能导入虽过安检，仍非零风险**。所有导入都要过同一道安全闸（注册表判决、防路径穿越、压缩比检查、剥离 `always:` 字段、写 `.hub-lock.json`），但社区 skill 跑起来仍能用到工具——给学习者用之前至少自己读一眼 SKILL.md
7. **没有官方商业支持**。Apache 2.0 + Discord/飞书/微信群社区支持。生产环境自建需自理

---

## 总结

**推荐指数：★★★★☆（4.5/5）**

DeepTutor 是这一波「AI 学习工具」里少数**想清楚了自己在做什么**的项目。市面上的产品大体分两种：大厂卖订阅，把学习档案锁在云端给你一个好用的黑箱；开源项目多停留在一个聊天框或一个 RAG 脚本。DeepTutor 走的是第三条路——**把整套家教拆成可组合、可检查、可替换的部件**：会话上下文共享、检索引擎可选可评测、记忆是你能打开改的文件、教材是可编辑的类型化块、题库能导到 Anki。它是在造「**你自己的家教**」，而不是「你订阅的家教」。

它最让我认可的三个设计，恰恰都不是模型能力：

1. **`deeptutor kb eval` 让「哪个检索引擎好」变成一个可以拿你的数据回答的问题**，而不是营销话术
2. **L1/L2/L3 记忆 + Memory Graph 的证据边**，把「个性化」从黑箱变成一个能审计的对象
3. **Book health / refresh-fingerprints**——承认教材会过期，并给你工具检测漂移

扣掉的半颗到一颗星：配置面宽到会劝退一半人；模块化之后的升级路径需要谨慎；论文指标虽然方向可信，但来自自建 benchmark 与模拟学生，别当成教学效果的实证。

**适合谁**：愿意花两小时配置、并且真的想长期学一门东西的人——考研党、转行自学者、要带班的老师、想把家里孩子的学习管起来又不想把数据交出去的家长。**不适合**：只想今天问一道题、明天可能就不用了的人。对后者来说，它是一座配置精美的图书馆，而你只需要一张便签纸。
