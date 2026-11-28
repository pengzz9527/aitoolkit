---
title: 'mini-swe-agent 评测：100 行 Python 的极简编码 Agent——只用 bash、无 tool-calling，SWE-bench verified 拿下 74%+'
date: 2026-11-28
tags: ['mini-swe-agent', 'SWE-bench', '编码 Agent', 'LLM', '开源工具', '基准测试', 'Python', '自动化']
categories: ['AI 工具评测']
description: 'mini-swe-agent（SWE-agent 团队，约 9,700 星，MIT）把编码 Agent 压缩到约 100 行 Python：只认 bash、不用模型的 tool-calling 接口、每个动作独立 subprocess 执行，却在 SWE-bench verified 上跑进 74%+，现已驱动 Ramp SWE-Bench 并在 DeepSWE 上击败 Claude Code 与 Codex。'
---

# mini-swe-agent 评测：100 行 Python 的极简编码 Agent——只用 bash、无 tool-calling，SWE-bench verified 拿下 74%+

**mini-swe-agent** 的官方定位一句话：**「那个只有 100 行的 AI Agent，能解 GitHub issue，也能在你自己的命令行里干活。」** 它出自 SWE-bench 与 SWE-agent 的缔造团队（Princeton NLP），2025 年 6 月 28 日建库，立项动机很反潮流：当时整个赛道都在往「更大」卷——更多工具、更复杂的历史处理器、更厚的配置层——它偏要往「最小」做：**Agent 类本体约 100 行 Python，除 bash 外没有任何工具，连模型自带的 tool-calling 接口都不用**，结果却跑出了大框架才有的基准成绩。2026-11-28 当日登上 GitHub Python Trending。

它现在的分量不只在代码量小：它**驱动了 Ramp SWE-Bench**（大厂用的评测基础设施），在 DeepSWE 基准上**击败了 Claude Code 和 Codex**，并内置对 Meta 新出的 ProgramBench 的支持（v2.4.6）。

- **GitHub 星标**：≈9,700；1,332 forks（2026-11-28）
- **GitHub 仓库**：https://github.com/SWE-agent/mini-swe-agent
- **官网 + 教程**：https://mini-swe-agent.com ｜ 极简 Agent 教程 https://minimal-agent.com
- **许可证**：MIT；主语言 Python（几乎零重型依赖）
- **核心代码量**：Agent 类 ≈100 行，environment/model/run 脚本各再加几十行，全部可通读
- **基准成绩**：SWE-bench verified（bash-only 榜）**>74%**；驱动 Ramp SWE-Bench；DeepSWE 上超过 Claude Code / Codex
- **官方推荐模型**：`anthropic/claude-opus-4-6` 档 / `openai/gpt-5.4`（经 LiteLLM 可接几乎所有模型）

---

## 核心功能

### 1. 极简到近乎「裸露」的控制流：一切只是 bash

mini-swe-agent 把编码 Agent 抽象到最小骨架，三个设计决定它「极简」：

| 设计选择 | 含义 |
|---|---|
| **只有 bash 一个工具** | 不注册 grep/edit/push 等工具，甚至不调用 LLM 的 tool-calling 接口——动作从回复里的三反引号代码块解析 |
| **完全线性的历史** | 每一步只向消息列表追加，没有历史压缩、没有分支，行为可预测 |
| **动作独立执行（subprocess.run）** | 每个命令都是独立子进程，不维护常驻 shell 会话，cd/export 不跨动作生效 |

官方把最后一条称为「trust me」原则：无状态执行避开了 shell 会话漂移、环境污染这一大类疑难 bug，代价是 Agent 要自己在每条命令里写全路径。对 LLM 来说这不是损失——它本来也很少正确维护跨命令状态。

### 2. 小骨架，大成绩：>74% SWE-bench verified

SWE-bench（bash-only 榜）专门评估「不同 LLM + 同一个极简 harness」的能力，剥离框架变量后直接看模型本身。mini-swe-agent 作为该榜标准 harness，配前沿模型可跑进 **74%+**（verified 子集），并作为底层驱动 **Ramp SWE-Bench**；在 DeepSWE 上**击败了 Claude Code 与 Codex**。结论很直白：**编码 Agent 的天花板主要由模型决定，脚手架做得越薄，模型能力透得越干净。**

### 3. 模型兼容性：LiteLLM 全家桶 + 开源模型友好

- 所有模型经 **LiteLLM** 接入（OpenAI / Anthropic / Gemini / 本地部署等），另支持 **OpenRouter、Portkey**；
- 支持 `/completion` 与 `/response` 两种端点形态、interleaved thinking；
- 正因为动作解析不依赖原生 tool-calling，**没有函数调用接口的开源/小模型也能直接驱动它**——这是很多「大框架」做不到的；
- 支持成本限额（`cost_limit`，计费失败的调用也会被计入，v2.4.6 修复）。

### 4. 完整的工程面：CLI、Python API、轨迹浏览器、批量评测

```bash
pip install mini-swe-agent
mini              # 交互式 CLI，丢一个 issue 进去
mini-extra        # 配置、密钥、评测等扩展工具
mini-extra swebench   # SWE-bench 批量评测：按实例隔离、并发、写 preds.json、回收沙箱
```

配套还有 **Python 绑定**（直接实例化 `DefaultAgent` 驱动，绕开交互确认，适合脚本化）、**轨迹浏览器**（可视化每一步命令与输出）、**E2B / Docker 沙箱**执行底座（阿里云函数计算云沙箱已有社区适配）。

### 5. 研究友好：做 FT/RL 的理想基线

