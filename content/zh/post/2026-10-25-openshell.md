---
title: 'NVIDIA OpenShell 评测：给自主 Agent 造一个「内核级牢笼」，网络规则还要过 SMT 证明'
date: 2026-10-25
tags: ['AI工具', 'AI Agent', '安全沙箱', 'NVIDIA', '开源', 'Rust', '零信任', 'Agent 安全']
categories: ['AI 工具评测']
description: 'NVIDIA OpenShell 是面向自主 Agent 的安全运行时：用 Landlock + seccomp 在内核层限制文件与系统调用，用 default-deny 的 L7 网络代理逐条放行请求，凭据只在批准的目标处注入，策略变更还要经过 SMT 形式化验证。19,601 Star、Apache 2.0、v0.1.5，本文拆解架构、实测安装命令的真实输出与它的真实边界。'
---

# NVIDIA OpenShell 评测：给自主 Agent 造一个「内核级牢笼」，网络规则还要过 SMT 证明

你让编码 Agent「把项目跑起来」。接下来它开始 `npm install`、`pip install`、读 `.env`、调用外部 API、顺手 `curl` 一个它觉得可能有用的地址。你给了它一个容器，看起来挺安全——但容器里放的是你的 SSH key、云厂商凭据和整个 home 目录，网络默认全通，而它今天的行为取决于模型此刻的判断。

2026 年，Agent 能力涨得比隔离手段快得多，这类问题已经从「理论风险」变成了部署时的第一道坎：沙箱、Agent 治理、零信任运行时在这个季度密集开源，GitHub 上一搜 `agent sandbox` 已有上万条结果。

**OpenShell** 是 NVIDIA 在 2026 年 2 月开源、如今已进入稳定发版节奏的 Agent 运行时。它的定位一句话说清：**让 Agent 能干所有需要凭据和网络的活，但永远碰不到真实的密钥、数据和全网通网络。** 你只声明「这个二进制可以访问哪些主机、能发什么请求」，剩下的由内核和代理执行。

截至今天，仓库有 **19,601 Star、1,940 Fork**，Rust 编写，Apache 2.0 协议，最新稳定版 v0.1.5（2026-10-20 发布），今天仍挂在 GitHub Trending 上（单日 +896）。

## 工具简介

**OpenShell** 是一套「Agent 安全运行时」，由网关（Gateway）、监督进程（Supervisor）、沙箱内运行时（Sandbox）三部分组成。它不绑定具体 Agent——OpenCode、Claude Code、Codex、Pi 只要打进了镜像就能跑，OpenShell 只负责决定「它能碰什么」。

- **GitHub**：https://github.com/NVIDIA/OpenShell
- **文档**：https://docs.nvidia.com/openshell/latest/
- **发布方**：NVIDIA
- **首次公开**：2026-02-24
- **最新稳定版**：v0.1.5（2026-10-20），稳定版基本每周发一次
- **Star / Fork**：19,601 / 1,940
- **主语言**：Rust
- **协议**：Apache 2.0
- **安装**：`install.sh` 一行装 CLI + 策略证明器 + 本地网关；Python 侧 `uv add openshell`
- **运行要求**：Linux（Debian/Ubuntu 的 amd64/arm64）、macOS Apple Silicon；Windows 需 WSL 2（实验性）。内核需 Landlock ABI 3+（Linux 6.2+）与 seccomp user-notification
- **沙箱后端**：Docker 28+ / Podman 5.x / MicroVM（KVM 或 Hypervisor.framework）
- **K8s 部署**：Helm chart，`oci://ghcr.io/nvidia/openshell/helm-chart`

## 核心功能

### 1. 内核级强制，不是「靠 Agent 自觉」

沙箱里的限制由内核模块执行，而不是靠包装一层 HTTP 客户端或让 Agent「读一下安全守则」：

