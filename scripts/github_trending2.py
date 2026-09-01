#!/usr/bin/env python3
import urllib.request, re, sys

# Better GitHub trending parser
url = "https://github.com/trending?since=daily&spoken_language_code="
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode("utf-8", errors="ignore")

print("=== GITHUB TRENDING ===")
# Look for article rows with different patterns
articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
for a in articles[:20]:
    # Try to get repo link
    repo_m = re.search(r'<h2[^>]*>\s*<a[^>]*href="(\/[^"]+)"', a)
    title_m = re.search(r'<h2[^>]*>\s*<a[^>]*>([^<]+)</a>', a)
    lang_m = re.search(r'<span itemprop="programmingLanguage">(.*?)</span>', a)
    stars_m = re.search(r'›\s*(\d[\d,]*)\s*stars?', a, re.IGNORECASE)
    desc_m = re.search(r'<p[^>]*>(.*?)</p>', a, re.DOTALL)
    
    if repo_m:
        repo = repo_m.group(1).strip()
        title = title_m.group(1).strip() if title_m else repo
        lang = lang_m.group(1) if lang_m else ""
        stars = stars_m.group(1) if stars_m else ""
        desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip()[:100] if desc_m else ""
        print(f"⭐{stars} {repo} | {lang} | {desc} | https://github.com{repo}")