官方 FAQ 明确推荐场景：**做模型微调（FT）或强化学习（RL），又不想让自己的策略过拟合到某个特定 Agent 脚手架**——mini-swe-agent 就是那个「最小可替换」的基线。它也是 minimal-agent.com 教程的主角，被当作「从零理解并构建一个编码 Agent」的标准教材。

---

## 适用人群

- **LLM 微调 / RL 研究者**：需要一个行为完全可控、可通读、可魔改的 Agent 基线，避免脚手架变量污染实验结果；
- **基准评测团队**：SWE-bench / DeepSWE / ProgramBench 批量评测要的就是稳定、快速、无状态漂移的 harness，`mini-extra swebench` 开箱即用；
- **想真正读懂编码 Agent 原理的开发者**：100 行 Agent 类 + 极简教程，比啃任何大框架源码都快；
- **个人/小团队的轻量 CLI 编码 Agent 需求**：本地跑 GitHub issue 修复、脚本化批处理，启动比大 CLI Agent 更快、依赖更干净；
- 不适用的：**需要 IDE 深度集成**（用 Cline/Roo Code/Claude Code）、**需要多工具协作与常驻会话状态**（用完整版 SWE-agent 或 OpenHands）的用户。

---

## 与同类工具对比

| 方案 | 定位 | mini-swe-agent 的差异 |
|---|---|---|
| **SWE-agent（完整版）** | 工具丰富、历史处理器可插拔、YAML 重配置 | mini 砍掉全部工具面只留 bash，100 行可读，沙箱与评测更快更稳 |
| **Claude Code / Codex CLI** | 闭源脚手架 + 强模型绑定，功能全但黑盒 | 完全开源透明、零锁定，DeepSWE 上反而赢了；但缺 IDE 级体验 |
| **OpenHands (OpenDevin)** | 事件驱动多 Agent + Web UI | 单循环 100 行，无 UI 开销，headless 环境更省心 |
| **Aider** | 终端交互式结对编程（人驱动，按块编辑） | mini 是**自主**跑完 issue（基准驱动），人只需验收 diff |
| **Cline / Roo Code** | IDE 扩展，每步人工确认 | CLI 独立运行，可脚本化、可批量，不依赖编辑器 |

一句话定位：它不是要取代 Claude Code 的「功能」，而是要证明**「模型在中央、脚手架退到最小」这条技术路线**——对研究者这是方法论，对使用者这是「100 行源码全看懂、随时能改」的底气。

---

## 如何使用

### 第一步：安装

```bash
# 隔离环境（推荐）
pip install uv && uvx mini-swe-agent

# 或当前环境
pip install mini-swe-agent
mini
```

### 第二步：配置模型与密钥

```bash
mini-extra config setup          # 首次运行自动引导
# 或手动
export ANTHROPIC_API_KEY=sk-...
mini-extra config set ANTHROPIC_API_KEY sk-...   # 写入配置文件，持久
# 换模型：直接填 litellm 命名（如 openai/gpt-5.4、anthropic/claude-opus-4-6-20260205）
```

### 第三步：丢一个 GitHub issue 给它

```bash
cd your-repo
mini "修复 issue #123：XXXX"
# Agent 循环：思考 → 发 bash → 看结果 → 再思考，直到自认为完成
# 结束时 diff 交给你验收，满意再提交
```

### 第四步：批量跑 SWE-bench（研究场景）

```bash
mini-extra swebench
# 按实例隔离、并发、写 preds.json、回收沙箱全部内置
```

非交互/脚本化环境注意：`mini` 收尾有交互确认，脚本里应直接驱动 Python API（`DefaultAgent`）而非 CLI。

### 第五步（进阶）：沙箱执行 + Python 绑定

```yaml
environment:
  environment_class: e2b   # 或 docker：动作在隔离沙箱里跑
```

```python
from minisweagent.agents.default import DefaultAgent
agent = DefaultAgent(config_yaml_path="my.yaml")
agent.interact_and_print()
```

---

## 总结

mini-swe-agent 是 2026 年编码 Agent 赛道里最有「反常识」色彩的项目：别人卷功能它卷删减，别人加厚脚手架它把 Agent 压回 100 行，结果 SWE-bench verified 74%+、驱动 Ramp 的大厂评测、DeepSWE 上击败 Claude Code 与 Codex。它给出的信息量大于工具本身——**「模型强到一定程度，编码 Agent 的最优解就是裸 bash + 线性历史」**，这对做 FT/RL 的人是方法论，对普通使用者是一份随时能读完、能改的透明实现。MIT 协议、零重型依赖，上车成本极低。

**扣分点：**

- **只有 bash 一个工具**：复杂工程里 IDE 级操作（精确多文件编辑、语义搜索）靠模型自己写命令，效率不如专用工具面；
- **无状态 shell**：cd/export 不跨动作生效，Agent 必须每条命令写全上下文（设计取舍，偶有绕路）；
- **强模型依赖**：换弱模型成绩直接掉档，「极简」只省脚手架不省 token；
- **无内置 UI/IDE 集成**：纯 CLI + 轨迹浏览器，重体验需求另找方案；
- **交互确认坑**：脚本化批量跑必须走 Python API，直接用 `mini` 会在收尾处 EOFError。

**推荐指数：⭐⭐⭐⭐☆（4/5）**

- **微调 / RL 研究者** → 首选基线，100 行源码随便改，4.5/5；
- **基准评测团队** → `mini-extra swebench` 直接用，稳定快速，4.5/5；
- **想搞懂编码 Agent 原理的人** → 配 minimal-agent.com 教程读完，4/5；
- **日常 IDE 重度用户** → 3/5，它更像「底层发动机」而非成品座驾。
