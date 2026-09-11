#!/usr/bin/env python3
"""Debug GitHub trending parsing."""
import re

with open("/root/aitoolkit/scripts/.cache/github_trending.html") as f:
    html = f.read()

articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
print(f"Total articles: {len(articles)}")

for i, art in enumerate(articles[:10]):
    href_m = re.search(r'<h2[^>]*>\s*<a href="(/[^"]+)"', art)
    title_m = re.search(r'<h2[^>]*>\s*<a[^>]*>(.*?)</a>', art, re.DOTALL)
    desc_m = re.search(r'<p class="col-9[^>]*>\s*(.*?)\s*</p>', art, re.DOTALL)
    stars_m = re.search(r'started</a>\s*<a[^>]*>\s*([\d,]+)\s*</a>', art)
    
    repo = href_m.group(1).strip().split("?")[0] if href_m else ""
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ""
    desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ""
    stars = stars_m.group(1) if stars_m else "?"
    
    print(f"--- Art {i}: {repo} | {title[:50]} | ⭐{stars} ---")
    print(f"    Desc: {desc[:100]}")
