---
title: 'AgentMercury 评测：用强化学习训练的 MCP 工具调用专家'
date: 2026-08-18
tags: ['AI工具', 'Agent', '强化学习', 'MCP', '开源模型', '工具调用', 'HuggingFace']
categories: ['AI工具评测']
description: 'AgentMercury 是基于 Qwen3.5-35B-A3B 的 agentic RL 微调模型，专为 MCP 协议工具调用设计。采用单轨迹异步优化（SAO）方法，在合成企业环境中训练，奖励提升近一倍，截断率从 44% 降至 5%。'
---

## 一句话介绍

**AgentMercury** 是一款基于 Qwen3.5-35B-A3B MoE 架构、通过 **单轨迹异步强化学习（SAO）** 微调的开源工具调用模型，专为 MCP（Model-Context-Protocol）协议下的多轮自主任务完成而设计。

---

## 工具简介

在 AI Agent 领域，如何让大模型真正"干活"而非只是"聊天"，一直是核心难题。主流做法是在 API 上叠加工具调用层，或是在服务器上微调 70B+ 参数模型。但这些方案要么依赖闭源 API，要么对硬件门槛要求极高。

**AgentMercury** 走了一条更激进的路：它直接在 **35B 参数的 MoE 模型** 上，用 **强化学习（RL）** 训练工具调用能力，而非传统的 SFT（监督微调）。训练环境是一个包含邮箱、聊天、日历、CRM 等 10-26 个 MCP 工具的合成企业系统，模型需要在没有任何人工干预的情况下自主规划、搜索、执行，最终完成任务。

更关键的是，AgentMercury 采用了一种名为 **SAO（Single-Rollout Asynchronous Optimization）** 的新 RL 方法——每个提示只需一次采样（而非传统方法的 8 次），通过引入学习的 critic 模型来估计优势，大幅降低了长轨迹训练的同步等待成本。

