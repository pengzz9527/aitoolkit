#!/usr/bin/env python3
import urllib.request, json, urllib.parse

# HN stories
ids = json.loads(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json').read())
hn = []
for sid in ids[:100]:
    try:
        d = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if d.get('type') == 'story':
            hn.append(d)
    except:
        pass

# GitHub trending repos
url = 'https://api.github.com/search/repositories?q=created:>=2026-08-03&sort=stars&order=desc&per_page=20'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
gh = json.loads(urllib.request.urlopen(req).read()).get('items', [])

# Filter AI
ai_kw = ['ai', 'llm', 'gpt', 'openai', 'claude', 'deepseek', 'anthropic', 'gemini',
         'machine learning', 'neural', 'transformer', 'agent', 'robot', 'autonomous',
         'inference', 'quantization', 'benchmark', 'coding agent']

print("=== HN ===")
for s in sorted(hn, key=lambda x: -x['score'])[:20]:
    t = (s['title'] + ' ' + s.get('url', '')).lower()
    if any(k in t for k in ai_kw) or s['score'] > 300:
        print(f"[{s['score']}] {s['title']} | {s.get('url', '')}")

print("\n=== GitHub ===")
for r in gh[:10]:
    d = (r['full_name'] + ' ' + (r.get('description') or '')).lower()
    if any(k in d for k in ai_kw):
        print(f"{r['stargazers_count']} ⭐ | {r['full_name']} | {r.get('description', '')[:80]}")
