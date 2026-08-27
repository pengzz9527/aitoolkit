#!/usr/bin/env python3
import json, urllib.request, sys

# Get AI/LLM related HN stories
url = 'https://hn.algolia.com/api/v1/search?query=AI+LLM+model+openai+claude+gemini&tags=front_page&hitsPerPage=15'
with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())
for h in data['hits']:
    print(f"{h['points']:>4} pts | {h['title'][:80]} | {h['url']}")
