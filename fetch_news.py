#!/usr/bin/env python3
"""Fetch today's AI news from multiple sources."""
import json, urllib.request, sys
from datetime import date

TODAY = date.today().isoformat()

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

# 1. Hacker News front page
print("=== HN FRONT PAGE ===")
try:
    data = json.loads(fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"))
    for h in data.get("hits", []):
        title = h.get("title", "")
        url = h.get("url", "") or h.get("objectID", "")
        points = h.get("points", 0)
        print(f"[{points}] {title} — {url}")
except Exception as e:
    print(f"HN error: {e}")

# 2. GitHub trending AI repos (created today)
print("\n=== GITHUB TRENDING (today's AI repos) ===")
try:
    data = json.loads(fetch("https://api.github.com/search/repositories?q=created:>2026-09-27&sort=stars&order=desc&per_page=15&q=AI+OR+llm+OR+agent+OR+model"))
    for r in data.get("items", []):
        name = r.get("full_name", "")
        stars = r.get("stargazers_count", 0)
        desc = (r.get("description") or "")[:100]
        print(f"[⭐{stars}] {name} — {desc}")
except Exception as e:
    print(f"GitHub error: {e}")

# 3. arXiv recent AI papers
print("\n=== arXiv AI PAPERS (recent) ===")
try:
    data = json.loads(fetch("http://arxiv.org/rss/cs.AI"))
    # Simple parsing
    import xml.etree.ElementTree as ET
    root = ET.fromstring(data)
    for item in root.findall(".//item")[:8]:
        t = item.findtext("title", "")
        link = item.findtext("link", "")
        print(f"{t} — {link}")
except Exception as e:
    print(f"arXiv error: {e}")
