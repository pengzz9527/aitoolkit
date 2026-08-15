#!/usr/bin/env python3
import json

files = ["/tmp/hn_models.json", "/tmp/hn_apps.json"]
for fpath in files:
    try:
        with open(fpath) as f:
            data = json.load(f)
        hits = data.get("hits", [])
        print(f"\n=== {fpath} ({len(hits)} hits) ===")
        for h in hits[:10]:
            print(f"  {h['title']} | {h.get('points',0)} pts | {h.get('num_comments',0)} comments | {h.get('url','')}")
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
