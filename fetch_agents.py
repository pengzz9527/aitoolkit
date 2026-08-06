#!/usr/bin/env python3
import urllib.request, urllib.parse, json

# Search GitHub for recent AI agent repos
queries = [
    'created:>=2026-08-03 agent llm OR ai agent',
    'created:>=2026-08-03 coding agent OR autonomous agent',
]
for q in queries:
    encoded = urllib.parse.quote(q)
    url = f'https://api.github.com/search/repositories?q={encoded}&sort=stars&order=desc&per_page=10'
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
    data = json.loads(urllib.request.urlopen(req).read())
    for item in data.get('items', [])[:5]:
        stars = item.get('stargazers_count', 0)
        lang = item.get('language', '')
        desc = (item.get('description') or '')[:100]
        name = item['full_name']
        print(f"{stars:4d} ⭐ | {name} ({lang}) | {desc}")
    print("---")
