#!/usr/bin/env python3
import json, urllib.request, sys, re, html

# Fetch HN with AI keywords
try:
    req = urllib.request.Request(
        "https://hn.algolia.com/api/v1/search?query=AI+artificial+intelligence+LLM+OpenAI+Google+DeepSeek+Claude&tags=front_page&hitsPerPage=20",
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

# Fetch more from Hacker News search
try:
    req = urllib.request.Request(
        "https://hn.algolia.com/api/v1/search?query=agent+LLM+model&tags=story&hitsPerPage=15&numericFilters=points>30",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== HNAGENTS ===")
    for h in data.get("hits", [])[:15]:
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
    print(f"HN agents error: {e}", file=sys.stderr)

# Try Reddit API for AI news
try:
    req = urllib.request.Request(
        "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=15",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== REDDITLLAMAMA ===")
    for post in data.get("data", {}).get("children", [])[:12]:
        d = post.get("data", {})
        title = d.get("title", "")
        score = d.get("score", 0)
        url = d.get("url", "")
        comments = d.get("num_comments", 0)
        print(f"{score}pts | {title}")
        if url:
            print(f"  -> {url}")
        print(f"  comments: {comments}")
        print()
except Exception as e:
    print(f"Reddit error: {e}", file=sys.stderr)
