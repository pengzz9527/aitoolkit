#!/usr/bin/env python3
"""Search for AI funding/news on web"""
import urllib.request, re, subprocess, sys

# Try DuckDuckGo HTML version
queries = [
    "AI startup funding August 2026",
    "OpenAI new model August 2026", 
    "Google Gemini update August 2026",
    "Anthropic Claude update 2026",
    "AI regulation policy August 2026",
]

for query in queries:
    print(f"\n=== SEARCH: {query} ===")
    result = subprocess.run(
        ["curl", "-s", f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"],
        capture_output=True, text=True, timeout=15
    )
    # Extract result links
    results = re.findall(r'<a class="result__a" href="([^"]*)"[^>]*>(.*?)</a>', result.stdout)
    snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', result.stdout)
    for i, (url, title) in enumerate(results[:5]):
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        snippet = re.sub(r'<[^>]+>', '', snippets[i]) if i < len(snippets) else ""
        print(f"{clean_title} | {url} | {snippet[:150]}")
