#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# HN front page
hn = fetch('https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30')
print("=== HN HOT ===")
for h in hn['hits'][:20]:
    print(f"[{h['points']}] {h['title']} - {h.get('url','')}")

# HN AI-related high points
print("\n=== HN AI (points>50) ===")
ai_kw = ['ai','llm','claude','gpt','openai','anthropic','google','deepseek','llama','hugging','model','agent','autonomous','neural','transformer','machine learning','prompt','embedding','vector','rAG','fine-tune','diffusion','claude','gemini','o3','sora','v0','cursor','copilot']
for h in hn['hits']:
    if h['points'] > 50:
        title_url = (h['title'] + ' ' + h.get('url','')).lower()
        if any(k in title_url for k in ai_kw):
            print(f"[{h['points']}] {h['title']} - {h.get('url','')}")

# GitHub trending repos (updated today)
print("\n=== GITHUB TRENDING (AI) ===")
gh = fetch('https://api.github.com/search/repositories?q=stars:>500&sort=updated&order=desc&per_page=20&since=today')
for r in gh.get('items',[]):
    print(f"⭐{r['stargazers_count']} {r['full_name']} - {r.get('description','')[:80]} - {r['html_url']}")