| 能力 | 实现 | 时机 |
|------|------|------|
| 文件读写范围 | Landlock LSM（ABI 3+，Linux 6.2 起） | 沙箱启动时生效，之后不可改 |
| 系统调用 | seccomp user-notification | 每次调用 |
| 网络出口 | seccomp 拦截 TCP open 与 DNS 查询，转交监督进程裁决 | 每次连接 |
| 进程身份 | 非 root 单用户、零 Linux capabilities | 创建沙箱时 |

官方文档里的关键设计是**边界两侧的职责分离**：监督进程在可信侧做决策；沙箱内运行时与不可信的 Agent 在同一侧，只负责「报告 Agent 想干什么」，**自己不做任何策略判断**。即使 Agent 拿到了沙箱内的 root，也改不了裁决逻辑。

### 2. 默认拒绝的 L7 网络策略（能区分 GET 和 POST）

每条出站连接在离开沙箱前都要过策略检查，而策略可以精细到 HTTP 方法级别。官方五分钟教程里的真实序列很能说明问题：

```bash
# 1. 建一个没有任何网络策略的沙箱
openshell sandbox create --name demo --from registry.example.com/team/agent-tools:1.0 \
  --no-auto-providers

# 2. 沙箱内直接 curl —— 被拦
curl -s https://api.github.com/zen
# curl: (56) Received HTTP code 403 from proxy after CONNECT

# 3. 主机侧查拒绝日志（每条拒绝都有二进制、目标、原因）
openshell logs demo --since 5m --source sandbox
# [sandbox] [OCSF] NET:OPEN [MED] DENIED /usr/bin/curl(64) -> api.github.com:443
#   [policy:- engine:opa] [reason:network connections not allowed by policy]

# 4. 只给 curl 开 GitHub API 的只读权限
openshell policy update demo \
  --rule-name github_api \
  --binary /usr/bin/curl \
  --add-endpoint api.github.com:443:read-only:rest:enforce \
  --wait

# 5. GET 通过
curl -s https://api.github.com/zen     # Anything added dilutes everything else.

# 6. POST 仍被拦
curl -s -X POST https://api.github.com/repos/octocat/hello-world/issues \
  -H "Content-Type: application/json" -d '{"title":"oops"}'
# {"error":"policy_denied", ..., "rule":"POST /repos/octocat/hello-world/issues"}
```

对应的 YAML 就是这几行：

```yaml
network_policies:
  github_api:
    endpoints:
      - host: api.github.com
        port: 443
        protocol: rest
        enforcement: enforce
        access: read-only
    binaries:
      - path: /usr/bin/curl
```

注意 `enforce` 之外还有 `enforcement: audit`——只记日志不拦截。这是渐进式收紧策略的正确用法：先 audit 看 Agent 到底想连哪，再切 enforce，而不是第一天就把 Agent 关到什么都干不了。

**规则热更新，不重启**：`policy update` 完成后规则直接在运行中的沙箱里生效，Agent 重试即可。文件系统和进程策略则是固定的——想改就得重建沙箱，这个取舍很清楚。

### 3. 凭据只在「批准的目标」处注入

Agent 看不到真实密钥。`provider` 是一等公民，把服务名和凭据绑定：

```bash
openshell provider create --name my-claude --type claude-code --from-existing
# 从当前 shell 的 ANTHROPIC_API_KEY / CLAUDE_API_KEY 读取并存入凭据库
```

监督进程掌握凭据，**只对策略批准的端点**下发。官方例子说得很直白：OpenRouter 的 key 只会被送到 `openrouter.ai`。即使 Agent 被提示注入策反，它也没有 key 可偷——这比「把 key 塞进环境变量并祈祷」强一个量级。

### 4. 策略变更先过 SMT 证明，再交给人批

OpenShell 最有辨识度的功能是**形式化验证**，不是 LLM 审 LLM。

