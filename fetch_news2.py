#!/usr/bin/env python3
import urllib.request, re, sys

urls = [
    'https://techcrunch.com/category/artificial-intelligence/',
    'https://www.theverge.com/ai-artificial-intelligence',
    'https://www.wired.com/tag/artificial-intelligence/',
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        # Extract article titles and links
        articles = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]{10,120})</a>', html)
        seen = set()
        for aurl, atitle in articles:
            atitle = atitle.strip()
            if atitle.lower() in ('sign in', 'subscribe', 'learn more', 'read more', 'continue reading', 'get access'):
                continue
            if len(atitle) > 15 and atitle not in seen:
                seen.add(atitle)
                print(f"[{url}] {atitle[:100]}")
                print(f"  -> {aurl[:150]}")
                print()
                if len(seen) >= 15:
                    break
        print(f"--- Done: {url} ---")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
