import json, urllib.request

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

# Get broader GitHub search for AI-related repos
gh = fetch('https://api.github.com/search/repositories?q=stars:>200+updated:>2026-09-06&sort=stars&order=desc&per_page=30')
print("=== GITHUB AI-RELATED TODAY ===")
for r in gh.get('items',[]):
    desc = (r.get('description') or '')[:100]
    name = r['full_name'].lower()
    print(f"⭐{r['stargazers_count']} {r['full_name']} - {desc} - {r['html_url']}")

# Also check ai-trader-bot and guaardvark specifically
print("\n=== SPECIFIC REPOS ===")
for name in ['MIgHTy-alIeN/ai-trader-bot', 'guaardvark/guaardvark', 'AnastasiyaW/codex-claude-code-config', 'jjang-ai/vmlx', 'sdsrss/code-graph-mcp']:
    try:
        data = fetch(f'https://api.github.com/repos/{name}')
        print(f"⭐{data['stargazers_count']} {name} - {data.get('description','')[:80]}")
    except:
        print(f"NOT FOUND: {name}")
