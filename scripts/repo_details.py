#!/usr/bin/env python3
"""Check specific AI-related GitHub repos from trending"""
import json, urllib.request, sys

repos = [
    "THU-MAIC/OpenMAIC",
    "K-Dense-AI/scientific-agent-skills",
    "unclecode/crawl4ai",
    "punkpeye/awesome-mcp-servers",
    "pollen-robotics/microduck_rl",
    "livekit/agents",
    "Leonxlnx/unlazy",
    "razzant/ouroboros",
    "Purewhiter/mobilegym",
]

for repo in repos:
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        stars = data.get("stargazers_count", 0)
        lang = data.get("language", "")
        desc = (data.get("description", "") or "")[:150]
        updated = data.get("updated_at", "")[:10]
        print(f"⭐{stars} {repo} | {lang} | updated:{updated} | {desc}")
    except Exception as e:
        print(f"Error {repo}: {e}")
