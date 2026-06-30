#!/usr/bin/env python3
"""Search for additional AI news from various sources."""
import json, urllib.request, sys, re

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'AI-Reporter/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

# 1. The Register AI section
print("=== THE REGISTER AI ===")
html = fetch_url('https://www.theregister.com/security/headlines/')
if html:
    headlines = re.findall(r'<a[^>]*href="/articles/[^"]*"[^>]*>([^<]+)</a>', html)
    for h in headlines[:10]:
        if any(kw in h.lower() for kw in ['ai', 'llm', 'gpt', 'openai', 'model', 'ml', 'chip', 'gpu', 'nvidia', 'semiconductor']):
            print(f"  - {h}")

# 2. Search for AI funding/news from recent articles
print("\n=== WIRED AI ===")
html = fetch_url('https://www.wired.com/tag/artificial-intelligence/')
if html:
    titles = re.findall(r'<h[23][^>]*class="[^"]*story-title[^"]*"[^>]*>([^<]+)</h[23]>', html, re.IGNORECASE)
    if not titles:
        titles = re.findall(r'<h[23][^>]*>([^<]{30,})</h[23]>', html)[:10]
    for t in titles:
        print(f"  - {t.strip()}")

# 3. VentureBeat AI
print("\n=== VENTUREBEAT AI ===")
html = fetch_url('https://venturebeat.com/category/ai/')
if html:
    titles = re.findall(r'<h[23][^>]*>([^<]{30,})</h[23]>', html)[:8]
    for t in titles:
        print(f"  - {t.strip()}")

# 4. TechCrunch (general)
print("\n=== TECHCRUNCH RECENT ===")
html = fetch_url('https://techcrunch.com/')
if html:
    titles = re.findall(r'<h[23][^>]*>([^<]{30,})</h[23]>', html)[:10]
    for t in titles:
        if any(kw in t.lower() for kw in ['ai', 'llm', 'gpt', 'openai', 'model', 'ml', 'chip', 'startup', 'fund', 'raise', 'nvidia', 'semiconductor', 'robot']):
            print(f"  - {t.strip()}")

# 5. Google News AI
print("\n=== GOOGLE NEWS AI ===")
html = fetch_url('https://news.google.com/rss/search?q=artificial+intelligence+latest&hl=en-US&gl=US&ceid=US:en')
if html:
    items = re.findall(r'<title>([^<]+)</title>', html)
    # Skip the header
    for item in items[1:12]:
        clean = re.sub(r'\|[^\|]*$', '', item).strip()
        print(f"  - {clean}")

# 6. Search for Ornith details
print("\n=== ORNITH DETAILS ===")
html = fetch_url('https://deep-reinforce.com/ornith_1_0.html')
if html:
    paragraphs = re.findall(r'<p[^>]*>([^<]{100,500})</p>', html)
    for p in paragraphs[:5]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean:
            print(f"  {clean[:300]}")
