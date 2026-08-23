#!/usr/bin/env python3
import urllib.request, json, re, sys

# Fetch HN front page
try:
    req = urllib.request.Request(
        'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=40',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.load(resp)
    print("=== HN HOT ===")
    for h in data.get('hits', [])[:40]:
        print(f"{h['points']} pts | {h.get('title','')[:120]}")
        print(f"  -> {h.get('url','')}")
        print(f"  comments: {h.get('num_comments',0)}")
        print()
except Exception as e:
    print(f"HN error: {e}", file=sys.stderr)

# Fetch GitHub Trending
try:
    req = urllib.request.Request(
        'https://github.com/trending?since=daily&spoken_language_code=',
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    print("=== GITHUB TRENDING ===")
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
    for a in articles[:20]:
        repo = re.search(r'<h2.*?>(.*?)</h2>', a, re.DOTALL)
        stars = re.findall(r'>(\d[\d,]*)\s*stars', a)
        total_stars = ''.join(stars) if stars else ''
        if repo:
            name = repo.group(1).strip()
            print(f"{total_stars} stars | {name}")
except Exception as e:
    print(f"GitHub error: {e}", file=sys.stderr)

# Fetch HN main page
try:
    req = urllib.request.Request(
        'https://news.ycombinator.com',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    print("=== HN MAIN PAGE ===")
    titles = re.findall(r'<span class="title">.*?<a[^>]*href="[^"]*"[^>]*>(.*?)</a>', html, re.DOTALL)
    for t in titles[:30]:
        print(t.strip())
except Exception as e:
    print(f"HN main error: {e}", file=sys.stderr)
