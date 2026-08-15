#!/usr/bin/env python3
import json, urllib.request, base64

repo = "KKKKhazix/human-writing"

# Get CHANGELOG
print("=== CHANGELOG ===")
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/contents/CHANGELOG.md",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read())
    content = base64.b64decode(data.get('content', '')).decode('utf-8')
    print(content[:2000])

# Get SKILL.md
print("\n=== SKILL.md ===")
req2 = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/contents/human-writing/SKILL.md",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req2, timeout=10) as resp2:
    data2 = json.loads(resp2.read())
    content2 = base64.b64decode(data2.get('content', '')).decode('utf-8')
    print(content2[:2000])

# Get dist version
print("\n=== dist/human-writing-lite.md ===")
req3 = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/contents/human-writing/dist/human-writing-lite.md",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req3, timeout=10) as resp3:
    data3 = json.loads(resp3.read())
    content3 = base64.b64decode(data3.get('content', '')).decode('utf-8')
    print(content3[:1500])
