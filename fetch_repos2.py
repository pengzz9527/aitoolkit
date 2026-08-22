#!/usr/bin/env python3
import json, urllib.request, sys

# Fetch GitHub repo details
repos = [
    "docling-project/docling",
    "browser-use/browser-use",
]

for r in repos:
    url = f"https://api.github.com/repos/{r}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        d = json.load(resp)
    print(f"=== {r} ===")
    print(f"Stars: {d['stargazers_count']}")
    print(f"Description: {d['description']}")
    print(f"Language: {d['language']}")
    print(f"Topics: {d.get('topics', [])}")
    print(f"URL: {d['html_url']}")
    print(f"License: {d.get('license', {}).get('spdx_id', 'N/A') if d.get('license') else 'N/A'}")
    print(f"Pushed: {d['pushed_at']}")
    print()
