#!/usr/bin/env python3
"""Fetch enriched data for the daily AI report."""
import json
import urllib.request
from datetime import datetime, timezone, timedelta

TODAY = datetime.now(timezone(timedelta(hours=8)))
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

# Fetch more HN stories (50)
hn_url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50"
resp = urllib.request.urlopen(hn_url, timeout=15)
hn_data = json.loads(resp.read())

hn_stories = []
for h in hn_data.get('hits', []):
    title = h.get('title', '')
    url = h.get('url', '') or h.get('hn_url', '') or "https://news.ycombinator.com/item?id=" + str(h.get('objectID', ''))
    points = h.get('points', 0)
    comments = h.get('num_comments', 0)
    hn_stories.append({'title': title, 'url': url, 'points': points, 'comments': comments})

print(f"HN stories: {len(hn_stories)}")
for s in hn_stories:
    print(f"  [{s['points']}] {s['title']}")

# Fetch GitHub repos - simpler query
gh_queries = [
    "machine+learning+stars:>50&sort=stars&order=desc&per_page=10",
    "artificial+intelligence+stars:>50&sort=stars&order=desc&per_page=10",
    "llm+agent+stars:>50&sort=stars&order=desc&per_page=10",
]

gh_repos = []
seen = set()
for q in gh_queries:
    try:
        gh_url = "https://api.github.com/search/repositories?q=" + q
        req = urllib.request.Request(gh_url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Daily-Report"
        })
        resp = urllib.request.urlopen(req, timeout=15)
        gh_data = json.loads(resp.read())
        for item in gh_data.get('items', []):
            name = item.get('full_name', '')
            if name not in seen:
                seen.add(name)
                desc = (item.get('description') or '')[:150]
                stars = item.get('stargazers_count', 0)
                lang = item.get('language', '')
                gh_repos.append({'name': name, 'desc': desc, 'stars': stars, 'lang': lang})
    except Exception as e:
        print(f"GitHub query error: {e}")

print(f"\nGitHub repos: {len(gh_repos)}")
for r in gh_repos:
    print(f"  [{r['stars']}⭐] {r['name']} ({r['lang']}) | {r['desc']}")

# Save
with open('/tmp/ai_data_full.json', 'w') as f:
    json.dump({'hn': hn_stories, 'gh': gh_repos, 'date_str': DATE_STR, 'date_display': DATE_DISPLAY}, f, indent=2)

print(f"\nSaved to /tmp/ai_data_full.json")
