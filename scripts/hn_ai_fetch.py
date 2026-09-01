#!/usr/bin/env python3
"""Fetch HN stories about AI/ML specifically"""
import json, urllib.request, sys

# Search HN for AI-related stories
queries = [
    ("AI agents", 15),
    ("LLM", 15),
    ("machine learning", 10),
    ("Claude Gemini GPT", 10),
]

for query, n in queries:
    print(f"\n=== HN SEARCH: {query} ===")
    url = f"https://hn.algolia.com/api/v1/search?tags=front_page&query={query}&hitsPerPage={n}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for h in data.get("hits", [])[:n]:
            points = h.get("points", 0)
            title = h.get("title", "")
            sid = h.get("objectID", "")
            url = h.get("url", "") or f"https://news.ycombinator.com/item?id={sid}"
            print(f"[{points}] {title} | {url}")
    except Exception as e:
        print(f"Error: {e}")

# Also check specific AI-related high-point stories
print("\n=== SPECIFIC AI STORIES ===")
# Haiku R1/beta6 release
url2 = "https://hn.algolia.com/api/v1/search?query=Haiku&hitsPerPage=5"
req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req2, timeout=15) as resp:
    data2 = json.loads(resp.read())
for h in data2.get("hits", []):
    print(f"[{h.get('points',0)}] {h.get('title','')} | https://news.ycombinator.com/item?id={h.get('objectID','')}")

# Continuous Diffusion LLM
url3 = "https://hn.algolia.com/api/v1/search?query=Continuous+Diffusion+Language+Model&hitsPerPage=5"
req3 = urllib.request.Request(url3, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req3, timeout=15) as resp:
    data3 = json.loads(resp.read())
for h in data3.get("hits", []):
    print(f"[{h.get('points',0)}] {h.get('title','')} | https://news.ycombinator.com/item?id={h.get('objectID','')}")
