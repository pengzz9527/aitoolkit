#!/usr/bin/env python3
"""Try web search via SearxNG or other open sources"""
import urllib.request, urllib.parse, json, re, html as htmlmod

# Try SearXNG public instances
instances = [
    "https://searx.be",
    "https://search.sapti.me", 
    "https://searx.tiekoetter.com",
]

queries = ["AI news July 2026", "OpenAI announcement July 2026", "AI funding startup 2026"]

for inst in instances:
    for q in queries:
        try:
            search_url = f"{inst}/search?q={urllib.parse.quote(q)}&format=json"
            req = urllib.request.Request(search_url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                for result in data.get('results', [])[:5]:
                    title = htmlmod.unescape(result.get('title', ''))
                    url = result.get('url', '')
                    content = htmlmod.unescape(result.get('content', '')[:150])
                    if title and url:
                        print(f"SEARX|{q}|{title}|{url}|{content}")
        except Exception as e:
            pass
