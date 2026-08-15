#!/usr/bin/env python3
import json, urllib.request, urllib.error

# Get HN top stories via Algolia
algolia_url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=25"
algolia_resp = urllib.request.urlopen(algolia_url, timeout=15)
data = json.loads(algolia_resp.read())

for h in data.get('hits', [])[:25]:
    title = h.get('title', '')
    url = h.get('url', '') or ''
    points = h.get('points', 0)
    print(f"[{points}] {title} | {url}")
