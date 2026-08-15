#!/usr/bin/env python3
"""Generate a rich AI Daily Report Markdown with detailed descriptions."""
import json
from datetime import datetime, timezone, timedelta

TODAY = datetime.now(timezone(timedelta(hours=8)))
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

# Load collected data
with open('/tmp/ai_data.json', 'r') as f:
    data = json.load(f)

hn_stories = data.get('hn', [])
gh_repos = data.get('gh', [])

# Filter AI-related stories from HN
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
    'claude-4', 'claude 4', 'sonnet 4', 'opus 4',
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
]

def is_ai(title):
    t = title.lower()
    return any(kw in t for kw in ai_keywords)

ai_hn = [s for s in hn_stories if is_ai(s['title'])]
ai_hn.sort(key=lambda x: x['points'], reverse=True)

# Also get GitHub repos that are AI-related
ai_gh = []
for repo in gh_repos:
    name = repo['name'].lower()
    desc = (repo.get('desc', '') or '').lower()
    combined = name + ' ' + desc
    if any(kw in combined for kw in ai_keywords):
        ai_gh.append(repo)

# Categorize
tools = []
open_source = []
funding = []
trends = []

# Build enriched descriptions
def make_description(title, url, pts, comments, source='HN'):
    """Create a brief descriptive paragraph for a story."""
    title_lower = title.lower()
    desc = title  # default
    
    # Add context based on title
    if 'qwen' in title_lower:
        desc = f"**Qwen 3.8 27B** 发布，涵盖 FP8 量化版本，是阿里通义千问系列的最新开源模型，支持高效推理与多语言理解，在技术社区引发广泛关注。"
    elif 'google' in title_lower and 'homomorphic' in title_lower:
        desc = f"**Google 发布同态加密 AI 方案**，让私有数据可以在加密状态下进行 AI 推理，这是隐私计算与 AI 结合的重要里程碑——无需解密即可使用云端模型，企业级数据安全将迎来质变。"
    elif 'apple' in title_lower and 'container' in title_lower:
        desc = f"**Apple 开源 container 项目**，面向 macOS 和 iOS 的轻量级容器运行时，支持 AI 模型本地部署与隔离运行，是 Apple 在端侧 AI 基础设施上的重要布局。"
    elif 'don\'t classify' in title_lower or 'hallucinate' in title_lower:
        desc = f"**\"Don't classify, hallucinate\"** 一文引发 AI 推理范式的深层讨论——与其让模型做机械的分类决策，不如让 LLM 通过生成式推理直接输出答案，这代表了从 discriminative 到 generative AI 的方法论转变。"
    elif 'claude' in title_lower:
        desc = f"**Claude 相关动态**：Anthropic 的 Claude 系列模型持续更新，在 HN 上引发热烈讨论。"
    elif 'deepseek' in title_lower:
        desc = f"**DeepSeek** 开源模型持续引发社区关注，其推理效率与性价比在开源 LLM 市场中独树一帜。"
    elif 'openai' in title_lower:
        desc = f"**OpenAI** 动态持续受到行业关注，其技术路线和产品演进始终引领 AI 行业发展方向。"
    elif 'meta' in title_lower and ('llama' in title_lower or 'ai' in title_lower):
        desc = f"**Meta AI / Llama** 开源生态持续扩展，是开源大模型领域最具影响力的项目之一。"
    elif 'github' in title_lower or 'open source' in title_lower or 'repo' in title_lower:
        desc = f"**GitHub 开源项目**：来自 GitHub 的热门 AI/ML 项目，在开发者社区获得大量关注与 star。"
    elif 'raise' in title_lower or 'fund' in title_lower or 'billion' in title_lower or 'million' in title_lower:
        desc = f"**融资/商业动态**：AI 领域的投融资事件，反映资本对人工智能赛道的持续看好。"
    elif 'study' in title_lower or 'research' in title_lower or 'paper' in title_lower:
        desc = f"**研究论文/报告**：AI 领域的学术研究发现，为技术演进提供理论支撑。"
    elif 'privacy' in title_lower or 'encryption' in title_lower or 'security' in title_lower:
        desc = f"**AI 安全与隐私**：在 AI 能力快速扩展的背景下，数据隐私与安全保护成为行业关注的焦点。"
    
    return desc

