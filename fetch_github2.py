#!/usr/bin/env python3
import urllib.request, json

# GitHub search for AI repos created recently
queries = [
    'created:>=2026-08-01 description:AI OR LLM OR machine-learning OR neural OR transformer OR agent',
    'created:>=2026-08-02 description:AI OR LLM OR machine-learning OR transformer',
]
for q in queries:
    url = f'https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=20'
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
    data = json.loads(urllib.request.urlopen(req).read())
    for item in data.get('items', []):
        lang = item.get('language', '')
        stars = item.get('stargazers_count', 0)
        desc = (item.get('description') or '')[:120]
        name = item['full_name']
        url_r = item['html_url']
        print(f"{stars:6d} ⭐ | {name} ({lang}) | {desc} | {url_r}")
    print("---")
