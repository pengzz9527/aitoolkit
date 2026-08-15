#!/usr/bin/env python3
import json, urllib.request

# GitHub trending repos
print("=== GitHub Trending Repos ===")
req = urllib.request.Request(
    "https://api.github.com/search/repositories?q=created:>2026-08-01&sort=stars&order=desc&per_page=20",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())
    for i, r in enumerate(data.get("items", [])):
        desc = r.get('description') or ''
        print(f"{i+1}. {r['full_name']} ⭐{r['stargazers_count']} - {desc[:80]}")

# HuggingFace trending models
print("\n=== HuggingFace Trending Models ===")
req2 = urllib.request.Request(
    "https://huggingface.co/api/models?limit=15&sort=trending&direction=-1",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req2, timeout=15) as resp2:
    data2 = json.loads(resp2.read())
    for i, m in enumerate(data2):
        print(f"{i+1}. {m['modelId']} likes={m.get('likes',0)} tags={m.get('tags',[])}")
