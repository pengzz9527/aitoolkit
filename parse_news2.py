#!/usr/bin/env python3
import json

files = ["/tmp/hn_ai4.json", "/tmp/hn_ai5.json", "/tmp/hn_ai6.json"]
for fpath in files:
    try:
        with open(fpath) as f:
            data = json.load(f)
        for h in data.get("hits",[])[:15]:
            print(f"{h['title']} | {h.get('points',0)} pts | {h.get('num_comments',0)} comments | {h.get('url','')}")
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
