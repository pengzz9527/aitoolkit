#!/usr/bin/env python3
import json, urllib.request, sys

# Try to get recent AI news from tech sites
urls = [
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", "rss"),
    ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "rss"),
]

for name, url, kind in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
        # Extract titles from RSS
        import re
        titles = re.findall(r'<title[^>]*>([^<]+)</title>', content)
        links = re.findall(r'<link[^>]*>([^<]+)</link>', content)
        for i, (t, l) in enumerate(zip(titles[2:12], links[2:12])):
            print(f"{name} [{i+1}] {t[:120]}")
            if l.startswith('http'):
                print(f"  {l}")
    except Exception as e:
        print(f"{name} error: {e}", file=sys.stderr)
