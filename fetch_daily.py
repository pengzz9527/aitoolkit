#!/usr/bin/env python3
"""Fetch AI news from multiple sources for daily report."""
import json
import urllib.request
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

def fetch_hn():
    """Fetch HN front page AI-related stories."""
    url = 'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=20'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    stories = []
    for h in data.get('hits', []):
        title = h.get('title', '')
        points = h.get('points', 0)
        url_val = h.get('url', '') or ''
        hn_url = h.get('objectURL', '')
        stories.append({
            'title': title,
            'points': points,
            'url': url_val or hn_url,
            'hn': True
        })
    return stories

def fetch_github_trending():
    """Fetch GitHub trending repos."""
    url = 'https://github.com/trending/python?since=daily'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout-15) as r:
        html = r.read().decode('utf-8', errors='replace')
    
    repos = []
    # Match repo links
    repo_matches = re.findall(r'<h2[^>]*>\s*<a href="/([^/]+/[^"]+)"', html)
    # Match descriptions
    desc_matches = re.findall(r'<p class="col-9 color-fg-muted my-1">(.*?)</p>', html)
    # Match stars
    star_matches = re.findall(r'(\d[\d,]*)\s*stars?', html)
    
    for i, repo in enumerate(repo_matches[:10]):
        desc = desc_matches[i].strip() if i < len(desc_matches) else ''
        stars = star_matches[i] if i < len(star_matches) else ''
        repos.append({
            'repo': repo,
            'description': desc,
            'stars': stars
        })
    return repos

def fetch_hn_ai_stories():
    """Fetch HN stories specifically about AI."""
    url = 'https://hn.algolia.com/api/v1/search?tags=front_page&query=AI&hitsPerPage=15'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())
    stories = []
    for h in data.get('hits', []):
        title = h.get('title', '')
        points = h.get('points', 0)
        url_val = h.get('url', '') or ''
        hn_url = h.get('objectURL', '')
        stories.append({
            'title': title,
            'points': points,
            'url': url_val or hn_url,
            'source': 'HN AI'
        })
    return stories

if __name__ == '__main__':
    print("Fetching HN front page...")
    hn_stories = fetch_hn()
    print(f"  Got {len(hn_stories)} stories")
    
    print("Fetching GitHub trending...")
    gh_trending = fetch_github_trending()
    print(f"  Got {len(gh_trending)} repos")
    
    print("Fetching HN AI stories...")
    hn_ai = fetch_hn_ai_stories()
    print(f"  Got {len(hn_ai)} AI stories")
    
    result = {
        'hn': hn_stories,
        'github_trending': gh_trending,
        'hn_ai': hn_ai,
        'fetched_at': datetime.now().isoformat()
    }
    
    with open('/root/aitoolkit/fetch_result.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("Results saved to /root/aitoolkit/fetch_result.json")
    for s in hn_stories[:10]:
        print(f"  [{s['points']}] {s['title']} -> {s['url']}")
    print("---GitHub Trending---")
    for r in gh_trending[:10]:
        print(f"  {r['repo']} - {r['description'][:60]}")
