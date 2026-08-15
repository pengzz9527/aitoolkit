#!/usr/bin/env python3
import json, urllib.request, sys

# HN front page
try:
    req = urllib.request.Request("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10")
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        for h in data.get('hits',[])[:10]:
            print(f"HN|{h['title']}|{h.get('points',0)} pts|{h.get('num_comments',0)} comments|{h.get('url','')}")
except Exception as e:
    print(f"HN_ERROR: {e}")

# GitHub trending AI repos
try:
    url = "https://api.github.com/search/repositories?q=AI+created:>2026-08-12&sort=stars&per_page=10"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        for r in data.get('items',[]):
            desc = (r.get('description') or '').replace('|', ' ')[:80]
            print(f"GHTREND|{r['full_name']}|⭐{r['stargazers_count']}|{desc}")
except Exception as e:
    print(f"GIT_ERROR: {e}")

# Top AI repos by stars
try:
    url = "https://api.github.com/search/repositories?q=artificial+intelligence+language&sort=stars&per_page=5"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        for r in data.get('items',[]):
            desc = (r.get('description') or '').replace('|', ' ')[:80]
            print(f"GITTOP|{r['full_name']}|⭐{r['stargazers_count']}|{desc}")
except Exception as e:
    print(f"GIT2_ERROR: {e}")
