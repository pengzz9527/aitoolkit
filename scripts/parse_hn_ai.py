#!/usr/bin/env python3
"""Parse AI-specific HN search results."""
import json

with open('/tmp/hn_ai.json', 'r') as f:
    data = json.load(f)

hits = data.get('hits', [])
for h in hits[:15]:
    title = h.get('title', '')
    score = h.get('points', 0)
    comments = h.get('num_comments', 0)
    url = h.get('url', '') or f"https://hn.algolia.com/?id={h.get('objectID','')}"
    print(f"Title:{title} | Score:{score} | Comments:{comments} | URL:{url}")
