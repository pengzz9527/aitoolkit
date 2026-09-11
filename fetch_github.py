#!/usr/bin/env python3
import json, urllib.request, sys, time

# GitHub trending AI repos from last 24h
url = "https://api.github.com/search/repositories?q=created:>2026-09-10+stars:>50&sort=stars&order=desc&per_page=10"
headers = {"Accept": "application/vnd.github.v3+json"}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    for i, h in enumerate(data.get('items', [])[:10]):
        name = h.get('full_name', '')
        desc = h.get('description', '') or ''
        stars = h.get('stargazers_count', 0)
        lang = h.get('language', '')
        url_g = h.get('html_url', '')
        print(f"{i+1}. [{name}]({url_g}) | {stars}⭐ | {lang} | {desc[:120]}")
except Exception as e:
    print(f"GitHub error: {e}", file=sys.stderr)

# Try fetching today's date filtered
url2 = "https://api.github.com/search/repositories?q=stars:>1000+language:Python&sort=updated&order=desc&per_page=10"
try:
    req2 = urllib.request.Request(url2, headers=headers)
    with urllib.request.urlopen(req2, timeout=15) as r:
        data2 = json.loads(r.read())
    for i, h in enumerate(data2.get('items', [])[:10]):
        name = h.get('full_name', '')
        desc = h.get('description', '') or ''
        stars = h.get('stargazers_count', 0)
        lang = h.get('language', '')
        url_g = h.get('html_url', '')
        updated = h.get('updated_at', '')[:10]
        print(f"  {i+1}. [{name}]({url_g}) | {stars}⭐ | updated: {updated} | {desc[:120]}")
except Exception as e:
    print(f"GitHub updated error: {e}", file=sys.stderr)
