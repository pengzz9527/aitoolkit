---
title: 'Cloudflare security-audit 评测：4 万 Star 的安全审计 Skill，把编码 Agent 变成会自我证伪的漏洞猎手'
date: 2026-10-23
tags: ['AI工具', '安全审计', 'AI Agent', 'Cloudflare', '开源', 'Claude Code', '代码安全', 'Agent Skills']
categories: ['AI 工具评测']
description: 'Cloudflare 开源的 security-audit 是一个给编码 Agent 用的安全审计 Skill，用侦察、覆盖账本、独立验证、结构化输出六个阶段把「让 AI 找漏洞」变成可复现的流程。40,036 Star、MIT 协议，内置 162 个攻击类与 11 个领域包，自带零依赖校验器。本文拆解它的设计、真实测试结果与局限。'
---

# Cloudflare security-audit 评测：4 万 Star 的安全审计 Skill，把编码 Agent 变成会自我证伪的漏洞猎手

让 Claude Code 或 Codex「审一遍这个仓库的安全」，你大概率会得到一份看起来很专业、但没法直接用的报告：几条泛泛的「建议加强输入校验」，一两个从训练数据里背下来的经典漏洞模式，然后上下文窗口满了，它忘了前面看过什么。

**security-audit** 是 Cloudflare 在 2026 年 6 月 18 日开源的一个 Agent Skill，专门解决这个问题。它不是又一个 SAST 工具，而是一套写给编码 Agent 的作业规程：先画架构和信任边界，再按「覆盖单元」派发并行的猎手 Agent，每个候选漏洞交给一个**没见过它**的验证 Agent 去证伪，最后只把通过了独立复核的记录写进 `findings.json`。截至今天，仓库已有 **40,036 Star、2,499 Fork**，MIT 协议，是今天 GitHub Trending 上星标增长最快的项目（单日 +2,979）。

它也是 Cloudflare 那套「漏洞发现流水线」的起点：官方博客里写明，这套流程从约 450 行的 Skill 起步，六周后扩展成覆盖 **128 个仓库**、跨仓库追踪依赖的扫描系统。

## 工具简介

**security-audit** 是一个模型无关（agent-neutral）的安全审计 Skill：把 Markdown 提示词、JSON Schema 和两个零依赖 Node 校验脚本打包在一起，任何支持工具调用和并行子 Agent 的编码 Agent 都能加载它。

- **GitHub**：https://github.com/cloudflare/security-audit-skill
- **发布方**：Cloudflare（Cloudforce One / 安全研究团队）
- **开源时间**：2026-06-18（同日发布配套博客《Build your own vulnerability harness》）
- **协议**：MIT
- **星标 / Fork**：40,036 / 2,499
- **主语言**：JavaScript（校验器）+ Markdown（提示词），无运行时依赖
- **规模**：`skills/security-audit/` 下 20 个文件，约 352 KB，1,778 行 Markdown 提示词
- **安装方式**：`npx skills add`（Skills CLI v1.7.4）
- **运行要求**：支持子 Agent 的编码 Agent + Node.js（跑校验器）+ OS 级沙箱（跑目标代码时）

## 核心功能

### 1. 六阶段审计流程，而不是一次「帮我看看」

Skill 强制执行六个阶段，每阶段有明确产物：

| 阶段 | 做什么 | 产物 |
|------|--------|------|
| 1. 侦察 | 梳理架构、信任边界、输入面、既有证据 | `architecture.md`、`coverage-ledger.json` |
| 2. 覆盖驱动狩猎 | 从账本单元派发隔离的猎手 Agent，覆盖率评审找缺口 | 账本更新 + 候选列表 |
| 3. 候选验证 | 每个候选交给全新的验证 Agent 尝试**推翻**它 | `candidate` / `rejected` |
| 4. 结构化输出 | 按 Schema 写入三种裁决 | `findings.json` |
| 5. 独立记录复核 | 新 Agent 复核最终源码引用，重大替换再审一遍 | 复核后的记录 |
| 6. 中立报告 | 从已验证记录派生报告，不给未验证项编严重级别 | `REPORT.md`、`FINDINGS-DETAIL.md`、`NEEDS-VALIDATION.md` |

