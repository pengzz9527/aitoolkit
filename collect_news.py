#!/usr/bin/env python3
"""Collect AI news from Hacker News, GitHub, and web sources."""
import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        return r.read().decode('utf-8', errors='replace')

# 1. HN top stories
print("=== HN TOP STORIES ===")
try:
    top_ids = json.loads(fetch("https://hacker-news.firebaseio.com/v0/topstories.json"))[:30]
    for sid in top_ids[:20]:
        item = json.loads(fetch(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"))
        title = item.get('title', '')
        score = item.get('score', 0)
        url = item.get('url', '') or f"https://news.ycombinator.com/item?id={sid}"
        if any(k in title.lower() or k in url.lower() for k in ['ai', 'llm', 'gpt', 'deepseek', 'claude', 'openai', 'anthropic', 'machine learning', 'neural', 'agent', 'coding', 'model']):
            print(f"  [{score}] {title} — {url}")
except Exception as e:
    print(f"HN error: {e}")

# 2. GitHub trending (scrape HTML)
print("\n=== GITHUB TRENDING (AI repos) ===")
try:
    html = fetch("https://github.com/trending?since=daily&spoken_language_code=&language=python")
    import re
    repos = re.findall(r'<h2\s+class="h3 lh-condensed"\s*>\s*<a\s+href="/([^"]+)"[^>]*>\s*(.+?)\s*</a>', html, re.DOTALL)
    descs = re.findall(r'<p\s+class="col-9\s+text-gray[^"]*">\s*(.+?)\s*</p>', html, re.DOTALL)
    for i, (repo, name) in enumerate(repos[:15]):
        desc = descs[i] if i < len(descs) else ''
        name_clean = re.sub(r'<[^>]+>', '', name).strip()
        repo_clean = repo.strip()
        desc_clean = re.sub(r'<[^>]+>', '', desc)[:120]
        print(f"  {repo_clean} — {desc_clean}")
except Exception as e:
    print(f"GitHub trending error: {e}")

# 3. GitHub search for recent AI repos
print("\n=== GITHUB RECENT AI REPOS ===")
try:
    import urllib.parse
    q = urllib.parse.quote("machine-learning created:>2026-09-18", safe='')
    url2 = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=15"
    resp = fetch(url2)
    data = json.loads(resp)
    for r in data.get('items', []):
        stars = r.get('stargazers_count', 0)
        desc = (r.get('description') or '')[:100]
        lang = r.get('language', '')
        if lang in ('Python', 'Rust', 'Go', 'TypeScript', 'C++', 'JavaScript'):
            print(f"  ⭐{stars} {r['full_name']} — {desc}")
except Exception as e:
    print(f"GitHub search error: {e}")

# 4. HN AI-specific via search
print("\n=== SEARCHING HN FOR AI ===")
try:
    # Use HN algolia search
    algolia_data = json.dumps({"params": "query=AI agent LLM model", "hitsPerPage": 15}).encode()
    req = urllib.request.Request(
        "https://hn.algolia.com/api/v1/search?tags=story",
        data=algolia_data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    resp = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode()
    hits = json.loads(resp).get('hits', [])
    for h in hits[:12]:
        title = h.get('title', '')
        points = h.get('points', 0)
        url = h.get('url', '') or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
        date = h.get('created_at_i', '')
        print(f"  [{points}] {title} — {url}")
except Exception as e:
    print(f"Algolia search error: {e}")
