#!/usr/bin/env python3
import re

with open('/tmp/verge.html') as f:
    html = f.read()
articles = re.findall(r'<a[^>]*href="([^"]*ai[^"]*|/ai-artificial-intelligence/[^"]+)"[^>]*>([^<]{15,150})</a>', html, re.IGNORECASE)
seen = set()
for aurl, atitle in articles:
    atitle = atitle.strip()
    if atitle.lower() in ('sign in', 'subscribe', 'learn more', 'read more', 'continue reading', 'get access', 'more', 'latest', 'see all'):
        continue
    if len(atitle) > 15 and atitle not in seen:
        seen.add(atitle)
        print(f'{atitle[:120]}')
        print(f'  -> {aurl}')
        print()
        if len(seen) >= 20:
            break
