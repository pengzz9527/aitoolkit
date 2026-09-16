#!/usr/bin/env python3
"""Fetch GitHub trending for all languages."""
import json
import urllib.request
import sys
import re

try:
    url = "https://github.com/trending?since=daily"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9"
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8', errors='ignore')
    
    repos = []
    repo_matches = re.findall(r'<article\s+class="Box-row"[^>]*>.*?</article>', html, re.DOTALL)
    for match in repo_matches:
        name_match = re.search(r'<h2[^>]*>.*?<a\s+href="/([^"]+)"[^>]*>', match)
        stars_match = re.search(r'([\d,]+)\s*stars', match)
        desc_match = re.search(r'<p\s+class="col-9[^"]*">([^<]+)</p>', match)
        lang_match = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', match)
        if name_match:
            repos.append({
                "name": name_match.group(1).strip(),
                "stars": stars_match.group(1).strip() if stars_match else "N/A",
                "description": desc_match.group(1).strip() if desc_match else "",
                "language": lang_match.group(1).strip() if lang_match else ""
            })
    
    with open('/tmp/github_trending.json', 'w') as f:
        json.dump(repos[:20], f, ensure_ascii=False, indent=2)
    print(f"Fetched {len(repos)} repos")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
