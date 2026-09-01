#!/usr/bin/env python3
import json, urllib.request, sys

# Hacker News front page
url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

print("=== HN TOPICS ===")
for h in data.get("hits", [])[:25]:
    points = h.get("points", 0)
    title = h.get("title", "")
    story_id = h.get("objectID", "")
    print(f"[{points}] {title} | https://news.ycombinator.com/item?id={story_id}")
