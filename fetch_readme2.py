#!/usr/bin/env python3
import json, urllib.request

url = 'https://api.github.com/repos/obra/superpowers/readme'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    d = json.loads(resp.read())
    import base64
    content = base64.b64decode(d['content']).decode('utf-8')
    print(content[:5000])
except Exception as e:
    print(f"Error: {e}")
