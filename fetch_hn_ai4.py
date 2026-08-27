#!/usr/bin/env python3
import json, urllib.request

url = 'https://hn.algolia.com/api/v1/search?query=AI+agent+LLM+model+openai&hitsPerPage=15&numericFilters=points>30'
with urllib.request.urlopen(url, timeout=10) as r:
    data = json.loads(r.read())
print('Total hits:', data['nbHits'])
for h in data['hits']:
    title = h.get('title', 'N/A')
    url = h.get('url', h.get('objectID', 'N/A'))
    points = h.get('points', 0)
    print(f"{points:>4} pts | {title[:80]} | {url}")
