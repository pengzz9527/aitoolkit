#!/usr/bin/env python3
import urllib.request, json

# Fetch Hacker News front page via Algolia
url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=25"
resp = urllib.request.urlopen(url, timeout=15)
data = json.loads(resp.read())

for h in data.get('hits', [])[:25]:
    title = h.get('title', '')
    story_url = h.get('url', '') or h.get('hn_url', '') or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
    points = h.get('points', 0)
    comments = h.get('num_comments', 0)
    print(f"[{points} pts] {title}")
    print(f"  → {story_url} (comments: {comments})")
    print()
