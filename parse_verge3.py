#!/usr/bin/env python3
import re

for fname, label in [('/tmp/v1.html', 'Greg Brockman OpenAI'), ('/tmp/v2.html', 'OpenAI Hugging Face Hack'), ('/tmp/v3.html', 'Claude Watermarks'), ('/tmp/v4.html', 'OpenAI Disbands Team'), ('/tmp/v5.html', 'OpenAI Hit Brakes')]:
    try:
        with open(fname) as f:
            html = f.read()
        title_m = re.search(r'<title>(.*?)</title>', html)
        snippet_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if not snippet_m:
            snippet_m = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ''
        snippet = snippet_m.group(1).strip() if snippet_m else ''
        print(f"=== {label} ===")
        print(f"Title: {title[:150]}")
        print(f"Snippet: {snippet[:250]}")
        print()
    except Exception as e:
        print(f"Error {label}: {e}")
