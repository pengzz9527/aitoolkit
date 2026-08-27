#!/usr/bin/env python3
import json, urllib.request

url = 'https://hn.algolia.com/api/v1/search?query=AI+agent+LLM+model+openai&hitsPerPage=15&numericFilters=points>30'
with urllib.request.urlopen(url, timeout=10) as r:
    data = json.loads(r.read())
print('Total hits:', data['nbHits'])
for h in data['hits']:
    print(f"{h['points']:>4} pts | {h['title'][:80]} | {h['url']}")
