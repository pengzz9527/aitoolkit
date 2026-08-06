#!/usr/bin/env python3
import json
d = json.load(open('/root/aitoolkit/github_data.json'))
for r in d.get('items', []):
    stargazers = r.get('stargazers_count', 0)
    if stargazers >= 50:
        lang = r.get('language', '')
        desc = (r.get('description') or '')[:120]
        name = r['full_name']
        print(f"{stargazers}|{lang}|{name}|{desc}")
