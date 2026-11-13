---
title: 'DeepInfer 评测：DeepSeek 开源自家生产推理框架，25.9k 星，NVIDIA/Ascend 双平台，跑 V4.1-Flash'
date: 2026-11-13
tags: ['DeepInfer', 'DeepSeek', '推理框架', 'vLLM', 'SGLang', 'MoE', '专家并行', '投机解码', '鲲鹏昇腾', '开源工具']
categories: ['AI 工具评测']
description: 'DeepInfer 是 DeepSeek 于 2026 年 10 月 16 日开源的官方推理框架，GitHub 星标 25,900+、Fork 3,180+，Apache-2.0 协议。它就是支撑 DeepSeek 线上大规模服务的引擎，主打 MoE EP + EPLB、DSpark 投机解码、SWA 有界重放、异步调度与批不变推理，支持 NVIDIA SM100 与华为昇腾 950 双平台。'
---

# DeepInfer 评测：DeepSeek 开源自家生产推理框架，25.9k 星，NVIDIA/Ascend 双平台，跑 V4.1-Flash

**DeepInfer**（deepseek-ai/DeepInfer）是 DeepSeek 在 2026 年 10 月 16 日于 GitHub 开源的官方推理框架，仓库描述写得很直白：**"DeepInfer: High-performance, large-scale inference framework for DeepSeek models"**。README 开篇更是点明身份——**它就是支撑 DeepSeek 大规模线上服务的那套推理引擎**，这次开源的是其中用于离线推理、但已覆盖大规模服务核心能力的部分。

发布不到一个月，DeepInfer 已获得 **25,900+ 星标、3,180+ Fork**，在 GitHub 新建 AI 仓库里排在最前列。这个热度很好理解：过去大家只能靠 vLLM / SGLang「猜」DeepSeek 官方是怎么把 MoE 大模型跑得又快又省的，现在官方直接把答案交出来了。

- **GitHub 星标**：25,900+
- **GitHub 仓库**：https://github.com/deepseek-ai/DeepInfer
- **许可证**：Apache-2.0
- **语言**：Python（含大量 C++ / CUDA / TileLang 内核）
- **版本状态**：0.1.0，Beta
- **当前支持的模型**：DeepSeek-V4.1-Flash（默认 checkpoint 为 `deepseek-ai/DeepSeek-V4.1-Flash-1017`）
- **硬件**：NVIDIA SM100 GPU、华为昇腾 950 NPU
- **环境要求**：Linux、GCC ≥ 13、Python 3.12、CUDA 13（NVIDIA）或 CANN 9.2（昇腾）

---

## 核心功能

### 1. 官方调优的算子栈，不靠社区猜

