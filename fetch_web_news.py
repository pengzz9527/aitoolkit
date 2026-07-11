#!/usr/bin/env python3
"""Search for recent AI news from multiple sources"""
import urllib.request, json, re

# Search DuckDuckGo for recent AI news
def search_ddg(query):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        results = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>.*?<a class="result__snippet" href="[^"]*">([^<]*)</a>', html, re.DOTALL)
        return results[:10]
    except Exception as e:
        return []

import urllib.parse

queries = [
    "AI startup funding July 2026",
    "OpenAI new release July 2026",
    "Google AI Gemini update 2026",
    "Anthropic Claude new model 2026",
    "AI regulation policy 2026",
    "GitHub AI project trending 2026",
]

for q in queries:
    results = search_ddg(q)
    for r in results:
        print(f"WEB|{q}|{r[1].strip()}|{r[0]}|{r[2].strip()[:100]}")
