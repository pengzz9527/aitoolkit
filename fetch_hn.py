#!/usr/bin/env python3
import json, sys, urllib.request

# Fetch HN front page
req = urllib.request.Request("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30")
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode())

for h in data.get('hits', [])[:30]:
    score = h.get('points', 0)
    if score >= 30:
        title = h.get('title', '')
        url = h.get('url', '') or h.get('objectID', '')
        comments = h.get('num_comments', 0)
        print(f"{score}|{comments}|{title}|{url}")
