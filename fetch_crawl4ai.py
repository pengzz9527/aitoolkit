#!/usr/bin/env python3
import urllib.request, json

url = 'https://api.github.com/repos/unclecode/crawl4ai'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    d = json.loads(r.read())

print("Stars:", d['stargazers_count'])
print("Forks:", d['forks_count'])
print("Language:", d['language'])
print("Description:", d['description'])
print("License:", d['license']['spdx_id'] if d.get('license') else 'N/A')
print("Updated:", d['updated_at'][:10])
print("Default branch:", d['default_branch'])
print("Homepage:", d.get('homepage'))
print("Open issues:", d['open_issues_count'])
print("Created:", d['created_at'][:10])
