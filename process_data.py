import json, sys

with open('/tmp/hn.json') as f:
    hn = json.load(f)

ai_kw = ['ai','llm','claude','gpt','openai','anthropic','google','deepseek','llama','hugging','model','agent','autonomous','neural','transformer','prompt','embedding','vector','rag','fine-tune','diffusion','gemini','o3','sora','v0','cursor','copilot','mistral','grok','xai','perplexity','codex','qwen','ollama','reasoning','thinking','chain','mixture','MoE','research','swarm','multi-agent','reinforcement','RLHF','LLM','alien','shuts','acceleration']
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

print("\n---GITHUB---\n")
with open('/tmp/gh.json') as f:
    gh = json.load(f)

for r in gh.get('items',[]):
    desc = (r.get('description') or '')[:100]
    name = r['full_name'].lower()
    print(f"⭐{r['stargazers_count']} {r['full_name']} - {desc} - {r['html_url']}")
