#!/usr/bin/env python3
"""Search for recent AI news using multiple approaches"""
import urllib.request, json, re, html as htmlmod

# Try to get HN item details for the AI-related ones we found
hn_ids = [48861717, 48865019, 48863490, 48866134, 48862365, 48863464, 48814170, 48795900, 48863080, 48865332, 48861213]

for sid in hn_ids:
    url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            item = json.loads(resp.read())
            title = htmlmod.unescape(item.get('title', 'N/A'))
            score = item.get('score', 0)
            url_link = item.get('url', '')
            by = item.get('by', '')
            print(f"HNDETAIL|{sid}|{score}|{title}|{url_link}")
    except Exception as e:
        pass

# Also fetch some specific story IDs from the raw page
extra_ids = [
    "Inference Optimization for MiMo v2.5",
    "How the terrorist group Boko Haram uses frontier AI",
    "AI 2040: Plan A",
]
