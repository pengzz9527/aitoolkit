#!/usr/bin/env python3
"""Fetch GitHub repos with simpler query."""
import json
import urllib.request
import sys

try:
    url = "https://api.github.com/search/repositories?q=AI+agent&sort=stars&order=desc&per_page=10&created:>2026-09-01"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mozilla/5.0"
    })
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    
    items = data.get("items", [])
    repos = []
    for r in items[:10]:
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
