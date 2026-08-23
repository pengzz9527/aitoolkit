#!/usr/bin/env python3
import re

with open('/tmp/ghtrend.html') as f:
    html = f.read()
articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
for a in articles[:20]:
    h2 = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', a, re.DOTALL)
    stars_match = re.search(r'(\d[\d,]*)\s*stars', a)
    desc = re.search(r'<p class="col-9 color-fg-muted my-1 pr-4">(.*?)</p>', a, re.DOTALL)
    lang = re.search(r'<span itemprop="programmingLanguage">(.*?)</span>', a)
    if h2:
        name = re.sub(r'<[^>]+>', '', h2.group(1)).strip()
    else:
        name = 'unknown'
    stars = stars_match.group(1) if stars_match else '?'
    d = re.sub(r'<[^>]+>', '', desc.group(1)).strip() if desc else ''
    l = lang.group(1) if lang else ''
    print(f'{stars} stars | {name} ({l})')
    if d:
        print(f'  {d[:100]}')
    print()
