#!/usr/bin/env python3
import json, urllib.request, sys

# Get HN front page with points > 100
url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30&numericFilters=points>100'
with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())
for h in data['hits']:
    print(f"{h['points']:>4} pts | {h['title'][:80]} | {h['url']}")
