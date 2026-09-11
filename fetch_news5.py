#!/usr/bin/env python3
import urllib.request, json, re, time

# Fetch HN pages 2-5
keywords = ['ai', 'agent', 'claude', 'gpt', 'openai', 'anthropic', 'llm', 'model', 'coding', 'automation', 'cursor', 'codex', 'gemini', 'deepseek', 'qwen', 'vision', 'neural', 'machine learning', 'deep learning', 'transformer', 'mcp', 'api', 'robot', 'multimodal', 'intelligence', 'chatgpt', 'artificial']
all_hits = []
for page in range(2, 5):
    url = f'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50&page={page}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for hit in data.get('hits', []):
            title_lower = hit['title'].lower()
            if any(kw in title_lower for kw in keywords):
                all_hits.append(hit)
                time.sleep(0.3)
    except Exception as e:
        print(f"Page {page} failed: {e}")

all_hits.sort(key=lambda x: -x['points'])
for hit in all_hits[:25]:
    url = hit.get('url', '')
    print(f"[{hit['points']}pts] {hit['title']}")
    print(f"  {url or 'https://news.ycombinator.com/item?id=' + str(hit.get('objectID',''))}")
print("---HN_PAGE234---")

# Also search by tags for AI-specific content
for tag in ['story', 'ask']:
    url = f'https://hn.algolia.com/api/v1/search_by_date?tags={tag}&query=AI agent model&hitsPerPage=10'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for hit in data.get('hits', []):
            url = hit.get('url', '')
            print(f"[{hit['points']}pts] [DATE] {hit['title']}")
            print(f"  {url or 'https://news.ycombinator.com/item?id=' + str(hit.get('objectID',''))}")
    except Exception as e:
        print(f"Date search failed: {e}")
print("---HN_DATE---")

# Try some known AI news sites
news_sites = [
    ('https://www.theverge.com/ai-artificial-intelligence', 'theverge'),
    ('https://venturebeat.com/category/ai/', 'venturebeat'),
]
for feed_url, name in news_sites:
    try:
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        links = re.findall(r'<a[^>]+href=["\']([^"\']+)[^>]*>([^<]+)</a>', content)
        for href, text in links[:15]:
            text_clean = text.strip()
            if len(text_clean) > 10 and any(k in text_clean.lower() for k in ['ai', 'agent', 'chatgpt', 'claude', 'openai', 'gpt', 'llm', 'google', 'anthropic', 'deepmind', 'meta ai']):
                print(f"[{name}] {text_clean}")
                print(f"  {href}")
    except Exception as e:
        print(f"{name} failed: {e}")
print("---NEWS_SITES---")
