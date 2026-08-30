#!/usr/bin/env python3
import json, urllib.request

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

for repo in ["stemdeckapp/stemdeck", "basedhardware/omi"]:
    try:
        data = fetch_json(f"https://api.github.com/repos/{repo}")
        print(f"=== {repo} ===")
        print(f"Stars: {data.get('stargazers_count', 0)}")
        print(f"Lang: {data.get('language', '')}")
        print(f"Desc: {data.get('description', '')}")
        print(f"URL: {data.get('html_url', '')}")
        print()
    except Exception as e:
        print(f"Failed {repo}: {e}")

# vLLM release
print("=== vLLM v0.28.0 ===")
try:
    data = fetch_json("https://api.github.com/repos/vllm-project/vllm/releases/tags/v0.28.0")
    print(f"Tag: {data.get('tag_name', '')}")
    print(f"Name: {data.get('name', '')}")
    body = data.get('body', '')
    # Get first few lines of body
    for line in body.split('\n')[:20]:
        if line.strip() and not line.startswith('---'):
            print(f"  {line[:120]}")
except Exception as e:
    print(f"vLLM failed: {e}")
