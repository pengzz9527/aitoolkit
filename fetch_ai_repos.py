#!/usr/bin/env python3
import urllib.request, json

# Fetch GitHub trending repos using a different approach
# Search for AI-related repos created recently
queries = [
    "created:>2026-08-01 AI language:python stars:>=50",
    "created:>2026-08-01 LLM language:python stars:>=50", 
    "created:>2026-08-01 machine-learning stars:>=100",
    "created:>2026-08-01 deep-learning stars:>=50",
]

for q in queries:
    req = urllib.request.Request(
        f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=10"
    )
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        print(f"=== Query: {q} ===")
        for r in data.get('items', [])[:5]:
            stargazers = r.get('stargazers_count', 0)
            lang = r.get('language', '')
            name = r['full_name']
            desc = (r.get('description') or '')[:100]
            print(f"{stargazers}|{lang}|{name}|{desc}")
        print()
    except Exception as e:
        print(f"Error: {e}")
