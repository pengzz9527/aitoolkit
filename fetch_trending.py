#!/usr/bin/env python3
import json, urllib.request

repos = [
    'addyosmani/agent-skills',
    'obra/superpowers',
    'google-labs-code/stitch-skills',
]

for r in repos:
    url = f'https://api.github.com/repos/{r}'
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json'})
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        d = json.loads(resp.read())
        print(f"{r}: {d.get('description','N/A')} | {d.get('stargazers_count',0)} stars | {d.get('language','')}")
    except Exception as e:
        print(f"{r}: ERROR {e}")
