#!/usr/bin/env python3
"""Get more HN story details from today's page"""
import urllib.request, json, re, html as htmlmod

# Fetch the full HN front page HTML
url = "https://news.ycombinator.com/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    page = resp.read().decode('utf-8', errors='ignore')

# Extract all story links and scores
items = re.findall(r'<span class="titleline">.*?<a[^>]*href="([^"]*item\?id=(\d+))"[^>]*>([^<]+)</a>', page, re.DOTALL)

for href, sid, title in items[:25]:
    title_clean = htmlmod.unescape(title.strip())
    # Now fetch detail
    try:
        surl = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
        req2 = urllib.request.Request(surl)
        with urllib.request.urlopen(req2, timeout=10) as resp2:
            item = json.loads(resp2.read())
            score = item.get('score', 0)
            url_link = item.get('url', '')
            if score > 30:
                print(f"HNFULL|{sid}|{score}|{title_clean}|{url_link}")
    except:
        pass
