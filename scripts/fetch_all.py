#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone, timedelta
import os

TODAY = datetime.now(timezone(timedelta(hours=8)))
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

# Fetch HN front page
print("Fetching HN...")
hn_url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=25"
resp = urllib.request.urlopen(hn_url, timeout=15)
hn_data = json.loads(resp.read())

hn_stories = []
for h in hn_data.get('hits', []):
    title = h.get('title', '')
    url = h.get('url', '') or h.get('hn_url', '') or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
    points = h.get('points', 0)
    comments = h.get('num_comments', 0)
    hn_stories.append({'title': title, 'url': url, 'points': points, 'comments': comments})

print(f"  Got {len(hn_stories)} HN stories")

# Fetch GitHub trending
print("Fetching GitHub...")
gh_url = "https://api.github.com/search/repositories?q=machine+learning+OR+artificial+intelligence+OR+deep+learning+OR+llm+OR+ai&sort=stars&order=desc&per_page=15"
req = urllib.request.Request(gh_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "AI-Daily-Report"})
resp = urllib.request.urlopen(req, timeout=15)
gh_data = json.loads(resp.read())

gh_repos = []
for item in gh_data.get('items', []):
    name = item.get('full_name', '')
    desc = (item.get('description') or '')[:120]
    stars = item.get('stargazers_count', 0)
    lang = item.get('language', '')
    gh_repos.append({'name': name, 'desc': desc, 'stars': stars, 'lang': lang})

print(f"  Got {len(gh_repos)} GitHub repos")

# Save raw data
with open('/tmp/ai_data.json', 'w') as f:
    json.dump({'hn': hn_stories, 'gh': gh_repos}, f, indent=2)

print("Data saved to /tmp/ai_data.json")
for s in hn_stories[:10]:
    print(f"  [{s['points']}] {s['title']}")
print("---")
for r in gh_repos[:5]:
    print(f"  [{r['stars']}⭐] {r['name']} ({r['lang']}) | {r['desc']}")
