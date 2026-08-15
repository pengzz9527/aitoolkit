#!/usr/bin/env python3
"""Generate a rich AI Daily Report from enriched data."""
import json
from datetime import datetime, timezone, timedelta

# Load enriched data
with open('/tmp/ai_data_full.json', 'r') as f:
    data = json.load(f)

hn_stories = data.get('hn', [])
gh_repos = data.get('gh', [])
DATE_STR = data.get('date_str', datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"))
DATE_DISPLAY = data.get('date_display', datetime.now(timezone(timedelta(hours=8))).strftime("%B %d, %Y").replace(" 0", " "))

# AI keywords
ai_keywords = [
    'ai', 'llm', 'gpt', 'claude', 'gemini', 'openai', 'anthropic', 'meta',
    'machine learning', 'deep learning', 'neural', 'transformer', 'model',
    'chatgpt', 'llama', 'mistral', 'cohere', 'perplexity', 'hugging',
    'diffusion', 'sora', 'vision', 'rag', 'agent', 'agentic',
    'foundation model', 'ollama', 'grok', 'xai', 'cursor', 'langchain',
    'langgraph', 'llama.cpp', 'vllm', 'sglang', 'mllm', 'multimodal',
    'reasoning', 'o1', 'o3', 'deepseek', 'qwen', 'gemma', 'agi',
    'prompt', 'fine-tune', 'rlhf', 'reinforcement learning',
    'mixture of experts', 'moe', 'kv cache', 'quantization',
    'inference', 'serve', 'gpt-4o', 'gpt-4.5', 'gpt-5',
    'claude-4', 'claude 4', 'sonnet 4', 'opus 4', 'opus 5', 'opus 5', 'opus',
    'hallucinate', 'hallucination', 'classify',
    'ai news', 'ai launch', 'ai tool', 'ai product',
    'chatbot', 'conversational ai', 'llm agent', 'coding assistant',
    'stable diffusion', 'text to image', 'text to video',
    'computer vision', 'natural language', 'nlp',
    'neural network', 'attention mechanism', 'parameter',
    'training data', 'benchmark', 'eval', 'score',
    'open source', 'api', 'sdk', 'framework',
    'claude computer use', 'computer use',
    'claude 4.6', 'claude sonnet 4.6', 'claude desktop',
    'google ai', 'google deepmind', 'alphafold',
    'ai safety', 'ai regulation', 'ai policy',
    'openrouter', 'fireworks', 'replicate', 'databricks',
    'coding agent', 'ai coding', 'autogpt',
    'homomorphic', 'encryption', 'privacy',
    'glm', 'cyber', 'capability',
    'verifier', 'gpu', 'kernel',
    'show hn',
]

def is_ai(title):
    t = title.lower()
    return any(kw in t for kw in ai_keywords)

ai_hn = [s for s in hn_stories if is_ai(s['title'])]
ai_hn.sort(key=lambda x: x['points'], reverse=True)

# GitHub AI repos
ai_gh = []
for repo in gh_repos:
    name = repo['name'].lower()
    desc = (repo.get('desc', '') or '').lower()
    combined = name + ' ' + desc
    if any(kw in combined for kw in ai_keywords):
        ai_gh.append(repo)

print(f"AI HN stories: {len(ai_hn)}")
for s in ai_hn:
    print(f"  [{s['points']}] {s['title']}")
print(f"\nAI GitHub repos: {len(ai_gh)}")
for r in ai_gh:
    print(f"  [{r['stars']}⭐] {r['name']}")

# Detailed descriptions for top HN stories
story_descriptions = {
    "GLM-5.3: Frontier coding with emergent cyber capabilities": {
        "cat": "open_source",
        "desc": "**智谱 AI 发布 GLM-5.3**，在 HN 上以 **1015 点赞 / 500 评论** 成为今日 AI 话题最高票。核心亮点：**(1) 编码能力前沿突破**：GLM-5.3 在代码生成、理解和调试方面达到了行业领先水平；**(2) 涌现的网络安全能力**：模型展现出此前未曾预期的安全相关能力，包括漏洞发现和防御建议；**(3) 开源策略**：智谱继续延续其开源路线，让更多研究者和开发者能够基于此模型进行二次开发。GLM-5.3 的发布标志着中国 AI 大模型在编码和网络安全领域迈出了重要一步，与 DeepSeek、Qwen 等共同构成了开源 LLM 的多元格局。（z.ai Blog，HN 1015 点赞）"
    },
    "Qwen 3.8 27B": {
        "cat": "open_source",
        "desc": "**阿里通义千问 Qwen 3.8 27B 开源模型**在 Hugging Face 上线，HN 热度 **786 点赞 / 517 评论**。核心亮点：**(1) FP8 量化版本**：官方提供了 FP8 精度版本，在几乎不损失精度的前提下大幅降低显存占用，使 27B 参数模型可以在消费级 GPU 上高效运行；**(2) 多语言支持**：继续强化中文和英文的理解与生成能力；**(3) 开源生态友好**：兼容主流推理框架如 vLLM、SGLang 等。Qwen 系列持续以高性能开源模型挑战闭源模型的领先地位，27B 规模恰好卡在\"高性能+可部署\"的黄金区间。（Hugging Face，HN 786 点赞）"
    },
    "Why does Opus 5 feel worse to work with?": {
        "cat": "trends",
        "desc": "**Claude Opus 5 用户体验争议**在 HN 上引发 **714 点赞 / 650 评论** 的激烈讨论——评论数甚至超过了点赞数，成为今日最具争议性的 AI 话题。作者通过实际工作场景对比指出，虽然 Opus 5 在基准测试中分数更高，但在实际编码和写作任务中，**用户体验反而不如前代**。核心讨论点：**(1) 基准测试与实际体验的脱节**：评测分数不能完全代表真实可用性；**(2) \"流畅度\"的主观性**：AI 输出是否\"感觉更好\"涉及大量主观因素，包括响应速度、格式偏好、错误模式等；**(3) 行业反思**：当所有顶级模型都在追求评测分数时，用户体验是否被忽视了？HN 评论区出现了大量开发者分享自己的实测对比，这场讨论反映了行业对 AI 模型评价体系的深层思考。（Mun Logadan Blog，HN 714 点赞）"
    },
    "Google is making private AI practical with homomorphic encryption": {
        "cat": "trends",
        "desc": "**Google 发布同态加密 AI 推理方案**，在 HN 上获得 **232 点赞 / 141 评论**。核心突破：**(1) 加密状态下的 AI 推理**：用户数据在加密状态下即可被模型处理，无需解密；**(2) 实用化进展**：Google 表明该技术已达到可在生产环境中部署的水平；**(3) 企业级隐私保护**：对于医疗、金融等敏感行业，这意味着可以使用强大的云端 AI 模型而无需担心数据泄露。同态加密曾是理论概念，如今正在走向实际应用——这是隐私计算与 AI 融合的重要里程碑。该技术若被广泛采用，将彻底改变企业 AI 部署的隐私保护范式。（Google Security Blog，HN 232 点赞）"
    },
    "Don't classify, hallucinate": {
        "cat": "trends",
        "desc": "**\"Don't classify, hallucinate\"** 一文在 HN 获得 **211 点赞 / 82 评论**，提出一个颠覆性的 AI 推理方法论：与其让模型做机械的分类决策，不如让 LLM 通过生成式推理直接输出答案。核心论点：**(1) 分类的局限性**：传统分类任务需要预定义类别，限制了模型的创造力；**(2) 幻觉作为优势**：在开放域问题中，\"幻觉\"（即生成式推理）反而是更强大的能力；**(3) 方法论转变**：从判别式 AI 转向生成式 AI 是更自然的进化路径。这篇文章引发了对 AI 推理本质的哲学讨论——当模型能够\"想象\"出答案时，我们是否还需要严格的分类边界？（Software Doug Blog，HN 211 点赞）"
    },
    "AI by Hand": {
        "cat": "tools",
        "desc": "**AI by Hand** 在 HN 获得 **163 点赞**，是一个倡导\"手动构建 AI\"理念的项目/博客。核心理念：在 AI 工具泛滥的时代，**理解 AI 的内部工作原理**比熟练使用工具更重要。通过手写代码实现神经网络、从头训练小模型，开发者可以获得对 AI 系统的深层理解——这种\"第一性原理\"思维在 Copilot 和 Claude Code 普及的当下尤为珍贵。该项目呼应了技术社区中越来越强的\"反黑盒\"思潮：当 AI 成为基础设施时，理解其基础原理是避免被工具绑架的关键。（byhand.ai，HN 163 点赞）"
    },
    "Maximizing the value of your Claude Code sessions": {
        "cat": "tools",
        "desc": "**Anthropic 官方博客**发布 **《Maximizing the value of your Claude Code sessions》**，在 HN 获得 **109 点赞 / 75 评论**。文章系统性地分享了 Claude Code 的最佳实践：**(1) 提示工程**：如何撰写高效的 prompt 以获得更准确的代码生成；**(2) 上下文管理**：在长时间会话中保持上下文质量的方法；**(3) 调试策略**：当 Claude Code 给出错误代码时的有效纠偏技巧。作为官方文档，这篇文章反映了 Claude Code 正在从\"实验性工具\"走向\"生产级开发辅助\"——Anthropic 在持续投入资源完善其开发者体验。（Anthropic Blog，HN 109 点赞）"
    },
    "Show HN: Mole – Deep research agent for your terminal": {
        "cat": "tools",
        "desc": "**Mole** 是一个终端中的深度研究 AI Agent，在 Show HN 获得 **35 点赞**。核心功能：**(1) 终端原生**：直接在命令行中运行，无需打开浏览器或 GUI；**(2) 深度研究**：能够自主搜索、阅读和总结多源信息；**(3) 开发者友好**：输出结构化结果，便于后续处理。在 \"AI Agent\" 成为 2026 年最热技术趋势的当下，Mole 切入的是一个尚未被巨头占领的细分市场——**终端研究者**。与 Cursor、Claude Code 等编码助手不同，Mole 专注于信息搜集和知识整合，适合需要快速调研的技术人员和研究者。（GitHub，Show HN 35 点赞）"
    },
    "A Contract-Grade Verifier for LLM-Generated GPU Kernels": {
        "cat": "open_source",
        "desc": "**\"A Contract-Grade Verifier for LLM-Generated GPU Kernels\"** 论文在 HN 获得 **29 点赞**，针对一个被广泛忽视的问题：LLM 生成的 GPU 内核代码可能存在微妙的正确性漏洞。核心贡献：**(1) 形式化验证**：提出了一套基于合约的验证框架，可以严格证明 LLM 生成的 GPU 代码的正确性；**(2) 实用性**：针对 CUDA/OpenCL 等主流 GPU 编程模型设计；**(3) 行业需求**：随着 LLM 被广泛用于自动生成高性能计算代码，确保这些代码的正确性变得日益重要。这篇论文填补了 AI 代码生成与形式化验证之间的关键空白。（arXiv:2608.12700，HN 29 点赞）"
    }
}

# GitHub repo descriptions
gh_descriptions = {
    "tensorflow/tensorflow": "Google 开源的端到端机器学习平台，支持从训练到部署的全生命周期，是 AI 基础设施的基石。",
    "huggingface/transformers": "Hugging Face 的 transformers 库，提供了数千个预训练模型的统一接口，是 NLP 和多模态 AI 开发的首选框架。",
    "agentscope-ai/qwenpaw": "基于 Qwen 模型的 AI 助手框架，支持多平台部署和自定义 Agent 行为，是个人 AI 助手的重要开源方案。",
    "gradio-app/gradio": "Gradio 是最流行的 ML 模型演示工具，一行代码即可创建可分享的 Web UI，广泛用于 AI 项目展示。",
    "ashishpatel26/500-ai-machine-learning-deep-learning-computer-vision-nlp-projects-with-code": "包含 500 个 AI/ML 项目的完整教程集合，覆盖计算机视觉、NLP、深度学习等方向，是学习实践的宝贵资源。",
    "lutzroeder/netron": "神经网络可视化工具，支持多种模型格式，帮助开发者理解和分析 AI 模型结构。",
    "eriklindernoren/ml-from-scratch": "从零实现的机器学习算法库，用纯 NumPy 编写，是理解 ML 原理的优秀教学项目。",
    "madslorentzen/ai-job-search": "基于 Claude Code 的 AI 求职助手，自动评估职位、定制简历和 Cover Letter，代表 AI Agent 在垂直领域的应用。",
}

# Categorize
tools = []
open_source = []
funding = []
trends = []

# Process HN stories
seen_titles = set()
for s in ai_hn:
    title = s['title']
    url = s['url']
    pts = s['points']
    comments = s['comments']
    
    if title in seen_titles:
        continue
    seen_titles.add(title)
    
    desc_entry = story_descriptions.get(title, None)
    if desc_entry is None:
        desc = "**" + title + "** 在 HN 获得 " + str(pts) + " 点赞 / " + str(comments) + " 评论，引发技术社区广泛关注。"
    else:
        desc = desc_entry.get('desc', title)
    
    title_lower = title.lower()
    # Tools: CLI, agent, assistant, coder, tool-specific
    if any(k in title_lower for k in ['show hn', 'tool', 'cli', 'framework', 'sdk', 'api', 'agent', 'assistant', 'coder', 'coding', 'verifier', 'by hand', 'mole', 'greptile']):
        tools.append((title, url, pts, comments, desc))
    # Open Source: model releases, github projects, glm, qwen
    elif any(k in title_lower for k in ['github', 'open source', 'oss', 'release', 'launch', '开源', 'glm', 'qwen', 'verifier', 'model', '27b', 'llama', 'mistral', 'deepseek', 'qwen', 'gemma']):
        open_source.append((title, url, pts, comments, desc))
    # Funding
    elif any(k in title_lower for k in ['raise', 'fund', 'funding', 'series', 'billion', 'million', 'valued', 'ipo', 'acquisition', '融资']):
        funding.append((title, url, pts, comments, desc))
    # Trends: everything else (Opus 5, hallucinate, etc.)
    else:
        trends.append((title, url, pts, comments, desc))

# Add GitHub repos (top 3)
gh_added = 0
for repo in ai_gh[:8]:
    name = repo['name']
    url = "https://github.com/" + name
    stars = repo['stars']
    name_lower = name.lower()
    desc = gh_descriptions.get(name_lower, "**" + name + "**" + " — " + (repo.get('desc', '') or '') + " (" + (repo.get('lang', '') or '') + ")")
    
    if 'tool' in name_lower or 'agent' in name_lower or 'cli' in name_lower:
        tools.append(("[GitHub] " + name, url, stars, 0, desc))
    else:
        open_source.append(("[GitHub] " + name, url, stars, 0, desc))
    gh_added += 1
    if gh_added >= 3:
        break

# Sort and trim
tools.sort(key=lambda x: x[2], reverse=True)
open_source.sort(key=lambda x: x[2], reverse=True)
funding.sort(key=lambda x: x[2], reverse=True)
trends.sort(key=lambda x: x[2], reverse=True)

tools = tools[:3]
open_source = open_source[:3]
funding = funding[:2]
trends = trends[:3]

# Build description
all_titles = []
for t, u, p, c, d in tools + open_source + funding + trends:
    clean = t.replace('[GitHub] ', '').replace(']', '').replace('[', '')
    all_titles.append(clean)
desc_preview = "、".join(all_titles[:6])
total_count = len(tools) + len(open_source) + len(funding) + len(trends)
desc = "今日 AI 圈：" + desc_preview + " 等。扫描 " + str(len(hn_stories)) + "+ HN 源，AI 筛选 " + str(total_count) + " 条最有价值的新闻"

# Generate markdown
lines = []
lines.append('---')
lines.append('title: "AI 日报 | ' + DATE_DISPLAY + '"')
lines.append('date: ' + DATE_STR + 'T07:00:00+08:00')
lines.append('description: "' + desc + '"')
lines.append('type: "daily"')
lines.append('---')
lines.append('')

# New Tools
lines.append('## 🛠️ 新工具')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(tools, 1):
    lines.append('### ' + str(i) + '. [' + title + '](' + url + ')')
    lines.append(desc_text)
    lines.append('')

# Open Source
lines.append('## 🔬 开源项目')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(open_source, 1):
    lines.append('### ' + str(i) + '. [' + title + '](' + url + ')')
    lines.append(desc_text)
    lines.append('')

# Funding
lines.append('## 💰 融资动态')
lines.append('')
if funding:
    for i, (title, url, pts, comments, desc_text) in enumerate(funding, 1):
        lines.append('### ' + str(i) + '. [' + title + '](' + url + ')')
        lines.append(desc_text)
        lines.append('')
else:
    lines.append('*今日暂无重要融资动态。*')
    lines.append('')

# Industry Trends
lines.append('## 📄 行业趋势')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(trends, 1):
    lines.append('### ' + str(i) + '. [' + title + '](' + url + ')')
    lines.append(desc_text)
    lines.append('')

lines.append('---')
lines.append('')
lines.append('*本日报由 AI 从 Hacker News、GitHub Trending 等信息源自动聚合筛选，仅供参考，不构成任何投资建议。*')
lines.append('')
lines.append('📌 浏览更多在线工具和 AI 资源：[198007.xyz 工具集](/tools/)')

markdown = '\n'.join(lines)

# Save
output_path = '/root/aitoolkit/content/daily/' + DATE_STR + '.md'
with open(output_path, 'w') as f:
    f.write(markdown)

print("Generated: " + output_path)
print("\n--- Full Report ---")
print(markdown)
print("\n--- Stats ---")
print("Tools: " + str(len(tools)) + ", Open Source: " + str(len(open_source)) + ", Funding: " + str(len(funding)) + ", Trends: " + str(len(trends)))
print("Total AI stories found: " + str(len(ai_hn)))
print("Total AI GitHub repos: " + str(len(ai_gh)))
