#!/usr/bin/env python3
"""
AI Daily Report Generator
Fetches AI-related news from HN and GitHub, then generates a daily report.
"""
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

TODAY = datetime.now(timezone(timedelta(hours=8)))
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%B %d, %Y").replace(" 0", " ")

def fetch_hn_frontpage():
    """Fetch HN front page stories via Algolia API."""
    url = "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=25"
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        data = json.loads(resp.read())
        return data.get('hits', [])
    except Exception as e:
        print(f"HN fetch error: {e}")
        return []

def fetch_github_trending():
    """Fetch GitHub trending AI repos."""
    url = "https://api.github.com/search/repositories?q=machine+learning+OR+artificial+intelligence+OR+deep+learning+OR+llm+OR+ai+stars:>50&sort=stars&order=desc&per_page=15"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Daily-Report"
        })
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        return data.get('items', [])
    except Exception as e:
        print(f"GitHub fetch error: {e}")
        return []

def is_ai_related(title):
    """Check if a story title is AI-related."""
    keywords = [
        'ai', 'llm', 'gpt', 'claude', 'gemini', 'openai', 'anthropic', 'meta',
        'machine learning', 'deep learning', 'neural', 'transformer', 'model',
        'chatgpt', 'llama', 'mistral', 'cohere', 'perplexity', 'hugging',
        'diffusion', 'sora', 'vision', 'rag',
        'agent', 'agentic', 'foundation model', 'ollama',
        'grok', 'xai', 'cursor', 'langchain', 'langgraph',
        'llama.cpp', 'vllm', 'sglang', 'mllm',
        'multimodal', 'reasoning', 'o1', 'o3', 'deepseek', 'qwen', 'gemma',
        'claude code', 'claude desktop', 'claude sonnet', 'claude opus',
        'grok 3', 'gemini 2', 'gemini 3',
        'openai o3', 'deepresearch', 'agi',
        'prompt', 'fine-tune', 'rlhf', 'reinforcement learning',
        'mixture of experts', 'moe', 'kv cache', 'quantization',
        'inference', 'serve', 'gpt-4o', 'gpt-4.5', 'gpt-5',
        'claude-4', 'claude 4', 'sonnet 4', 'opus 4',
        'ai news', 'ai launch', 'ai tool', 'ai product',
        'chatbot', 'conversational ai', 'llm agent', 'coding assistant',
        'stable diffusion', 'text to image', 'text to video',
        'computer vision', 'natural language', 'nlp',
        'neural network', 'attention mechanism', 'parameter',
        'training data', 'benchmark', 'eval', 'score',
        'open source', 'api', 'sdk', 'framework',
        'claude computer use', 'computer use', 'claude art',
        'claude 4.6', 'claude sonnet 4.6',
        'google ai', 'google deepmind', 'alphafold',
        'ai safety', 'ai regulation', 'ai policy',
    ]
    title_lower = title.lower()
    return any(kw in title_lower for kw in keywords)

def main():
    print(f"Fetching data for {DATE_STR}...")
    
    hn_stories = fetch_hn_frontpage()
    print(f"  HN: {len(hn_stories)} stories fetched")
    
    github_repos = fetch_github_trending()
    print(f"  GitHub: {len(github_repos)} repos fetched")
    
    # Collect AI-related stories
    ai_stories = []
    for h in hn_stories:
        title = h.get('title', '')
        if is_ai_related(title):
            url = h.get('url', '') or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
            ai_stories.append({
                'title': title,
                'url': url,
                'points': h.get('points', 0),
                'comments': h.get('num_comments', 0),
                'source': 'HN'
            })
    
    # Collect GitHub repos
    for repo in github_repos:
        name = repo.get('full_name', '')
        if 'ai' in name.lower() or 'llm' in name.lower() or 'ml' in name.lower() or 'lang' in name.lower():
            desc = repo.get('description', '') or ''
            ai_stories.append({
                'title': f"[GitHub] {name}",
                'url': f"https://github.com/{name}",
                'points': repo.get('stargazers_count', 0),
                'comments': 0,
                'source': 'GitHub',
                'description': desc
            })
    
    # Sort by points
    ai_stories.sort(key=lambda x: x['points'], reverse=True)
    
    print(f"\nFound {len(ai_stories)} AI-related stories:")
    for s in ai_stories[:15]:
        print(f"  [{s['points']}] {s['title']}")
    
    # Save for report generation
    with open('/tmp/ai_stories.json', 'w') as f:
        json.dump(ai_stories, f, indent=2)
    
    print(f"\nData saved to /tmp/ai_stories.json")

if __name__ == '__main__':
    main()
