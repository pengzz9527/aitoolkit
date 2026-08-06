#!/usr/bin/env python3
import urllib.request, json, urllib.parse

# GitHub repos
url = 'https://api.github.com/search/repositories?q=created:>=2026-08-01&sort=stars&order=desc&per_page=20'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
data = json.loads(urllib.request.urlopen(req).read())
for item in data.get('items', [])[:10]:
    print(f"{item['stargazers_count']} ⭐ | {item['full_name']} | {item.get('description') or 'N/A'[:100]} | {item['html_url']}")
