#!/usr/bin/env python3
import json, urllib.request, sys

# GitHub search for AI repos
url = "https://api.github.com/search/repositories?q=AI+LLM+2026&sort=stars&order=desc&per_page=15"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

print("=== GITHUB AI REPOS ===")
for r in data.get("items", []):
    stars = r.get("stargazers_count", 0)
    name = r.get("full_name", "")
    lang = r.get("language", "")
    desc = (r.get("description", "") or "")[:120]
    url = r.get("html_url", "")
    print(f"⭐{stars} {name} | {lang} | {desc} | {url}")
