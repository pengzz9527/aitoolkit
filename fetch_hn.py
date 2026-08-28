#!/usr/bin/env python3
import json, urllib.request, time

# Fetch top HN story IDs
req = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json")
story_ids = json.loads(req.read())

stories = []
for sid in story_ids[:50]:
    try:
        req2 = urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
        story = json.loads(req2.read())
        if story.get('type') == 'story' and story.get('score', 0) >= 50:
            stories.append({
                'id': sid,
                'title': story.get('title', ''),
                'url': story.get('url', ''),
                'score': story.get('score', 0),
                'points': story.get('score', 0),
            })
    except Exception as e:
        pass
    time.sleep(0.05)

# Print AI-related stories
ai_keywords = ['ai', 'llm', 'gpt', 'openai', 'anthropic', 'deepseek', 'claude', 'gemini', 
               'model', 'neural', 'machine learning', 'gpt-4', 'gpt-5', 'reasoning',
               'agent', 'coding agent', 'code generation', 'rag', 'transformer',
               'llama', 'grok', 'xai', 'mistral', 'claude', 'o1', 'o3', 'chatgpt',
               'sora', 'multimodal', 'foundation', 'inference', 'api', 'chip',
               'nvidia', 'gpu', 'compute', 'hbm', 'memory', 'cost', 'pricing',
               'open source', 'github', 'hugging face', 'arxiv', 'paper',
               'benchmark', 'evaluation', 'safety', 'alignment', 'rlhf',
               'multimodal', 'vision', 'image', 'video', 'audio', 'speech',
               'reasonix', 'pricing', 'discount', 'financing', 'funding']

for s in stories:
    title_lower = (s['title'] + ' ' + s.get('url','')).lower()
    if any(kw in title_lower for kw in ai_keywords):
        print(f"ID:{s['id']} | Score:{s['score']} | {s['title']} | {s['url']}")
