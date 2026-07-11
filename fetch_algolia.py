#!/usr/bin/env python3
"""Search for AI news via Brave Search alternative"""
import urllib.request, json, re, html as htmlmod

# Try to get AI-related news from various RSS feeds or search
urls_to_try = [
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=AI&hitsPerPage=10",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=openai&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=GPT&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=LLM&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=machine%20learning&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=neural&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=deep%20learning&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=agent&hitsPerPage=5",
    "https://hn.algolia.com/api/v1/search?tags=front_page&query=model&hitsPerPage=5",
]

for u in urls_to_try:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            for hit in data.get('hits', []):
                title = htmlmod.unescape(hit.get('title', ''))
                url = hit.get('url', '')
                score = hit.get('points', 0)
                date = hit.get('created_at_i', 0)
                if score > 20 and title:
                    print(f"ALGOLIA|{score}|{title}|{url}")
    except Exception as e:
        pass
