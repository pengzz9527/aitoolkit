#!/usr/bin/env python3
import re

with open('/tmp/verge.html') as f:
    html = f.read()
# Find article links with AI content
articles = re.findall(r'<a[^>]*href="(/ai-artificial-intelligence/[^"]+)"[^>]*>([^<]{10,150})</a>', html)
seen = set()
for aurl, atitle in articles:
    atitle = atitle.strip()
    if atitle.lower() in ('sign in', 'subscribe', 'learn more', 'read more', 'continue reading', 'get access', 'more', 'latest', 'see all'):
        continue
    if len(atitle) > 10 and atitle not in seen:
        seen.add(atitle)
        print(f'{atitle[:120]}')
        print(f'  -> https://www.theverge.com{aurl}')
        print()
        if len(seen) >= 15:
            break
