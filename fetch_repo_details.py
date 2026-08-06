#!/usr/bin/env python3
import urllib.request, json

# GitHub trending AI repos with details
repos = [
    "FareedKhan-dev/kimi-k3-in-c",
    "openai/ten-proofs",
    "Anionex/codex-vision-proxy",
    "patchy631/time-to-first-token",
    "disler/super-simple-software-factory",
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
        print(f"{repo} | {stars}⭐ | {lang}")
        print(f"  {desc}")
        print(f"  {data['html_url']}")
        print()
    except Exception as e:
        print(f"Error: {repo} - {e}")
        print()
