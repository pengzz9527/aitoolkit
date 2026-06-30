#!/usr/bin/env python3
"""Fetch detailed info on specific AI stories."""
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

# 1. Qwen 3.6 27B blog post
print("=== QWEN 3.6 27B ===")
html = fetch_url('https://quesma.com/blog/qwen-36-is-awesome/')
if html:
    # Get title
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', html)
    if title_m:
        print(f"Title: {title_m.group(1)}")
    # Get some paragraph text
    paragraphs = re.findall(r'<p[^>]*>([^<]{50,500})</p>', html)
    for p in paragraphs[:5]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean:
            print(f"  {clean[:200]}")

# 2. Ornith 1.0
print("\n=== ORNITH 1.0 ===")
html = fetch_url('https://github.com/deepreinforce-ai/Ornith-1')
if html:
    desc_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html)
    if desc_m:
        print(f"Desc: {desc_m.group(1)}")
    repo_desc = re.search(r'<p class="p-note[^"]*".*?>([^<]+)</p>', html)
    if repo_desc:
        print(f"Repo: {repo_desc.group(1)}")
    stars = re.search(r'aria-label=".*?stars.*?">([^<]+)<', html)
    if stars:
        print(f"Stars: {stars.group(1)}")

# 3. Micro-Agent vLLM blog
print("\n=== MICRO-AGENT vLLM ===")
html = fetch_url('https://vllm.ai/blog/2026-06-29-micro-agent-frontier-models')
if html:
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', html)
    if title_m:
        print(f"Title: {title_m.group(1)}")
    paragraphs = re.findall(r'<p[^>]*>([^<]{50,500})</p>', html)
    for p in paragraphs[:5]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean:
            print(f"  {clean[:200]}")

# 4. South Korea $1T AI/Robotics investment
print("\n=== SOUTH KOREA $1T INVESTMENT ===")
html = fetch_url('https://arstechnica.com/ai/2026/06/south-korea-to-spend-1t-on-more-memory-chip-production-and-humanoid-robots/')
if html:
    title_m = re.search(r'<title[^>]*>([^<]+)</title>', html)
    if title_m:
        print(f"Title: {title_m.group(1)}")
    paragraphs = re.findall(r'<p[^>]*>([^<]{100,600})</p>', html)
    for p in paragraphs[:4]:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if clean:
            print(f"  {clean[:300]}")

# 5. Apple Neural Engine paper
print("\n=== APPLE NEURAL ENGINE ===")
html = fetch_url('https://arxiv.org/abs/2606.22283')
if html:
    title_m = re.search(r'<meta[^>]*name="dc.title"[^>]*content="([^"]*)"', html)
    if not title_m:
        title_m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    if title_m:
        print(f"Title: {title_m.group(1)}")
    abstract = re.search(r'<blockquote class="abstract.*?">(.*?)</blockquote>', html, re.DOTALL)
    if abstract:
        clean = re.sub(r'<[^>]+>', ' ', abstract.group(1)).strip()
        print(f"Abstract: {clean[:400]}")
