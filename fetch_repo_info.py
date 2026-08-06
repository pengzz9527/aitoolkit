#!/usr/bin/env python3
import urllib.request, json

# GitHub repos with more detail
repos = [
    "disler/super-simple-software-factory",
    "FareedKhan-dev/kimi-k3-in-c",
    "Anionex/codex-vision-proxy",
    "malwarejake/CUSTODY-framework",
    "openai/ten-proofs",
    "lyogavin/airllm",
]
for repo in repos:
    try:
        url = f'https://api.github.com/repos/{repo}'
        req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
        data = json.loads(urllib.request.urlopen(req).read())
        stars = data.get('stargazers_count', 0)
        lang = data.get('language', '')
        desc = (data.get('description') or '')[:120]
        pushed = data.get('pushed_at', '')[:10]
        print(f"{repo} | {stars}⭐ | {lang} | pushed {pushed}")
        print(f"  {desc}")
        print()
    except Exception as e:
        print(f"Error: {repo} - {e}")