关键在阶段 2 和 3 的隔离：**发现漏洞的 Agent 永远不是验证它的那个 Agent**。官方设计原则写得很直白——对抗式验证，验证者必须是「无偏的第三方」，用另一套权重和训练数据去压力测试发现者的假设。

### 2. 覆盖账本：让「审了多少」变成可数的事实

`coverage-ledger.json` 把目标拆成稳定的覆盖单元（surface × boundary × attack class），每次运行后更新；多次运行是**累加**的，会读上一次的账本和 `findings.json`，对改动过的源码重新验证，而不是把旧结论当成已覆盖。

这点直接对应官方博客里的一个反直觉数据：**单次运行只能找到多次运行合计漏洞的约一半**，而且偏向更简单、更不隐蔽的那部分。所以「跑十遍再人工 diff」正是他们后来要做编排层的原因。Skill 在单仓库范围内把这个「多轮累加」做进了流程里。

### 3. 三种裁决，严重级别只给已证实的

`findings.json` 里每条记录只能是三种状态之一：

- `confirmed`：有完整源码追踪 + 有界复现结果，才允许给严重级别（critical/high/medium/low/informational）
- `needs_validation`：源码层面成立，但缺一个具体的外部事实（部署配置、网关行为、身份策略……），**不给严重级别**
- `rejected`：被证伪的候选，也留档，避免下一轮重复劳动

严重级别锚点也写得具体：critical 是未认证者拿到代码执行或任意账户接管；high 是完整绕过一个显式安全控制（认证绕过、跨租户读写）；「纵深防御少了一层」明确**不算**漏洞，只能作为加固建议。这条规则能挡掉一大类 AI 生成的「看似严重」的噪声。

### 4. 11 个领域包、162 个攻击类

不是只查 SQL 注入。除核心攻击类（注入、访问控制、资源与文件处理、加密与密钥、业务逻辑、特性滥用、漏洞链、Wildcard、Obvious things）外，还有按目标类型拆分的 11 个领域包：

| 领域包 | 攻击类数 | 典型场景 |
|--------|---------|---------|
| `MEMORY-SAFETY-AND-BINARY.md` | 20 | C/C++/Rust unsafe、内核模块、解析器、JIT |
| `WEB-PROTOCOL-AND-AUTH.md` | 20 | HTTP 请求走私、缓存、JWT/OAuth/SAML、MFA |
| `DESKTOP-MOBILE-AND-LOCAL-IPC.md` | 16 | 深链、WebView 桥、导出组件、Unix socket |
| `CLOUD-AND-DEPLOYMENT.md` | 15 | IAM、IaC、容器/K8s、Serverless、入口配置 |
| `DATA-ISOLATION-AND-LIFECYCLE.md` | 15 | 多租户隔离、缓存/搜索、导出备份、删除恢复 |
| `AI-AND-LLM.md` | 14 | 提示注入、记忆投毒、工具调用、MCP 信任边界 |
| `CLIENT-SIDE.md` | 14 | DOM 注入、postMessage 信任、原型污染 |
| `PROTOCOLS-RPC-AND-MESSAGING.md` | 14 | gRPC、GraphQL、队列、webhook、流式 RPC |
| `RESOURCE-EXHAUSTION-AND-AVAILABILITY.md` | 13 | 配额、队列、worker、按量计费型资源耗尽 |
| `SUPPLY-CHAIN-AND-RELEASE.md` | 12 | 依赖解析、CI、签名发布、插件生态 |
| `ATTACK-CLASSES.md`（核心） | 9 | 通用 Web/库/CLI/服务目标 |

`AI-AND-LLM.md` 这一类值得单独提：它把「Agent 自己也是攻击面」写进了检查项——MCP 与子 Agent 的信任关系、工具 schema 的越权、模型可控动作的绑定，这些是传统 SAST 规则库里基本没有的东西。

