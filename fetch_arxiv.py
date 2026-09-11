#!/usr/bin/env python3
import json, urllib.request, sys

# Search for AI news via web RSS/API
urls_to_try = [
    ("arxiv", "https://arxiv.org/rss/cs.AI"),
]

for name, url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Extract titles from RSS
            import re
            titles = re.findall(r'<title>([^<]+)</title>', content)
            links = re.findall(r'<link>([^<]+)</link>', content)
            descs = re.findall(r'<description>([^<]+)</description>', content)
            for j in range(min(10, len(titles))):
                t = titles[j].replace('&apos;', "'").replace('&quot;', '"').strip()
                if 'arXiv' in t or 'cs.AI' in t:
                    t = re.sub(r'\[.*?\]', '', t).strip()
                link = links[j] if j < len(links) else ''
                desc = (descs[j] if j < len(descs) else '')[:150].replace('<[^>]+>', '').replace('&amp;', '&').replace('&#39;', "'")
                print(f"ARXIV_{j+1}|{t}|{link}|{desc}")
            break
    except Exception as e:
        print(f"arxiv error: {e}")
