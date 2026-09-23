#!/usr/bin/env python3
"""Fetch GitHub trending repos via API as fallback."""
import json
import urllib.request
import re

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

# Try GitHub search API for recently created trending repos
url = "https://api.github.com/search/repositories?q=created:>=2026-09-22&sort=stars&order=desc&per_page=15&accept=application/vnd.github.v3.text-match+json"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    items = data.get("items", [])
    print(f"GitHub API returned {len(items)} repos")
    for item in items[:15]:
        name = item["full_name"]
        desc = item.get("description") or ""
        stars = item["stargazers_count"]
        print(f"  {name} ⭐{stars} - {desc[:80]}")
except Exception as e:
    print(f"GitHub API error: {e}")
