#!/usr/bin/env python3
"""Fetch additional AI news from various sources."""
import urllib.request
import json
import urllib.parse

# Fetch more HN pages
def fetch_hn_deep():
    keywords = ['ai', 'agent', 'claude', 'gpt', 'openai', 'anthropic', 'llm', 'model', 'coding', 'automation', 'cursor', 'codex', 'gemini', 'deepseek', 'qwen', 'vision', 'language model', 'neural', 'machine learning', 'deep learning', 'transformer', 'chatgpt', 'artificial intelligence', 'robot', 'multimodal', 'mcp', 'api']
    all_hits = []
    for page in range(2, 5):
        req = urllib.request.Request(
            f'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50&page={page}',
            headers={'Accept': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            for hit in data.get('hits', []):
                title_lower = hit['title'].lower()
                if any(kw in title_lower for kw in keywords):
                    url = hit.get('url', '')
                    all_hits.append((hit['points'], hit['title'], url, hit.get('objectID',''), hit.get('created_at_ip','')))
        except Exception as e:
            print(f"Page {page} failed: {e}")
    
    all_hits.sort(key=lambda x: -x[0])
    for pts, title, url, oid, date in all_hits[:20]:
        display_url = url or f'https://news.ycombinator.com/item?id={oid}'
        print(f"[{pts}pts] {title}")
        print(f"  {display_url}")
    print("---HN3_END---")

# Try fetching some AI news sites
def fetch_tech_news():
    """Try to fetch from tech news RSS feeds."""
    feeds = [
        'https://www.theverge.com/ai-artificial-intelligence',
        'https://techcrunch.com/category/artificial-intelligence/',
    ]
    for feed_url in feeds:
        try:
            req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
            # Simple keyword extraction
            import re
            links = re.findall(r'<a[^>]+href=["\']([^"\']+)[^>]*>([^<]+)</a>', content)
            for href, text in links[:10]:
                if any(k in text.lower() for k in ['ai', 'agent', 'chatgpt', 'claude', 'openai', 'gpt', 'llm', 'anthropic', 'google deepmind']):
                    print(f"[NEWS] {text.strip()}")
                    print(f"  {href}")
        except Exception as e:
            print(f"Feed {feed_url} failed: {e}")
    print("---FEED_END---")

if __name__ == '__main__':
    fetch_hn_deep()
    fetch_tech_news()
