#!/usr/bin/env python3
import json

files = ["/tmp/hn_ai4.json", "/tmp/hn_ai5.json", "/tmp/hn_ai6.json", "/tmp/hn_hardware.json", "/tmp/hn_launch.json"]
for fpath in files:
    try:
        with open(fpath) as f:
            text = f.read()
        if not text.strip():
            print(f"{fpath}: EMPTY")
            continue
        data = json.loads(text)
        hits = data.get("hits", [])
        print(f"\n=== {fpath} ({len(hits)} hits) ===")
        for h in hits[:10]:
            print(f"  {h['title']} | {h.get('points',0)} pts | {h.get('num_comments',0)} comments | {h.get('url','')}")
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
