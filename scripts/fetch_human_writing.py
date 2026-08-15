#!/usr/bin/env python3
import json, urllib.request

# Get more details about human-writing repo
repo = "KKKKhazix/human-writing"
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    d = json.loads(resp.read())
    print("Full description:", d.get('description'))
    print("Homepage:", d.get('homepage'))
    print("Size:", d.get('size'))
    print("Forks:", d.get('forks_count'))
    print("Open issues:", d.get('open_issues_count'))
    print("Watchers:", d.get('subscribers_count'))
    print("Default branch:", d.get('default_branch'))
    print("License:", d.get('license', {}).get('name') if d.get('license') else 'None')
    print("URL:", d.get('html_url'))
    
# Get README
print("\n=== README ===")
req2 = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/readme",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req2, timeout=10) as resp2:
    readme_data = json.loads(resp2.read())
    import base64
    readme_content = base64.b64decode(readme_data.get('content', '')).decode('utf-8')
    print(readme_content[:3000])
