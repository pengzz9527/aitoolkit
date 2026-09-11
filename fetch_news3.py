#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# GitHub trending repos
print("=== GITHUB TOP REPOS TODAY ===")
gh = fetch('https://api.github.com/search/repositories?q=stars:>100&sort=updated&order=desc&per_page=25&since=today')
for r in gh.get('items',[]):
    desc = (r.get('description') or '')[:100]
    print(f"⭐{r['stargazers_count']} {r['full_name']} - {desc} - {r['html_url']}")

# HN all hits
print("\n=== HN ALL HIT ===")
hn = fetch('https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=50')
ai_kw = ['ai','llm','claude','gpt','openai','anthropic','google','deepseek','llama','hugging','model','agent','autonomous','neural','transformer','prompt','embedding','vector','rag','fine-tune','diffusion','gemini','o3','sora','v0','cursor','copilot','gpt-4','gpt-5','mistral','grok','xai','perplexity','claude code','codex','deepseek-r1','qwen','ollama','lm studio','llama.cpp','swe-agent','autoGPT','hyperwrite','writing agent']
seen = set()
for h in hn['hits']:
    title = h.get('title','')
    url = h.get('url','') or ''
    combined = (title + ' ' + url).lower()
    if any(k in combined for k in ai_kw):
        key = title[:50] + url[:30]
        if key not in seen:
            seen.add(key)
            pts = h.get('points', 0)
            print(f"[{pts}] {title} - {url}")
