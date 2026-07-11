#!/usr/bin/env python3
"""Fetch GitHub trending with better parsing"""
import urllib.request, re

url = "https://github.com/trending?since=daily"
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml'
})
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    # Better parsing - look for repo links in article tags
    articles = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    
    for art in articles[:15]:
        # Get repo name
        repo_match = re.search(r'<h2[^>]*>.*?<a\s+href="/([^"]+)"', art, re.DOTALL)
        desc_match = re.search(r'<p class="[^"]*col-9[^"]*">([^<]+)</p>', art, re.DOTALL)
        lang_match = re.search(r'<span[^>]*itemprop="programmingLanguage"[^>]*>([^<]+)</span>', art, re.DOTALL)
        
        if repo_match:
            repo = repo_match.group(1).strip()
            desc = desc_match.group(1).strip() if desc_match else ''
            lang = lang_match.group(1).strip() if lang_match else ''
            print(f"GHTREND|{repo}|{desc}|{lang}")
except Exception as e:
    print(f"ERROR: {e}")
