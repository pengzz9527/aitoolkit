#!/usr/bin/env python3
"""Fetch more AI-specific news."""
import json, urllib.request, urllib.parse, re, html, sys

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# Search HN for AI-related terms
print("=" * 60)
print("HN AI-RELATED STORIES")
print("=" * 60)
try:
    # Try different query combinations
    queries = [
        "openai gpt",
        "anthropic claude",
        "deepseek",
        "llm model",
        "ai agent",
        "machine learning",
        "transformer",
        "diffusion",
    ]
    seen = set()
    for q in queries:
        encoded = urllib.parse.quote(q)
        try:
            data = fetch_json(f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=front&hitsPerPage=5&numericFilters=points>20")
            for h in data.get("hits", []):
                key = h.get("objectID", "")
                if key not in seen:
                    seen.add(key)
                    score = h.get("points", 0)
                    title = html.unescape(h.get("title", ""))
                    url = h.get("url", f"https://news.ycombinator.com/item?id={h.get('objectID','')}")
                    print(f"[{score}pts] {title}")
                    print(f"  {url}")
                    print()
        except Exception as e:
            print(f"Query '{q}' failed: {e}")
except Exception as e:
    print(f"HN search failed: {e}")

# GitHub search for recently starred AI repos
print("=" * 60)
print("GITHUB RECENTLY POPULAR AI")
print("=" * 60)
try:
    data = fetch_json("https://api.github.com/search/repositories?q=language:python+stars:>100&sort=updated&order=desc&per_page=10")
    for i, r in enumerate(data.get('items', [])):
        stars = r.get('stargazers_count', 0)
        lang = r.get('language', '')
        name = r.get('full_name', '')
        desc = (r.get('description') or '')[:120]
        updated = r.get('updated_at', '')[:10]
        print(f"{i+1}. {name} ⭐{stars} ({lang}) [updated: {updated}]")
        print(f"   {desc}")
        print()
except Exception as e:
    print(f"GitHub search failed: {e}")
