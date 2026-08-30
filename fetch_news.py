#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

# Try GitHub trending
print("=== GitHub Trending (AI/ML) ===")
try:
    req = urllib.request.Request(
        "https://github.com/trending/python?since=daily",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    html = fetch("https://github.com/trending/python?since=daily")
    # Extract repo names and stars
    repos = re.findall(r'<h2[^>]*><a href="/([^"]+)"[^>]*>\s*([^<]+)\s*</a></h2>', html)
    import re
    for i, (owner_repo, name) in enumerate(repos[:15]):
        stars_match = re.search(r'[\d,]+ star', html)
        print(f"{i+1}. {owner_repo.strip()}/{name.strip()}")
    print()
except Exception as e:
    print(f"GitHub trending failed: {e}")

# Search for AI news
print("=== Searching for AI News ===")
# Try TechCrunch AI section
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/search?query=OpenAI%20Google%20Anthropic%20model&tags=front&hitsPerPage=15"))
    for i, h in enumerate(data.get("hits", [])):
        score = h.get("points", 0)
        title = h.get("title", "")
        url = h.get("url", "")
        print(f"[{score}pts] {title}")
        if url:
            print(f"  {url}")
        print()
except Exception as e:
    print(f"Search failed: {e}")
