#!/usr/bin/env python3
import urllib.request, re, sys

# GitHub trending
url = "https://github.com/trending?since=daily&spoken_language_code="
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

print("=== GITHUB TRENDING ===")
articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
for a in articles[:15]:
    title_m = re.search(r'<a[^>]*class="[^"]*"[^>]*>(.*?)</a>', a)
    lang_m = re.search(r'<span itemprop="programmingLanguage">(.*?)</span>', a)
    stars_m = re.search(r'›\s*(\d[\d,]*)\s*stars', a)
    url_m = re.search(r'href="(\/[^"]+)"', a)
    if title_m:
        t = title_m.group(1).strip()
        l = lang_m.group(1) if lang_m else ""
        s = stars_m.group(1) if stars_m else ""
        u = "https://github.com" + url_m.group(1) if url_m else ""
        print(f"{s} {t} ({l}) | {u}")
