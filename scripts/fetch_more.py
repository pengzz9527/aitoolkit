#!/usr/bin/env python3
"""Get GitHub stars for Ornith repo."""
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
        return None

# Ornith GitHub
print("=== ORNITH GITHUB ===")
html = fetch_url('https://github.com/deepreinforce-ai/Ornith-1')
if html:
    # Try to find star count
    stars = re.findall(r'href="/deepreinforce-ai/Ornith-1/stargazers"[^>]*>\s*([\d,]+)', html)
    if stars:
        print(f"Stars: {stars[0]}")
    forks = re.findall(r'href="/deepreinforce-ai/Ornith-1/network"\s+class="d-inline-block"[^>]*>\s*([\d,]+)', html)
    if forks:
        print(f"Forks: {stars[0]}")
    # Readme
    readme = re.search(r'<td class="repo-file-content.*?><p[^>]*>([^<]{100,800})</p>', html, re.DOTALL)
    if readme:
        print(f"Readme: {readme.group(1)}")
    # Try other patterns for stars
    all_stars = re.findall(r'(\d[\d,]*)\s*stars', html, re.IGNORECASE)
    if all_stars:
        print(f"All star mentions: {all_stars[:5]}")

# Quesma blog - more details
print("\n=== QWEN 3.6 BLOG ===")
html = fetch_url('https://quesma.com/blog/qwen-36-is-awesome/')
if html:
    # Look for benchmark comparisons
    benchmarks = re.findall(r'(?:benchmark|score|accuracy|pass@1|MMLU|GPQA|LiveCode)[^<]{0,200}', html, re.IGNORECASE)
    for b in benchmarks[:10]:
        clean = re.sub(r'<[^>]+>', '', b).strip()
        if len(clean) > 20:
            print(f"  {clean[:200]}")

# Micro-Agent details
print("\n=== MICRO-AGENT DETAILS ===")
html = fetch_url('https://vllm.ai/blog/2026-06-29-micro-agent-frontier-models')
if html:
    # Look for key claims
    claims = re.findall(r'(?:beat|surpass|outperform|improve|reduce|cost|latency)[^<]{0,300}', html, re.IGNORECASE)
    for c in claims[:10]:
        clean = re.sub(r'<[^>]+>', '', c).strip()
        if len(clean) > 20:
            print(f"  {clean[:250]}")
