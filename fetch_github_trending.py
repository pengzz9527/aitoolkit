#!/usr/bin/env python3
import re, urllib.request, sys

url = 'https://github.com/trending/python?since=daily'
with urllib.request.urlopen(url) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Extract repo links
repos = re.findall(r'<h2[^>]*>.*?<a href="/([^"]+)"[^>]*>([^<]+)</a>', html)
descriptions = re.findall(r'<p class="col-9 color-fg-muted my-1 pr-4">([^<]+)</p>', html)
for i, (repo, desc) in enumerate(repos[:15]):
    print(f"{i+1}. {repo.strip()} | {desc.strip()[:100]}")
