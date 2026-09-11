#!/usr/bin/env python3
import urllib.request, json, ssl

ctx = ssl.create_default_context()
headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}

name = "browser-use/browser-use"
req = urllib.request.Request(f"https://api.github.com/repos/{name}", headers=headers)
data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode())

print(f"Name: {data.get('full_name','')}")
print(f"Description: {data.get('description','')}")
print(f"Stars: {data.get('stargazers_count',0)}")
print(f"Forks: {data.get('forks_count',0)}")
print(f"Language: {data.get('language','')}")
print(f"Topics: {data.get('topics',[])}")
print(f"URL: {data.get('html_url','')}")
print(f"Created: {data.get('created_at','')}")
print(f"Updated: {data.get('updated_at','')}")
print(f"License: {data.get('license',{}).get('spdx_id','') if data.get('license') else 'N/A'}")

# Get README
try:
    req2 = urllib.request.Request(f"https://raw.githubusercontent.com/{name}/main/README.md", headers={"User-Agent": "Mozilla/5.0"})
    readme = urllib.request.urlopen(req2, context=ctx, timeout=10).read().decode(errors="ignore")
    print(f"\n=== README ===\n{readme[:5000]}")
except Exception as e:
    print(f"README error: {e}")

# Get recent releases
try:
    req3 = urllib.request.Request(f"https://api.github.com/repos/{name}/releases/latest", headers=headers)
    release = json.loads(urllib.request.urlopen(req3, context=ctx, timeout=10).read().decode())
    print(f"\n=== Latest Release ===")
    print(f"Tag: {release.get('tag_name','')}")
    print(f"Name: {release.get('name','')}")
    print(f"Body: {release.get('body','')[:1000]}")
except Exception as e:
    print(f"Release error: {e}")
