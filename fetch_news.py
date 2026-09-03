#!/usr/bin/env python3
import json, urllib.request, sys

# Fetch HN front page
print("=== HN Front Page ===")
try:
    req = urllib.request.Request(
        'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    for h in data.get('hits', [])[:25]:
        print(f"{h.get('points',0)}pts | {h.get('title','')} | {h.get('url','')}")
except Exception as e:
    print(f"HN error: {e}")

print("\n=== GitHub Recent AI Stars ===")
try:
    req2 = urllib.request.Request(
        'https://api.github.com/search/repositories?q=created:>2026-09-01+stars:>100&sort=stars&order=desc&per_page=15',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req2, timeout=15) as resp2:
        data2 = json.loads(resp2.read().decode())
    for r in data2.get('items', [])[:15]:
        desc = (r.get('description') or '')[:80]
        print(f"⭐{r['stargazers_count']} | {r['full_name']} | {desc} | {r['html_url']}")
except Exception as e:
    print(f"GitHub error: {e}")

print("\n=== HN AI Stories Today ===")
try:
    req3 = urllib.request.Request(
        'https://hn.algolia.com/api/v1/search?tags=story&query=AI&hitsPerPage=15&numericFilters=created_at_i>1788249600',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req3, timeout=15) as resp3:
        data3 = json.loads(resp3.read().decode())
    for h in data3.get('hits', [])[:15]:
        print(f"{h.get('points',0)}pts | {h.get('title','')} | {h.get('url','')}")
except Exception as e:
    print(f"HN AI error: {e}")

print("\n=== GitHub Trending (Python) ===")
try:
    req4 = urllib.request.Request(
        'https://api.gitter.dev/user/following',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
except:
    pass

print("\nDone.")