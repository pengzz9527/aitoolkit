#!/usr/bin/env python3
import urllib.request, re, sys

url = 'https://github.com/trending/python?since=daily'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

articles = re.findall(r'<article[^>]*>.*?</article>', html, re.DOTALL)
for art in articles[:20]:
    repo_m = re.search(r'<a[^>]*href="/([^"]+?)"[^>]*class="[^"]*Link[^"]*"', art)
    desc_m = re.search(r'<p[^>]*>(.*?)</p>', art, re.DOTALL)
    stars_m = re.search(r'([\d,]+)\s*stars', art)
    lang_m = re.search(r'<span itemprop="programmingLanguage">(.*?)</span>', art)
    if repo_m:
        repo = repo_m.group(1)
        d = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ''
        s = stars_m.group(1) if stars_m else ''
        l = lang_m.group(1) if lang_m else ''
        # filter AI-related
        combo = (repo + ' ' + d).lower()
        if any(k in combo for k in ['ai', 'llm', 'gpt', 'claude', 'model', 'neural', 'transformer',
                                      'agent', 'machine learning', 'deep learning', 'vision',
                                      'generation', 'hugging', 'pytorch', 'tensorflow', 'langchain']):
            print(f"{repo} | {s}⭐ | {l} | {d[:100]}")
