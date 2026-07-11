#!/usr/bin/env python3
import json, urllib.request

# Get top story IDs from HN
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req, timeout=15) as resp:
    ids = json.loads(resp.read())[:30]

# Fetch details for each story
for sid in ids[:20]:
    surl = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    req2 = urllib.request.Request(surl)
    try:
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            item = json.loads(resp2.read())
            score = item.get('score', 0)
            title = item.get('title', 'N/A')
            url_link = item.get('url', '')
            if score > 50:
                print(f"HN|{score}|{title}|{url_link}")
    except Exception as e:
        pass
