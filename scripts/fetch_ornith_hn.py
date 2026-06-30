#!/usr/bin/env python3
"""Get Ornith HN item details."""
import json, urllib.request, sys, re

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Reporter/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

# Search for Ornith on HN
print("=== SEARCH ORNITH ON HN ===")
# Try common HN IDs around the time we saw it
for id_candidate in [42065928, 42060000, 42070000, 42050000, 42080000]:
    item = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{id_candidate}.json')
    if item and item.get('title') and 'ornith' in item.get('title', '').lower():
        print(f"Found! ID: {id_candidate}")
        print(f"  Title: {item.get('title')}")
        print(f"  Points: {item.get('points')}")
        print(f"  URL: {item.get('url')}")
        break

# Also try searching via the blog post link
print("\n=== CHECK BLOG POST ===")
html = fetch_json('https://hacker-news.firebaseio.com/v0/item/42067000.json')
if html:
    print(html)

# Try to get Ornith from the HN algolia search
print("\n=== ALGOLIA SEARCH ===")
req = urllib.request.Request(
    'https://hn.algolia.com/api/v1/search?query=Ornith&hitsPerPage=5',
    headers={'User-Agent': 'AI-Reporter/1.0'}
)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    for h in data.get('hits', []):
        print(f"  [{h.get('title','')}] points:{h.get('points',0)} url:{h.get('url','')}")
except Exception as e:
    print(f"Error: {e}")