DeepInfer 直接整合了 DeepSeek 自家的整套底层内核：[FlashMLA](https://github.com/deepseek-ai/FlashMLA)（MLA 注意力）、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM)（GEMM 库）、[DeepEP](https://github.com/deepseek-ai/DeepEP)（专家并行通信）、TileKernels、DeepSelect，以及仓库内自带的 TileLang 内核。这意味着你拿到的不是「通用框架 + 适配层」，而是**厂商自己跑生产用的那套实现**。这也是它和 vLLM 跑同一个模型时，性能曲线能贴得更近的根本原因。

### 2. MoE 专家并行 + EPLB 负载均衡

V4.1-Flash 是 MoE 架构，DeepInfer 的并行策略围绕这一点设计：**注意力走数据并行（DP）/ 均衡 CP，MoE 走专家并行（EP）+ EPLB（Expert-Parallel Load Balancing）**。EPLB 会周期性统计各专家的请求分布，把热门专家复制成冗余副本并重新分配，避免少数专家被挤爆、其余专家空转。文档里给出的实测 MoE 负载不均衡度 `moe_lb` 约为 1.090，已接近理想值。

### 3. DSpark 投机解码 + 置信度调度验证

内置投机解码（speculative decoding）方案 **DSpark**：先用草稿 token 加速解码，再用置信度估计来调度验证——置信度高的直接接受、低的才走完整验证，从而在保证输出质量的前提下提升吞吐。通过 `DEEPINFER_ENABLE_MTP_VARLEN=1` 开启，`DEEPINFER_USE_NEXTN_DECODE` 控制最大草稿长度（默认 5）。

### 4. SWA 有界重放：把 prefill 成本砍到常数

这是文档里最「硬核」的一项优化。对滑动窗口注意力（SWA）和 YOCO 架构，命中前缀缓存时不需要完整重算——**只重放最近 128 个 token，把注意力窗口截断在重放段内**，重算成本变成与上下文长度、层数无关的常数。官方称这项优化「几乎让总 prefill 计算减半」，128k 长上下文的收益尤其明显。

### 5. 异步调度 + 批不变推理 + 确定性采样

三个偏「工程可靠性」的特性，恰恰是生产环境最在意的：

- **异步调度**（默认开启）：CPU 批次调度与设备执行重叠，调度开销约等于零。
- **批不变推理**（`DEEPINFER_BATCH_INVARIANT=1`，仅 NVIDIA）：同一请求无论和谁拼在一个 batch 里，结果完全一致——这对离线评测和回归测试至关重要。
- **确定性采样**：相同输入 + 相同采样参数 + 固定 `seq_seed`，输出逐 token 复现，便于问题定位与自动化测试。

### 6. 结构化输出（regex / JSON Schema / EBNF）

通过 `SamplingParams` 的 `so_args={"schema_type": ..., "schema": ...}`，可以把生成严格约束成正则、JSON Schema 或 EBNF 文法。内置 `--check_structured_output` 可在一次离线运行里同时校验 PPL 和结构化输出，失败即整体失败，便于 CI 集成。

### 7. NVIDIA 与昇腾双平台

同一套代码同时支持 NVIDIA SM100 和华为昇腾 950，靠 `DEEPINFER_ACCELERATOR=nvidia|ascend` 切换。对国内团队来说这点价值不小——**在国产算力上跑官方最优实现，不用等第三方适配**。

---

## 适用人群

- **有 SM100 / 昇腾 950 集群的推理团队**：想把 V4.1-Flash 跑到接近官方线上水平，DeepInfer 是唯一「原厂」答案。
- **vLLM / SGLang 深度用户**：想搞清楚 DeepSeek 官方在 MoE 并行、投机解码、KV 缓存上到底做了哪些取舍，仓库本身就是最好的教材。
- **做 Agent / 长上下文产品的团队**：V4.1-Flash 支持 1M 上下文，配合 SWA 有界重放和 KV 缓存复用，长文档、多轮 Agent 场景的成本结构会明显改善。
- **国产算力适配方**：需要一套在昇腾上验证过的 DeepSeek 推理实现。
- **推理框架研究者**：EPLB、DSpark、批不变推理这些机制的代码与文档，都是第一手材料。

**不太适合：**

- **个人开发者 / 单卡用户**：硬件门槛极高，官方文档也明确说最高效的部署单元是 **64 卡 prefill + 64 卡 decode**，消费级显卡完全够不着。
- **想「一键跑起来」的人**：这是要自己编译 C++/CUDA、装 vendor 依赖、还可能自己补 KV 缓存系统的框架，不是 `pip install` 就能用的工具。
- **需要多模型统一服务的团队**：目前只支持 V4.1-Flash 一个模型，要做模型路由还得另搭一层。

---

## 与同类工具对比

| 维度 | DeepInfer | vLLM | SGLang | TensorRT-LLM |
|------|-----------|------|--------|--------------|
| 开源协议 | ✅ Apache-2.0 | ✅ Apache-2.0 | ✅ Apache-2.0 | ✅ Apache-2.0 |
| 出品方 | **DeepSeek 官方** | 社区 / 伯克利系 | 社区 / 清华系 | NVIDIA |
| 模型覆盖 | ❗仅 V4.1-Flash | ✅ 极广 | ✅ 广 | ✅ 主流模型 |
| 定位 | 官方生产引擎 | 通用推理框架 | 通用高性能框架 | NVIDIA 硬件最优 |
| MoE EP + EPLB | ✅ 官方实现 | ✅（EPLB 已内置） | ✅ | ✅ |
| 投机解码 | ✅ DSpark（置信度调度） | ✅ 多种 | ✅ EAGLE 等 | ✅ |
| 批不变推理 | ✅ 独立开关 | 部分 | 部分 | 部分 |
| 确定性采样 | ✅ 可逐 token 复现 | 部分 | 部分 | 部分 |
| 昇腾支持 | ✅ 官方 | 社区适配 | 社区适配 | ❌ |
| 上手难度 | **很高（源码编译）** | 低 | 中 | 高 |
| 直接可用度 | ❗需自补 KV 缓存 / PD 分离 | ✅ 开箱即用 | ✅ 开箱即用 | ✅ 需转换引擎 |

`pyproject.toml` 里 DeepInfer 自己写明「originally built primarily on vLLM，with additional inspiration from SGLang and TensorRT-LLM」——**它本质上是 vLLM 谱系上的一个深度特化分支**。这个对比结论因此很清晰：

- **追求模型广度和开箱即用** → vLLM / SGLang，DeepInfer 完全替代不了。
- **追求 V4.1-Flash 极限性能、且手里有对应硬件** → DeepInfer 是官方答案，尤其在昇腾上几乎没有竞品。
- **追求「官方怎么做」的可解释性** → DeepInfer 的价值可能不在跑，而在读。

> ⚠️ 三个必须知道的坑：
> 1. **开源的是「离线推理」，不是完整服务**。README 明确列出「not included in this release」的三项：KV 缓存系统、VE/Prefill/Decode 分离、DP 副本间负载均衡。其中 KV 缓存和负载均衡「与内部基础设施强耦合，尚未完全开源」，若要做生产级在线服务，这部分得自己补。
> 2. **只支持 V4.1-Flash 一个模型**，不是通用框架。
> 3. **检查点约 763B 总参数（FP8）**，权重和卡数开销都要按百 B 级别估算。

---

## 如何使用

### 第一步：准备环境

这是**从源码编译**的流程，先把前置条件对齐：

- Linux
- GCC ≥ 13.0
- Python 3.12（官方建议**新建一个空的 Python 3.12 虚拟环境**）
- NVIDIA：CUDA 13；昇腾：CANN 9.2

```bash
# 建一个干净的 3.12 环境（conda / uv / venv 都行）
python3.12 -m venv deepinfer-env
source deepinfer-env/bin/activate
```

### 第二步：拉代码并编译

```bash
git clone https://github.com/deepseek-ai/DeepInfer.git
cd DeepInfer

# NVIDIA 平台；昇腾平台改成 ascend
export DEEPINFER_ACCELERATOR=nvidia

./build.sh
```

`build.sh` 会做三件事：装对应平台的依赖（`requirements-nvidia.txt` 或 `requirements-ascend.txt`）、编译 vendor 目录下的第三方组件、编译 DeepInfer 本体。NVIDIA 路径还会顺带把 NCCL 强制装到 `2.32.3`。注意 `DEEPINFER_ACCELERATOR` 需要在**运行** DeepInfer 的环境里保持导出状态，不只是编译时。

### 第三步：跑一次离线推理

默认 checkpoint 是 `deepseek-ai/DeepSeek-V4.1-Flash-1017`，首次运行会自动从 Hugging Face 下载到本地缓存（体积很大，提前准备好盘）：

```bash
python examples/offline_inference.py
```

常用并行配置：

```bash
# 8 路专家并行
python examples/offline_inference.py --ep 8

# EP2 + DP8
python examples/offline_inference.py --ep 2 --dp 8

# EP2 + CP8
python examples/offline_inference.py --ep 2 --cp 8

# 长上下文压测（16389 输入 / 4096 输出）
python examples/offline_inference.py --long_context

# 顺带校验结构化输出（regex / JSON / EBNF）
python examples/offline_inference.py --check_structured_output
```

已经下好权重的话，直接用本地目录，避免联网：

```bash
export DEEPINFER_HF_MODEL_DIR=/path/to/DeepSeek-V4.1-Flash-1017
python examples/offline_inference.py --ep 8
```

> 小提示：`DEEPINFER_HF_MODEL_DIR` 只对默认模型生效，如果你显式传了 `--model_name`，以 `--model_name` 为准。

### 第四步：压测拿性能数据

想看吞吐/延迟曲线，用 `benchmark.py`。prefill 和 decode 两个阶段是解耦的，可以分别调参：

```bash
# 单节点先设定可见设备
export WORLD_SIZE=1 RANK=0
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

# 默认配置
python examples/benchmark.py

# CP8 + prefill chunk 放大到 65536
python examples/benchmark.py --cp 8 --prefill_batch_size 65536

# 低延迟：单请求 decode
python examples/benchmark.py --decode_num_requests 1

# 128k 上下文 + YoCo 截断
python examples/benchmark.py --decode_num_requests 64 --context_length 131072 --yoco_clip
```

跑完 `dp_rank 0` 会打印三个核心指标：**prefill 吞吐（tokens/s/GPU）**、**decode 平均 SPS（steps/s）**、**decode 吞吐（tokens/s/GPU）**。加 `--result_jsonl <FILE>` 可把原始数据落成 JSONL。想画帕累托曲线，用 `examples/sweep/run_sweep.sh` 扫一批点再用 `plot_pareto.py` 出图。

### 第五步：调几个关键开关

| 目标 | 设置 |
|------|------|
| 开投机解码 | `DEEPINFER_ENABLE_MTP_VARLEN=1`，草稿长度用 `DEEPINFER_USE_NEXTN_DECODE`（默认 5，设 0 关闭） |
| 长上下文 prefill 截断 | `DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact` + `DEEPINFER_YOCO_PREFILL_KEEP_TOKENS=140`（默认值） |
| 批不变推理 | `DEEPINFER_BATCH_INVARIANT=1`（仅 NVIDIA） |
| 确定性采样 | `DEEPINFER_BATCH_INVARIANT=1` + `DEEPINFER_ENABLE_MTP_VARLEN=0`，并给 `SamplingParams` 传固定 `seq_seed` |
| 结构化输出 | `SamplingParams(so_args={"schema_type": ..., "schema": ...})` |

参考 `examples/_structured_output.py` 和 `examples/README.md`，参数细节都在里面。

### 第六步：如果要做在线服务

这一步官方没给现成的。README 明确说明还缺 **KV 缓存系统、PD 分离、DP 副本负载均衡** 三块，但「most required engine functionality is already implemented」。Q&A 文档（`doc/inference_deployment_qa.md`）详细讲了官方线上方案的设计与实测数据，包括 EPLB 参数、KV 缓存分层、解码负载均衡的路由策略等，可以据此自行补齐——这部分内容本身就有很高的参考价值。

---

## 总结

DeepInfer 是 2026 年推理框架领域最值得关注的发布之一，原因不在「又多了一个框架」，而在**它是第一次由模型厂商把自家线上推理系统的核心部分公开**。25.9k 星标反映了社区长期存在的需求：不要再靠猜，把答案给出来。

它的技术含量是实打实的：FlashMLA / DeepGEMM / DeepEP 的官方整合、MoE EP + EPLB、DSpark 置信度投机解码、SWA 有界重放把 prefill 成本压成常数、异步调度与批不变推理——这些都是从真实大流量生产环境里磨出来的取舍，而不是论文里的理想假设。

**扣分点：**

- **硬件门槛极高**：只有 SM100 和昇腾 950 两条路径，高效部署单元是 64+64 卡，个人和中小团队基本无缘
- **不是完整服务**：KV 缓存、PD 分离、副本负载均衡三项未开源，做在线服务要自己补
- **只支持一个模型**：V4.1-Flash，通用性远不如 vLLM / SGLang
- **编译部署成本高**：源码编译 + CUDA 13 / CANN 9.2 + GCC 13 + Python 3.12，任一项对不上就得排查半天
- **版本还是 0.1.0 Beta**：接口和默认配置都在快速变动，没有正式 release，也没有 tag
- **文档门槛**：Q&A 写得非常细，但默认读者是熟悉推理系统的工程师，新手读起来会吃力

**推荐指数：⭐⭐⭐⭐（4/5）**

- **有 SM100 或昇腾 950 集群、要跑 V4.1-Flash** → **强烈建议上手**，这是唯一的原厂最优解，昇腾上尤其如此。
- **用 vLLM / SGLang 但想学官方怎么做** → **强烈建议读代码和 Q&A 文档**，即使不部署，收获也很大。
- **只有消费级显卡 / 单机** → **不用试**，直接上 vLLM 跑量化版更实际。
- **需要一套框架服务多种模型** → **继续用 vLLM / SGLang**，DeepInfer 不是这个定位。
