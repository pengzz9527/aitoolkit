#!/usr/bin/env python3
import re

for fname in ['/tmp/tc1.html', '/tmp/tc2.html', '/tmp/tc3.html']:
    try:
        with open(fname) as f:
            html = f.read()
        title_m = re.search(r'<title>(.*?)</title>', html)
        snippet_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if not snippet_m:
            snippet_m = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ''
        snippet = snippet_m.group(1).strip() if snippet_m else ''
        print(f"=== {fname} ===")
        print(f"Title: {title[:150]}")
        print(f"Snippet: {snippet[:200]}")
        print()
    except Exception as e:
        print(f"Error: {e}")
