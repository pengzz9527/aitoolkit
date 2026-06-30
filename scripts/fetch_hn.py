#!/usr/bin/env python3
"""Fetch HN top stories and AI-related news."""
import json, urllib.request, sys

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Reporter/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

# Fetch HN top stories
try:
    ids = fetch_json('https://hacker-news.firebaseio.com/v0/topstories.json')
    stories = []
    for iid in ids[:30]:
        try:
            item = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{iid}.json')
            if item and item.get('title'):
                stories.append({
                    'id': iid,
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'points': item.get('points', 0),
                    'comments': item.get('descendants', 0),
                    'type': item.get('type', '')
                })
        except:
            pass
    
    # Sort by points
    stories.sort(key=lambda x: x['points'], reverse=True)
    
    # Print AI-related ones prominently
    ai_keywords = ['ai', 'llm', 'gpt', 'openai', 'anthropic', 'claude', 'gemini', 
                   'model', 'machine learning', 'deep learning', 'neural', 'transformer',
                   'diffusion', 'stable diffusion', 'mistral', 'grok', 'xai',
                   'artificial intelligence', 'coder', 'agent', 'rag', 'vector',
                   'embeddings', 'chatbot', 'nlp', 'vision', 'robotics', 'llama',
                   'sora', 'midjourney', 'dalle', 'stability', 'meta ai', 'google ai']
    
    print("=== ALL TOP STORIES ===")
    for i, s in enumerate(stories[:25], 1):
        is_ai = any(kw in s['title'].lower() for kw in ai_keywords)
        tag = " [AI]" if is_ai else ""
        print(f"{i}. [{s['title']}] ({s['points']}⚡ {s['comments']}💬){tag} {s.get('url','')}")
    
    print("\n=== AI-RELATED STORIES ===")
    for i, s in enumerate(stories[:25], 1):
        is_ai = any(kw in s['title'].lower() for kw in ai_keywords)
        if is_ai:
            print(f"- {s['title']} | {s['points']}⚡ {s['comments']}💬 | {s.get('url','')}")
            
except Exception as e:
    print(f"Error fetching HN: {e}", file=sys.stderr)
