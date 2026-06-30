#!/usr/bin/env python3
"""Get Ornith repo stars and Qwen 3.6 blog benchmark data."""
import json, urllib.request, sys, re

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'AI-Reporter/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

# Ornith GitHub - get stars
print("=== ORNITH GITHUB ===")
html = fetch_url('https://github.com/deepreinforce-ai/Ornith-1')
if html:
    # Multiple patterns for star count
    patterns = [
        r'sta[rR]s["\s>]*>\s*([\d,]+)',
        r'aria-label="[^"]*([\d,]+)[^"]*stars"',
        r'Stars\s*</a>\s*<a[^>]*>\s*([\d,]+)',
    ]
    for p in patterns:
        m = re.search(p, html)
        if m:
            print(f"Stars ({p}): {m.group(1)}")
    
    # Readme first paragraph
    readme = re.findall(r'<td class="markdown-body[^"]*">(.*?)</div>', html, re.DOTALL)
    if readme:
        clean = re.sub(r'<[^>]+>', ' ', readme[0])
        clean = re.sub(r'\s+', ' ', clean).strip()
        print(f"Readme: {clean[:500]}")

# Qwen 3.6 blog - get benchmark scores
print("\n=== QWEN 3.6 BLOG ===")
html = fetch_url('https://quesma.com/blog/qwen-36-is-awesome/')
if html:
    # Find benchmark numbers
    score_patterns = re.findall(r'([\d.]+)\s*(?:%|\/|out of|points?)', html)
    # Find model names and scores near each other
    blocks = re.findall(r'(?:Qwen|Gemini|Claude|GPT|Opus)[^<]{0,200}', html)
    for b in blocks[:15]:
        clean = re.sub(r'<[^>]+>', '', b).strip()
        if clean and len(clean) > 10:
            print(f"  {clean[:200]}")
    
    # Find table-like data
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    if tables:
        for t in tables[:2]:
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.DOTALL)
            for row in rows[:10]:
                cells = re.findall(r'<(?:td|th)[^>]*>(.*?)</(?:td|th)>', row, re.DOTALL)
                if cells:
                    clean_cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                    print(f"  Table: {' | '.join(clean_cells[:5])}")

# Also check Ornith on HN directly
print("\n=== ORNITH ON HN ===")
html = fetch_url('https://news.ycombinator.com/item?id=42065928')  # approximate
if not html:
    # Try to find the actual HN item
    html = fetch_url('https://github.com/deepreinforce-ai/Ornith-1')
    if html:
        # Check if there's an HN link
        hn_links = re.findall(r'hn\.algolia\.com|news\.ycombinator\.com/item\?id=(\d+)', html)
        if hn_links:
            print(f"HN IDs: {hn_links[:3]}")
