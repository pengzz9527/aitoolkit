#!/usr/bin/env python3
import urllib.request, json

# Fetch MIT Tech Review AI news
url = "https://www.technologyreview.com/topic/artificial-intelligence/feed"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode()
    import re
    titles = re.findall(r'<title>([^<]+)</title>', content)
    links = re.findall(r'<link>([^<]+)</link>', content)
    for t, l in zip(titles[:10], links[:10]):
        if 'MIT Technology Review' not in t and 'Artificial Intelligence' not in t:
            print(f"{t.strip()}|{l.strip()}")
except Exception as e:
    print(f"Error: {e}")
