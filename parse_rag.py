#!/usr/bin/env python3
import json

for fname in ["/tmp/hn_rag.json", "/tmp/hn_infer.json"]:
    try:
        with open(fname) as f:
            content = f.read().strip()
        if not content:
            print(f"{fname}: EMPTY")
            continue
        d = json.loads(content)
        hts = d.get("hits", [])
        print(f"\n=== {fname} ({len(hts)} hits) ===")
        for h in hts[:8]:
            print(f"  {h['title']} | {h.get('points',0)} pts | {h.get('num_comments',0)} comments | {h.get('url','')}")
    except Exception as e:
        print(f"Error: {fname}: {e}")
