---
title: 'Jina Embeddings v4 评测：多模态多语言嵌入模型的新标杆'
date: 2026-06-30T08:00:00+08:00
description: 'Jina Embeddings v4 是 Jina AI 推出的新一代多模态多语言嵌入模型，支持文本、图像和视觉文档的统一嵌入，覆盖 30+ 语言，基于 Qwen2.5-VL-3B 构建，适用于 RAG、语义搜索和多模态检索等场景。'
tags:
  - AI
  - 嵌入模型
  - 多模态
  - 多语言
  - 工具评测
  - 开源
  - Jina AI
categories:
  - AI 工具评测
---

## 一句话介绍

**Jina Embeddings v4** 是 Jina AI 推出的新一代通用嵌入模型，基于 Qwen2.5-VL-3B-Instruct 构建，首次实现了文本、图像和视觉文档的统一嵌入表示。它支持 30+ 种语言，覆盖检索、文本匹配和代码理解三大任务，特别擅长处理包含图表、表格和插图的复杂文档。GitHub 星标 527+，是目前多模态嵌入领域最先进的开源模型之一。

---

## 核心功能

### 1. 统一的多模态嵌入

Jina Embeddings v4 最大的突破在于它能够同时处理纯文本、图像和视觉文档（如 PDF、图片格式的报表和图表），并将它们映射到同一个向量空间中。这意味着你可以用一段文字去检索相关的图片，也可以用一张图片去查找语义相似的文档，无需为每种模态单独训练模型。

这种统一嵌入的能力对于 RAG（检索增强生成）系统尤其重要——传统方案往往只能检索文本片段，而 Jina Embeddings v4 可以直接检索包含关键信息的图表和文档页面。

### 2. 强大的多语言支持

模型原生支持 30+ 种语言的嵌入计算，包括英语、中文、日语、韩语、阿拉伯语、法语、德语、西班牙语等主流语言。与以往的多语言模型不同，Jina Embeddings v4 在多语言场景下保持了极高的跨语言语义对齐能力，例如可以用中文查询检索英文文档，反之亦然。

### 3. 三种专用任务适配器

模型内置了三个任务特定的适配器（Adapter），可在推理时按需切换：

- **Retrieval（检索）**：专为文档检索优化，支持最大 32768 token 的上下文长度，适合构建 RAG 系统的知识库索引
- **Text-Matching（文本匹配）**：用于判断两段文本的语义相似度，适用于问答匹配、重复检测等场景
- **Code（代码理解）**：专门针对代码语义进行优化，可以用自然语言描述搜索代码片段，或反过来用代码搜索相关文档

### 4. 灵活的 Matryoshka 嵌入维度

Jina Embeddings v4 支持 Matryoshka 表示学习，即同一个模型可以输出不同维度的嵌入向量。默认维度为 2048，但可截断至 128、256、512 或 1024 维度，性能损失极小。这让你可以根据存储预算和检索精度需求灵活选择——在资源受限的边缘设备上可以使用 128 维，而在追求精度的生产环境中使用 2048 维。

### 5. 视觉文档检索（VDR）专长

这是 Jina Embeddings v4 区别于其他嵌入模型的核心竞争力。传统嵌入模型在处理包含复杂排版、表格、图表的文档时表现不佳，而 Jina Embeddings v4 基于视觉语言模型 Qwen2.5-VL 构建，能够理解文档的视觉结构。无论是财务报表中的柱状图、论文中的示意图还是产品手册中的装配图，模型都能将其转化为高质量的嵌入向量。

---

## 适用人群

- **RAG 系统开发者**：如果你正在构建基于大语言模型的检索增强系统，Jina Embeddings v4 可以提供比传统文本嵌入模型更丰富的语义表示，尤其适合处理包含图表和复杂排版的文档库
- **多模态搜索引擎工程师**：需要同时索引和检索文本、图像、PDF 文档的团队，可以借助此模型实现统一的向量搜索
- **企业知识库建设者**：大量企业内部文档（合同、技术手册、财务报表）都包含丰富的视觉元素，Jina Embeddings v4 能更好地理解和检索这些非纯文本内容
- **多语言应用开发者**：面向全球用户的搜索或推荐系统，需要在一个模型中覆盖多种语言场景
- **学术研究团队**：视觉文档检索（Visual Document Retrieval）是一个新兴的研究方向，Jina AI 同时发布了配套的 Jina-VDR 基准测试数据集

---

## 与同类工具对比

| 特性 | Jina Embeddings v4 | BGE-M3 | E5-Mistral | CLIP |
|------|-------------------|--------|------------|------|
| 多模态支持 | ✅ 文本+图像+视觉文档 | ❌ 仅文本 | ❌ 仅文本 | ✅ 文本+图像 |
| 多语言 | ✅ 30+ 语言 | ✅ 100+ 语言 | ❌ 主要英文 | ❌ 主要英文 |
| 最大序列长度 | 32768 token | 8192 token | 8192 token | 固定分辨率 |
| 任务适配器 | ✅ 检索/匹配/代码 | ❌ | ❌ | ❌ |
| Matryoshka 维度 | ✅ 128-2048 | ❌ | ❌ | ❌ |
| 视觉文档理解 | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐ |
| 许可证 | Qwen Research License | Apache 2.0 | Apache 2.0 | CC-BY-NC-4.0 |
| vLLM 兼容 | ✅ 独立版本 | ✅ | ✅ | ❌ |

**与 BGE-M3 对比**：BGE-M3 是多语言嵌入的经典选择，支持 100+ 语言和密集/稀疏/多向量三种检索方式。但 BGE-M3 仅处理纯文本，无法理解图像和视觉文档。如果你的知识库以文字为主，BGE-M3 仍是不错的选择；但如果涉及图表、扫描件或复杂排版文档，Jina Embeddings v4 的优势明显。

