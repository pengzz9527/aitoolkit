#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

# Fetch HN front page
print("=== HN Front Page ===")
data = fetch("https://hn.algolia.com/api/v1/search?tags=front&page=1&hitsPerPage=30")
for i, h in enumerate(data.get("hits", [])):
    score = h.get("points", 0)
    title = h.get("title", "")
    url = h.get("url", "")
    print(f"[{score}pts] {title}")
    if url:
        print(f"  {url}")
    print()

# Fetch AI-related HN
print("=== HN AI Search ===")
data2 = fetch("https://hn.algolia.com/api/v1/search?query=AI&tags=front&hitsPerPage=20&numericFilters=points>30")
for i, h in enumerate(data2.get("hits", [])):
    score = h.get("points", 0)
    title = h.get("title", "")
    url = h.get("url", "")
    print(f"[{score}pts] {title}")
    if url:
        print(f"  {url}")
    print()
