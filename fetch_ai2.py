#!/usr/bin/env python3
import json, urllib.request, sys, urllib.parse

# Fetch more AI-specific items with URL-encoded queries
queries = ["AI agent", "LLM", "GPT", "deep learning", "machine learning"]
for q in queries:
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=front_page&hitsPerPage=5"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        for h in data.get('hits', [])[:5]:
            title = h.get('title', '')
            hn_url = h.get('url', '') or h.get('objectURL', '')
            points = h.get('points', 0)
            print(f"[{q}] [{title}]({hn_url}) | points: {points}")
    except Exception as e:
        print(f"Error for {q}: {e}", file=sys.stderr)
