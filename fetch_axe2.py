#!/usr/bin/env python3
import json, urllib.request

# Get Axe GitHub details
url = 'https://raw.githubusercontent.com/jrswab/axe/main/README.md'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    md = r.read().decode('utf-8', errors='ignore')
lines = md.split('\n')
for line in lines[:20]:
    if line.strip() and not line.startswith('#'):
        print(line[:120])
