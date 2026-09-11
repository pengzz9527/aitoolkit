#!/usr/bin/env python3
import json
with open("/root/aitoolkit/scripts/.cache/hn_ai_front.json") as f:
    d = json.load(f)
hits = d.get("hits", [])
print(f"Total hits: {len(hits)}")
for h in hits:
    title = h.get("title", "")
    pts = h.get("points", 0)
    cmts = h.get("num_comments", 0)
    url = h.get("url", "")
    if not url:
        url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
    created = h.get("created_at", "")
    tags = h.get("tags", [])
    print(f"{pts}pts/{cmts}c [{','.join(tags)}] {title} | {url} | {created}")
