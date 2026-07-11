#!/usr/bin/env python3
import json, urllib.request

url = 'https://api.github.com/repos/obra/superpowers'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json'})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())

if d.get('readme_url'):
    req2 = urllib.request.Request(d['readme_url'].replace('{format}', 'raw'))
    resp2 = urllib.request.urlopen(req2, timeout=10)
    readme = resp2.read().decode('utf-8')
    print(readme[:5000])
