#!/usr/bin/env python3
"""Search for more AI news from HN."""
import json
import urllib.request

# Search for more AI-related front page stories
queries = [
    "deepseek", "llama", "openai", "anthropic", "model", "benchmark",
    "autonomous agent", "rag", "vector", "embedding", "robot",
    "computer vision", "generative ai", "o1", "o3", "reasoning"
]

all_hits = []
seen_ids = set()

for q in queries:
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={q}&tags=front_page&hitsPerPage=5"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        for h in data.get('hits', []):
            oid = h.get('objectID', '')
            if oid not in seen_ids:
                seen_ids.add(oid)
                all_hits.append(h)
    except:
        pass

# Sort by points
all_hits.sort(key=lambda x: x.get('points', 0), reverse=True)
for h in all_hits[:15]:
    title = h.get('title', '')
    score = h.get('points', 0)
    comments = h.get('num_comments', 0)
    url = h.get('url', '') or f"https://hn.algolia.com/?id={h.get('objectID','')}"
    print(f"Title:{title} | Score:{score} | Comments:{comments} | URL:{url}")
