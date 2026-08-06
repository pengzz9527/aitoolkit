#!/usr/bin/env python3
import re
html = open('/root/aitoolkit/hn_front.html').read()
items = re.findall(r'<span class="rank">(\d+)</span>.*?<span class="score">(\d+)\s*points</span>.*?<a[^>]*href="[^"]+"[^>]*>([^<]+)</a>', html, re.DOTALL)
for rank, score, title in items[:25]:
    score_int = int(score)
    if score_int >= 30:
        print(f"{score_int}|{rank}|{title}")
