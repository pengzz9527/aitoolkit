#!/usr/bin/env python3
"""Parse and analyze collected AI news data."""
import json, re, sys, os

def parse_github_trending(html_path):
    """Parse GitHub Trending HTML."""
    with open(html_path) as f:
        html = f.read()
    
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', html, re.DOTALL)
    results = []
    ai_kws = ["ai", "llm", "gpt", "claude", "openai", "agent", "llama", "deepseek",
               "nlp", "ml", "neural", "transformer", "rag", "vector", "embed",
               "tts", "voice", "synthesis", "model", "inference", "coding",
               "copilot", "cursor", "security", "trading", "video", "swarm",
               "mcp", "sora", "browser-use", "adhd", "freecad"]
    
    for art in articles:
        # Extract repo link
        href_m = re.search(r'<a href="(/[^"]+)"(?![^>]*class="d-inline")', art)
        # Get title from h2
        title_m = re.search(r'<h2[^>]*>\s*<a[^>]*>(.*?)</a>', art, re.DOTALL)
        # Get description
        desc_m = re.search(r'<p class="col-9[^>]*>\s*(.*?)\s*</p>', art, re.DOTALL)
        # Get stars
        stars_m = re.search(r'>([\d,]+)\s*stars?today', art, re.IGNORECASE)
        
        if not href_m:
            # Try alternate pattern
            href_m = re.search(r'href="(/\S+)"', art)
        
        repo = href_m.group(1).strip() if href_m else ""
        title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ""
        desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ""
        stars = stars_m.group(1) if stars_m else "?"
        
        text = (title + " " + desc).lower()
        if any(k in text for k in ai_kws):
            # Also get total stars
            total_stars_m = re.search(r'[\d,]+\s*stars', art)
            results.append({
                'repo': repo,
                'title': title,
                'desc': desc[:200],
                'stars_today': stars,
                'total_stars': total_stars_m.group(0) if total_stars_m else ''
            })
    
    return results

def parse_hn_cache(json_path):
    """Parse cached HN JSON."""
    if not os.path.exists(json_path):
        return []
    with open(json_path) as f:
        data = json.load(f)
    
    hits = data.get("hits", [])
    ai_kws = ["ai", "llm", "gpt", "claude", "openai", "anthropic", "chatgpt",
               "gemini", "gemma", "mistral", "ollama", "agent", "llama",
               "deepseek", "grok", "sora", "multimodal", "rag", "autogpt",
               "cursor", "copilot", "machine-learning", "deep-learning",
               "coding agent", "synthetic data", "foundation model"]
    
    results = []
    for h in hits:
        title = h.get("title", "")
        points = h.get("points", 0)
        comments = h.get("num_comments", 0)
        url = h.get("url", "")
        if not url:
            url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
        tags = [t.lower() for t in h.get("tags", [])]
        title_lower = title.lower()
        
        if any(t in tags for t in ai_kws) or any(k in title_lower for k in ai_kws):
            results.append({
                'title': title,
                'points': points,
                'comments': comments,
                'url': url,
                'tags': tags
            })
    return results

if __name__ == "__main__":
    gh_path = "/root/aitoolkit/scripts/.cache/github_trending.html"
    hn_path = "/root/aitoolkit/scripts/.cache/hn_front.json"
    
    print("=== GitHub Trending ===")
    gh = parse_github_trending(gh_path)
    for item in gh:
        print(f"⭐{item['stars_today']} today | {item['repo']} | {item['title']}")
        print(f"   {item['desc'][:150]}")
        print()
    
    print("=== HN Front Page ===")
    hn = parse_hn_cache(hn_path)
    for item in hn:
        print(f"[{item['points']}pts/{item['comments']}c] {item['title']} | {item['url']}")
