#!/usr/bin/env python3
import json, urllib.request

url = "https://api.github.com/repos/fuxicodex/Fuxi"
req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    d = json.load(r)

print(json.dumps({k: d[k] for k in ["full_name","description","stargazers_count","language","homepage","topics","html_url","created_at"] if k in d}, indent=2))

# Get README
readme_url = d.get("readme_url")
if readme_url:
    req2 = urllib.request.Request(readme_url, headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req2, timeout=15) as r2:
        import base64
        data = json.load(r2)
        content = base64.b64decode(data.get("content","")).decode("utf-8", errors="replace")
        print("\n=== README ===")
        print(content[:3000])
