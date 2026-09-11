#!/usr/bin/env python3
import json, os

cache_dir = "/root/aitoolkit/scripts/.cache"
all_stories = []
seen_titles = set()

for fname in sorted(os.listdir(cache_dir)):
    if not fname.endswith(".json") or not fname.startswith("hn_"):
        continue
    path = os.path.join(cache_dir, fname)
    with open(path) as f:
        d = json.load(f)
    
    hits = []
    if isinstance(d, list):
        hits = d
    elif isinstance(d, dict):
        hits = d.get("hits", [])
    
    for h in hits:
        if isinstance(h, str):
            continue
        title = h.get("title", "")
        if title in seen_titles:
            continue
        seen_titles.add(title)
        pts = h.get("points", 0)
        cmts = h.get("num_comments", 0)
        url = h.get("url", "")
        if not url:
            url = f"https://news.ycombinator.com/item?id={h.get('objectID', '')}"
        created = h.get("created_at", "")
        tags = h.get("tags", [])
        all_stories.append({
            "title": title,
            "points": pts,
            "comments": cmts,
            "url": url,
            "tags": tags,
            "created_at": created,
        })

all_stories.sort(key=lambda x: x["points"], reverse=True)

print(f"Total unique stories: {len(all_stories)}")
for s in all_stories:
    print(f"  [{s['points']}pts/{s['comments']}c] {s['title'][:70]} | {s['url']} | {s['created_at']}")
