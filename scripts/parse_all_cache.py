#!/usr/bin/env python3
import json, os

for fname in ['hn_claude', 'hn_deepseek', 'hn_osai']:
    path = f"/root/aitoolkit/scripts/.cache/{fname}.json"
    if os.path.exists(path):
        with open(path) as f:
            d = json.load(f)
        hits = d.get("hits", [])
        print(f"\n=== {fname}: {len(hits)} hits ===")
        for h in hits:
            title = h.get("title", "")
            pts = h.get("points", 0)
            cmts = h.get("num_comments", 0)
            url = h.get("url", "")
            if not url:
                url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
            print(f"  {pts}pts/{cmts}c | {title[:70]} | {url}")
