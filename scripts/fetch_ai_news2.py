#!/usr/bin/env python3
import json, urllib.request, sys, re

# Fetch AI-specific HN posts (search for AI/ML related)
try:
    req = urllib.request.Request(
        "https://hn.algolia.com/api/v1/search?query=AI+artificial+intelligence+LLM+OpenAI+Google+DeepSeek&tags=front_page&hitsPerPage=20&numericFilters=points>50",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== HNAI ===")
    for h in data.get("hits", [])[:20]:
        title = h.get("title", "")
        score = h.get("points", 0)
        url = h.get("url", "")
        comments = h.get("num_comments", 0)
        print(f"{score}pts | {title}")
        if url:
            print(f"  -> {url}")
        print(f"  comments: {comments}")
        print()
except Exception as e:
    print(f"HN AI search error: {e}", file=sys.stderr)

# Try to fetch some AI news sites
news_sites = [
    ("https://www.anthropic.com/news", "Anthropic"),
    ("https://openai.com/news", "OpenAI"),
    ("https://blog.google/technology/ai/", "Google AI"),
]

for url, name in news_sites:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode()[:5000]
        # Extract some titles
        titles = re.findall(r'<[^>]+>([^<]{20,})</', html)
        print(f"\n=== {name} ===")
        for t in titles[:5]:
            print(f"  - {t}")
    except Exception as e:
        print(f"{name} error: {e}")
