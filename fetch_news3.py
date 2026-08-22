#!/usr/bin/env python3
"""Fetch GitHub trending repos with stars info."""
import urllib.request, json, re, sys

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='replace')

# GitHub trending Python daily
print("=== GitHub Trending (all languages, today) ===")
try:
    html = fetch("https://github.com/trending?since=daily")
    # Extract repo rows
    rows = re.findall(r'<article class="Box-row">.*?</article>', html, re.DOTALL)
    for i, row in enumerate(rows[:12]):
        repo_match = re.search(r'<h2[^>]*>.*?<a href="/([^"]+)"', row, re.DOTALL)
        desc_match = re.search(r'<p class="col-9 color-fg-muted my-1 pr-4">([^<]+)</p>', row)
        stars_match = re.search(r'(\d[\d,]+)\s*stars', row)
        lang_match = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', row)
        repo = repo_match.group(1).strip() if repo_match else "?"
        desc = desc_match.group(1).strip()[:120] if desc_match else ""
        stars = stars_match.group(1) if stars_match else "?"
        lang = lang_match.group(1).strip() if lang_match else ""
        print(f"[{i+1}] {repo} | {stars} stars | {lang} | {desc}")
except Exception as e:
    print(f"Error: {e}")

# GitHub search for recent AI repos
print("\n=== GitHub Recent AI repos (created this week) ===")
try:
    q = fetch("https://api.github.com/search/repositories?q=created:>2026-08-13&sort=stars&order=desc&per_page=10&language=python")
    data = json.loads(q)
    for r in data.get("items", [])[:10]:
        stars = r.get("stargazers_count", 0)
        name = r.get("full_name", "")
        desc = (r.get("description") or "")[:120]
        url = r.get("html_url", "")
        created = r.get("created_at", "")[:10]
        print(f"[{stars} stars] {name} (created {created})")
        print(f"  {desc}")
        print(f"  {url}")
        print()
except Exception as e:
    print(f"Error: {e}")

print("\nDone.")
