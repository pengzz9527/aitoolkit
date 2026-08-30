#!/usr/bin/env python3
"""Fetch AI news from multiple sources for daily report."""
import json, urllib.request, urllib.parse, re, html, sys

def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def fetch_text(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

# 1. HN Top stories
print("=" * 60)
print("HN TOP STORIES")
print("=" * 60)
try:
    data = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
    top_ids = data[:30]
    for sid in top_ids:
        try:
            item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json?print=pretty")
            if item and item.get('score', 0) >= 30 and item.get('type') == 'story':
                title = html.unescape(item.get('title', ''))
                url = item.get('url', '') or f"https://news.ycombinator.com/item?id={sid}"
                score = item.get('score', 0)
                print(f"[{score}pts] {title}")
                print(f"  {url}")
                print()
        except:
            pass
except Exception as e:
    print(f"HN API failed: {e}")

# 2. GitHub search for AI repos
print("=" * 60)
print("GITHUB AI REPOS")
print("=" * 60)
try:
    query = urllib.parse.quote("AI OR LLM OR machine-learning OR deep-learning created:>2026-08-28")
    data = fetch_json(f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10")
    for i, r in enumerate(data.get('items', [])):
        stars = r.get('stargazers_count', 0)
        lang = r.get('language', '') or ''
        name = r.get('full_name', '')
        desc = (r.get('description') or '')[:120]
        print(f"{i+1}. {name} ⭐{stars} ({lang})")
        print(f"   {desc}")
        print()
except Exception as e:
    print(f"GitHub API failed: {e}")

# 3. GitHub trending Python
print("=" * 60)
print("GITHUB TRENDING PYTHON")
print("=" * 60)
try:
    html_content = fetch_text("https://github.com/trending/python?since=daily")
    repos = re.findall(
        r'<h2[^>]*>\s*<a href="/([^"]+)"[^>]*>\s*<span[^>]*>([^<]+)</span>',
        html_content
    )
    star_rows = re.findall(
        r'<a[^>]*class="[^(?:social)]*"[^>]*>\s*<svg[^>]*>.*?<span[^>]*>([\d,]+)\s*stars',
        html_content, re.DOTALL
    )
    # Simpler approach - find repo links
    repo_links = re.findall(r'href="/([^/]+/[^/]+)"[^>]*class="link-block"', html_content)
    seen = set()
    for link in repo_links[:15]:
        if link not in seen:
            seen.add(link)
            print(f"  {link}")
    # Also try another pattern
    full_repos = re.findall(r'<span class="repo-name">\s*([^<]+)<', html_content)
    for r in full_repos[:15]:
        print(f"  {r.strip()}")
except Exception as e:
    print(f"GitHub trending failed: {e}")
