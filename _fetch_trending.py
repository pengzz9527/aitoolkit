#!/usr/bin/env python3
import json, urllib.request

# GitHub API: trending AI repos from last month
url1 = "https://api.github.com/search/repositories?q=created:>2026-08-01+language:python&sort=stars&order=desc&per_page=15"
req = urllib.request.Request(url1, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.load(r)
print("=== GitHub Trending (Recent AI Repos) ===")
for item in data.get("items", []):
    print(f"[{item['stargazers_count']}★] {item['full_name']} - {item.get('description','')[:80]}")
    print(f"    {item['html_url']}")

print()

# HuggingFace trending models
url2 = "https://huggingface.co/api/models?sort=trending&limit=10&search=llama"
req2 = urllib.request.Request(url2, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req2, timeout=15) as r:
    data2 = json.load(r)
print("=== HuggingFace Trending Models ===")
for m in data2:
    mid = m.get("modelId", "")
    desc = m.get("description", "")
    down = m.get("downloads", 0)
    print(f"  {mid} - downloads={down} - {str(desc)[:80] if desc else 'no desc'}")
