#!/usr/bin/env python3
import json
d = json.load(open('/root/aitoolkit/hn_data.json'))
for h in d.get('hits', []):
    score = h.get('points', 0)
    if score >= 30:
        title = h.get('title', '')
        url = h.get('url', '') or h.get('objectID', '')
        comments = h.get('num_comments', 0)
        print(f"{score}|{comments}|{title}|{url}")
