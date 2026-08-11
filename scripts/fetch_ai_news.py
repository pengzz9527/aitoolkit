#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys
from datetime import datetime

# Fetch HN front page
try:
    req = urllib.request.Request(
        "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    
    print("=== HNRANKINGS ===")
    for h in data.get("hits", [])[:25]:
        title = h.get("title", "")
        score = h.get("points", 0)
        url = h.get("url", "")
        comments = h.get("num_comments", 0)
        print(f"{score}pts | {title}")
        if url:
            print(f"  -> {url}")
        print(f"  comments: {comments}")
        print()
except Exception as e:
    print(f"HN error: {e}", file=sys.stderr)

# Fetch GitHub trending
try:
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?q=created:>2026-08-09&sort=stars&order=desc&per_page=15",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    
    print("=== GITHUBTRENDING ===")
    for r in data.get("items", [])[:15]:
        stars = r.get("stargazers_count", 0)
        name = r.get("full_name", "")
        desc = r.get("description", "") or ""
        url = r.get("html_url", "")
        lang = r.get("language", "")
        print(f"{stars:,}⭐ | {name} [{lang}]")
        if desc:
            print(f"  {desc}")
        print(f"  -> {url}")
        print()
except Exception as e:
    print(f"GitHub error: {e}", file=sys.stderr)
