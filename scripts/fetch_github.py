#!/usr/bin/env python3
import urllib.request, json

# GitHub trending (recent AI repos)
url = "https://api.github.com/search/repositories?q=machine+learning+stars:>50&sort=stars&order=desc&per_page=10"
req = urllib.request.Request(url, headers={
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "AI-Daily-Report"
})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())

for item in data.get('items', [])[:10]:
    name = item.get('full_name', '')
    desc = (item.get('description') or '')[:120]
    stars = item.get('stargazers_count', 0)
    lang = item.get('language', '')
    print(f"[{stars}⭐] {name} ({lang})")
    print(f"  {desc}")
    print()
