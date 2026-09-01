#!/usr/bin/env python3
"""Fetch details on GitHub repos"""
import json, urllib.request, sys

repos = [
    ("THU-MAIC/OpenMAIC", "Open Multi-Agent Interactive Classroom"),
    ("unclecode/crawl4ai", "Crawl4AI - LLM Friendly Web Crawler"),
    ("punkpeye/awesome-mcp-servers", "Awesome MCP Servers"),
    ("Leonxlnx/unlazy", "Unlazy - Anti-laziness skill for AI agents"),
    ("razzant/ouroboros", "Ouroboros - Self-creating AI agent"),
    ("Purewhiter/mobilegym", "MobileGym - Mobile GUI Agent Platform"),
    ("K-Dense-AI/scientific-agent-skills", "Scientific Agent Skills"),
]

for repo, desc in repos:
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        stars = data.get("stargazers_count", 0)
        lang = data.get("language", "")
        desc_detail = (data.get("description", "") or "")[:200]
        topics = data.get("topics", [])
        updated = data.get("pushed_at", "")[:10]
        print(f"⭐{stars:,} {repo} | {lang} | updated:{updated} | topics:{topics[:5]} | {desc_detail}")
    except Exception as e:
        print(f"Error {repo}: {e}")
