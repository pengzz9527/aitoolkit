#!/usr/bin/env python3
import json, urllib.request

# Get more details about AWS DuckLabs acquisition
url = 'https://ducklabs.com/news/2026/08/26/ducklabs-to-join-aws'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')
# Extract title and key paragraphs
import re
titles = re.findall(r'<title>([^<]+)</title>', html)
paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
print(f"Title: {titles[0] if titles else 'N/A'}")
for p in paragraphs[:8]:
    print(f"  - {p.strip()[:120]}")
