#!/usr/bin/env python3
"""Fetch AI news from multiple sources and generate daily report."""
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
import re

def fetch_hn_top():
    """Fetch HN top stories and filter AI-related ones."""
    try:
        req = urllib.request.Request("https://hacker-news.firebaseio.com/v0/topstories.json")
        with urllib.request.urlopen(req, timeout=15) as resp:
            ids = json.loads(resp.read())[:30]
        
        stories = []
        ai_keywords = ['ai', 'llm', 'gpt', 'model', 'neural', 'deep learning', 
                       'machine learning', 'openai', 'anthropic', 'claude', 'gemini',
                       'transformer', 'diffusion', 'rag', 'agent', 'coding',
                       'artificial intelligence', 'llama', 'mistral', 'grok',
                       'sora', 'chatgpt', 'ollama', 'vllm', 'llava', 'mcp',
                       'computer', 'robot', 'vision', 'audio', 'speech',
                       'code', 'dev', 'github', 'python', 'rust', 'search',
                       'database', 'optimization', 'np-hard', 'convex']
        
        for sid in ids:
            try:
                sreq = urllib.request.Request(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
                with urllib.request.urlopen(sreq, timeout=10) as sresp:
                    item = json.loads(sresp.read())
                    if item and item.get('type') == 'story' and item.get('title'):
                        score = item.get('score', 0)
                        url = item.get('url', f'https://news.ycombinator.com/item?id={sid}')
                        title = item['title']
                        title_lower = title.lower()
                        url_lower = url.lower()
                        combined = title_lower + ' ' + url_lower
                        if any(kw in combined for kw in ai_keywords):
                            stories.append((title, url, score))
            except Exception:
                continue
        return sorted(stories, key=lambda x: x[2], reverse=True)[:15]
    except Exception as e:
        print(f"HN fetch error: {e}")
        return []

def fetch_github_trending():
    """Fetch trending AI repos from GitHub search."""
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "AI-Daily-Bot"}
    repos = []
    
    queries = [
        "stars:>200 pushed:2026-07-17..2026-07-19",
        "stars:>100 created:2026-07-17..2026-07-19",
        "stars:>500 pushed:2026-07-18",
    ]
    
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=10"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
                for item in data.get('items', [])[:5]:
                    name = item['full_name']
                    stars = item['stargazers_count']
                    desc = item.get('description') or ''
                    lang = item.get('language', '')
                    # Check if AI-related
                    name_lower = name.lower()
                    desc_lower = desc.lower()
                    if any(kw in name_lower or kw in desc_lower for kw in 
                           ['ai', 'llm', 'agent', 'ml', 'nlp', 'vision', 'model', 
                            'torch', 'diffusion', 'coder', 'dev', 'embed', 'vector',
                            'neural', 'transformer', 'rag', 'chat']):
                        repos.append((name, stars, desc, lang))
        except Exception as e:
            print(f"GitHub query '{q}' error: {e}")
    
    seen = set()
    unique = []
    for r in repos:
        if r[0] not in seen:
            seen.add(r[0])
            unique.append(r)
    return unique[:10]

def fetch_web_news():
    """Search DuckDuckGo for recent AI news."""
    results = []
    queries = [
        "AI artificial intelligence news July 2026",
        "OpenAI Anthropic Google DeepMind latest news 2026",
        "AI startup funding raise 2026",
        "large language model new release 2026",
        "AI regulation policy announcement 2026",
    ]
    
    for q in queries:
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8')
            
            pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)
            snippets_pattern = r'<a class="result__snippet[^"]*"[^>]*>([^<]+)</a>'
            snippets = re.findall(snippets_pattern, html)
            
            for i, (href, title) in enumerate(matches[:4]):
                snippet = snippets[i] if i < len(snippets) else ''
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                if len(clean_title) > 10 and clean_title.lower() not in str(results).lower():
                    results.append((clean_title, href, clean_snippet[:200]))
        except Exception as e:
            print(f"DuckDuckGo error for '{q}': {e}")
    
    return results[:10]

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Fetching AI news for {today}...")
    
    hn_stories = fetch_hn_top()
    print(f"Found {len(hn_stories)} HN AI stories")
    
    gh_repos = fetch_github_trending()
    print(f"Found {len(gh_repos)} GitHub AI repos")
    
    news_items = fetch_web_news()
    print(f"Found {len(news_items)} web news items")
    
    output = {
        "date": today,
        "hn_stories": [{"title": t, "url": u, "score": s} for t, u, s in hn_stories],
        "github_repos": [{"name": n, "stars": st, "desc": d, "lang": l} for n, st, d, l in gh_repos],
        "news_items": [{"title": t, "url": u, "snippet": s} for t, u, s in news_items]
    }
    
    with open("/tmp/ai_daily_data.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n=== HN Stories ===")
    for title, url, score in hn_stories[:10]:
        print(f"  [{score}] {title}")
        print(f"    {url}")
    
    print("\n=== GitHub Repos ===")
    for name, stars, desc, lang in gh_repos[:10]:
        print(f"  ⭐{stars} {name} ({lang})")
        print(f"    {desc[:100]}")
    
    print("\n=== Web News ===")
    for title, url, snippet in news_items[:10]:
        print(f"  {title}")
        print(f"    {url}")
        print(f"    {snippet[:120]}")

if __name__ == "__main__":
    main()
