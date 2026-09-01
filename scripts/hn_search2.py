#!/usr/bin/env python3
"""Fetch more AI-specific data"""
import json, urllib.request, sys, urllib.parse

# More targeted HN searches
queries = [
    ("OpenAI", 10),
    ("Claude", 10),
    ("DeepSeek", 10),
    ("GPT-5", 10),
    ("LLM open source", 10),
    ("AI model", 10),
    ("HuggingFace", 10),
]

for query, n in queries:
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search?tags=front_page&query={encoded}&hitsPerPage={n}"
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
        print(f"Error for {query}: {e}")
