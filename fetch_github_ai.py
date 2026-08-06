#!/usr/bin/env python3
import urllib.request, json, urllib.parse

queries = [
    "created:>2026-08-01 language:python stars:>500 topic:artificial-intelligence",
    "created:>2026-08-01 topic:llm stars:>200",
    "created:>2026-08-01 topic:machine-learning stars:>300",
    "created:>2026-08-01 AI stars:>1000",
]

for q in queries:
    encoded = urllib.parse.quote(q)
    url = f"https://api.github.com/search/repositories?q={encoded}&sort=stars&order=desc&per_page=5"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        for r in data.get('items', []):
            stargazers = r.get('stargazers_count', 0)
            lang = r.get('language', '')
            name = r['full_name']
            desc = (r.get('description') or '')[:100]
            print(f"{stargazers}|{lang}|{name}|{desc}")
    except Exception as e:
        print(f"Error for {q}: {e}")
