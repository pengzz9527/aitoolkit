#!/usr/bin/env python3
import json

# Parse the main HN front page data I already have
with open("/tmp/hn.json") as f:
    data = json.load(f)
hits = data.get("hits", [])
print("=== Main Front Page AI-Related Stories ===")
for h in hits:
    title = h.get("title", "")
    pts = h.get("points", 0)
    comments = h.get("num_comments", 0)
    url = h.get("url", "")
    print(f"  {title} | {pts} pts | {comments} comments | {url}")

# Parse the AI search results
for fname in ["/tmp/hn_ai.json", "/tmp/hn_ai2.json", "/tmp/hn_ai3.json", "/tmp/hn_companies.json", "/tmp/hn_bench.json", "/tmp/hn_mcp.json"]:
    try:
        with open(fname) as f:
            content = f.read().strip()
        if not content:
            print(f"\n{fname}: EMPTY")
            continue
        d = json.loads(content)
        hts = d.get("hits", [])
        if hts:
            print(f"\n=== {fname} ({len(hts)} hits) ===")
            for h in hts[:8]:
                print(f"  {h['title']} | {h.get('points',0)} pts | {h.get('num_comments',0)} comments | {h.get('url','')}")
    except Exception as e:
        print(f"Error: {fname}: {e}")
