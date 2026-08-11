#!/usr/bin/env python3
import json, urllib.request, sys

# GitHub trending repos (created today, sorted by stars)
try:
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?q=created:>2026-08-09&sort=stars&order=desc&per_page=15",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== GHTRENDING ===")
    for r in data.get("items", [])[:15]:
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

# GitHub trending repos (all time, AI/ML related)
try:
    req = urllib.request.Request(
        "https://api.github.com/search/repositories?q=AI+OR+machine+learning+OR+LLM+OR+openai+OR+deepseek&sort=stars&order=desc&per_page=10&since=daily",
        headers={"User-Agent": "AI-Daily/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    print("=== GHAITRENDING ===")
    for r in data.get("items", [])[:10]:
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
    print(f"GitHub AI error: {e}", file=sys.stderr)
