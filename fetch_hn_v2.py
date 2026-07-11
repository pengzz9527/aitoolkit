#!/usr/bin/env python3
"""Get detailed HN story info with proper title parsing"""
import urllib.request, json, re, html as htmlmod

url = "https://news.ycombinator.com/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    page = resp.read().decode('utf-8', errors='ignore')

# Better parsing - find subtext lines which contain score and then find the title above
lines = page.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    # Look for rank+title pattern
    rank_match = re.search(r'<span class="rank">(\d+)</span>', line)
    if rank_match:
        # Title is in the same row or next
        title_match = re.search(r'<a[^>]*class="titleline"[^>]*>(.*?)</a>', '\n'.join(lines[i:i+2]), re.DOTALL)
        url_match = re.search(r'href="([^"]*)"', '\n'.join(lines[i:i+2]), re.DOTALL)
        
        if title_match:
            title = htmlmod.unescape(title_match.group(1).strip())
            # Get URL - could be in the same titleline or next span
            full_text = '\n'.join(lines[i:i+3])
            url_m = re.search(r'class="titleline".*?href="([^"]*)"', full_text, re.DOTALL)
            link = url_m.group(1) if url_m else ''
            
            # Now fetch score from HN API
            sid_match = re.search(r'id=(\d+)', full_text)
            if sid_match:
                sid = sid_match.group(1)
                try:
                    surl = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    req2 = urllib.request.Request(surl)
                    with urllib.request.urlopen(req2, timeout=8) as resp2:
                        item = json.loads(resp2.read())
                        score = item.get('score', 0)
                        title_api = htmlmod.unescape(item.get('title', title))
                        url_api = item.get('url', link)
                        print(f"HN|{sid}|{score}|{title_api}|{url_api}")
                except:
                    pass
    i += 1
