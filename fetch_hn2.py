#!/usr/bin/env python3
import json, urllib.request, sys, re, html

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

# Parse HN front page HTML
hn_html = fetch("https://news.ycombinator.com")

# Extract stories
stories = re.findall(r'class="titleline">.*?<a href="(https?://[^"]+)">([^<]+)</a>.*?<span class="score">(\d+) points</span>.*?<span class="age"[^>]*title="([^"]+)"', hn_html, re.DOTALL)

print("=== HN Top Stories ===")
for i, (url, title, score, date) in enumerate(stories[:30]):
    title = html.unescape(title.strip())
    score = int(score)
    if score >= 20:
        print(f"[{score}pts] {title}")
        print(f"  {url}")
        print(f"  {date[:10]}")
        print()

# Also search for AI-related on HN
print("=== HN AI/Search ===")
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/search?query=AI%20LLM%20model&tags=front&hitsPerPage=20&numericFilters=points>20"))
    for i, h in enumerate(data.get("hits", [])):
        score = h.get("points", 0)
        title = h.get("title", "")
        url = h.get("url", "")
        print(f"[{score}pts] {title}")
        if url:
            print(f"  {url}")
        print()
except Exception as e:
    print(f"Algolia search failed: {e}")
