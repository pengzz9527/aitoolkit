#!/usr/bin/env python3
import json, urllib.request

# GitHub trending repos
url1 = "https://api.github.com/search/repositories?q=created:>2026-07-01&sort=stars&order=desc&per_page=20"
req1 = urllib.request.Request(url1, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req1, timeout=10) as r:
        d = json.loads(r.read())
        print("=== GitHub Trending Repos ===")
        for i, r in enumerate(d.get('items', [])[:20]):
            desc = (r.get('description') or 'N/A')[:80]
            print(f"{i+1}. {r['full_name']} - {desc} - ⭐{r['stargazers_count']}")
except Exception as e:
    print(f"GitHub error: {e}")

print()

# Hugging Face trending models
url2 = "https://huggingface.co/api/models?sort=trending&limit=20"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req2, timeout=10) as r:
        d = json.loads(r.read())
        print("=== Hugging Face Trending Models ===")
        for i, m in enumerate(d[:20]):
            print(f"{i+1}. {m['id']} - {m.get('likes',0)} likes - {m.get('pipeline_tag','N/A')}")
except Exception as e:
    print(f"HF error: {e}")