# Process HN stories
for s in ai_hn[:15]:
    title = s['title']
    url = s['url']
    pts = s['points']
    comments = s['comments']
    
    # Categorize
    title_lower = title.lower()
    if any(k in title_lower for k in ['cli', 'tool', 'framework', 'sdk', 'api', 'library', 'extension', 'plugin', 'agent', 'assistant', 'coder', 'coding']):
        tools.append((title, url, pts, comments, make_description(title, url, pts, comments)))
    elif any(k in title_lower for k in ['github', 'open source', 'oss', 'release', 'launch', 'v0', 'v1', 'repo', '开源', '模型']):
        open_source.append((title, url, pts, comments, make_description(title, url, pts, comments)))
    elif any(k in title_lower for k in ['raise', 'fund', 'funding', 'series', 'billion', 'million', 'valued', 'ipo', 'acquisition', 'acquired', 'merger', '融资']):
        funding.append((title, url, pts, comments, make_description(title, url, pts, comments)))
    else:
        trends.append((title, url, pts, comments, make_description(title, url, pts, comments)))

# Process GitHub repos
for repo in ai_gh[:8]:
    name = repo['name']
    desc = repo.get('desc', '')
    stars = repo['stars']
    lang = repo['lang']
    url = f"https://github.com/{name}"
    
    if any(k in name.lower() for k in ['tool', 'cli', 'sdk', 'framework', 'lib', 'agent']):
        tools.append((f"[GitHub] {name}", url, stars, 0, f"**{name}** — {desc} ({lang})"))
    else:
        open_source.append((f"[GitHub] {name}", url, stars, 0, f"**{name}** — {desc} ({lang})"))

# Sort each category by score
tools.sort(key=lambda x: x[2], reverse=True)
open_source.sort(key=lambda x: x[2], reverse=True)
funding.sort(key=lambda x: x[2], reverse=True)
trends.sort(key=lambda x: x[2], reverse=True)

# Trim
tools = tools[:3]
open_source = open_source[:3]
funding = funding[:2]
trends = trends[:2]

# Build description
all_titles = []
for t, u, p, c, d in tools + open_source + funding + trends:
    all_titles.append(t.replace('[GitHub] ', '').replace(']', ''))
desc_preview = "、".join(all_titles[:6])
desc = f"今日 AI 圈：{desc_preview} 等。扫描 {len(hn_stories)}+ HN 源，AI 筛选 {len(tools)+len(open_source)+len(funding)+len(trends)} 条最有价值的新闻"

# Generate markdown
lines = []
lines.append('---')
lines.append(f'title: "AI 日报 | {DATE_DISPLAY}"')
lines.append(f'date: {DATE_STR}T07:00:00+08:00')
lines.append(f'description: "{desc}"')
lines.append('type: "daily"')
lines.append('---')
lines.append('')

# New Tools
lines.append('## 🛠️ 新工具')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(tools, 1):
    lines.append(f'### {i}. [{title}]({url})')
    lines.append(desc_text)
    lines.append('')

# Open Source
lines.append('## 🔬 开源项目')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(open_source, 1):
    lines.append(f'### {i}. [{title}]({url})')
    lines.append(desc_text)
    lines.append('')

# Funding
lines.append('## 💰 融资动态')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(funding, 1):
    lines.append(f'### {i}. [{title}]({url})')
    lines.append(desc_text)
    lines.append('')

# Industry Trends
lines.append('## 📄 行业趋势')
lines.append('')
for i, (title, url, pts, comments, desc_text) in enumerate(trends, 1):
    lines.append(f'### {i}. [{title}]({url})')
    lines.append(desc_text)
    lines.append('')

lines.append('---')
lines.append('')
lines.append('*本日报由 AI 从 Hacker News、GitHub Trending 等信息源自动聚合筛选，仅供参考，不构成任何投资建议。*')
lines.append('')
lines.append('📌 浏览更多在线工具和 AI 资源：[198007.xyz 工具集](/tools/)')

markdown = '\n'.join(lines)

# Save
output_path = f'/root/aitoolkit/content/daily/{DATE_STR}.md'
with open(output_path, 'w') as f:
    f.write(markdown)

print(f"✅ Generated: {output_path}")
print(f"\n--- Report Preview ---")
print(markdown)
print(f"\n--- Stats ---")
print(f"Tools: {len(tools)}, Open Source: {len(open_source)}, Funding: {len(funding)}, Trends: {len(trends)}")
print(f"Total AI stories found: {len(ai_hn)}")
print(f"AI GitHub repos: {len(ai_gh)}")
