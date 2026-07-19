#!/usr/bin/env python3
"""Fetch additional news sources."""
import urllib.request
import re
import json

# Fetch HN RSS for more stories
try:
    url = 'https://hnrss.org/frontpage?points=100'
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Daily-Bot/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8')
    
    ai_kw = ['ai', 'llm', 'gpt', 'model', 'neural', 'openai', 'anthropic', 
             'claude', 'gemini', 'transformer', 'agent', 'coding', 'chatgpt',
             'deep learning', 'machine learning', 'llama', 'mistral', 'sora',
             'diffusion', 'rag', 'robot', 'vision', 'speech', 'code', 'convex',
             'np-hard', 'optimization', 'stackoverflow', 'typing']
    
    print('=== HN RSS (100+ points) ===')
    # Parse RSS items
    title_pattern = r'<title>(.*?)</title>'
    link_pattern = r'<link>(.*?)</link>'
    titles = re.findall(title_pattern, content)
    links = re.findall(link_pattern, content)
    
    for t, l in zip(titles[:20], links[:20]):
        clean = re.sub(r'<[^>]+>', '', t).strip()
        cl = clean.lower()
        if any(kw in cl for kw in ai_kw):
            print(f'  {clean}')
            print(f'    {l}')
except Exception as e:
    print(f'RSS error: {e}')

# Fetch arXiv
try:
    url = 'http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10'
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Daily-Bot/1.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8')
    
    titles = re.findall(r'<title>(.*?)</title>', content)
    summaries = re.findall(r'<summary>(.*?)</summary>', content)
    links = re.findall(r'<id>(.*?)</id>', content)
    
    print('\n=== arXiv cs.AI Recent ===')
    for i, (t, s, lnk) in enumerate(zip(titles[:10], summaries[:10], links[:10])):
        clean_t = re.sub(r'<[^>]+>', '', t).strip()
        clean_s = re.sub(r'<[^>]+>', '', s).strip()[:200]
        if clean_t and not clean_t.startswith('arXiv'):
            print(f'  {clean_t}')
            print(f'    {lnk}')
            print(f'    {clean_s}')
except Exception as e:
    print(f'arXiv error: {e}')

# Try fetching from some tech news sites
news_sites = [
    ('https://www.theverge.com/ai-artificial-intelligence', 'The Verge AI'),
    ('https://techcrunch.com/category/artificial-intelligence/', 'TechCrunch AI'),
]

for url, name in news_sites:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        
        # Extract headlines
        h_patterns = [r'<h[23][^>]*class="[^"]*headline[^"]*"[^>]*>(.*?)</h[23]>',
                      r'<a[^>]*href="([^"]*)"[^>]*>([^<]{20,})</a>.*?(?=</li>)',
                      r'<title>([^<]+)</title>']
        
        all_titles = []
        for pat in h_patterns:
            all_titles.extend(re.findall(pat, html))
        
        if all_titles:
            print(f'\n=== {name} ===')
            for item in all_titles[:5]:
                if isinstance(item, tuple):
                    clean = re.sub(r'<[^>]+>', '', item[1]).strip()
                else:
                    clean = re.sub(r'<[^>]+>', '', item).strip()
                if len(clean) > 15:
                    print(f'  {clean}')
    except Exception as e:
        print(f'{name} error: {e}')
