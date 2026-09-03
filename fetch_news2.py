#!/usr/bin/env python3
import json, urllib.request, sys

# Parse HN front page
with open('/tmp/hn_front.json') as f:
    hn = json.load(f)

print("=== HN Top Stories ===")
for h in hn.get('hits', [])[:20]:
    title = h.get('title','')
    url = h.get('url','')
    pts = h.get('points',0)
    comments = h.get('num_comments',0)
    print(f"{pts}pts({comments}c) | {title} | {url}")

# Parse GitHub
with open('/tmp/github_repos.json') as f:
    gh = json.load(f)

print("\n=== GitHub Repos ===")
for r in gh.get('items', []):
    desc = (r.get('description') or '')[:100]
    print(f"⭐{r['stargazers_count']} | {r['full_name']} | {desc} | {r['html_url']}")

# Search for AI/LLM trending repos
print("\n=== Searching GitHub for AI repos ===")
try:
    req = urllib.request.Request(
        'https://api.github.com/search/repositories?q=language:Python+stars:>500&sort=stars&order=desc&per_page=10',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    for r in data.get('items', [])[:10]:
        desc = (r.get('description') or '')[:80]
        print(f"⭐{r['stargazers_count']} | {r['full_name']} | {desc} | {r['html_url']}")
except Exception as e:
    print(f"Error: {e}")

# Fetch specific articles
print("\n=== Fetching Gemini 3.8 Flash ===")
try:
    req = urllib.request.Request(
        'https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode(errors='ignore')[:2000]
    # Extract key info
    import re
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        print(f"Title: {title_match.group(1)}")
    print(f"Content snippet: {content[:500]}")
except Exception as e:
    print(f"Error: {e}")

print("\nDone.")