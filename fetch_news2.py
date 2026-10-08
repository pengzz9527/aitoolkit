#!/usr/bin/env python3
"""Fetch AI news and write daily report."""
import json, urllib.request, sys, os, re
from datetime import date, datetime

TODAY = date.today()
TODAY_STR = TODAY.isoformat()
DAY_READABLE = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

# ── HN front page ──────────────────────────────────────────
hn_items = []
try:
    raw = fetch("https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30")
    data = json.loads(raw)
    for h in data.get("hits", []):
        title = h.get("title", "")
        url = h.get("url", "") or ""
        points = h.get("points", 0)
        hn_items.append({"title": title, "url": url, "points": points})
except Exception as e:
    print(f"HN fetch error: {e}", file=sys.stderr)

# ── GitHub trending AI repos (created yesterday/today) ─────
gh_repos = []
try:
    q = "AI OR llm OR agent OR model OR openai OR anthropic OR transformer"
    url = f"https://api.github.com/search/repositories?q={urllib.request.quote(q)}&sort=stars&order=desc&per_page=15"
    raw = fetch(url)
    data = json.loads(raw)
    for r in data.get("items", []):
        name = r.get("full_name", "")
        stars = r.get("stargazers_count", 0)
        desc = (r.get("description") or "")[:120]
        lang = r.get("language", "")
        gh_repos.append({"name": name, "stars": stars, "desc": desc, "lang": lang})
except Exception as e:
    print(f"GitHub fetch error: {e}", file=sys.stderr)

# ── arXiv latest AI papers (CSSearch + Computation Language) ─
arxiv_papers = []
try:
    raw = fetch("http://arxiv.org/rss/cs.CL")
    import xml.etree.ElementTree as ET
    root = ET.fromstring(raw)
    for item in root.findall(".//item")[:6]:
        t = item.findtext("title", "")
        link = item.findtext("link", "")
        arxiv_papers.append({"title": t, "url": link})
except Exception as e:
    print(f"arXiv fetch error: {e}", file=sys.stderr)

# ── Print all raw data for analysis ────────────────────────
print(f"HN items: {len(hn_items)}")
for i in hn_items:
    print(f"  [{i['points']}] {i['title']} → {i['url'][:100]}")

print(f"\nGitHub repos: {len(gh_repos)}")
for r in gh_repos:
    print(f"  ⭐{r['stars']} {r['name']} ({r['lang']}) — {r['desc']}")

print(f"\narXiv papers: {len(arxiv_papers)}")
for p in arxiv_papers:
    print(f"  {p['title'][:100]} → {p['url'][:80]}")
