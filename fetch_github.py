#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

# GitHub trending AI repos
print("=== GitHub Trending AI ===")
data = fetch("https://api.github.com/search/repositories?q=created:>2026-08-29&sort=stars&order=desc&per_page=10")
for i, r in enumerate(data.get("items", [])):
    stars = r.get("stargazers_count", 0)
    lang = r.get("language", "")
    name = r.get("full_name", "")
    desc = (r.get("description") or "")[:100]
    print(f"{i+1}. {name} ⭐{stars} ({lang})")
    print(f"   {desc}")
    print()

# Also get recently updated popular AI repos
print("=== Recently Updated AI Repos ===")
data2 = fetch("https://api.github.com/search/repositories?q=ai+OR+LLM+OR+machine+learning&sort=updated&order=desc&per_page=10")
for i, r in enumerate(data2.get("items", [])[:10]):
    stars = r.get("stargazers_count", 0)
    lang = r.get("language", "")
    name = r.get("full_name", "")
    desc = (r.get("description") or "")[:100]
    updated = r.get("updated_at", "")[:10]
    print(f"{i+1}. {name} ⭐{stars} ({lang}) [updated: {updated}]")
    print(f"   {desc}")
    print()
