#!/usr/bin/env python3
import json, urllib.request

# Get Qwen blog details
url = 'https://qwen.ai/blog?id=qwen3.8-flash-next'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')
import re
paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
h2s = re.findall(r'<h[23][^>]*>([^<]+)</h[23]>', html)
print("Headings:", h2s[:5])
for p in paragraphs[:8]:
    text = p.strip()
    if text and len(text) > 30:
        print(f"  - {text[:150]}")
