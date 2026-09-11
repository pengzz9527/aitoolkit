#!/usr/bin/env python3
"""Search for today's fresh AI news."""
import urllib.request, json, re, time, urllib.parse

# Search HN for recently created AI stories (today)
today = "2026-09-06"
keywords = ['ai', 'agent', 'claude', 'gpt', 'openai', 'anthropic', 'llm', 'model', 'coding', 'automation', 'cursor', 'codex', 'gemini', 'deepseek', 'qwen', 'vision', 'neural', 'machine learning', 'deep learning', 'transformer', 'mcp', 'api', 'robot', 'multimodal', 'intelligence', 'chatgpt', 'artificial']

# Use Algolia search with date range
for query in ['AI', 'agent', 'LLM', 'GPT', 'Claude', 'OpenAI']:
    url = f'https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(query)}&tags=front_page&hitsPerPage=30&numericFilters=created_at_i>1757059200'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        for hit in data.get('hits', []):
            created = hit.get('created_at_ip', '')
            title_lower = hit['title'].lower()
            # Check if created today (2026-09-06)
            if '2026-09-06' in created or '2026-09-05' in created:
                print(f"[{hit['points']}pts] [{created}] {hit['title']}")
                print(f"  {hit.get('url','https://news.ycombinator.com/item?id='+str(hit.get('objectID','')))}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Query '{query}' failed: {e}")

print("---HN_NEW---")

# Try ArXiv for recent AI papers
try:
    url = 'https://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8')
    # Extract titles
    titles = re.findall(r'<title>([^<]+)</title>', content)
    for t in titles[:10]:
        if t != 'feed' and t != 'atom':
            print(f"[arXiv] {t}")
    entries = re.findall(r'<title>(?:arXiv:[^)]* |)([^<]+)</title>', content)
    links = re.findall(r'<link[^>]+href=["\']([^"\']+)[^>]*>', content)
    for i, (title, link) in enumerate(zip(entries, links)):
        if 'cs.AI' in title.lower() or 'cs.LG' in title.lower():
            print(f"[arXiv] {title[:80]}")
            print(f"  {link}")
except Exception as e:
    print(f"ArXiv failed: {e}")
print("---ARXIV---")

# Try to fetch specific article details
articles = [
    ('https://collusion.wiki/', 'Collusion Wiki'),
    ('https://arxiv.org/abs/2609.03344', 'LLM Cognitive Virus'),
    ('https://www.techpolicy.press/americas-two-largest-school-districts-impose-ai-moratoriums/', 'School AI Moratorium'),
]
for url, name in articles:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')[:3000]
        # Extract some text
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"--- {name} ---")
        print(text[:500])
        print()
    except Exception as e:
        print(f"{name} fetch failed: {e}")
