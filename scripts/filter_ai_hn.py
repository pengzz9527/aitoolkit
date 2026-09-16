#!/usr/bin/env python3
"""Parse main HN data for AI-related stories."""
import json

with open('/tmp/hn_algolia.json', 'r') as f:
    data = json.load(f)

hits = data.get('hits', [])
ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'claude', 'gemini', 'model', 'agent', 'openai', 'anthropic', 'deepseek', 'llama', 'neural', 'transformer', 'benchmark', 'inference', 'training', 'rag', 'vector', 'embedding', 'computer vision', 'robot', 'autonomous']

for h in hits[:30]:
    title = h.get('title', '').lower()
    url = h.get('url', '') or ''
    desc = h.get('url', '').lower()
    combined = title + ' ' + url + ' ' + desc
    is_ai = any(kw in combined for kw in ai_keywords)
    if is_ai:
        score = h.get('points', 0)
        comments = h.get('num_comments', 0)
        print(f"AI:{title} | Score:{score} | Comments:{comments} | URL:{h.get('url','')}")
