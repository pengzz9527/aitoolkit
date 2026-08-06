#!/usr/bin/env python3
import urllib.request, json

# Fetch recent arxiv papers about AI
url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&start=0&max_results=15&sortBy=submittedDate&sortOrder=descending"
req = urllib.request.Request(url)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    content = resp.read().decode()
    # Parse XML and extract titles
    import re
    titles = re.findall(r'<title>([^<]+)</title>', content)
    links = re.findall(r'<id>(https?://arxiv.org/[^<]+)</id>', content)
    for t, l in zip(titles, links):
        if 'Abstract' not in t and 'Submitted' not in t:
            print(f"{t}|{l}")
except Exception as e:
    print(f"Error: {e}")
