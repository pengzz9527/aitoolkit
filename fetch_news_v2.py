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

def main():
    results = []
    
    # HN front page
    try:
        data = fetch_url("https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=30")
        for h in data.get("hits", []):
            results.append({
                "type": "hn",
                "title": h.get("title", ""),
                "url": h.get("url", h.get("objectURL", "")),
                "points": h.get("points", 0),
                "comments": len(h.get("children", []))
            })
    except Exception as e:
        print(f"HN error: {e}", file=sys.stderr)
    
    # HN AI-related search
    try:
        data = fetch_url("https://hn.algolia.com/api/v1/search?query=LLM+OR+agent+OR+RAG+OR+AI&page=1&hitsPerPage=20&tags=front_page")
        for h in data.get("hits", []):
            if h.get("points", 0) >= 5:
                results.append({
                    "type": "hn_ai",
                    "title": h.get("title", ""),
                    "url": h.get("url", h.get("objectURL", "")),
                    "points": h.get("points", 0),
                    "comments": len(h.get("children", []))
                })
    except Exception as e:
        print(f"HN AI search error: {e}", file=sys.stderr)
    
    # GitHub trending (recent AI repos)
    try:
        data = fetch_url("https://api.github.com/search/repositories?q=created:>2026-07-25+language:python&sort=stars&order=desc&per_page=15")
        for r in data.get("items", []):
            results.append({
                "type": "github",
                "title": r.get("full_name", ""),
                "url": r.get("html_url", ""),
                "points": r.get("stargazers_count", 0),
                "description": (r.get("description") or "")[:150]
            })
    except Exception as e:
        print(f"GitHub error: {e}", file=sys.stderr)
    
    # HN show HN
    try:
        data = fetch_url("https://hn.algolia.com/api/v1/search?tags=show_hn&page=1&hitsPerPage=15")
        for h in data.get("hits", []):
            if h.get("points", 0) >= 3:
                results.append({
                    "type": "show_hn",
                    "title": h.get("title", ""),
                    "url": h.get("url", h.get("objectURL", "")),
                    "points": h.get("points", 0),
                    "comments": len(h.get("children", []))
                })
    except Exception as e:
        print(f"Show HN error: {e}", file=sys.stderr)
    
    # Save to file
    output = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "fetched": datetime.utcnow().isoformat() + "Z",
        "items": results
    }
    
    with open("/root/aitoolkit/news_data.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Fetched {len(results)} items")
    for item in results[:20]:
        print(f"  [{item.get('points',0):5d}] {item['title'][:80]}")
        if item.get('url'):
            print(f"       {item['url'][:100]}")

if __name__ == "__main__":
    main()
