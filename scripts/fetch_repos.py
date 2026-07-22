import json, sys, urllib.request

repos = [
    'kvcache-ai/ktransformers',
    'moonshine-ai/moonshine',
    'handy-computer/transcribe.cpp',
    'PrefectHQ/fastmcp',
    'msitarzewski/agency-agents',
]

for repo in repos:
    url = f'https://api.github.com/repos/{repo}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        d = json.loads(resp.read())
        print(f'=== {d.get("full_name")} ===')
        print(f'Stars: {d.get("stargazers_count")}')
        print(f'Forks: {d.get("forks_count")}')
        print(f'Desc: {d.get("description")}')
        print(f'Language: {d.get("language")}')
        print(f'Updated: {d.get("updated_at")}')
        print(f'Topics: {d.get("topics")}')
        print()
    except Exception as e:
        print(f'Error for {repo}: {e}')
        print()
