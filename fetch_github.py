#!/usr/bin/env python3
import json, urllib.request

# Fetch GitHub trending repos (last 24h, sorted by stars)
req = urllib.request.Request(
    "https://api.github.com/search/repositories?"
    "q=created:>2026-08-04&sort=stars&order=desc&per_page=20"
)
req.add_header("Accept", "application/vnd.github.v3+json")
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

for r in data.get('items', [])[:20]:
    stargazers = r.get('stargazers_count', 0)
    if stargazers >= 50:
        lang = r.get('language', '')
        desc = (r.get('description') or '')[:120]
        name = r['full_name']
        print(f"{stargazers}|{lang}|{name}|{desc}")
