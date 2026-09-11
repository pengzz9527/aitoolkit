#!/usr/bin/env python3
"""Collect AI news from multiple sources."""
import json, urllib.request, re, sys, os

def fetch_hn():
    """Fetch HN front page for AI-related stories."""
    try:
        url = "https://hn.algolia.com/api/v1/search?tags=front_page&page=1&hitsPerPage=40"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        hits = data.get("hits", [])
        results = []
        ai_keywords = ["ai", "llm", "gpt", "claude", "openai", "anthropic", "chatgpt", 
                       "gemini", "gemma", "mistral", "ollama", "agent", "llama",
                       "deepseek", "grok", "sora", "multimodal", "rag", "autogpt",
                       "cursor", "copilot", "machine-learning", "deep-learning",
                       "coding agent", "ai agent"]
        for h in hits:
            title = h.get("title", "")
            points = h.get("points", 0)
            comments = h.get("num_comments", 0)
            url = h.get("url", "")
            if not url:
                url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
            tags = [t.lower() for t in h.get("tags", [])]
            title_lower = title.lower()
            
            is_ai = any(t in tags for t in ai_keywords)
            title_match = any(kw in title_lower for kw in ai_keywords)
            
            if is_ai or title_match:
                results.append((title, points, comments, url, ",".join(tags)))
        return results
    except Exception as e:
        print(f"HN error: {e}", file=sys.stderr)
        return []

def fetch_github_trending():
    """Fetch GitHub trending AI repos via API."""
    try:
        # Use GitHub search API to find trending AI repos
        url = "https://api.github.com/search/repositories?q=created:>2026-09-01&sort=stars&order=desc&per_page=20"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        results = []
        for item in data.get("items", []):
            desc = item.get("description", "") or ""
            name = item.get("full_name", "")
            stars = item.get("stargazers_count", 0)
            html_url = item.get("html_url", "")
            topics = [t.lower() for t in item.get("topics", [])]
            ai_keywords = ["ai", "llm", "gpt", "claude", "agent", "llama", "deepseek",
                          "nlp", "ml", "machine-learning", "deep-learning", "neural",
                          "transformer", "rag", "vector", "embed", "tts", "voice"]
            if any(k in topics + [t.lower() for t in desc.split()] for k in ai_keywords):
                results.append((name, desc[:150], stars, html_url, topics))
        return results
    except Exception as e:
        print(f"GitHub API error: {e}", file=sys.stderr)
        return []

def fetch_github_trending_v2():
    """Try fetching GitHub trending directly with fewer restrictions."""
    try:
        url = "https://github.com/trending/python?since=daily"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
        results = []
        ai_kws = ["ai", "llm", "gpt", "claude", "openai", "agent", "llama", "deepseek",
                   "nlp", "ml", "neural", "transformer", "rag", "vector", "embed", 
                   "tts", "voice", "synthesis", "model", "inference", "coding"]
        
        for art in articles:
            href_m = re.search(r'href="(/[^"]+)"', art)
            title_m = re.search(r'<h2[^>]*>(.*?)</h2>', art, re.DOTALL)
            desc_m = re.search(r'<p class="col-9[^>]*>(.*?)</p>', art, re.DOTALL)
            stars_m = re.search(r'>([\d,]+)\s*star', art)
            
            repo = href_m.group(1).strip() if href_m else ""
            title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ""
            desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ""
            stars = stars_m.group(1) if stars_m else "0"
            
            text = (title + " " + desc).lower()
            if any(k in text for k in ai_kws):
                results.append((repo, title, desc[:150], stars))
        return results
    except Exception as e:
        print(f"GitHub trending v2 error: {e}", file=sys.stderr)
        return []

def fetch_news_ycombinator():
    """Fetch top stories from HN directly."""
    try:
        url = "https://hn.algolia.com/api/v1/search?tags=story&page=1&hitsPerPage=40"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        hits = data.get("hits", [])
        results = []
        ai_kws = ["ai", "llm", "gpt", "claude", "openai", "anthropic", "chatgpt",
                   "gemini", "gemma", "mistral", "ollama", "agent", "llama",
                   "deepseek", "grok", "sora", "multimodal", "rag", "autogpt",
                   "cursor", "copilot", "machine-learning", "deep-learning"]
        for h in hits:
            title = h.get("title", "")
            points = h.get("points", 0)
            comments = h.get("num_comments", 0)
            u = h.get("url", "")
            if not u:
                u = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
            tags = [t.lower() for t in h.get("tags", [])]
            title_lower = title.lower()
            if any(t in tags for t in ai_kws) or any(k in title_lower for k in ai_kws):
                results.append((title, points, comments, u))
        return results
    except Exception as e:
        print(f"News error: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    out_dir = "/root/aitoolkit/scripts/.cache"
    os.makedirs(out_dir, exist_ok=True)
    
    print("=== Fetching HN Front Page ===")
    hn = fetch_hn()
    for title, pts, cmts, url, tags in hn:
        print(f"[{pts}pts/{cmts}c] {title} | {url} | tags:{tags}")
    
    print("\n=== Fetching HN Stories ===")
    stories = fetch_news_ycombinator()
    for title, pts, cmts, url in stories:
        print(f"[{pts}pts/{cmts}c] {title} | {url}")
    
    print("\n=== Fetching GitHub Trending (API) ===")
    gh_api = fetch_github_trending()
    for name, desc, stars, url, topics in gh_api:
        print(f"{stars}⭐ {name} | {desc} | topics:{topics}")
    
    print("\n=== Fetching GitHub Trending (HTML) ===")
    gh_html = fetch_github_trending_v2()
    for repo, title, desc, stars in gh_html:
        print(f"{stars}⭐ {repo} | {title} | {desc}")
