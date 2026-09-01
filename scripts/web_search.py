#!/usr/bin/env python3
"""Search for recent AI news using web"""
import urllib.request, re, sys

# Search Bing for AI news
searches = [
    "site:techcrunch.com AI news August 2026",
    "site:theverge.com AI news August 2026", 
    "OpenAI announcement August 2026",
    "Google DeepMind AI release August 2026",
]

for query in searches:
    print(f"\n=== SEARCH: {query} ===")
    import subprocess
    result = subprocess.run(
        ["curl", "-s", f"https://www.bing.com/search?q={query.replace(' ', '+')}"],
        capture_output=True, text=True, timeout=15
    )
    # Extract results
    results = re.findall(r'<li class="b_algo"><h2><a href="([^"]*)"[^>]*>(.*?)</a></h2>.*?<p>(.*?)</p>', result.stdout, re.DOTALL)
    for i, (url, title, snippet) in enumerate(results[:5]):
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()[:150]
        print(f"{clean_title} | {url} | {clean_snippet}")
