#!/usr/bin/env python3
import json, urllib.request, sys

# Fetch HN front page
url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"
try:
    with urllib.request.urlopen(url, timeout=15) as r:
        data = json.loads(r.read())
    for i, h in enumerate(data.get('hits', [])[:30]):
        title = h.get('title', '')
        hn_url = h.get('url', '') or h.get('objectURL', '')
        points = h.get('points', 0)
        author = h.get('author', '')
        print(f"{i+1}. [{title}]({hn_url}) | points: {points}")
except Exception as e:
    print(f"HN error: {e}", file=sys.stderr)

# Also search AI-specific
print("\n--- AI-specific HN ---")
url2 = "https://hn.algolia.com/api/v1/search?query=AI+machine+learning+LLM&tags=front_page&hitsPerPage=20"
try:
    with urllib.request.urlopen(url2, timeout=15) as r:
        data2 = json.loads(r.read())
    for i, h in enumerate(data2.get('hits', [])[:20]):
        title = h.get('title', '')
        hn_url = h.get('url', '') or h.get('objectURL', '')
        points = h.get('points', 0)
        print(f"{i+1}. [{title}]({hn_url}) | points: {points}")
except Exception as e:
    print(f"HN AI error: {e}", file=sys.stderr)
