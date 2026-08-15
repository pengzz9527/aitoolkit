#!/usr/bin/env python3
import json

with open("/tmp/hn.json") as f:
    data = json.load(f)
for h in data.get("hits",[])[:20]:
    print(f"HN|{h['title']}|{h.get('points',0)} pts|{h.get('num_comments',0)} comments|{h.get('url','')}")

with open("/tmp/gh_trend.json") as f:
    data = json.load(f)
for r in data.get("items",[]):
    desc = (r.get("description") or "").replace("|", " ")[:80]
    print(f"GHTREND|{r['full_name']}|⭐{r['stargazers_count']}|{desc}")

with open("/tmp/gh_top.json") as f:
    data = json.load(f)
for r in data.get("items",[]):
    desc = (r.get("description") or "").replace("|", " ")[:80]
    print(f"GITTOP|{r['full_name']}|⭐{r['stargazers_count']}|{desc}")

with open("/tmp/hn_ai.json") as f:
    data = json.load(f)
for h in data.get("hits",[])[:15]:
    print(f"HNAI|{h['title']}|{h.get('points',0)} pts|{h.get('num_comments',0)} comments|{h.get('url','')}")

with open("/tmp/hn_ai2.json") as f:
    data = json.load(f)
for h in data.get("hits",[])[:15]:
    print(f"HNAI2|{h['title']}|{h.get('points',0)} pts|{h.get('num_comments',0)} comments|{h.get('url','')}")

with open("/tmp/hn_ai3.json") as f:
    data = json.load(f)
for h in data.get("hits",[])[:15]:
    print(f"HNAI3|{h['title']}|{h.get('points',0)} pts|{h.get('num_comments',0)} comments|{h.get('url','')}")
