#!/usr/bin/env python3
import urllib.request, json

# Fetch Hacker News stories about AI today
queries = [
    "AI",
    "artificial intelligence", 
    "machine learning",
    "LLM",
    "deep learning",
    "GPT",
    "Claude",
    "OpenAI",
    "Anthropic",
    "Mistral",
]

for q in queries:
    # Search Algolia for HN stories with AI keywords
    url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=front_page&hitsPerPage=5"
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        for h in data.get('hits', []):
            score = h.get('points', 0)
            if score >= 50:
                title = h.get('title', '')
                url = h.get('url', '') or h.get('objectID', '')
                print(f"{score}|{q}|{title}|{url}")
    except Exception as e:
        pass
