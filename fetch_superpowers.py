#!/usr/bin/env python3
import json, urllib.request

# Get detailed info about obra/superpowers
url = 'https://api.github.com/repos/obra/superpowers'
req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json'})
resp = urllib.request.urlopen(req, timeout=10)
d = json.loads(resp.read())
print("=== REPO INFO ===")
print(f"Name: {d.get('full_name')}")
print(f"Description: {d.get('description')}")
print(f"Stars: {d.get('stargazers_count')}")
print(f"Forks: {d.get('forks_count')}")
print(f"Language: {d.get('language')}")
print(f"Topics: {d.get('topics')}")
print(f"Created: {d.get('created_at')}")
print(f"Updated: {d.get('updated_at')}")
print(f"Homepage: {d.get('homepage')}")
print(f"License: {d.get('license', {}).get('spdx_id', 'N/A') if d.get('license') else 'N/A'}")
print(f"Open Issues: {d.get('open_issues_count')}")
print(f"Size: {d.get('size')}")
print(f"Default Branch: {d.get('default_branch')}")

# Check README
if d.get('readme_url'):
    req2 = urllib.request.Request(d['readme_url'].replace('{format}', 'raw'))
    resp2 = urllib.request.urlopen(req2, timeout=10)
    readme = resp2.read().decode('utf-8')
    # Print first 2000 chars
    print("\n=== README (first 2000 chars) ===")
    print(readme[:2000])