- **HuggingFace**: https://huggingface.co/Minbyul/AgentMercury-Qwen3.5-35B-A3B-SAO
- **配套论文**: [arXiv:2607.07508](https://arxiv.org/abs/2607.07508)
- **许可证**: Apache-2.0
- **基础模型**: Qwen/Qwen3.5-35B-A3B（MoE 架构，35B 总参数，3.8B 激活）
- **语言**: 英文（训练语料全为英文）
- **推理框架**: SGLang（推荐）或 Transformers

---

## 核心功能

### 1. MCP 协议原生工具调用

AgentMercury 在训练时直接对接 **MCP（Model-Context-Protocol）** 标准，支持 10-26 个工具的多轮调用（平均 16.2 个/任务）。模型能够自主决定调用哪个工具、以什么参数调用、以及如何组合多个工具来完成复杂任务。与传统的 function calling 不同，MCP 提供了更标准化的工具描述和交互协议。

### 2. 单轨迹异步强化学习（SAO）

这是 AgentMercury 最核心的技术突破。传统 RL 方法（如 PPO）需要对每个提示采样多个轨迹（通常 8 条）来计算优势函数，这在长轨迹场景下代价极高。SAO 的做法是：

- **每条提示只需 1 次采样**，而非 8 次
- 引入一个**学习到的 critic 模型**（token 级别的 GAE 优势估计），替代组内均值基线
- **无需同步屏障**——任何一条轨迹完成后立即入队，不受最慢轨迹拖累

这使得 20 步长的 Agent 轨迹训练效率提升了数倍。

### 3. 状态变化的真实任务评估

与传统 RLHF 用"回答质量"作为奖励信号不同，AgentMercury 的奖励基于**环境最终状态的严格断言**：模型是否完成了所有要求的操作（创建/更新/删除记录）？奖励是**密集的部分分数**而非简单的通过/不通过，这意味着部分完成也能获得相应回报。

### 4. 去退化机制

训练过程中引入了一个行为乘数，对以下退化行为进行惩罚：

- 短语重复（输出啰嗦）
- 回答后的无效续写（"post-answer runaway"）
- 不必要的截断

这使得模型不仅"能做对"，还能"干净利落地做完"。

### 5. 长上下文支持

模型支持 **131072 token 上下文窗口**，能够处理复杂的长轨迹 Agent 任务。基准测试显示，模型的"所有效果通过率"从基线的 0.8% 提升到 4.7%，平均响应长度从 9.7k tokens 增长到 12.9k tokens，而截断率从 44% 骤降至 5%。

---

## 适用人群

- **AI Agent 研究者**：对强化学习在 Agent 领域的应用感兴趣，尤其是单轨迹 RL 方法的实验者
- **企业级 Agent 开发者**：需要构建基于 MCP 协议的多工具调用 Agent 的系统工程师
- **大模型部署工程师**：希望在本地部署 35B 级别 MoE 模型并启用工具调用能力的团队
- **RL for LLM 实践者**：对 SAO、actor-critic 在长轨迹场景下的应用感兴趣的研究人员

**不适合**的人群：

- 需要中文多语言支持的场景（训练语料全为英文）
- 需要多模态（视觉）理解的场景（该模型为纯文本输出）
- 资源受限无法部署 35B 模型的团队

---

## 与同类工具对比

| 维度 | AgentMercury (SAO) | AgentMercury (Group-Baseline) | 传统 SFT 工具调用模型 | Claude/GPT-4 API |
|---|---|---|---|---|
| 训练方法 | 单轨迹 RL（SAO） | 多轨迹 RL（8 rollout） | 监督微调 | API 调用 |
| 轨迹采样 | 1 条/提示 | 8 条/提示 | 无 | 无 |
| 奖励信号 | 环境状态断言 + LLM Judge | 同左 | 人工标注偏好 | 无（黑盒） |
| 工具协议 | MCP | MCP | 各厂商私有 | 各厂商私有 |
| 参数规模 | 35B MoE (3.8B 激活) | 35B MoE | 通常 7B-70B | 闭源 |
| 开源程度 | ✅ Apache-2.0 | ✅ Apache-2.0 | 部分开源 | ❌ 闭源 |
| 本地部署 | ✅ 需 A100-80G×1 或等效 | ✅ 同上 | ✅ 视参数量而定 | ❌ |
| 中文支持 | ❌ 英文为主 | ❌ 英文为主 | 部分模型支持 | ✅ |

**与 SGLang 生态的对比**：AgentMercury 专为 SGLang 推理引擎验证，其 MoE experts 以非融合格式存储，SGLang 的 `--moe-runner-backend triton` 是当前最优选择。相比之下，vLLM 对这种非融合 MoE 布局的支持仍在改进中。

---

## 如何使用

### 方式一：SGLang 部署（推荐）

```bash
# 安装 SGLang
pip install sglang[all]

# 启动推理服务器（需至少 80GB GPU 显存）
python3 -m sglang.launch_server \
  --model-path Minbyul/AgentMercury-Qwen3.5-35B-A3B-SAO \
  --served-model-name agentmercury-sao-35b \
  --host 0.0.0.0 --port 30000 \
  --tp-size 1 --context-length 131072 --mem-fraction-static 0.85 \
  --moe-runner-backend triton --attention-backend triton \
  --reasoning-parser qwen3 --tool-call-parser qwen3_coder \
  --trust-remote-code
```

部署成功后，通过 OpenAI 兼容端点调用：

```python
import openai

client = openai.Client(base_url="http://localhost:30000/v1", api_key="dummy")

response = client.chat.completions.create(
    model="agentmercury-sao-35b",
    messages=[{"role": "user", "content": "帮我查一下 CRM 系统中张三的最近订单状态"}],
    extra_body={"tools": [
        {"type": "function", "function": {
            "name": "get_order_status",
            "description": "查询订单状态",
            "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}
        }}
    ]}
)
```

**关键提醒**：务必设置 `--context-length 131072`，否则模型在短上下文下会返回空响应，看起来像是"坏模型"。

### 方式二：Transformers 直接加载

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "Minbyul/AgentMercury-Qwen3.5-35B-A3B-SAO",
    torch_dtype="bfloat16",
    device_map="auto",
    trust_remote_code=True,
)
tok = AutoTokenizer.from_pretrained(
    "Minbyul/AgentMercury-Qwen3.5-35B-A3B-SAO",
    trust_remote_code=True,
)
```

### 注意事项

1. **该模型为纯文本**，不含视觉编码器（vision tower），调用时请做好缺失权重处理
2. **MoE experts 为非融合格式**，SGLang 兼容性最好，其他推理引擎可能需额外适配
3. **模型是中途检查点**（第 159/200 步），训练仍在进行中，最终版本可能更强
4. **推理成本较高**：35B MoE 模型在单卡 A100-80G 上可运行，但多卡并行（TP=2/4）会更稳定

---

## 总结推荐指数

| 维度 | 评分（满分 5 分） |
|---|---|
| 技术创新性 | ⭐⭐⭐⭐⭐ |
| 工具调用能力 | ⭐⭐⭐⭐ |
| 开源友好度 | ⭐⭐⭐⭐⭐ |
| 部署便利性 | ⭐⭐⭐ |
| 中文支持 | ⭐ |
| 性价比（开源替代 API） | ⭐⭐⭐⭐ |

**总体推荐指数：4.0 / 5.0**

AgentMercury 代表了当前 **Agent RL 微调** 的前沿方向。SAO 方法在理论上 elegantly 解决了长轨迹 RL 的训练效率瓶颈，实验数据也显示了实质性的性能提升（奖励从 0.348 → 0.649，截断率从 44% → 5%）。

对于研究者，这是一份值得精读的实践案例——它展示了如何用强化学习让模型"真正干活"，而非只是"说得好听"。对于工程实践者，如果你正在构建基于 MCP 的企业级 Agent，AgentMercury 提供了一个高质量的开源起点，尽管它目前仍是英文单语言、纯文本的限制需要你评估是否适合你的场景。

**一句话评价**：在"让 AI 真正用工具解决问题"这条路上，AgentMercury 用强化学习给出了当前最扎实的答案之一。
