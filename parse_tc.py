#!/usr/bin/env python3
import re

with open('/tmp/tc.html') as f:
    html = f.read()
articles = re.findall(r'<a[^>]*href="([^"]*2026/08/[^"]*)"[^>]*>([^<]{15,150})</a>', html)
seen = set()
for aurl, atitle in articles:
    atitle = atitle.strip()
    if atitle.lower() in ('sign in', 'subscribe', 'learn more', 'read more', 'continue reading', 'get access', 'more', 'latest'):
        continue
    if len(atitle) > 15 and atitle not in seen:
        seen.add(atitle)
        print(f'{atitle[:120]}')
        print(f'  -> {aurl}')
        print()
        if len(seen) >= 20:
            break