### 5. 零依赖校验器，能直接进 CI

`validate-findings.cjs` 和 `validate-coverage-ledger.cjs` 不依赖任何 npm 包，只做一件事：按 `report-schema.json` 检查记录是否合规、指纹是否重复、账本单元是否自洽。阶段 1 建立账本后立刻跑一次，阶段 4 和每次阶段 5 替换后再跑。

这意味着 AI 的输出可以被**机器拒绝**，而不是靠人眼看它「像不像真的」。对想把安全审计接进 CI 的团队来说，这是整个仓库里最实用的一块。

### 6. 默认不信任目标代码

这个 Skill 的安全设计比大多数同类项目认真：跑目标的构建、测试、浏览器、fuzzer 必须在一个 OS 强制沙箱里，要求**无外网**、空环境变量（只从允许列表注入）、目标只读、只能写自己的 `scratch/`、明确的 CPU/内存/进程/文件大小/墙钟上限。如果沙箱能力凑不齐，它不会「凑合跑一下」，而是把结论降级成 `needs_validation`，并给出安全的验证方案。

它甚至规定了产物提升（promotion）的 10 步流程：不跟随符号链接、`fstat` 校验 inode 与链接数、逐段 no-follow 打开目录、限制单文件和累计字节数。这些细节说明作者真的想过「审计工具本身被目标仓库反向攻击」的场景。

## 实际验证：校验器跑通了，完整审计没跑

为了不只停留在读 README，我把仓库克隆下来，实际执行了两个校验器的测试套件（Node v22.22.0）：

```bash
git clone --depth 1 https://github.com/cloudflare/security-audit-skill.git
cd security-audit-skill/skills/security-audit
node validate-findings.test.cjs
node validate-coverage-ledger.test.cjs
```

真实输出：

| 测试套件 | 用例数 | 通过 | 失败 | 耗时 |
|---------|--------|------|------|------|
| `validate-findings.test.cjs` | 34 | 34 | 0 | ~3.1s |
| `validate-coverage-ledger.test.cjs` | 31 | 31 | 0 | ~2.4s |

测试覆盖的不是「跑通 happy path」这么简单，还包括「在受限 Node 堆下限制超限 findings 输出」「共享 helper 与账本校验器保持一致」「接受接近最大长度的多字节 ID」这类边界用例。两个校验器共 65 个用例全绿，作为 CI 门禁的可信度是够的。

**没跑的部分要说清楚**：完整审计需要接一个有并行子 Agent 能力的编码 Agent，并且要准备 OS 级沙箱，本环境不具备，所以我没有产出真实的漏洞报告——本文里的效果数据（单次约一半、128 仓库、上下文占用 <25%）均来自 Cloudflare 官方博客，不是我的实测。任何声称「跑一遍就能替代渗透测试」的说法，目前都没有公开的独立基准支撑。

## 适用人群

- **有源码的中小团队**：没有专职安全团队，但需要在上线前过一遍认证、多租户、文件处理这类高风险面
- **AI/Agent 产品团队**：`AI-AND-LLM.md` 覆盖提示注入、MCP 信任、工具越权，是当前 SAST 的空白区
- **要把安全审查接进 CI 的平台组**：JSON Schema + 零依赖校验器可以做成硬门禁
- **安全团队做初筛**：把「翻遍 128 个仓库找候选」的体力活交给 Agent，人只看 `confirmed` 和 `needs_validation`
- **想自建漏洞流水线的团队**：官方博客把从 Skill 到 harness 的演进路径写得很具体，可以直接当架构参考

## 与同类工具对比

