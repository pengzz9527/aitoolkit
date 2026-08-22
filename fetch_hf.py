#!/usr/bin/env python3
import json, urllib.request, sys

url = "https://huggingface.co/api/models?sort=trending&limit=20&search=python"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.load(resp)

for m in data:
    print(f"{m['modelId']} | downloads: {m.get('downloads',0)} | tags: {m.get('tags', [])[:5]}")