- **政策顾问（Policy Advisor）**：Agent 撞到没权限的目标时，OpenShell 拒绝请求并把它整理成一条「窄规则提案」，按 host / port / 调用程序分组。
- **证明器（Prover）**：每条提案用 SMT 求解器检查，是否引入了新的风险访问——比如「带凭据访问一个新主机」「调用一个新的 API 方法」「访问云元数据地址」。有任何命中就**阻断自动批准**，等人工复核。
- **边界检查**：`openshell-prover` 可独立使用（不需要网关），回答「候选策略有没有超出我定义的权限边界」，适合塞进 CI 或让父 Agent 校验给子 Agent 写的策略。

```bash
# 列出待批提案 → 批准或拒绝
openshell rule get my-agent --status pending
openshell rule approve my-agent --chunk-id <chunk-id>
openshell rule reject my-agent --chunk-id <chunk-id> --reason "Not needed for this task."

# 批量批准（默认跳过带安全标记的提案，并报告跳过了多少条）
openshell rule approve-all my-agent
```

它自己也承认了保证有限：证明器的覆盖范围等于它建模过的策略特性；策略里出现 GraphQL、MCP 规则时，它会明说「无法检查」，而不是当作通过。文档还专门提醒——**边界检查和提案风险检查回答的是不同问题，过了其中一个不代表过了另一个**。

### 5. 从笔记本到 K8s，同一套策略

同一个网关可以跑本地 Docker/Podman，也可以 Helm 装进集群（CNI 必须真的执行 `NetworkPolicy`）。网关管理员还能下发**全局策略**，覆盖所有沙箱自己的策略——注意是**替换**而不是「取交集」，生效期间沙箱无法自己改策略，provider 附带的网络规则也会被压制。企业里统一收紧权限时这个语义很好用，误用也很容易把所有人的 Agent 一次搞哑。

## 适用人群

- **把编码 Agent 放进真实仓库的团队**：Agent 需要装包、跑测试、推代码，但绝不能碰生产凭据和整个 home 目录
- **平台 / 基础设施团队**：一次定义策略，本地和 K8s 共用，还能让子 Agent 通过 `openshell-prover` 自我约束
- **安全与合规**：每条放行的网络请求都有结构化审计日志（OCSF 格式，可导出到 SIEM），能回答「这个 Agent 昨天连了哪些主机」
- **多 Agent 编排者**：子 Agent 的权限上限由父 Agent 证明，越权提案进不了流水线
- **NVIDIA GPU 环境**：沙箱支持 GPU 资源，跑本地模型或微调任务时同样受策略约束

**不太适合**：只想在本地跑个 Agent 试试新玩法的人（Docker 已经够用）、Windows 主力机用户（WSL 2 还是实验性）、以及不愿意维护策略文件的纯个人用户——策略写得越细，维护成本越高。

## 与同类工具对比

| 维度 | OpenShell | OpenSandbox | CubeSandbox | ksigs/agent-sandbox | Microsoft Agent Governance Toolkit | Docker 裸容器 |
|------|-----------|-------------|-------------|---------------------|-----------------------------------|---------------|
| Star | 19.6k | 16.1k | 13.0k | 4.4k | 6.5k | — |
| 定位 | Agent 安全运行时 | 沙箱运行时（代码/浏览器/桌面） | 轻量高并发沙箱 | K8s 上的隔离工作负载 | Agent 治理套装 | 通用容器 |
| 文件/系统调用隔离 | Landlock + seccomp | 容器 / Firecracker | 微 VM 隔离 | Pod 级 | 执行沙箱 | 容器默认 |
| 网络策略粒度 | **L7（按二进制 + HTTP 方法）** | 每沙箱出入口策略 | 有 | K8s NetworkPolicy | 策略引擎 | 通常全通 |
| 凭据处理 | provider，按端点注入 | Credential Vault | 有 | 无内置 | 零信任身份 | 环境变量 |
| 策略变更验证 | **SMT 形式化证明 + 提案审核** | 无 | 无 | 无 | 有策略引擎，非形式化 | 无 |
| 冷启动性能 | 依赖容器/microVM 后端 | Firecracker P50 64ms | 主打并发密度 | K8s 调度 | — | 秒级 |
| 学习曲线 | 陡（概念多：gateway/supervisor/provider/prover） | 中 | 中 | 中（需 K8s） | 中 | 低 |
| 适合 | 给不可信 Agent 划最小权限 | 大规模并行沙箱、RL 训练 | 高并发、成本敏感 | 已有 K8s 的团队 | 治理与合规全套 | 快速实验 |

