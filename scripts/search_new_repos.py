#!/usr/bin/env python3
"""Search for new trending AI repos created recently."""
import json
import urllib.request

def search_repos(query, per_page=20):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}"
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Reporter/1.0'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Search for recently created AI repos
print("=== New AI repos created after 2026-07-25 ===")
results = search_repos("created:>2026-07-25&stars:>1000", 20)
for i, item in enumerate(results.get('items', [])[:20], 1):
    print(f"{i}. {item['full_name']} | ⭐{item['stargazers_count']} | {item['description']}")
    print(f"   Created: {item['created_at']} | Language: {item['language']} | License: {item.get('license',{}).get('name','N/A')}")
    print()
