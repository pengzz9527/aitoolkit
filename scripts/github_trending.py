#!/usr/bin/env python3
import json, urllib.request, urllib.error

# GitHub trending repositories (daily, AI/ML related)
github_url = "https://api.github.com/search/repositories?q=machine+learning+OR+artificial+intelligence+OR+deep+learning&sort=stars&order=desc&per_page=15&since=daily"
req = urllib.request.Request(github_url, headers={
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "AI-Daily-Report"
})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    for item in data.get('items', [])[:15]:
        name = item.get('full_name', '')
        desc = (item.get('description') or '')[:100]
        stars = item.get('stargazers_count', 0)
        lang = item.get('language', '')
        print(f"[{stars}⭐] {name} ({lang}) | {desc}")
except Exception as e:
    print(f"Error: {e}")
