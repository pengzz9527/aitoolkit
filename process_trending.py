#!/usr/bin/env python3
import re
html = open('/root/aitoolkit/trending.html').read()
articles = re.findall(r'<article[^>]*>.*?</article>', html, re.DOTALL)
for a in articles[:30]:
    repo_match = re.findall(r'href="(/\S+)"[^>]*\sh3', a)
    title_match = re.findall(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', a, re.DOTALL)
    desc_match = re.findall(r'<p[^>]*>(.*?)</p>', a, re.DOTALL)
    lang_match = re.findall(r'<span[^>]*class="[^"]*repo-language"[^"]*">(.*?)</span>', a)
    stars_match = re.findall(r'([\d,]+)\s+stars today', a)
    if repo_match:
        repo = repo_match[0].strip()
        title = title_match[0].strip() if title_match else ""
        lang = lang_match[0].strip() if lang_match else ""
        desc = desc_match[0].strip()[:120] if desc_match else ""
        stars = stars_match[0] if stars_match else ""
        print(f"{repo}|{title}|{lang}|{stars}|{desc}")
