#!/usr/bin/env python3
import json, urllib.request

# Get details about Qwen3.8-Flash-Next
url = 'https://qwen.ai/blog?id=qwen3.8-flash-next'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')
import re
titles = re.findall(r'<title>([^<]+)</title>', html)
paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
print(f"Title: {titles[0] if titles else 'N/A'}")
for p in paragraphs[:6]:
    print(f"  - {p.strip()[:150]}")
