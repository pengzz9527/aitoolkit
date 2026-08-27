#!/usr/bin/env python3
import json, urllib.request

# Get details about Mcp-Agent
url = 'https://github.com/lastmile-ai/mcp-agent'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')
import re
description = re.findall(r'<meta name="description" content="([^"]+)"', html)
print(f"Description meta: {description[0] if description else 'N/A'}")
paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
for p in paragraphs[:4]:
    print(f"  - {p.strip()[:120]}")
