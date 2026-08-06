#!/usr/bin/env python3
import urllib.request, json, urllib.parse

# Get GitHub trending with more detail
url = 'https://api.github.com/search/repositories?q=created:>=2026-08-01+AI+agent&sort=stars&order=desc&per_page=15'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
data = json.loads(urllib.request.urlopen(req).read())
for item in data.get('items', [])[:10]:
    stars = item.get('stargazers_count', 0)
    lang = item.get('language', '')
    desc = (item.get('description') or '')[:100]
    name = item['full_name']
    url_r = item['html_url']
    created = item['created_at'][:10]
    print(f"{stars:5d} ⭐ | {name} ({lang}, {created}) | {desc}")
    print(f"  {url_r}")
    print()
