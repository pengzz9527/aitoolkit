#!/usr/bin/env python3
import json
import urllib.request
import sys
from datetime import datetime

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; AIToolkit/1.0)"
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def fetch_hn():
    data = fetch_url("https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=30")
    return data.get("hits", [])

def fetch_github():
    data = fetch_url("https://api.github.com/search/repositories?q=created:>2026-08-01+language:python&sort=stars&order=desc&per_page=15")
    return data.get("items", [])

def fetch_reddit():
    results = []
    for url, name in [
        ("https://www.reddit.com/r/LocalLLaMA/hot.json?limit=15", "Reddit LocalLLaMA"),
        ("https://www.reddit.com/r/MachineLearning/hot.json?limit=15", "Reddit ML"),
    ]:
        try:
            data = fetch_url(url)
            for post in data.get("data", {}).get("children", [])[:8]:
                d = post.get("data", {})
                results.append({
                    "title": d.get("title", ""),
                    "url": "https://reddit.com" + d.get("permalink", ""),
                    "score": d.get("score", 0),
                    "source": name
                })
        except Exception as e:
            print(f"  [warn] {name}: {e}", file=sys.stderr)
    return results

if __name__ == "__main__":
    today = datetime.utcnow().strftime("%Y-%m-%d")
    
    print(f"=== HN Front Page ({today}) ===")
    for h in fetch_hn()[:25]:
        print(f"  [{h.get('points',0):4d}] {h.get('title','')}")
        print(f"       {h.get('url','') or h.get('objectURL','')}")
    
    print(f"\n=== GitHub Trending ===")
    for r in fetch_github()[:12]:
        print(f"  ⭐{r.get('stargazers_count',0):5d}  {r.get('full_name','')}")
        print(f"       {(r.get('description') or '')[:100]}")
        print(f"       {r.get('html_url','')}")
    
    print(f"\n=== Reddit AI ===")
    for r in fetch_reddit()[:12]:
        print(f"  ▲{r.get('score',0):5d}  {r.get('title','')}")
        print(f"       {r.get('url','')}")
