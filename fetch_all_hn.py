#!/usr/bin/env python3
import urllib.request, json

# Get more HN top stories for AI news
hn_ids = [
    49161518, 49157930, 49156111, 49156683, 49132992,
    49162086, 49158581, 49156682, 49158474, 49155629,
    49156011, 49160437, 49157997, 49106935, 49161801,
    49082937, 49123105, 49131250, 49124213, 49159676,
    49154228, 49152842, 49158287, 49159970, 49158714,
    49160631, 49156750, 49153374, 49158141, 49157807
]

ai_keywords = ['ai', 'llm', 'gpt', 'openai', 'claude', 'anthropic', 'gemini', 'deepseek',
               'machine learning', 'neural', 'transformer', 'model', 'chatgpt',
               'grok', 'perplexity', 'mistral', 'agi', 'artificial intelligence',
               'robot', 'autonomous', 'agent', 'llama', 'vision', 'generation',
               'hugging', 'fine-tun', 'coding', 'inference', 'quantization',
               'r1', 'o1', 'qwen', 'claude', 'deepseek', 'glm', 'kimi',
               'benchmark', 'evaluation', 'reasoning', 'tool-use', 'mcp']

results = []
for sid in hn_ids:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            title_lower = data['title'].lower()
            url_lower = data.get('url', '').lower()
            combined = title_lower + ' ' + url_lower
            is_ai = any(k in combined for k in ai_keywords)
            results.append({
                'score': data['score'],
                'title': data['title'],
                'url': data.get('url', ''),
                'is_ai': is_ai,
                'comments': data.get('descendants', 0),
                'by': data.get('by', '')
            })
    except:
        pass

# Sort by score, show AI ones first
ai_results = sorted([r for r in results if r['is_ai']], key=lambda x: -x['score'])
other_results = sorted([r for r in results if not r['is_ai']], key=lambda x: -x['score'])

print("=== AI Related ===")
for r in ai_results[:15]:
    print(f"[{r['score']:5d}] {r['title'][:80]} | {r['url'][:100]}")

print("\n=== Other ===")
for r in other_results[:10]:
    print(f"[{r['score']:5d}] {r['title'][:80]} | {r['url'][:100]}")