**怎么选**：要做的是「一堆沙箱跑得快、跑得多」，OpenSandbox 和 CubeSandbox 在密度和启动延迟上更对口（Firecracker P50 64ms 这种数字 OpenShell 并不主打）；要做的是「这一个 Agent 到底被允许干什么」，尤其需要 L7 网络控制、凭据不出沙箱和变更可验证，那是 OpenShell 的独有区间。两者并不冲突：OpenShell 的 compute driver 本身就可以跑在 microVM 上。

还有一个新鲜对手：strands-agents/box（2026-10-02 开源，Rust，468 Star）走的是极简路线——OS 隔离 + default-deny 策略 + 凭据注入，目前只支持 Apple Silicon。理念与 OpenShell 高度相似，但生态、K8s 支持和形式化证明还差得远。

## 如何使用

### 第 1 步：安装

```bash
curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | sh
openshell status                    # 确认 CLI 能连到本地网关
```

安装脚本会按平台选包（Debian/Ubuntu 走 deb，Fedora/RHEL 走 rpm，macOS 用 Homebrew 并把网关注册成服务，监听 `https://localhost:17670`），同时装上 CLI、`openshell-prover` 和本地网关。要固定版本就设 `OPENSHELL_VERSION=v0.1.5`。

> 安全提示：把任何 `curl | sh` 放进生产流程之前，先下载脚本读一遍，并核对发布产物的校验和（release 页提供了 `openshell-prover-checksums-sha256.txt`）。

### 第 2 步：先建一个空沙箱，看默认拒绝真的生效

```bash
openshell sandbox create --name demo
```

默认镜像是极简 Ubuntu，**连 Agent 都没装**——这是刻意的：先让你看到「默认什么都干不了」，再逐项放行。

### 第 3 步：配 provider，别把 key 写进镜像

```bash
openshell profile import \
  --url https://raw.githubusercontent.com/NVIDIA/OpenShell/main/providers/openrouter.yaml

export OPENROUTER_API_KEY=...        # 只在这一步存在于你的 shell
openshell provider create --name openrouter --type openrouter --from-existing
```

`profile` 定义了「哪个二进制可以访问哪些端点」，`provider` 只存凭据。两者分开，团队里可以共享 profile，各自管自己的 key。

### 第 4 步：起真正的 Agent

```bash
openshell sandbox create \
  --name my-agent \
  --from ghcr.io/anomalyco/opencode:latest \
  --provider openrouter \
  -- opencode -m openrouter/nvidia/nemotron-3.5-lightning:free
```

`--` 之后是 Agent 自己的命令行参数，OpenShell 不干预。用免费模型这一段不花钱，适合先跑通链路。

### 第 5 步：按需授权，而不是一次给足

Agent 撞墙时，OpenShell 拒绝并起草规则：

```bash
openshell rule get my-agent --status pending
openshell rule approve my-agent --chunk-id <chunk-id>   # 或者 reject 并写原因
```

批准后规则热加载，Agent 重试就行。建议的节奏是：**先 audit 攒数据 → 再 enforce**，并且把 `--include-security-flagged` 留给真正需要它的场景——默认跳过带安全标记的提案，是故意让你多看一眼。

### 第 6 步（可选）：把边界检查接进 CI

```bash
# boundary.yaml 定义环境允许的最大权限，candidate.yaml 是被测策略
openshell-prover --boundary boundary.yaml --candidate candidate.yaml
```

退出码即门禁：谁要是提了个能访问云元数据地址的规则，流水线直接红掉——而不是等上线后才发现 Agent 会自己读 IAM 临时凭据。

