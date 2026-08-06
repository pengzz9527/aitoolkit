#!/usr/bin/env python3
import urllib.request, json, urllib.parse

# Search for AI news/industry
queries = [
    'site:techcrunch.com AI OR "artificial intelligence"',
    'site:venturebeat.com AI OR "artificial intelligence"',
]
for q in queries:
    encoded = urllib.parse.quote(q)
    url = f'https://api.github.com/search/repositories?q={encoded}'
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
        data = json.loads(urllib.request.urlopen(req).read())
        print(f"Query: {q[:50]}")
        print(f"Items: {data.get('total_count', 0)}")
        for item in data.get('items', [])[:5]:
            print(f"  {item['full_name']} - {item['stargazers_count']} stars")
        print()
    except Exception as e:
        print(f"Error: {e}")
