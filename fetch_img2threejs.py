#!/usr/bin/env python3
import json, urllib.request, sys

# Search for img2threejs info
url = "https://api.github.com/search/repositories?q=img2threejs&per_page=5"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    d = json.loads(r.read())
    for item in d.get('items', []):
        print(f"Repo: {item['full_name']}")
        print(f"Stars: {item['stargazers_count']}")
        print(f"Description: {item.get('description', 'N/A')}")
        print(f"URL: {item['html_url']}")
        print(f"Language: {item.get('language', 'N/A')}")
        print(f"Topics: {item.get('topics', [])}")
        print()