### 策略文件本身也值得做版本管理

策略是 YAML，天生适合代码化。把它们放进仓库后，可以用本站的 [JSON 格式化工具](https://198007.xyz/tools/json-formatter/) 先把策略或审计日志转成 JSON 校对结构（日志里混了 `[OCSF]` 这类标记，肉眼核对容易漏），用 [文本差异对比工具](https://198007.xyz/tools/diff-checker/) 对比两次 `openshell policy get demo --base` 的输出，一眼看出这次授权到底多开了哪几个主机；再用 [正则测试工具](https://198007.xyz/tools/regex-tester/) 写一条模式，从几万行 deny 日志里筛出「带凭据访问新主机」的记录。全程在浏览器本地完成，日志不外传——审安全日志的工具自己先得体面。

## 局限与注意事项

1. **还在 0.x，Python 包标注 Alpha**：PyPI 上的 `openshell` 仍是 `Development Status :: 3 - Alpha`，API 稳定性要打问号。官方承诺 Stable 接口在补丁版本内向后兼容，但 Experimental 标记的东西可能在补丁版里就没了。
2. **概念密度高**：gateway、supervisor、sandbox、provider、profile、advisor、prover、boundary policy——第一天上手要读不少文档。想「装完就跑」的人会很挫败。
3. **形式化验证不是万能**：证明器只保证它建模过的特性。GraphQL、MCP 规则它会报「无法检查」。而且边界检查与提案风险检查是两个不同问题，别把其中一个的通过当成整体安全。
4. **平台限制明确**：Linux 需要内核 6.2+ 才有 Landlock ABI 3；Windows 走 WSL 2 仍是实验性；老版本内核直接跑不起来。
5. **全局策略语义是「替换」**：管理员一开全局策略，所有沙箱自己的策略和 provider 网络规则都会被压制，正在干活的 Agent 会突然全挂。生产环境先在小范围网关验证。
6. **遥测默认开启**：官方声明只收集运营类计数，不采集沙箱名、路径、提示词、凭据。要关就设 `OPENSHELL_TELEMETRY_ENABLED=false`（Helm 用 `server.telemetryEnabled=false`）。
7. **不是性能型沙箱**：OpenShell 不主打冷启动延迟和并发密度，那是 OpenSandbox、CubeSandbox 的赛道。要大规模并行跑评测，选型时别搞混。
8. **策略写错照样会出事**：默认拒绝只能保证「没批的进不去」，不能保证「批了的是对的」。给 Agent 开 `read-write` 到整个 `/etc` 再证明十遍也没用。

## 总结

**推荐指数：★★★★☆（4.5/5）**

OpenShell 解决的是 2026 年 Agent 部署里最尴尬的那个矛盾：**Agent 越有用，就越需要凭据、网络和写权限；而这三样恰好是它最不该无限拥有的东西。** 它的答案不是「限制 Agent 能力」，而是在能力外面修三道墙——内核级的文件与系统调用墙、按二进制和 HTTP 方法放行的网络墙、以及只对批准端点生效的凭据墙；再给这三道墙配一个能形式化验证变更的监理。

真正让它区别于一堆沙箱产品的，是那个 SMT 证明器。它把「谁能批准权限」从模型手里拿走，交给一个数学求解器加一个人类——AI 提需求、机器验风险、人做决定，这个分工本身就是当下 Agent 安全最合理的形态。

它不完美：0.x 版本、概念重、平台受限、不适合追求启动延迟的场景。但如果你的团队真的把编码 Agent 放进了有凭据的仓库，这套东西值得花一个下午装起来跑一遍那个五分钟教程——被 `curl: (56) 403 from proxy` 拦一次，比读十篇安全宣讲都直观。

**适合谁**：要把 Agent 接进真实基础设施的平台团队、需要给多 Agent 划最小权限的编排者、以及任何已经因为「Agent 能不能别碰 .env」跟同事吵过架的人。