**与 CLIP 对比**：CLIP 是图像-文本检索的开创者，但它只处理标准尺寸的图像，无法理解文档页面的复杂布局。Jina Embeddings v4 在视觉文档理解方面远超 CLIP，因为它直接基于视觉语言模型构建，能够感知文档的结构化信息。

**独家优势**：Jina Embeddings v4 是唯一同时具备多语言、多模态、任务适配器和视觉文档理解四大能力的开源嵌入模型，在复杂文档检索场景下几乎没有直接竞争对手。

---

## 如何使用

### 方法一：通过 Jina AI API 使用（最简单）

Jina AI 提供了托管的嵌入 API，无需自行部署模型即可使用：

```bash
pip install jina
```

```python
from jina import JinaClient

client = JinaClient(api_key='YOUR_JINA_API_KEY')

# 文本嵌入
result = client.embed(
    model='jina-embeddings-v4',
    texts=['这是一段中文文本', 'This is English text'],
    task='retrieval'
)

# 图像嵌入
result = client.embed(
    model='jina-embeddings-v4',
    images=['https://example.com/chart.png'],
    task='retrieval'
)

# 多模态混合嵌入
result = client.embed(
    model='jina-embeddings-v4',
    input=[
        {'text': '气候变化对沿海城市的影响'},
        {'text': '海滩上美丽的日落'},
        {'image': 'https://example.com/beach.jpg'}
    ],
    task='retrieval'
)
```

### 方法二：本地部署（transformers）

如果你有 GPU 资源，可以选择本地部署以获得更好的隐私控制和成本效益：

```bash
pip install transformers>=4.52.0 torch>=2.6.0 peft>=0.15.2 torchvision pillow
```

```python
from transformers import AutoModel
import torch

# 加载模型
model = AutoModel.from_pretrained(
    'jinaai/jina-embeddings-v4',
    trust_remote_code=True,
    torch_dtype=torch.float16
)
model.to('cuda')

# 文本检索嵌入
query_emb = model.encode_text(
    texts=['Overview of climate change impacts'],
    task='retrieval',
    prompt_name='query'
)

# 图像嵌入
image_emb = model.encode_image(
    images=['https://example.com/chart.png'],
    task='retrieval'
)

# 多向量嵌入（late interaction）
multi_vec = model.encode(
    sentences=['这是一篇关于人工智能的长文档...'],
    task='retrieval',
    vector_type='multi'
)
```

### 方法三：通过 vLLM 高性能部署

对于高并发生产环境，Jina AI 提供了专门适配 vLLM 的版本：

```bash
# 检索任务 vLLM 版本
pip install vllm

# 启动服务
python -m vllm.entrypoints.api_server \
    --model jinaai/jina-embeddings-v4-vllm-retrieval \
    --port 8000
```

### 方法四：通过 sentence-transformers 接口

```bash
pip install sentence-transformers
```

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('jinaai/jina-embeddings-v4')

# 批量编码
embeddings = model.encode([
    '第一篇文章的内容',
    '第二篇文章的内容',
    '第三篇文章的内容'
], task='retrieval')

# 语义相似度计算
similarities = model.similarity(embeddings[0], embeddings[1:])
```

---

## 性能亮点

根据 Jina AI 官方发布的评估结果：

- **MTEB 多语言排行榜**：在多语言嵌入任务中位居前列，中文和英文检索准确率均超过 90%
- **Jina-VDR 基准测试**：在视觉文档检索任务上大幅领先传统文本嵌入模型，特别是在包含图表和表格的文档场景中
- **Matryoshka 效率**：使用 256 维嵌入即可达到 2048 维约 95% 的性能，但存储成本降低 87.5%
- **推理速度**：基于 3B 参数规模，在单张 A100 GPU 上可实现每秒数千条文本的嵌入计算

---

## 总结与推荐

**推荐指数：⭐⭐⭐⭐⭐（5/5）**

Jina Embeddings v4 是嵌入模型领域的一次重大飞跃。它将多语言、多模态和视觉文档理解三个曾经需要分别解决的问题整合到一个模型中，极大地简化了复杂检索系统的架构设计。

**值得推荐的理由：**
1. 视觉文档理解能力在开源嵌入模型中独一无二，特别适合处理 PDF、报表和含图表的技术文档
2. 三种任务适配器覆盖了检索、匹配和代码理解的主要应用场景
3. Matryoshka 嵌入设计让模型可以在精度和效率之间灵活权衡
4. 提供 API、transformers、vLLM 和 sentence-transformers 四种使用方式，门槛极低
5. 基于 Qwen2.5-VL 构建，继承了阿里通义千问优秀的多语言和多模态能力

**需要注意的地方：**
1. 模型基于 Qwen2.5-VL-3B，需要一定的 GPU 内存（至少 6GB 用于 FP16 推理）
2. 许可证为 Qwen Research License，商业使用需留意授权条款
3. 相比纯文本嵌入模型，推理延迟略高（因为需要处理视觉信息）

**最佳适用场景：** 构建面向复杂文档（PDF、报表、含图表的技术手册）的 RAG 系统，或需要同时检索文本和图像的多模态搜索应用。

如果你正在搭建 RAG 系统，不妨先用 [198007.xyz 的工具集](/tools/) 处理一下待嵌入的文本数据——比如用 [JSON 格式化工具](/tools/json-formatter/) 清洗结构化数据，或用 [文本计数器](/tools/word-counter/) 估算 token 数量。

**项目地址：** https://huggingface.co/jinaai/jina-embeddings-v4
**API 文档：** https://jina.ai/embeddings
**技术报告：** https://arxiv.org/abs/2506.18902
