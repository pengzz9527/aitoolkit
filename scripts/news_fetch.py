#!/usr/bin/env python3
import urllib.request, re, sys

# Search for AI news headlines
queries = [
    "AI news today site:techcrunch.com",
    "artificial intelligence funding site:techcrunch.com",
    "AI open source release site:techcrunch.com",
    "LLM model release site:venturebeat.com",
]
for q in queries:
    print(f"\n=== SEARCH: {q} ===")
    try:
        # Use Bing search as fallback
        import subprocess
        result = subprocess.run(
            ["curl", "-s", f"https://www.bing.com/search?q={q.replace(' ', '+')}"],
            capture_output=True, text=True, timeout=15
        )
        # Extract titles
        titles = re.findall(r'<li class="b_algo"><h2><a[^>]*>(.*?)</a></h2>', result.stdout, re.DOTALL)
        urls = re.findall(r'<li class="b_algo"><h2><a href="([^"]+)"', result.stdout)
        for i, t in enumerate(titles[:5]):
            clean = re.sub(r'<[^>]+>', '', t).strip()
            u = urls[i] if i < len(urls) else ""
            print(f"{clean} | {u}")
    except Exception as e:
        print(f"Error: {e}")
