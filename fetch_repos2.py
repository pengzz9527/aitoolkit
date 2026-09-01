#!/usr/bin/env python3
import json, urllib.request

# Get more trending repos
repos = [
    'pollen-robotics/microduck_rl',
    'corsairdev/corsair',
    'every-app/open-seo',
    'colinhacks/zod',
    'abhigyanpatwari/GitNexus',
    'tt-a1i/archify',
    'p-e-w/heretic',
    'handsomestWei/patent-disclosure-skill',
    'mvanhorn/last30days-skill',
]

for repo in repos:
    url = f'https://api.github.com/repos/{repo}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
    license = d.get('license', {}).get('spdx_id', 'N/A') if d.get('license') else 'N/A'
    print(f"=== {repo} ===")
    print(f"Stars: {d['stargazers_count']}, Forks: {d['forks_count']}, Language: {d['language']}")
    print(f"Description: {d['description']}")
    print(f"License: {license}, Updated: {d['updated_at'][:10]}")
    print(f"Topics: {d.get('topics', [])}")
    print()
