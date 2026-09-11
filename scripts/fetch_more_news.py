#!/usr/bin/env python3
"""Search for recent AI news via multiple sources."""
import json, urllib.request, re, sys, os, time

def fetch_hn_search(query, tag="story"):
    """Search HN via Algolia API."""
    try:
        url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags={tag}&hitsPerPage=10"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode()).get("hits", [])
    except Exception as e:
        print(f"HNSearch error: {e}", file=sys.stderr)
        return []

def fetch_ai_news_aggregator():
    """Try fetching from an AI news aggregator."""
    sources = [
        ("https://hn.algolia.com/api/v1/search?query=AI&tags=front_page&hitsPerPage=15", "AI front page"),
        ("https://hn.algolia.com/api/v1/search?query=large+language+model&tags=story&hitsPerPage=10", "LLM stories"),
        ("https://hn.algolia.com/api/v1/search?query=AI+agent&tags=story&hitsPerPage=10", "AI Agent stories"),
    ]
    results = []
    for url, label in sources:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            for h in data.get("hits", []):
                title = h.get("title", "")
                points = h.get("points", 0)
                comments = h.get("num_comments", 0)
                story_url = h.get("url", "")
                if not story_url:
                    story_url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
                tags = h.get("tags", [])
                results.append((title, points, comments, story_url, tags, label))
        except Exception as e:
            print(f"Source {label} error: {e}", file=sys.stderr)
    return results

def fetch_reddit_ai():
    """Try fetching from Reddit AI subreddits."""
    try:
        url = "https://www.reddit.com/r/MachineLearning/hot.json?limit=15"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        results = []
        for post in data.get("data", {}).get("children", []):
            d = post.get("data", {})
            title = d.get("title", "")
            score = d.get("score", 0)
            num_comments = d.get("num_comments", 0)
            url = d.get("url", "")
            if not url or url.startswith("/"):
                url = f"https://reddit.com{url}" if url.startswith("/") else url
            results.append((title, score, num_comments, url))
        return results
    except Exception as e:
        print(f"Reddit error: {e}", file=sys.stderr)
        return []

def fetch_arxiv():
    """Fetch recent AI papers from arXiv."""
    try:
        from xml.etree import ElementTree as ET
        url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_data = resp.read().decode()
        
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_data)
        results = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns)
            summary = entry.find("atom:summary", ns)
            link = entry.find("atom:link", ns)
            if title is not None and summary is not None:
                title_text = re.sub(r'<[^>]+>', '', title.text).strip()
                summary_text = re.sub(r'<[^>]+>', '', summary.text).strip()[:200]
                link_text = link.get("href") if link is not None else ""
                results.append((title_text, summary_text, link_text))
        return results
    except Exception as e:
        print(f"ArXiv error: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    print("=== AI News Aggregator ===")
    news = fetch_ai_news_aggregator()
    seen = set()
    for title, pts, cmts, url, tags, source in news:
        key = title[:50]
        if key not in seen:
            seen.add(key)
            print(f"[{pts}pts/{cmts}c] ({source}) {title} | {url}")
    
    print("\n=== Reddit r/MachineLearning Hot ===")
    reddit = fetch_reddit_ai()
    for title, score, cmts, url in reddit:
        print(f"[{score}↑/{cmts}c] {title} | {url}")
    
    print("\n=== arXiv Latest cs.AI/cs.LG ===")
    papers = fetch_arxiv()
    for title, summary, url in papers:
        print(f"{title}")
        print(f"  {summary}")
        print(f"  {url}")
        print()
