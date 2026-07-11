#!/usr/bin/env python3
import urllib.request, json

# Search recent AI news via web (using a simple approach)
# We'll fetch the HN page directly for titles
url = "https://news.ycombinator.com/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    import re
    
    # Extract title links
    titles = re.findall(r'class="titleline".*?<a[^>]*>([^<]+)</a>', html, re.DOTALL)
    scores = re.findall(r'class="age".*?title="(\d+ points)",', html)
    
    results = []
    for i, t in enumerate(titles[:25]):
        score = scores[i] if i < len(scores) else '0'
        results.append(f"HNRAW|{score}|{t.strip()}")
    
    for r in results:
        print(r)
except Exception as e:
    print(f"ERROR: {e}")
