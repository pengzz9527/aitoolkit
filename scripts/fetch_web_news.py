#!/usr/bin/env python3
"""Fetch recent AI news from web sources."""
import json, urllib.request, sys, re

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'AI-Reporter/1.0',
        'Accept': 'application/json, text/html, */*'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

print("=== TECH NEWS HEADLINES ===")

# Try TechCrunch AI section
techcrunch = fetch_url('https://techcrunch.com/category/artificial-intelligence/')
if techcrunch:
    titles = re.findall(r'<title[^>]*>([^<]+)</title>', techcrunch)
    # Get article headlines from listing
    h2_titles = re.findall(r'<h[23][^>]*class="[^"]*entry-title[^"]*"[^>]*>([^<]+)</h[23]>', techcrunch, re.IGNORECASE)
    if not h2_titles:
        h2_titles = re.findall(r'<h[23][^>]*>([^<]{20,})</h[23]>', techcrunch)[:10]
    print("TechCrunch AI:")
    for t in h2_titles[:8]:
        print(f"  - {t.strip()}")
else:
    print("TechCrunch: unavailable")

# Try The Verge AI
verge = fetch_url('https://www.theverge.com/ai-artificial-intelligence')
if verge:
    h2_titles = re.findall(r'<h[23][^>]*>([^<]{20,})</h[23]>', verge)[:8]
    print("\nThe Verge AI:")
    for t in h2_titles:
        print(f"  - {t.strip()}")
else:
    print("The Verge: unavailable")

# Try Ars Technica AI
ars = fetch_url('https://arstechnica.com/tag/artificial-intelligence/')
if ars:
    h2_titles = re.findall(r'<h[23][^>]*>([^<]{20,})</h[23]>', ars)[:8]
    print("\nArs Technica AI:")
    for t in h2_titles:
        print(f"  - {t.strip()}")
else:
    print("Ars Technica: unavailable")

# Try Hacker News search for AI
hn_search = fetch_url('https://hn.algolia.com/api/v1/search?query=AI&tags=front_page&hitsPerPage=10')
if hn_search:
    data = json.loads(hn_search)
    hits = data.get('hits', [])[:10]
    print("\nHN AI Search Results:")
    for h in hits:
        print(f"  - [{h.get('title','')}] ({h.get('points',0)}⚡) {h.get('url','')}")
