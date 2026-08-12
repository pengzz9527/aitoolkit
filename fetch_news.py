#!/usr/bin/env python3
"""Fetch AI news from HN and GitHub for daily report."""
import urllib.request, json, sys, os

def fetch_hn_front():
    url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=20"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    hits = []
    for h in data.get("hits", []):
        hits.append({
            "title": h.get("title", ""),
            "points": h.get("points", 0),
            "url": h.get("url") or h.get("hn_url", ""),
            "created": h.get("created_at", "")[:10],
        })
    return hits

def fetch_hn(query):
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=front_page&hitsPerPage=5"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    return [h for h in data.get("hits", []) if h.get("points", 0) > 200]

def fetch_github_trending():
    url = "https://api.github.com/search/repositories?q=created:>2026-08-11&sort=stars&order=desc&per_page=10"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    repos = []
    for repo in data.get("items", [])[:10]:
        desc = (repo.get("description") or "")[:150]
        repos.append({
            "name": repo["full_name"],
            "stars": repo["stargazers_count"],
            "desc": desc,
            "url": repo["html_url"],
            "lang": repo.get("language", ""),
        })
    return repos

if __name__ == "__main__":
    import urllib.parse
    hn_front = fetch_hn_front()
    hn_ai = fetch_hn("AI agent open source model LLM")
    gh = fetch_github_trending()
    
    print("=== HN FRONT PAGE ===")
    for h in hn_front:
        print(f"[{h['points']}] {h['title']} | {h['url']}")
    
    print("\n=== HN AI SEARCH ===")
    for h in hn_ai[:10]:
        print(f"[{h['points']}] {h['title']} | {h['url']}")
    
    print("\n=== GITHUB TRENDING ===")
    for r in gh:
        print(f"⭐{r['stars']} {r['name']} [{r['lang']}] | {r['desc']} | {r['url']}")
