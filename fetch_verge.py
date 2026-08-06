#!/usr/bin/env python3
import urllib.request, json

# Fetch The Verge AI news
url = "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode()
    import re
    titles = re.findall(r'<title>([^<]+)</title>', content)
    links = re.findall(r'<link>([^<]+)</link>', content)
    descriptions = re.findall(r'<description>([^<]+)</description>', content)
    for i, (t, l) in enumerate(zip(titles[:10], links[:10])):
        if i > 0:
            print(f"{t.strip()}|{l.strip()}")
except Exception as e:
    print(f"Error: {e}")
