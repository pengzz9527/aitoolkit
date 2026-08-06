#!/usr/bin/env python3
import urllib.request, json

# GitHub repos for AI
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
        print(f"{repo} | {data['stargazers_count']}⭐ | {data.get('language', '')}")
        print(f"  {data.get('description', '')[:100]}")
    except Exception as e:
        print(f"Error: {repo} - {e}")