| 维度 | security-audit | Semgrep | CodeQL | claude-code-security-review | 人工渗透测试 |
|------|----------------|---------|--------|----------------------------|-------------|
| 定位 | Agent 审计作业规程 | 规则型 SAST | 语义查询 SAST | PR diff 安全审查 Action | 人工攻防 |
| 检测方式 | LLM + 并行子 Agent + 覆盖账本 | 模式匹配规则 | 数据流/污点查询 | 单次 LLM 审查变更 | 经验与工具结合 |
| 跨文件/业务逻辑 | ✅ 强（覆盖单元 + 漏洞链） | 部分 | 中等 | 弱（只看 diff） | ✅ 最强 |
| 误报控制 | 独立验证 Agent + 三态裁决 + 强制降级 | 规则精度决定 | 查询精度决定 | 依赖模型 | 人工判断 |
| 接入成本 | 中（需 Agent + 沙箱） | 低 | 中高（需构建数据库） | 低（GitHub Action） | 高 |
| 成本模型 | Token 消耗，多 Agent 多轮，较贵 | 免费/按席位 | 免费/按席位 | Token 消耗较低 | 人力 |
| 协议/开源 | MIT | 开源 + 商业版 | 开源（限制商用） | 开源 | — |
| 适合 | 全仓深审、AI 应用审计 | 快速门禁、已知模式 | 高精度查询、合规 | PR 级增量审查 | 关键系统定级 |

**怎么选**：Semgrep/CodeQL 是「确定性检测」，规则命中的东西不需要 LLM 再确认，适合每次提交都跑；security-audit 是「探索性检测」，目标是找出规则写不出来的逻辑漏洞和跨组件信任问题，适合发版前、重大重构后、以及新接入的第三方仓库。两者不是替代关系——比较合理的组合是 Semgrep 挡住已知模式，security-audit 做周期性深审，Anthropic 的 `claude-code-security-review`（6,495 Star）挂在 PR 上做增量兜底。

## 如何使用

### 安装

用 Skills CLI 安装到项目级或用户级：

```bash
# 项目级（写入当前项目的 skills 目录）
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit

# 用户级，所有项目可用
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit \
  --global
```

### 触发审计

在目标仓库里启动编码 Agent，直接说人话即可，Skill 会根据措辞自动区分模式：

```text
security audit this codebase
find security vulnerabilities in ./src
do a security review, output to ~/audits/my-project
```

注意它的**双模式**设计：问「这个 JWT 校验有什么问题」只会走**指导模式**（只回答，不建目录、不写报告）；只有明确说「审计整个代码库」「端到端安全审查」「输出报告」才会进入完整六阶段流程。这个区分很重要——不然一次随口的提问就会触发几十个 Agent 的 token 消耗。

### 产物结构

完整审计默认输出到 `~/security-audit-skill/<repo-name>/run-<N>/`：

```text
run-1/
├── run-metadata.json      # run_id、target、source_ref、profile、budget
├── architecture.md        # 架构、信任边界、输入面
├── coverage-ledger.json   # 覆盖单元与状态
├── findings.json          # confirmed / needs_validation / rejected
├── REPORT.md              # 面向负责人的结论
├── FINDINGS-DETAIL.md     # 逐条证据与最小修复
├── NEEDS-VALIDATION.md    # 缺什么事实、怎么补
└── agents/<agent-id>/     # 每个猎手/验证者的隔离工作区
```

### 控制成本：先设预算

跑大仓库前建议用 profile + budget 约束规模：

- `quick`：小目标/复跑，一波猎手 + 一次覆盖率评审，成本最低
- `standard`：默认，多波次 + 候选验证与最终复核分离
- `deep`：高风险目标，按子系统×生命周期拆单元，覆盖率评审跑到干净为止

预算按「Agent 调用次数」计。Skill 会强制预留侦察、覆盖率评审和验证的调用额度；如果预算连最小流程都撑不起，它会**一个 Agent 都不启动**，直接报 `budget_cannot_fund_reconnaissance_and_reserves`，而不是悄悄降级成「假装审过了」。这个行为在同类工具里很少见，但对控制成本很关键。

### 把校验器接进 CI

```bash
# 审计跑完后校验产物（用法就是一个参数：文件路径）
node skills/security-audit/validate-findings.cjs \
  ~/audits/my-project/run-1/findings.json

node skills/security-audit/validate-coverage-ledger.cjs \
  ~/audits/my-project/run-1/coverage-ledger.json
```

