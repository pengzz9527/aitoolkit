#!/usr/bin/env python3
import urllib.request, json, urllib.parse

# GitHub API for AI repos
params = urllib.parse.quote('created:>=2026-08-01 description:AI OR LLM OR machine-learning OR neural OR transformer OR agent')
url = f'https://api.github.com/search/repositories?q={params}&sort=stars&order=desc&per_page=15'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
data = json.loads(urllib.request.urlopen(req).read())
for item in data.get('items', [])[:12]:
    lang = item.get('language', '')
    stars = item.get('stargazers_count', 0)
    desc = (item.get('description') or '')[:120]
    name = item['full_name']
    url_r = item['html_url']
    print(f"{stars:5d} ⭐ | {name} ({lang}) | {desc} | {url_r}")
