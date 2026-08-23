#!/usr/bin/env python3
import json, sys

with open('/tmp/hn.json') as f:
    data = json.load(f)
for h in data.get('hits', [])[:40]:
    print(f"{h['points']} pts | {h.get('title','')[:120]}")
    print(f"  -> {h.get('url','')}")
    print(f"  comments: {h.get('num_comments',0)}")
    print()
