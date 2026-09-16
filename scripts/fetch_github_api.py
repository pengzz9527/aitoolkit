#!/usr/bin/env python3
"""Fetch GitHub API for AI repos."""
import json
import urllib.request
import sys
from urllib.parse import quote

try:
    # Search for AI repos created in last day
    query = "AI+machine+learning+created:>2026-09-15"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=15"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mozilla/5.0"
    })
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    
    items = data.get("items", [])
    repos = []
    for r in items[:15]:
        repos.append({
            "name": r["full_name"],
            "stars": r["stargazers_count"],
            "description": r.get("description") or "",
            "language": r.get("language") or "",
            "url": r["html_url"]
        })
    
    with open('/tmp/github_repos.json', 'w') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(json.dumps(repos, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    print(json.dumps([]))
