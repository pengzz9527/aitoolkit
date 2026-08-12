#!/usr/bin/env python3
"""Fetch additional details for the AI daily report."""
import urllib.request, json, urllib.parse

def fetch_article(title_or_url):
    return None

# Try to get more details from the key articles
urls_to_check = [
    "https://stolen-thoughts.com/",
    "https://www.modular.com/blog/modular-26-5-mojo-1-0-is-here",
    "https://manus.im/blog/a-note-to-our-users",
    "https://github.com/openclaw/openclaw",
]

for url in urls_to_check:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode("utf-8", errors="ignore")
        # Extract relevant text snippets
        print(f"\n=== {url} ===")
        # Find meta description
        import re
        desc = re.search(r'<meta[^>]*description[^>]*content="([^"]*)"', content, re.IGNORECASE)
        if desc:
            print(f"Desc: {desc.group(1)[:200]}")
        title = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        if title:
            print(f"Title: {title.group(1)[:200]}")
    except Exception as e:
        print(f"Failed {url}: {e}")
