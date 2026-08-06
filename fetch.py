#!/usr/bin/env python3
import urllib.request, json

# Fetch HN top stories
ids = json.loads(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json').read())
stories = []
for sid in ids[:50]:
    try:
        data = json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json').read())
        if data.get('type') == 'story':
            stories.append(data)
    except:
        pass

# Filter AI related
ai_keywords = ['ai', 'llm', 'gpt', 'openai', 'claude', 'deepseek', 'anthropic', 'gemini',
               'machine learning', 'neural', 'transformer', 'model', 'agent', 'robot',
               'autonomous', 'coding agent', 'inference', 'quantization', 'benchmark']

for s in sorted(stories, key=lambda x: -x['score']):
    title_lower = s['title'].lower()
    url_lower = s.get('url', '').lower()
    is_ai = any(k in title_lower or k in url_lower for k in ai_keywords)
    if is_ai or s['score'] > 300:
        print(f"[{s['score']}] {s['title']} | {s.get('url', '')}")
