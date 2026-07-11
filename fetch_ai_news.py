#!/usr/bin/env python3
"""Search for recent AI industry news"""
import urllib.request, urllib.parse, json, re, html as htmlmod

# Try Hacker News Algolia for AI-related topics today
queries = [
    ("startup funding", 5),
    ("OpenAI", 5),
    ("Anthropic", 5),
    ("Google Gemini", 5),
    ("Apple AI", 5),
    ("Meta AI", 5),
    ("Claude", 5),
    ("MCP server", 5),
    ("agentic AI", 5),
    ("AI regulation", 5),
    ("LLM", 5),
    ("transformer", 5),
    ("multimodal", 5),
    ("AI chip", 5),
    ("NVIDIA AI", 5),
]

for q, n in queries:
    try:
        url = f"https://hn.algolia.com/api/v1/search?tags=story&query={urllib.parse.quote(q)}&hitsPerPage={n}&numericFilters=created_at_i>1752153600"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            for hit in data.get('hits', []):
                title = htmlmod.unescape(hit.get('title', ''))
                url_link = hit.get('url', '')
                score = hit.get('points', 0)
                if score > 10 and title:
                    print(f"NEWS|{q}|{score}|{title}|{url_link}")
    except Exception as e:
        pass
