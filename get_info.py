#!/usr/bin/env python3
import urllib.request, json, ssl

ctx = ssl.create_default_context()
headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/vnd.github.v3+json"}

repos = [
    ("microsoft/markitdown", "https://github.com/microsoft/markitdown"),
    ("browser-use/browser-use", "https://github.com/browser-use/browser-use"),
]

for name, url in repos:
    print(f"\n=== {name} ===")
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{name}", headers=headers)
        data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=10).read().decode())
        print(f"Description: {data.get('description','N/A')}")
        print(f"Stars: {data.get('stargazers_count',0)}")
        print(f"Language: {data.get('language','N/A')}")
        print(f"Topics: {data.get('topics',[])}")
        print(f"URL: {data.get('html_url','N/A')}")
    except Exception as e:
        print(f"Error: {e}")

    # Try README for more info
    try:
        req2 = urllib.request.Request(f"https://raw.githubusercontent.com/{name}/main/README.md", headers={"User-Agent": "Mozilla/5.0"})
        readme = urllib.request.urlopen(req2, context=ctx, timeout=10).read().decode(errors="ignore")[:2000]
        print(f"\nREADME preview:\n{readme}")
    except Exception as e:
        print(f"README error: {e}")
