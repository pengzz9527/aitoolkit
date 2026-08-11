#!/usr/bin/env python3
import json, urllib.request, sys

# GitHub trending repos - today's new repos with AI keywords
try:
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?q=created:>=2026-08-09&sort=stars&order=desc&per_page=20",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== GHTRENDING ===")
    for r in data.get("items", [])[:20]:
        stars = r.get("stargazers_count", 0)
        name = r.get("full_name", "")
        desc = r.get("description", "") or ""
        url = r.get("html_url", "")
        lang = r.get("language", "")
        print(f"{stars:,}⭐ | {name} [{lang}]")
        if desc:
            print(f"  {desc}")
        print(f"  -> {url}")
        print()
except Exception as e:
    print(f"GitHub error: {e}", file=sys.stderr)

# Search for AI news via web
try:
    # Use a simple search approach - look for AI-specific news
    print("\n=== SEARCHING AI NEWS ===")
    search_queries = [
        "AI artificial intelligence latest news",
        "LLM large language model release",
        "OpenAI Google DeepSeek",
    ]
    for q in search_queries:
        try:
            url = f"https://www.google.com/search?q={q.replace(' ', '+')}&tbs=qdr:d"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode()
            print(f"  Search: {q} - {len(html)} bytes")
        except Exception as e:
            print(f"  Search error: {e}")
except Exception as e:
    print(f"Web search error: {e}")