校验器会从技能目录读取 `report-schema.json`，通过时退出码为 0，失败时打印前 100 条错误并以非 0 退出。直接把退出码当 CI 门禁即可：

校验失败就让流水线红掉——这样「AI 编了一条没有源码依据的高危漏洞」会在合并前被拦住，而不是躺在周报里。

### 想自建流水线？官方给了路线

Cloudflare 博客里那段建议比很多架构文章实在：

1. 先用 Skill 在开发环境里把提示词调到能出真漏洞；
2. 最小可用 harness 只需要 **Recon + Hunt + Validate** 三段，加一个不能自己提单的独立 Validator；
3. 每个阶段写同一个 SQLite，键是 `(run_id, repo, stage)`，任何阶段可恢复、重试、被后续 run 复用；
4. **先做持久化，再做并行**——别因为一个意外错误丢掉五小时的运行；
5. 每个 Agent 的上下文控制在窗口的 25% 以下，职责切得足够窄；
6. 发现用一个模型、验证用另一个模型，跨供应商交叉检验；
7. 跨仓库追踪和去重 Agent 都晚点再上，等「没有它真的卡住」时再加。

## 局限与注意事项

1. **单次覆盖不完整**：官方自己说单次运行约找到多次运行合计的一半，且偏简单。把它当「一次性体检」会漏，必须靠账本累加、定期复跑。
2. **Token 成本不低**：一个标准 run 会启动侦察、多个猎手、覆盖率评审、每个候选一个验证者、以及最终复核。大仓库 + `deep` profile 可能达到数百次 Agent 调用，先算预算再跑。
3. **不是 SAST 替代品**：它靠 LLM 读代码，缺少编译期信息、数据流引擎和规则库的确定性。已知模式（硬编码密钥、明显的 SQL 拼接）用 Semgrep 更快更便宜。
4. **对沙箱要求高**：没有 OS 级隔离时，目标代码不能执行，大量结论会停在 `needs_validation`——安全上正确，但报告可用性会下降。
5. **模型能力决定上限**：弱模型会产出更多「看似合理」的候选，虽然验证阶段能过滤，但会烧掉预算。官方建议用当前最强的模型，并且发现/验证用不同模型。
6. **输出可能含敏感信息**：`architecture.md` 和 `FINDINGS-DETAIL.md` 会记录内部路径、配置片段、攻击路径。别把审计目录提交进仓库（Skill 默认写在仓库外，就是为了这个）。
7. **不要对线上服务跑**：规则明确禁止探测已部署端点、共享基础设施、生产身份和真实用户数据；所有验证都限制在源码和本地 fixture 内。

## 总结

**推荐指数：★★★★☆（4.5/5）**

security-audit 的价值不在于「AI 能找漏洞」——这件事 2025 年就有人证明了；它的价值在于把「AI 找漏洞」变成了**可以被审计的过程**：覆盖账本回答「审了哪些、漏了哪些」，独立验证回答「凭什么信这条」，三态裁决和 Schema 校验回答「怎么防止模型编造」，沙箱规则回答「审别人代码时自己怎么不被打」。

它也有明显的边界：单次覆盖约一半、成本高、依赖强模型、没有公开的独立基准。所以正确的用法不是「替代安全团队」，而是把它当成一个不知疲倦、需要复核的初级审计员——让它把 128 个仓库翻一遍，人只看 `confirmed` 和 `needs_validation`。

**适合谁**：有源码、需要周期性深审的团队；做 AI/Agent 产品、需要检查提示注入和 MCP 信任边界的人；想把安全审查做成可校验流水线的平台工程师。

**不适合谁**：只想在 CI 里加一道快速规则扫描的团队（用 Semgrep）；没有沙箱环境、也不打算搭的团队；期待「一句话出渗透测试报告」的人——这个 Skill 会拒绝你这么用。
